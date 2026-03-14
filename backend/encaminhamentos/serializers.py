from rest_framework import serializers
from .models import Especialidade, Procedimento, Encaminhamento


# ----------------------------------------------
# Serializer de especialidade
# Converte objeto do banco para JSON
# ----------------------------------------------
class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = ['id', 'nome']


# ----------------------------------------------
# Serializer de procedimento
# ----------------------------------------------
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
            'tipo',
            'especialidade',
            'procedimento',
            'profissional',
            'prioridade',
            'status',
            'observacao',
            'data_solicitacao'
        ]

    # -----------------------------------------------------
    # Validação personalizada
    # -----------------------------------------------------
    def validate(self, data):

        paciente = data['paciente']
        especialidade = data['especialidade']
        procedimento = data.get('procedimento')

        # -------------------------------------------------
        # Verifica se já existe encaminhamento semelhante
        # -------------------------------------------------
        queryset = Encaminhamento.objects.filter(

            paciente=paciente,
            especialidade=especialidade,
            procedimento=procedimento,

            # apenas se ainda não foi realizado
            status__in=['solicitado', 'aguardando']

        )
        # -------------------------------------------------
        # Se estiver editando (PUT/PATCH)
        # remove o próprio registro da verificação
        # -------------------------------------------------
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                "Paciente já possui encaminhamento aguardando para este procedimento/especialidade."
            )
        return data


