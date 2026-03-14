from datetime import date

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
        ('resultado_disponivel', 'Resultado Disponível'),

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
    # Data em que o exame foi realizado
    # -------------------------------------------------
    data_entregue = models.DateField(

        null=True,
        blank=True
    )
    # -------------------------------------------------
    # Data em que o exame foi realizado
    # -------------------------------------------------
    data_resultado_disponivel = models.DateField(

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

         # verifica status antigo
        status_antigo = None

        if not novo:

            status_antigo = Encaminhamento.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)



        # -------------------------------------------------
        # registra histórico
        # -------------------------------------------------
        if novo or status_antigo != self.status:

            HistoricoEncaminhamento.objects.create(

            encaminhamento=self,
            status=self.status
        )

        # Se foi criado um novo encaminhamento
        if novo:

            recalcular_fila(self.especialidade, self.procedimento)

        # Se mudou para Guia Disponivel
        if self.status in ['guia_disponivel', 'entregue', 'resultado_disponivel']:

            recalcular_fila(self.especialidade, self.procedimento)
    
    def prioridade_valor(self):

        mapa = {
            'urgente': 1,
            'preferencial': 2,
            'normal': 3
        }
        return mapa.get(self.prioridade, 3)
    
    # -------------------------------------------------
    # Calcula o tempo entre as etapas do encaminhamento
    # -------------------------------------------------
    def calcular_tempos(self):

        historico = self.historico.order_by('data')

        tempos = []

        anterior = None

        for item in historico:

            if anterior:

                dias = (item.data - anterior.data).days

                tempos.append({

                    "de": anterior.status,
                    "para": item.status,
                    "dias": dias

                })

            anterior = item

        return tempos
    
    
# -------------------------------------------------
# Histórico de status do encaminhamento
# -------------------------------------------------
class HistoricoEncaminhamento(models.Model):

    encaminhamento = models.ForeignKey(
        Encaminhamento,
        on_delete=models.CASCADE,
        related_name="historico"
    )

    status = models.CharField(
        max_length=20
    )

    data = models.DateTimeField(
        auto_now_add=True
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return f"{self.encaminhamento.id} - {self.status}"

# -------------------------------------------------
# Arquivos anexados ao encaminhamento
# Ex: resultado de exame, laudo, receita etc
# -------------------------------------------------
class AnexoEncaminhamento(models.Model):

    # -------------------------------------------------
    # Tipos de anexos
    # -------------------------------------------------
    TIPO_ANEXO = [

    ("solicitacao", "Solicitação"),

    ("resultado", "Resultado do Exame"),

    ("outro", "Outro Documento")
    ]
    
    # -------------------------------------------------
    # Tipo do documento anexado
    # -------------------------------------------------
    tipo = models.CharField(

        max_length=20,

        choices=TIPO_ANEXO,

        default="resultado"
    )

    # -------------------------------------------------
    # Encaminhamento relacionado
    # Um encaminhamento pode ter vários arquivos
    # -------------------------------------------------
    encaminhamento = models.ForeignKey(

        Encaminhamento,
        on_delete=models.CASCADE,

        # permite acessar:
        # encaminhamento.anexos.all()
        related_name="anexos"

    )

    # -------------------------------------------------
    # Arquivo enviado
    # Pode ser PDF, imagem, etc
    # -------------------------------------------------
    arquivo = models.FileField(

        upload_to="resultados_exames/"
    )

    # -------------------------------------------------
    # Descrição opcional do arquivo
    # Ex: "Resultado ECG", "Laudo médico"
    # -------------------------------------------------
    descricao = models.CharField(

        max_length=200,
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # Data do envio do arquivo
    # -------------------------------------------------
    data_upload = models.DateTimeField(

        auto_now_add=True
    )

    # -------------------------------------------------
    # Representação do objeto
    # -------------------------------------------------
    def __str__(self):

        return f"Anexo {self.id} - Encaminhamento {self.encaminhamento.id}"

     # -------------------------------------------------
    # Automação ao anexar resultado
    # -------------------------------------------------
    def save(self, *args, **kwargs):

        # verifica se é um novo anexo
        novo = self.pk is None

        # salva o anexo normalmente
        super().save(*args, **kwargs)

        # se for novo anexo
        if novo:

            enc = self.encaminhamento

            # muda status para realizado
            enc.status = "resultado_disponivel"

            # salva data de realização
            enc.data_realizacao = date.today()

            enc.save()




def recalcular_fila(especialidade, procedimento):

    encaminhamentos = Encaminhamento.objects.filter(

        especialidade=especialidade,
        procedimento=procedimento,

        status__in=['solicitado', 'aguardando']

    ).order_by('data_solicitacao')

     # ordena por prioridade e data
    encaminhamentos = sorted(

        encaminhamentos,

        key=lambda x: (x.prioridade_valor(), x.data_solicitacao)
    )

    # Reorganiza posições
    for index, enc in enumerate(encaminhamentos, start=1):

        enc.posicao_fila = index

        enc.save(update_fields=['posicao_fila'])

