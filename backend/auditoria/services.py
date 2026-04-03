from .models import Auditoria


def registrar_auditoria(usuario, acao, descricao):

    Auditoria.objects.create(
        usuario=usuario,
        acao=acao,
        descricao=descricao
    )

from .models import EventoAuditoria


def registrar_evento(
    tipo,
    paciente=None,
    usuario=None,
    modelo=None,
    objeto_id=None,
    descricao=None,
    dados_extras=None
):
    EventoAuditoria.objects.create(
        tipo_evento=tipo,
        paciente=paciente,
        usuario=usuario,
        modelo=modelo,
        objeto_id=objeto_id,
        descricao=descricao,
        dados_extras=dados_extras or {}
    )