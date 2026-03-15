from django.db import models
from pacientes.models import Paciente


# -------------------------------------------------
# Tipos de serviços administrativos
# -------------------------------------------------
TIPO_SERVICO = [

    ("tfd", "Declaração TFD"),

    ("renovacao_receita", "Renovação de Receita"),

    ("declaracao_area", "Declaração de Morador da Área"),

    ("declaracao_comparecimento", "Declaração de Comparecimento"),

    ("outro", "Outro")
]


class ServicoSolicitado(models.Model):

    # -------------------------------------------------
    # Paciente relacionado
    # -------------------------------------------------
    paciente = models.ForeignKey(

        Paciente,
        on_delete=models.CASCADE
    )

    # -------------------------------------------------
    # Tipo do serviço solicitado
    # -------------------------------------------------
    tipo = models.CharField(

        max_length=50,
        choices=TIPO_SERVICO
    )

    # -------------------------------------------------
    # Observação
    # -------------------------------------------------
    observacao = models.TextField(

        blank=True,
        null=True
    )

    # -------------------------------------------------
    # Status do serviço
    # -------------------------------------------------
    status = models.CharField(

        max_length=20,

        choices=[

            ("solicitado", "Solicitado"),

            ("em_andamento", "Em andamento"),

            ("concluido", "Concluído")

        ],

        default="solicitado"
    )

    # -------------------------------------------------
    # Data da solicitação
    # -------------------------------------------------
    data_solicitacao = models.DateTimeField(

        auto_now_add=True
    )

    # -------------------------------------------------
    # Data de conclusão
    # -------------------------------------------------
    data_conclusao = models.DateTimeField(

        null=True,
        blank=True
    )

    def __str__(self):

        return f"{self.paciente} - {self.tipo}"
