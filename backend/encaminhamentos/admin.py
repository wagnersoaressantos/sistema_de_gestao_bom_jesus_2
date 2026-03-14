from django.contrib import admin
from .models import AnexoEncaminhamento, Especialidade, Procedimento, Encaminhamento


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

# -------------------------------------------------
# Inline para mostrar anexos no encaminhamento
# -------------------------------------------------
class AnexoInline(admin.TabularInline):

    model = AnexoEncaminhamento

    extra = 0


class EncaminhamentoAdmin(admin.ModelAdmin):

    # Colunas exibidas na lista
    list_display = (

        'paciente',
        'tipo',
        'especialidade',
        'procedimento',
        'prioridade',
        'status',
        'data_solicitacao',
        "possui_anexo",
        "posicao_fila"
    )


     # mostra anexos dentro da tela do encaminhamento
    inlines = [

        AnexoInline
    ]
    # Filtros laterais
    list_filter = (
        'tipo',
        'status',
        'prioridade',
        'especialidade'
    )


    # Campo de busca
    search_fields = (
        'paciente__nome',
    )

    # -------------------------------------------------
    # Verifica se o encaminhamento possui anexos
    # obj é o objeto da linha do banco
    # -------------------------------------------------
    def possui_anexo(self, obj):

        return obj.anexos.exists()

    # mostra ícone ✔ ou ✖ no admin
    possui_anexo.boolean = True

    # nome da coluna
    possui_anexo.short_description = "Tem anexo?"

# -------------------------------------------------
# Admin dos anexos
# -------------------------------------------------
@admin.register(AnexoEncaminhamento)
class AnexoEncaminhamentoAdmin(admin.ModelAdmin):

    # campos mostrados na lista
    list_display = (

        "id",
        "encaminhamento",
        "descricao",
        "data_upload"

    )




# Registrando os modelos no painel admin
admin.site.register(Especialidade, EspecialidadeAdmin)
admin.site.register(Procedimento, ProcedimentoAdmin)
admin.site.register(Encaminhamento, EncaminhamentoAdmin)