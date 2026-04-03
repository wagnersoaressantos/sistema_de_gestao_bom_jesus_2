from django.contrib import admin
from .models import Paciente, MicroArea


# ======================================================
# ADMIN MICROÁREA
# ======================================================

@admin.register(MicroArea)
class MicroAreaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "microarea",
        "agente",
        "ativa"
    )

    search_fields = (
        "microarea",
        "agente"
    )

    list_filter = (
        "ativa",
    )


# ======================================================
# ADMIN PACIENTE
# ======================================================

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):

    # campos exibidos na lista
    list_display = (
        "id",
        "nome",
        "cpf",
        "cns",
        "microarea",
        "vinculo",
        "telefone",
        "ativo"
    )

    # filtros laterais
    list_filter = (
        "microarea",
        "vinculo",
        "ativo"
    )

    # busca
    search_fields = (
        "nome",
        "cpf",
        "cns",
        "telefone"
    )

    # ordenação
    ordering = (
        "nome",
    )