from django.db import models
from django.utils.timezone import now
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

    # -------------------------------------------------
    # Tipo de encaminhamento
    # -------------------------------------------------
    TIPO_ENCAMINHAMENTO = [

        ('especialista', 'Especialista'),

        ('exame', 'Exame'),

    ]

    # -------------------------------------------------
    # Status do encaminhamento
    # -------------------------------------------------
    STATUS_CHOICES = [

        ('solicitado', 'Solicitado'),

        ('aguardando', 'Aguardando Marcação'),

        ('guia_disponivel', 'Guia Disponível'),

        ('entregue', 'Entregue'),

    ]

    # -------------------------------------------------
    # Prioridade do encaminhamento
    # -------------------------------------------------
    PRIORIDADE_CHOICES = [

        ('normal', 'Normal'),

        ('urgente', 'Urgente'),

        ('preferencial', 'Preferencial'),

    ]

    # -------------------------------------------------
    # Paciente relacionado
    # -------------------------------------------------
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE
    )

    # -------------------------------------------------
    # Tipo do encaminhamento
    # especialista ou exame
    # -------------------------------------------------
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_ENCAMINHAMENTO,
        default='exame'
    )

    # -------------------------------------------------
    # Especialidade relacionada
    # cardiologia, ortopedia, etc
    # -------------------------------------------------
    especialidade = models.ForeignKey(
        'Especialidade',
        on_delete=models.CASCADE
    )

    # -------------------------------------------------
    # Procedimento (opcional)
    # usado quando for exame
    # -------------------------------------------------
    procedimento = models.ForeignKey(
        'Procedimento',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # -------------------------------------------------
    # Profissional que solicitou
    # -------------------------------------------------
    profissional = models.CharField(
        max_length=200
    )

    # -------------------------------------------------
    # Prioridade
    # -------------------------------------------------
    prioridade = models.CharField(
        max_length=20,
        choices=PRIORIDADE_CHOICES,
        default='normal'
    )

    # -------------------------------------------------
    # Status atual
    # -------------------------------------------------
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='solicitado'
    )

    # -------------------------------------------------
    # Observações
    # -------------------------------------------------
    observacao = models.TextField(
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # Data da solicitação
    # -------------------------------------------------
    data_solicitacao = models.DateField(
    default=now
)
    # -------------------------------------------------
    # Posição do paciente na fila
    # -------------------------------------------------
    posicao_fila = models.IntegerField(
        null=True,
        blank=True
    )


    # -------------------------------------------------
    # Representação do objeto
    # -------------------------------------------------
    def __str__(self):

        return f"{self.paciente} - {self.especialidade}"

    # -------------------------------------------------
    # Função para recalcular a fila
    # -------------------------------------------------

    def save(self, *args, **kwargs):

        novo = self.pk is None

        super().save(*args, **kwargs)

        # Se foi criado um novo encaminhamento
        if novo:

            recalcular_fila(self.especialidade)

        # Se mudou para Guia Disponivel
        if self.status == 'guia_disponivel':

            recalcular_fila(self.especialidade)

def recalcular_fila(especialidade):

        encaminhamentos = Encaminhamento.objects.filter(

        especialidade=especialidade,

        status__in=['solicitado', 'aguardando']

        ).order_by('data_solicitacao')

        # Reorganiza posições
        for index, enc in enumerate(encaminhamentos, start=1):

            enc.posicao_fila = index
            enc.save(update_fields=['posicao_fila'])
