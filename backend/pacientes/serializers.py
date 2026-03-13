from rest_framework import serializers
from .models import Paciente


# Serializer converte o modelo Paciente para JSON
class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paciente

        # Campos que serão enviados pela API
        fields = [
            'id',
            'nome',
            'cpf',
            'cns',
            'data_nascimento',
            'telefone',
            'nome_mae',
            'endereco',
            'microarea'
        ]
