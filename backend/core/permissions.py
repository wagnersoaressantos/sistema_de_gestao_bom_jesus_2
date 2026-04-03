from rest_framework.permissions import BasePermission


class GrupoPermission(BasePermission):

    grupo = None

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.groups.filter(
            name=self.grupo
        ).exists()


class IsAdministrador(GrupoPermission):
    grupo = "Administrador"


class IsGestor(GrupoPermission):
    grupo = "Gestor"


class IsRecepcao(GrupoPermission):
    grupo = "Recepcao"


class IsEnfermeiro(GrupoPermission):
    grupo = "Enfermeiro"

class IsMedico(GrupoPermission):
    grupo = "Medico"

class IsAcsTacs(GrupoPermission):
    grupo = "ACS/TACS"