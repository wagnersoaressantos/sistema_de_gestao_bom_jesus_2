from rest_framework import serializers
from .models import Especialidade, Encaminhamento, IndicadorDiario, STATUS_FILA


class IndicadorDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicadorDiario
        fields = "__all__"

class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = "__all__"



class EncaminhamentoSerializer(serializers.ModelSerializer):

    paciente_nome = serializers.CharField(source="paciente.nome", read_only=True)
    especialidade_nome = serializers.CharField(source="especialidade.nome", read_only=True)

    class Meta:
        model = Encaminhamento
        fields = "__all__"
        read_only_fields = ["posicao_fila"]

class EncaminhamentoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Encaminhamento
        exclude = ["posicao_fila"]

    def validate(self, data):

        paciente = data.get("paciente")
        especialidade = data.get("especialidade")

        request = self.context.get("request")

        # 🔹 valida duplicidade
        encaminhamento_existente = Encaminhamento.objects.filter(
            paciente=paciente,
            especialidade=especialidade,
            status__in=STATUS_FILA
        ).first()

        if encaminhamento_existente:

            from auditoria.services import registrar_evento

            # 🔥 REGISTRA EVENTO (muito bom - nível avançado)
            registrar_evento(
                tipo="tentativa_duplicidade",
                paciente=paciente,
                usuario=request.user,
                modelo="Encaminhamento",
                descricao=f"Tentativa de duplicidade para {encaminhamento_existente.especialidade.nome}",
                dados_extras={
                    "especialidade_id": especialidade.id,
                    "status_atual": encaminhamento_existente.status,
                    "data_solicitacao": str(encaminhamento_existente.data_solicitacao)
                }
            )

            raise serializers.ValidationError({
                "erro": "Já existe encaminhamento ativo",
                "detalhes": {
                    "especialidade": encaminhamento_existente.especialidade.nome,
                    "status": encaminhamento_existente.status,
                    "data": encaminhamento_existente.data_solicitacao
                }
            })

        return data

# class EncaminhamentoCreateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Encaminhamento
#         exclude=["posicao_fila"]
#
#
#     def validate(self, data):
#
#         paciente = data.get("paciente")
#         especialidade = data.get("especialidade")
#
#         request = self.context.get("request")
#
#         encaminhamento_existente = Encaminhamento.objects.filter(
#             paciente=paciente,
#             especialidade=especialidade,
#             status__in=STATUS_FILA
#         ).first()
#
#         if encaminhamento_existente:
#
#             from auditoria.services import registrar_evento
#
#             registrar_evento(
#                 tipo="tentativa_duplicidade",
#                 paciente=paciente,
#                 usuario=request.user,
#                 modelo="Encaminhamento",
#                 descricao=f"Tentativa de duplicidade para {encaminhamento_existente.especialidade.nome}",
#                 dados_extras={
#                     "especialidade_id": especialidade.id,
#                     "status_atual": encaminhamento_existente.status,
#                     "data_solicitacao": str(encaminhamento_existente.data_solicitacao)
#                 }
#             )
#
#             raise serializers.ValidationError({
#                 "erro": "Já existe encaminhamento ativo",
#                 "detalhes": {
#                     "especialidade": encaminhamento_existente.especialidade.nome,
#                     "status": encaminhamento_existente.status,
#                     "data": encaminhamento_existente.data_solicitacao
#                 }
#             })
#
#         return data