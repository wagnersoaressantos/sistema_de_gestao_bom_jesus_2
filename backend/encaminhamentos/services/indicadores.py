from datetime import date
from django.db.models import Avg, F, ExpressionWrapper, DurationField
from encaminhamentos.models import Encaminhamento, IndicadorDiario, STATUS_FILA
from encaminhamentos.models import IndicadorEspecialidade, Especialidade
from django.db.models import Max, Count
from auditoria.models import EventoAuditoria

# def gerar_indicador_diario():
#
#     hoje = date.today()
#
#     queryset = Encaminhamento.objects.all()
#
#     total_encaminhamentos = queryset.count()
#
#     fila = queryset.filter(status__in=STATUS_FILA)
#
#     total_fila = fila.count()
#
#     # tempo médio
#     tempos = fila.annotate(
#         tempo_espera=ExpressionWrapper(
#             hoje - F("data_solicitacao"),
#             output_field=DurationField()
#         )
#     )
#
#     media = tempos.aggregate(media=Avg("tempo_espera"))
#
#     media_dias = media["media"].days if media["media"] else 0
#
#     maximo = tempos.aggregate(maximo=Max("tempo_espera"))
#
#     tempo_maximo = maximo["maximo"].days if maximo["maximo"] else 0
#
#     demanda = (
#         fila.values("especialidade")
#         .annotate(total=Count("id"))
#         .order_by("-total")
#     )
#
#     for item in demanda:
#         especialidade_id = item["especialidade"]
#
#         especialidade = Especialidade.objects.get(id=especialidade_id)
#
#     # 🔹 Conta duplicidades evitadas no dia
#     duplicidades = EventoAuditoria.objects.filter(
#         tipo_evento="tentativa_duplicidade",  # ✔ nome correto do campo
#         data_evento__date=hoje  # ✔ filtro correto por data
#     ).count()
#
#     # salva no banco
#     IndicadorDiario.objects.update_or_create(
#         data=hoje,
#         defaults={
#             "total_encaminhamentos": total_encaminhamentos,
#             "total_fila": total_fila,
#             "tempo_medio_espera": media_dias,
#             "tempo_maximo_espera": tempo_maximo,
#             "especialidade_mais_demandada": especialidade.nome,
#             "duplicidades_evitas": duplicidades
#         }
#     )
#
#     for item in demanda:
#         nome = item["especialidade__nome"]
#
#         especialidade = Especialidade.objects.get(id=item["especialidade"])
#
#         esp_fila = fila.filter(especialidade=especialidade)
#
#         tempos_esp = esp_fila.annotate(
#             tempo_espera=ExpressionWrapper(
#                 hoje - F("data_solicitacao"),
#                 output_field=DurationField()
#             )
#         )
#
#         media_esp = tempos_esp.aggregate(media=Avg("tempo_espera"))
#         max_esp = tempos_esp.aggregate(maximo=Max("tempo_espera"))
#         duplicidades_por_especialidade = (
#             EventoAuditoria.objects
#             .filter(tipo_evento="tentativa_duplicidade")
#             .values("dados_extras__especialidade_id")
#             .annotate(total=Count("id"))
#         )
#
#         IndicadorEspecialidade.objects.update_or_create(
#             data=hoje,
#             especialidade=especialidade,
#             defaults={
#                 "total_fila": esp_fila.count(),
#                 "tempo_medio": media_esp["media"].days if media_esp["media"] else 0,
#                 "tempo_maximo": max_esp["maximo"].days if max_esp["maximo"] else 0
#             }
#         )
# def gerar_indicador_diario():
#     hoje = date.today()
#
#     queryset = Encaminhamento.objects.all()
#
#     total_encaminhamentos = queryset.count()
#
#     fila = queryset.filter(status__in=STATUS_FILA)
#     total_fila = fila.count()
#
#     # 🔹 Tempo de espera
#     tempos = fila.annotate(
#         tempo_espera=ExpressionWrapper(
#             hoje - F("data_solicitacao"),
#             output_field=DurationField()
#         )
#     )
#
#     # 🔹 Média
#     media = tempos.aggregate(media=Avg("tempo_espera"))
#     media_dias = media["media"].days if media["media"] else 0
#
#     # 🔹 Máximo
#     maximo = tempos.aggregate(maximo=Max("tempo_espera"))
#     tempo_maximo = maximo["maximo"].days if maximo["maximo"] else 0
#
#     # 🔹 Demanda por especialidade
#     demanda = (
#         fila
#         .values("especialidade__nome")
#         .annotate(total=Count("id"))
#         .order_by("-total")
#     )
#
#     especialidade_top = demanda[0]["especialidade__nome"] if demanda else None
#
#     # 🔹 Duplicidades evitadas no dia
#     duplicidades = EventoAuditoria.objects.filter(
#         tipo_evento="tentativa_duplicidade",
#         data_evento__date=hoje
#     ).count()
#
#     # ✅ SALVA APENAS UMA VEZ (CORRETO)
#     IndicadorDiario.objects.update_or_create(
#         data=hoje,
#         defaults={
#             "total_encaminhamentos": total_encaminhamentos,
#             "total_fila": total_fila,
#             "tempo_medio_espera": media_dias,
#             "tempo_maximo_espera": tempo_maximo,
#             "especialidade_mais_demandada": especialidade_top,
#             "duplicidades_evitas": duplicidades
#         }
#     )
#     duplicidades_por_especialidade = (
#         EventoAuditoria.objects
#         .filter(tipo_evento="tentativa_duplicidade")
#         .values("dados_extras__especialidade_id")
#         .annotate(total=Count("id"))
#     )
#
#     # 🔹 INDICADORES POR ESPECIALIDADE
#     for item in demanda:
#         nome = item["especialidade__nome"]
#
#         especialidade = Especialidade.objects.get(nome=nome)
#
#         esp_fila = fila.filter(especialidade=especialidade)
#
#         tempos_esp = esp_fila.annotate(
#             tempo_espera=ExpressionWrapper(
#                 hoje - F("data_solicitacao"),
#                 output_field=DurationField()
#             )
#         )
#
#         media_esp = tempos_esp.aggregate(media=Avg("tempo_espera"))
#         max_esp = tempos_esp.aggregate(maximo=Max("tempo_espera"))
#
#         IndicadorEspecialidade.objects.update_or_create(
#             data=hoje,
#             especialidade=especialidade,
#             defaults={
#                 "total_fila": esp_fila.count(),
#                 "tempo_medio": media_esp["media"].days if media_esp["media"] else 0,
#                 "tempo_maximo": max_esp["maximo"].days if max_esp["maximo"] else 0
#             }
#         )

from datetime import date
from django.db.models import Avg, F, ExpressionWrapper, DurationField, Max, Count
from encaminhamentos.models import (
    Encaminhamento,
    IndicadorDiario,
    IndicadorEspecialidade,
    Especialidade,
    STATUS_FILA
)
from auditoria.models import EventoAuditoria


def gerar_indicador_diario():
    hoje = date.today()

    # 🔹 Base geral
    queryset = Encaminhamento.objects.all()

    total_encaminhamentos = queryset.count()

    # 🔹 Apenas fila ativa
    fila = queryset.filter(status__in=STATUS_FILA)
    total_fila = fila.count()

    # 🔹 Calcula tempo de espera
    tempos = fila.annotate(
        tempo_espera=ExpressionWrapper(
            hoje - F("data_solicitacao"),
            output_field=DurationField()
        )
    )

    # 🔹 Média de tempo
    media = tempos.aggregate(media=Avg("tempo_espera"))
    media_dias = media["media"].days if media["media"] else 0

    # 🔹 Tempo máximo
    maximo = tempos.aggregate(maximo=Max("tempo_espera"))
    tempo_maximo = maximo["maximo"].days if maximo["maximo"] else 0

    # 🔹 Demanda por especialidade (CORRIGIDO)
    demanda = (
        fila
        .values("especialidade__id", "especialidade__nome")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # 🔹 Especialidade mais demandada
    especialidade_top = demanda[0]["especialidade__nome"] if demanda else None

    # 🔹 Duplicidades evitadas no dia (CORRIGIDO)
    duplicidades = EventoAuditoria.objects.filter(
        tipo_evento="tentativa_duplicidade",
        data_evento__date=hoje  # ✔ campo correto
    ).count()

    # ✅ SALVA INDICADOR GERAL (UMA ÚNICA VEZ)
    IndicadorDiario.objects.update_or_create(
        data=hoje,
        defaults={
            "total_encaminhamentos": total_encaminhamentos,
            "total_fila": total_fila,
            "tempo_medio_espera": media_dias,
            "tempo_maximo_espera": tempo_maximo,
            "especialidade_mais_demandada": especialidade_top,
            "duplicidades_evitas": duplicidades
        }
    )

    # 🔹 Mapa de duplicidades por especialidade (MELHORIA)
    duplicidades_por_especialidade = (
        EventoAuditoria.objects
        .filter(tipo_evento="tentativa_duplicidade")
        .values("dados_extras__especialidade_id")
        .annotate(total=Count("id"))
    )

    duplicidade_map = {
        item["dados_extras__especialidade_id"]: item["total"]
        for item in duplicidades_por_especialidade
    }

    # 🔹 Indicadores por especialidade
    for item in demanda:
        especialidade_id = item["especialidade__id"]

        especialidade = Especialidade.objects.get(id=especialidade_id)

        esp_fila = fila.filter(especialidade=especialidade)

        tempos_esp = esp_fila.annotate(
            tempo_espera=ExpressionWrapper(
                hoje - F("data_solicitacao"),
                output_field=DurationField()
            )
        )

        media_esp = tempos_esp.aggregate(media=Avg("tempo_espera"))
        max_esp = tempos_esp.aggregate(maximo=Max("tempo_espera"))

        IndicadorEspecialidade.objects.update_or_create(
            data=hoje,
            especialidade=especialidade,
            defaults={
                "total_fila": esp_fila.count(),
                "tempo_medio": media_esp["media"].days if media_esp["media"] else 0,
                "tempo_maximo": max_esp["maximo"].days if max_esp["maximo"] else 0,
                # 🔥 melhoria pronta para uso futuro
                # "duplicidades": duplicidade_map.get(especialidade_id, 0)
            }
        )