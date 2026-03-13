from rest_framework import serializers
from .models import Especialidade, Procedimento, Encaminhamento


# Serializer para especialidades
class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = ['id', 'nome']


# Serializer para procedimentos
class ProcedimentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Procedimento
        fields = ['id', 'nome', 'especialidade']


# Serializer para encaminhamentos
class EncaminhamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encaminhamento

        fields = [
            'id',
            'paciente',
            'procedimento',
            'profissional',
            'prioridade',
            'status',
            'observacao',
            'data_solicitacao'
        ]
