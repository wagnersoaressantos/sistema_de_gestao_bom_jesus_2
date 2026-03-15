from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from encaminhamentos.models import Encaminhamento
from servicos.models import ServicoSolicitado

from .models import Paciente
from .serializers import PacienteSerializer


# ViewSet cria automaticamente:
# GET, POST, PUT, DELETE
class PacienteViewSet(viewsets.ModelViewSet):

    # busca todos os pacientes
    queryset = Paciente.objects.all()

    # usa o serializer que criamos
    serializer_class = PacienteSerializer



@api_view(['GET'])
def historico_paciente(request, paciente_id):

    historico = []

    # -------------------------------------------------
    # Buscar encaminhamentos
    # -------------------------------------------------
    encaminhamentos = Encaminhamento.objects.filter(

        paciente_id=paciente_id
    )

    for e in encaminhamentos:

        historico.append({

            "tipo": "encaminhamento",

            "descricao": f"{e.especialidade.nome} - {e.procedimento.nome if e.procedimento else 'Consulta'}",

            "status": e.status,

            "data": e.data_solicitacao

        })

    # -------------------------------------------------
    # Buscar serviços administrativos
    # -------------------------------------------------
    servicos = ServicoSolicitado.objects.filter(

        paciente_id=paciente_id
    )

    for s in servicos:

        historico.append({

            "tipo": "servico",

            "descricao": s.get_tipo_display(),

            "status": s.status,

            "data": s.data_solicitacao

        })

    # ordena pela data
    historico.sort(key=lambda x: x["data"], reverse=True)

    return Response(historico)

