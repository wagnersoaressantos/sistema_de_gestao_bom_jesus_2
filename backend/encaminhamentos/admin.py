from django.contrib import admin
from .models import Especialidade, Procedimento, Encaminhamento


# Configuração do admin para Especialidade
class EspecialidadeAdmin(admin.ModelAdmin):

    # Mostra o nome da especialidade
    list_display = ('nome',)


# Configuração do admin para Procedimento
class ProcedimentoAdmin(admin.ModelAdmin):

    # Mostra especialidade e nome do procedimento
    list_display = (
        'nome',
        'especialidade'
    )

    # Permite filtrar procedimentos pela especialidade
    list_filter = (
        'especialidade',
    )


class EncaminhamentoAdmin(admin.ModelAdmin):

    # Colunas exibidas na lista
    list_display = (
        'paciente',
        'procedimento',
        'prioridade',
        'status',
        'data_solicitacao'
    )

    # Filtros laterais
    list_filter = (
        'status',
        'prioridade',
        'procedimento'
    )

    # Campo de busca
    search_fields = (
        'paciente__nome',
    )



# Registrando os modelos no painel admin
admin.site.register(Especialidade, EspecialidadeAdmin)
admin.site.register(Procedimento, ProcedimentoAdmin)
admin.site.register(Encaminhamento, EncaminhamentoAdmin)
