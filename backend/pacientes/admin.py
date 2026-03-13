from django.contrib import admin
from .models import Paciente


# Classe que configura como o modelo Paciente aparece no painel admin
class PacienteAdmin(admin.ModelAdmin):

    # Campos que aparecem na lista de pacientes
    list_display = (
        'nome',
        'cpf',
        'data_nascimento',
        'telefone',
        'microarea'
    )

    # Permite buscar pacientes pelo nome ou CPF
    search_fields = (
        'nome',
        'cpf'
    )

    # Adiciona filtros na lateral direita
    list_filter = (
        'microarea',
    )


# Registra o modelo Paciente com a configuração acima
admin.site.register(Paciente, PacienteAdmin)
