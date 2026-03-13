from django.db import models

class Paciente(models.Model):

    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    cns = models.CharField(max_length=15, blank=True, null=True)

    data_nascimento = models.DateField()

    telefone = models.CharField(max_length=20, blank=True, null=True)

    nome_mae = models.CharField(max_length=200)

    endereco = models.CharField(max_length=255, blank=True, null=True)

    microarea = models.CharField(max_length=50, blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome