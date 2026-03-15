from django.contrib import admin
from .models import ServicoSolicitado


# -------------------------------------------------
# Admin para visualizar serviços solicitados
# -------------------------------------------------
@admin.register(ServicoSolicitado)
class ServicoSolicitadoAdmin(admin.ModelAdmin):

    list_display = (

        "id",
        "paciente",
        "tipo",
        "status",
        "data_solicitacao"
    )

    list_filter = (

        "tipo",
        "status"
    )

    search_fields = (

        "paciente__nome",
    )
