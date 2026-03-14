from rest_framework import serializers
from .models import AnexoEncaminhamento, Especialidade, HistoricoEncaminhamento, Procedimento, Encaminhamento


class HistoricoEncaminhamentoSerializer(serializers.ModelSerializer):

    class Meta:

        model = HistoricoEncaminhamento

        fields = [

            "status",
            "data",
            "observacao"
        ]

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

# -------------------------------------------------
# Serializer responsável pelo upload de arquivos
# -------------------------------------------------
class AnexoEncaminhamentoSerializer(serializers.ModelSerializer):

    class Meta:

        model = AnexoEncaminhamento

        # campos que a API irá receber ou retornar
        fields = [

            "id",

            # encaminhamento relacionado
            "encaminhamento",

            "tipo",

            # arquivo enviado
            "arquivo",

            # descrição opcional
            "descricao",

            # data automática do upload
            "data_upload"

        ]

        # data é apenas leitura
        read_only_fields = [

            "data_upload"
        ]


# Serializer para encaminhamentos
class EncaminhamentoSerializer(serializers.ModelSerializer):

    # -------------------------------------------------
    # Campos legíveis
    # -------------------------------------------------
    paciente_nome = serializers.CharField(
        source="paciente.nome",
        read_only=True
    )

    especialidade_nome = serializers.CharField(
        source="especialidade.nome",
        read_only=True
    )

    procedimento_nome = serializers.CharField(
        source="procedimento.nome",
        read_only=True
    )

    # -------------------------------------------------
    # Histórico de status do encaminhamento
    # -------------------------------------------------
    historico = HistoricoEncaminhamentoSerializer(
        many=True,
        read_only=True
    )

    tempos = serializers.SerializerMethodField()

    # -------------------------------------------------
    # Lista de arquivos anexados
    # -------------------------------------------------
    anexos = AnexoEncaminhamentoSerializer(
        many=True,
        read_only=True
    )



    class Meta:
        model = Encaminhamento
        # fields = "__all__"
        fields = [

            'id',
            'paciente',
            'paciente_nome',
            'tipo',
            'especialidade',
            'especialidade_nome',
            'procedimento',
            'procedimento_nome',
            'profissional',
            'prioridade',
            'status',
            'observacao',
            'data_solicitacao',
            'historico',
            "anexos",
            'tempos'
        ]

    # -------------------------------------------------
    # Validação para evitar duplicidade
    # -------------------------------------------------
    def validate(self, data):

        paciente = data.get("paciente")
        especialidade = data.get("especialidade")
        procedimento = data.get("procedimento")

        # -------------------------------------------------
        # Verifica se já existe encaminhamento semelhante
        # -------------------------------------------------
        queryset = Encaminhamento.objects.filter(

            paciente=paciente,
            especialidade=especialidade,
            procedimento=procedimento,

            # apenas se ainda não foi realizado
            status__in=[
                "solicitado",
                "aguardando",
                "guia_disponivel"
            ]

        )
        # -------------------------------------------------
        # Se estiver editando (PUT/PATCH)
        # remove o próprio registro da verificação
        # -------------------------------------------------
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():

            enc = queryset.first()

            raise serializers.ValidationError({

                "erro": "Paciente já possui encaminhamento ativo",

                "posicao_fila": enc.posicao_fila,

                "status": enc.status

            })
        return data

    def get_tempos(self, obj):

        return obj.calcular_tempos()
    
