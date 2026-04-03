
from django.contrib import admin
from .models import Especialidade, Encaminhamento, IndicadorDiario


class FilaEsperaFilter(admin.SimpleListFilter):
    title = ('Fila de Espera') # Nome que aparece no topo do filtro
    parameter_name = 'status_fila' # O parâmetro que vai na URL

    def lookups(self, request, model_admin):
        # Opções que o usuário verá no menu lateral
        return (
            ('ativa', ('Apenas Fila de Espera')),
        )

    def queryset(self, request, queryset):
        # Se o usuário clicar em "Apenas Fila de Espera"
        if self.value() == 'ativa':
            return queryset.filter(status__in=[
                "solicitado",
                "aguardando",
                "enviado_regulacao",
                "enviado_regulacao_upae",
                "retornado_sem_vaga"
            ])
        return queryset


@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "tipo",
        "ativa",
    )

    list_filter = (
        "tipo",
        "ativa"
    )

    search_fields = (
        "nome",
    )




# @admin.register(Fila)
# class FilaAdmin(admin.ModelAdmin):
#     list_display = (
#         "paciente",
#         "especialidade",
#         "status",
#         "prioridade",
#         "posicao_fila",
#         "data_solicitacao"
#     )
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#
#         return qs.filter(status__in=[
#             "solicitado",
#             "aguardando",
#             "enviado_regulacao",
#             "enviado_regulacao_upae",
#             "retornado_sem_vaga"
#         ])

@admin.register(Encaminhamento)
class EncaminhamentoAdmin(admin.ModelAdmin):

    list_display = (
        "paciente",
        "especialidade",
        "status",
        "prioridade",
        "posicao_fila",
        "data_solicitacao"
    )

    fields = (
        "paciente",
        "especialidade",
        "data_solicitacao",
        "profissional_solicitante",
        "prioridade",
        "status",
        "observacao"
    )

    list_filter = (
        FilaEsperaFilter,
        "especialidade",
        "prioridade",
        "status"
    )

    search_fields = (
        "paciente__nome",
    )


    ordering = ("posicao_fila",)



@admin.register(IndicadorDiario)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = (
        "data",
        "total_encaminhamentos",
        "total_fila",
        "tempo_medio_espera",
        "tempo_maximo_espera",
        "duplicidades_evitas"
    )