from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from rest_framework import viewsets
from .models import Especialidade, Procedimento, Encaminhamento
from .serializers import (
    EspecialidadeSerializer,
    ProcedimentoSerializer,
    EncaminhamentoSerializer
)
from datetime import date

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


# ---------------------------------------------------
# API para encaminhamentos
# ---------------------------------------------------
class EncaminhamentoViewSet(viewsets.ModelViewSet):

    # IMPORTANTE:
    # queryset precisa ser QuerySet e não lista
    queryset = Encaminhamento.objects.all()

    serializer_class = EncaminhamentoSerializer
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
            status='realizado'
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
