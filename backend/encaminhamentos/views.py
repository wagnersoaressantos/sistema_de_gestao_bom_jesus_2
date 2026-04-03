from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count,Case, When, IntegerField, Avg, F, ExpressionWrapper, DurationField
from .models import Encaminhamento, Especialidade, HistoricoStatus, STATUS_FILA
from rest_framework.viewsets import ModelViewSet
from .serializers import EspecialidadeSerializer, EncaminhamentoCreateSerializer
from rest_framework import status
from datetime import date
from .serializers import EncaminhamentoSerializer
from auditoria.services import registrar_evento

class EncaminhamentoViewSet(ModelViewSet):

    queryset = Encaminhamento.objects.all()

    def perform_create(self, serializer):

        instance = serializer.save()


        HistoricoStatus.objects.create(
            encaminhamento=instance,
            status=instance.status,
            usuario=self.request.user,
            observacao="Encaminhamento criado"
        )

    def perform_update(self, serializer):

        instancia_antiga = self.get_object()
        status_antigo = instancia_antiga.status

        instance = serializer.save()

        if status_antigo != instance.status:
            from .models import HistoricoStatus

            HistoricoStatus.objects.create(
                encaminhamento=instance,
                status=instance.status,
                usuario=self.request.user,
                observacao=f"Alterado de {status_antigo} para {instance.status}"
            )

    def get_serializer_class(self):

        if self.action == "create":
            return EncaminhamentoCreateSerializer


        return EncaminhamentoSerializer

class EspecialidadeViewSet(ModelViewSet):

    queryset = Especialidade.objects.all().order_by("nome")
    serializer_class = EspecialidadeSerializer

class FilaEspecialidadeView(APIView):

    def get(self, request, especialidade_id):


        fila = Encaminhamento.objects.filter(
            especialidade_id=especialidade_id,
            status__in=STATUS_FILA
        ).annotate(
            prioridade_ordem=Case(
                When(prioridade="preferencial", then=0),
                When(prioridade="urgente", then=1),
                When(prioridade="normal", then=2),
                output_field=IntegerField()
            )
        ).order_by(
            "prioridade_ordem",
            "data_solicitacao"
        )

        if not fila.exists():
            return Response({
                "mensagem": "Nenhum paciente na fila para essa especialidade"
            })

        hoje = date.today()

        dados = []

        for e in fila:
            dados.append({
                "posicao": e.posicao_fila,
                "paciente": e.paciente.nome,
                "prioridade": e.prioridade,
                "status": e.status,
                "data_solicitacao": e.data_solicitacao,
                "dias_espera": (hoje - e.data_solicitacao).days
            })

        return Response(dados)

class QuantidadePorEspecialidadeView(APIView):

    def get(self, request):

        dados = (
            Especialidade.objects
            .annotate(total=Count("encaminhamento"))
            .values("id", "nome", "tipo", "total")
            .order_by("-total")
        )

        if not dados:
            return Response({
                "mensagem": "Nenhuma especialidade cadastrada ainda"
            })

        return Response(dados)

class TempoMedioEsperaView(APIView):

    def get(self, request):

        hoje = date.today()

        encaminhamentos = Encaminhamento.objects.filter(
            status__in=STATUS_FILA
        ).annotate(
            tempo_espera=ExpressionWrapper(
                hoje - F("data_solicitacao"),
                output_field=DurationField()
            )
        )

        resultado = (
            encaminhamentos
            .values("especialidade__nome")
            .annotate(media_espera=Avg("tempo_espera"))
            .order_by("-media_espera")
        )

        dados = []

        for item in resultado:

            dias = item["media_espera"].days if item["media_espera"] else 0

            dados.append({
                "especialidade": item["especialidade__nome"],
                "media_dias_espera": dias
            })

        return Response(dados)

class DemandaReprimidaView(APIView):

    def get(self, request):

        dados = (
            Encaminhamento.objects
            .filter(
                status__in=STATUS_FILA
            )
            .values("especialidade__nome")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        if not dados:
            return Response({
                "mensagem": "Nenhuma demanda reprimida no momento"
            })

        return Response(dados)

class DashboardView(APIView):

    def get(self, request):

        hoje = date.today()

        queryset = Encaminhamento.objects.filter(
            status__in=STATUS_FILA
        )

        # 📊 Total na fila
        total_fila = queryset.count()

        # 📊 Demanda por especialidade
        demanda = (
            queryset
            .values("especialidade__nome")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        especialidade_mais_demandada = (
            demanda[0]["especialidade__nome"]
            if demanda else None
        )

        # 📊 Tempo médio geral
        tempos = queryset.annotate(
            tempo_espera=ExpressionWrapper(
                hoje - F("data_solicitacao"),
                output_field=DurationField()
            )
        )

        media = tempos.aggregate(media=Avg("tempo_espera"))

        media_dias = (
            media["media"].days
            if media["media"] else 0
        )

        return Response({
            "total_pacientes_fila": total_fila,
            "especialidade_mais_demandada": especialidade_mais_demandada,
            "tempo_medio_espera_dias": media_dias
        })

class GerarIndicadorView(APIView):

    def post(self, request):

        from .services.indicadores import gerar_indicador_diario

        gerar_indicador_diario()

        return Response({"mensagem": "Indicador gerado com sucesso"})

class IndicadoresView(APIView):

    def get(self, request):
        from .models import IndicadorDiario

        dados = IndicadorDiario.objects.all().order_by("data")

        # 🔹 filtros por período (BOA IMPLEMENTAÇÃO)
        inicio = request.GET.get("inicio")
        fim = request.GET.get("fim")

        if inicio:
            dados = dados.filter(data__gte=inicio)

        if fim:
            dados = dados.filter(data__lte=fim)

        resultado = []

        for i in dados:
            resultado.append({
                "data": i.data,
                "total_encaminhamentos": i.total_encaminhamentos,
                "total_fila": i.total_fila,
                "tempo_medio_espera": i.tempo_medio_espera,
                "tempo_maximo_espera": i.tempo_maximo_espera,
                "duplicidades_evitas": i.duplicidades_evitas,
                "especialidade_mais_demandada": i.especialidade_mais_demandada
            })

        return Response(resultado)

# class IndicadoresView(APIView):
#
#     def get(self, request):
#
#         from .models import IndicadorDiario
#
#         dados = IndicadorDiario.objects.all().order_by("data")
#
#         inicio = request.GET.get("inicio")
#         fim = request.GET.get("fim")
#
#         if inicio:
#             dados = dados.filter(data__gte=inicio)
#
#         if fim:
#             dados = dados.filter(data__lte=fim)
#
#         resultado = []
#
#         for i in dados:
#             resultado.append({
#                 "data": i.data,
#                 "total_encaminhamentos": i.total_encaminhamentos,
#                 "total_fila": i.total_fila,
#                 "tempo_medio_espera": i.tempo_medio_espera,
#                 "tempo_maximo_espera": i.tempo_maximo_espera,
#                 "duplicidades_evitas": i.duplicidades_evitas,
#                 "especialidade_mais_demandada": i.especialidade_mais_demandada
#             })
#
#         return Response(resultado)