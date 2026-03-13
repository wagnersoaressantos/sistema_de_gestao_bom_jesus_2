from django.db import models
from django.core.exceptions import ValidationError
from pacientes.models import Paciente

class Especialidade(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Procedimento(models.Model):

    especialidade = models.ForeignKey(
        Especialidade,
        on_delete=models.CASCADE
    )

    nome = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.especialidade.nome} - {self.nome}"

class Encaminhamento(models.Model):

    # Opções de status do encaminhamento
    STATUS_CHOICES = [
        ("solicitado", "Solicitado"),
        ("aguardando", "Aguardando Marcação"),
        ("guia_disponivel", "Guia Disponível"),
        ("realizado", "Realizado"),
    ]

    # Paciente relacionado ao encaminhamento
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE
    )

    # Procedimento solicitado (ECG, ECO, Ultrassom, etc)
    procedimento = models.ForeignKey(
        Procedimento,
        on_delete=models.CASCADE
    )

    # Profissional que solicitou o encaminhamento
    profissional = models.CharField(max_length=200)

    # Data da solicitação
    data_solicitacao = models.DateField(auto_now_add=True)

    # Opções de prioridade do encaminhamento
    PRIORIDADE_CHOICES = [
    ("normal", "Normal"),
    ("urgente", "Urgente"),
    ("preferencial", "Preferencial"),
    ]

    # Prioridade do encaminhamento
    prioridade = models.CharField(
    max_length=20,
    choices=PRIORIDADE_CHOICES,
    default="normal"
    )

    # Status atual do encaminhamento
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="solicitado"
    )

    # Observações adicionais
    observacao = models.TextField(blank=True, null=True)

    # Data de criação no sistema
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente.nome} - {self.procedimento}"

    # ---------------------------------------------------------
    # Validação para evitar encaminhamento duplicado
    # ---------------------------------------------------------
    def clean(self):

        # Verifica se já existe encaminhamento para
        # o mesmo paciente e mesmo procedimento
        existe = Encaminhamento.objects.filter(
            paciente=self.paciente,
            procedimento=self.procedimento,
            status__in=[
                "solicitado",
                "aguardando",
                "guia_disponivel"
            ]
        ).exclude(id=self.id).exists()

        # Se existir, bloqueia o cadastro
        if existe:
            raise ValidationError(
                "Este paciente já possui um encaminhamento ativo para esse procedimento."
            )
