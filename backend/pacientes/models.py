from django.db import models


# ======================================================
# MICROÁREA
# Representa a divisão territorial da USF
# ======================================================

class MicroArea(models.Model):

    microarea = models.CharField(
        max_length=2,
        unique=True
    )

    agente = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Nome do Agente Comunitário de Saúde responsável"
    )

    ativa = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Microárea {self.microarea}"

# ======================================================
# PACIENTE
# Representa o cidadão atendido pela unidade
# ======================================================

class Paciente(models.Model):
    # --------------------------------------------------
    # Nome completo do paciente
    # --------------------------------------------------

    nome = models.CharField(
        max_length=200,
        db_index=True,
    )

    # --------------------------------------------------
    # CPF do paciente
    # Pode ser usado para identificação
    # --------------------------------------------------

    cpf = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        db_index=True
    )

    # --------------------------------------------------
    # Cartão Nacional de Saúde (SUS)
    # --------------------------------------------------

    cns = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        help_text="Cartão Nacional de Saúde"
    )

    # --------------------------------------------------
    # Data de nascimento
    # --------------------------------------------------

    data_nascimento = models.DateField(
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Sexo do paciente
    # --------------------------------------------------

    sexo = models.CharField(
        max_length=10,
        choices=[
            ("M", "Masculino"),
            ("F", "Feminino"),
            ("I", "Indeterminado")
        ],
        blank=True,
        null=True
    )

    # --------------------------------------------------
    # Nome da mãe
    # Campo muito usado no SUS para identificação
    # --------------------------------------------------
    nome_mae = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # Contato
    # -------------------------------------------------

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    endereco = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # Território
    # -------------------------------------------------

    microarea = models.ForeignKey(
        MicroArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    vinculo = models.CharField(
        max_length=30,
        choices=[
            ("ativo", "Vinculado à área"),
            ("sem_vinculo", "Sem vínculo"),
        ],
        default="ativo"
    )

    # -------------------------------------------------
    # Controle
    # -------------------------------------------------
    sincronizado = models.BooleanField(
        default=True,
        help_text="Indica se o paciente apareceu na última importação"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    ativo = models.BooleanField(
        default=True
    )


    # -------------------------------------------------
    # Representação do objeto
    # -------------------------------------------------

    def __str__(self):
        return self.nome