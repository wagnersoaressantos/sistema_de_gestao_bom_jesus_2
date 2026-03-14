from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AnexoEncaminhamento, Especialidade, Procedimento, Encaminhamento
from .serializers import (
    AnexoEncaminhamentoSerializer,
    EspecialidadeSerializer,
    ProcedimentoSerializer,
    EncaminhamentoSerializer
)
from datetime import date



# ---------------------------------------------------
# API para especialidades
# ---------------------------------------------------
class EspecialidadeViewSet(viewsets.ModelViewSet):

    # Queryset busca todos os registros do banco
    queryset = Especialidade.objects.all()

    # Serializer que converte para JSON
    serializer_class = EspecialidadeSerializer


# ---------------------------------------------------
# API para procedimentos
# ---------------------------------------------------
class ProcedimentoViewSet(viewsets.ModelViewSet):

    # Retorna todos os procedimentos
    queryset = Procedimento.objects.all()

    serializer_class = ProcedimentoSerializer

# -------------------------------------------------
# View responsável por gerenciar anexos
# upload de resultados de exames
# -------------------------------------------------
class AnexoEncaminhamentoViewSet(viewsets.ModelViewSet):

    # lista todos os anexos
    queryset = AnexoEncaminhamento.objects.all()

    # serializer utilizado
    serializer_class = AnexoEncaminhamentoSerializer

     # -------------------------------------------------
    # Permite upload de arquivos
    # -------------------------------------------------
    parser_classes = [

        MultiPartParser,
        FormParser
    ]


# ---------------------------------------------------
# API para encaminhamentos
# ---------------------------------------------------
class EncaminhamentoViewSet(viewsets.ModelViewSet):

    # IMPORTANTE:
    # queryset precisa ser QuerySet e não lista
    queryset = Encaminhamento.objects.all()

    serializer_class = EncaminhamentoSerializer

    # -------------------------------------------------
    # Endpoint para atualizar status do encaminhamento
    # -------------------------------------------------
    @action(detail=True, methods=['post'])
    def atualizar_status(self, request, pk=None):

        encaminhamento = self.get_object()

        novo_status = request.data.get("status")

        # verifica se status é válido
        status_validos = [
            "solicitado",
            "aguardando",
            "guia_disponivel",
            "entregue",
            "resultado_disponivel"
        ]

        if novo_status not in status_validos:

            return Response(
                {"erro": "Status inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # atualiza status
        encaminhamento.status = novo_status
        encaminhamento.save()

        return Response({
            "mensagem": "Status atualizado com sucesso",
            "status": novo_status
        })

# -------------------------------------------------
# Estatísticas de demanda reprimida
# -------------------------------------------------
@api_view(['GET'])
def demanda_reprimida(request):
    # Conta encaminhamentos aguardando por especialidade
    dados = (
        Encaminhamento.objects
        # Apenas os que ainda não foram realizados
        .filter(status__in=['solicitado', 'aguardando'])
        # Agrupa por especialidade
        .values('especialidade__nome')
        # Conta quantidade
        .annotate(total=Count('id'))
        # Ordena do maior para menor
        .order_by('-total')
    )
    
    resultado = []

    for item in dados:

        resultado.append({

            "especialidade": item['especialidade__nome'],
            "total": item['total']
        })

    return Response(resultado)

# -------------------------------------------------
# Tempo médio de espera por especialidade
# -------------------------------------------------
@api_view(['GET'])
def tempo_medio_espera(request):

    especialidades = Especialidade.objects.all()

    resultado = []

    for esp in especialidades:

        realizados = Encaminhamento.objects.filter(
            especialidade=esp,
            status='entregue'
        )

        if realizados.exists():

            dias = []

            for enc in realizados:

                tempo = (enc.data_realizacao - enc.data_solicitacao).days

                dias.append(tempo)

            media = sum(dias) / len(dias)

        else:

            media = 0

        resultado.append({

            "especialidade": esp.nome,

            "tempo_medio_dias": round(media)

        })

    return Response(resultado)

# -------------------------------------------------
# Define nível de alerta da fila
# -------------------------------------------------
def calcular_alerta(fila, tempo_medio):

    if fila > 20 or tempo_medio > 90:
        return "critico"

    if fila > 10:
        return "atencao"

    return "normal"


# -------------------------------------------------
# Painel de demanda da unidade
# -------------------------------------------------
@api_view(['GET'])
def painel_fila(request):


    resultado = []
    # -------------------------------------------------
    # Primeiro: especialidades (consultas)
    # -------------------------------------------------
    especialidades = Especialidade.objects.all()
    for esp in especialidades:
        fila = Encaminhamento.objects.filter(

            especialidade=esp,
            procedimento__isnull=True,

            status__in=['solicitado', 'aguardando']

        ).count()

        realizados = Encaminhamento.objects.filter(

            especialidade=esp,
            procedimento__isnull=True,
            status='entregue'

        )
        # calcula tempo médio
        tempos = []
        for enc in realizados:

            if enc.data_realizacao:

                dias = (enc.data_realizacao - enc.data_solicitacao).days

                tempos.append(dias)

        if tempos:

            media = sum(tempos) / len(tempos)

        else:

            media = 0

        alerta = calcular_alerta(fila, media)    

        resultado.append({

            "especialidade": esp.nome,
            "procedimento": "Consulta",
            "fila": fila,
            "tempo_medio_dias": media,
            "alerta" : alerta

        })
    # -------------------------------------------------
    # Depois: procedimentos (exames)
    # -------------------------------------------------
    procedimentos = Procedimento.objects.all()

    for proc in procedimentos:

        # pacientes aguardando
        fila = Encaminhamento.objects.filter(

            procedimento=proc,
            status__in=['solicitado', 'aguardando']

        ).count()


        # exames já realizados
        realizados = Encaminhamento.objects.filter(

            procedimento=proc,
            status='entregue'

        )

        # calcula tempo médio
        tempos = []

        for enc in realizados:

            if enc.data_realizacao:

                dias = (enc.data_realizacao - enc.data_solicitacao).days

                tempos.append(dias)

        if tempos:

            media = sum(tempos) / len(tempos)

        else:

            media = 0

        alerta = calcular_alerta(fila, media)    

        resultado.append({

            "especialidade": proc.especialidade.nome,

            "procedimento": proc.nome,

            "fila": fila,

            "tempo_medio_dias": round(media),
            "alerta" : alerta

        })

    return Response(resultado)