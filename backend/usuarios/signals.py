from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def criar_grupos(sender, **kwargs):

    grupos = [
        "Administrador",
        "Gestor",
        "Recepcao",
        "Enfermeiro",
        "Medico"
    ]

    for nome in grupos:
        Group.objects.get_or_create(name=nome)
