from rest_framework import serializers
from .models import Paciente, MicroArea


# ======================================================
# SERIALIZER MICROÁREA
# ======================================================

class MicroAreaSerializer(serializers.ModelSerializer):

    class Meta:

        model = MicroArea

        fields = [
            "id",
            "microarea",
            "agente",
            "ativa"
        ]

# ======================================================
# SERIALIZER PACIENTE
# ======================================================

class PacienteSerializer(serializers.ModelSerializer):

    # mostra numero da microárea no retorno
    microarea_numero= serializers.CharField(
        source="microarea.microarea",
        read_only=True
    )

    class Meta:

        model = Paciente

        fields = [

            "id",

            "nome",

            "cpf",

            "cns",

            "data_nascimento",

            "sexo",

            "telefone",

            "endereco",

            "microarea",
            "microarea_numero",

            "vinculo",

            "ativo",

            "data_cadastro"
        ]

        read_only_fields = [
            "id",
            "data_cadastro"
        ]



class ImportacaoPacienteSerializer(serializers.Serializer):

    arquivo = serializers.FileField()