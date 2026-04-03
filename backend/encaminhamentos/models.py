from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Case, When, IntegerField
from pacientes.models import Paciente
from django.db import models

STATUS_FILA = [
    "solicitado",
    "aguardando",
    "enviado_regulacao",
    "enviado_regulacao_upae",
    "retornado_sem_vaga"
]


class Especialidade(models.Model):
    TIPO_CHOICES = [
        ("consulta", "Consulta"),
        ("exame", "Exame"),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES
    )

    nome = models.CharField(
        max_length=150,
        unique=True
    )

    descricao = models.TextField(
        blank=True,
        null=True
    )

    ativa = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nome



class Encaminhamento(models.Model):
    STATUS_CHOICES = [
        ("solicitado", "Solicitado"),
        ("aguardando", "Aguardando"),
        ("enviado_regulacao", "Enviado para regulação"),
        ("enviado_regulacao_upae", "Enviado para regulação UPAE"),
        ("retornado_sem_vaga", "Retornou sem vaga"),
        ("disponivel", "Guia Disponível"),
        ("entregue", "Guia Entregue"),
        ("cancelado", "Cancelado"),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="encaminhamentos"
    )


    PRIORIDADE_CHOICES = [
        ("normal", "Normal"),
        ("urgente", "Urgente"),
        ("preferencial","Preferencial")
    ]

    especialidade = models.ForeignKey(
        "Especialidade",
        on_delete=models.PROTECT
    )

    data_solicitacao = models.DateField()  # data do encaminhamento médico

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )  # quando entrou no sistema

    profissional_solicitante = models.CharField(
        max_length=200
    )

    prioridade = models.CharField(
        max_length=20,
        choices=PRIORIDADE_CHOICES,
        default="normal"
    )

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default="solicitado"
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )

    posicao_fila = models.IntegerField(null=True, blank=True)

    def clean(self):

        existe = Encaminhamento.objects.filter(
            paciente=self.paciente,
            especialidade=self.especialidade,
            status__in=STATUS_FILA
        ).exclude(pk=self.pk).first()

        if existe:
            raise ValidationError({
                "paciente": "Já existe encaminhamento ativo para essa especialidade"
            })


    def save(self, *args, **kwargs):

        if self.pk:
            antigo = Encaminhamento.objects.get(pk=self.pk)
            status_antigo = antigo.status
        else:
            status_antigo = None
        self.full_clean()

        super().save(*args, **kwargs)

        recalcular_fila(self.especialidade)


class HistoricoStatus(models.Model):

    encaminhamento = models.ForeignKey(
        Encaminhamento,
        on_delete=models.CASCADE,
        related_name="historico"
    )

    status = models.CharField(
        max_length=100,
        choices=Encaminhamento.STATUS_CHOICES
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )

    alteracao_manual = models.BooleanField(
        default=True
    )


    def __str__(self):
        return f"{self.encaminhamento} - {self.status}"

def recalcular_fila(especialidade):
    fila = Encaminhamento.objects.filter(
        especialidade=especialidade,
        status__in=STATUS_FILA
    ).annotate(
        prioridade_ordem=Case(
            When(prioridade="preferencial", then=0),
            When(prioridade="urgente", then=1),
            When(prioridade="normal", then=2),
            output_field=IntegerField()
        )
    ).order_by("prioridade_ordem","data_solicitacao")

    for index, enc in enumerate(fila,start=1):
        enc.posicao_fila=index
        Encaminhamento.objects.filter(pk=enc.pk).update(
            posicao_fila=index
        )

class IndicadorDiario(models.Model):
    data = models.DateField(unique=True)  # 🔥 evita duplicidade de registros

    total_encaminhamentos = models.IntegerField(default=0)
    total_fila = models.IntegerField(default=0)
    duplicidades_evitas = models.IntegerField(default=0)

    tempo_medio_espera = models.FloatField(default=0)
    tempo_maximo_espera = models.IntegerField(default=0)

    especialidade_mais_demandada = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Indicadores {self.data}"


class IndicadorEspecialidade(models.Model):

    data = models.DateField()
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    total_fila = models.IntegerField()
    tempo_medio = models.IntegerField()
    tempo_maximo = models.IntegerField()