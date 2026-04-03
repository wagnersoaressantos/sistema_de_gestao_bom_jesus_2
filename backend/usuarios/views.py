from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Usuario
from .serializers import UsuarioSerializer
from core.permissions import IsAdministrador,IsRecepcao, IsGestor, IsEnfermeiro, IsMedico, IsAcsTacs


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API responsável por gerenciar usuários do sistema
    """

    queryset = Usuario.objects.all()

    serializer_class = UsuarioSerializer

    # permission_classes = [AllowAny]

    permission_classes = [
        IsAuthenticated,
        IsAdministrador,
        IsRecepcao,
        IsGestor,
        IsEnfermeiro,
        IsMedico,
        IsAcsTacs
    ]