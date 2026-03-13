from django.shortcuts import render

from rest_framework import viewsets
from .models import Paciente
from .serializers import PacienteSerializer


# ViewSet cria automaticamente:
# GET, POST, PUT, DELETE
class PacienteViewSet(viewsets.ModelViewSet):

    # busca todos os pacientes
    queryset = Paciente.objects.all()

    # usa o serializer que criamos
    serializer_class = PacienteSerializer
