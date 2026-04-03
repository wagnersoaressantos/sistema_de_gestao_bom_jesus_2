from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from encaminhamentos.models import Encaminhamento
from .models import Auditoria


# 🔹 Guarda estado anterior
@receiver(pre_save, sender=Encaminhamento)
def capturar_estado_anterior(sender, instance, **kwargs):

    if instance.pk:
        try:
            antigo = Encaminhamento.objects.get(pk=instance.pk)
            instance._status_antigo = antigo.status
        except Encaminhamento.DoesNotExist:
            instance._status_antigo = None
    else:
        instance._status_antigo = None


# 🔹 Registra auditoria
@receiver(post_save, sender=Encaminhamento)
def registrar_alteracao(sender, instance, created, **kwargs):

    if created:
        Auditoria.objects.create(
            usuario=None,
            acao="Criação",
            descricao=f"Encaminhamento criado para {instance.paciente.nome} "
                      f"({instance.especialidade.nome})"
        )

    else:
        status_antigo = getattr(instance, "_status_antigo", None)
        status_novo = instance.status

        # Só registra se mudou
        if status_antigo != status_novo:

            Auditoria.objects.create(
                usuario=None,
                acao="Alteração de status",
                descricao=(
                    f"Encaminhamento de {instance.paciente.nome} "
                    f"({instance.especialidade.nome}) "
                    f"alterado de '{status_antigo}' → '{status_novo}'"
                )
            )