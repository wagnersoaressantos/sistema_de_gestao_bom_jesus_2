from rest_framework import serializers
from .models import Usuario



class UsuarioSerializer(serializers.ModelSerializer):

    """
    Serializer responsável por converter
    o modelo Usuario em JSON e vice-versa
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario

        fields = [
            "id",
            "cpf",
            "nome",
            "email",
            "cargo",
            "unidade",
            "is_active",
            "password",
            "data_criacao"
        ]

        read_only_fields = [
            "id",
            "data_criacao"
        ]

    # ---------------------------------------------------
    # CRIA USUÁRIO COM SENHA CRIPTOGRAFADA
    # ---------------------------------------------------

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = Usuario(**validated_data)

        user.set_password(password)

        user.save()

        return user
