from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# ======================================================
# GERENCIADOR DE USUÁRIO
# responsável por criar usuários e superusuários
# ======================================================

class UsuarioManager(BaseUserManager):

    def create_user(self, cpf, nome, password=None, **extra_fields):

        if not cpf:
            raise ValueError('CPF obrigatório')

        user = self.model(
            cpf=cpf,
            nome=nome,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, nome, password, **extra_fields)

# ======================================================
# MODELO DE USUÁRIO
# ======================================================

class Usuario(AbstractBaseUser, PermissionsMixin):

    # identificação principal
    cpf = models.CharField(
        max_length=11,
        unique=True,
    )

    nome = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    cargo = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    unidade = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    # gerenciador
    objects = UsuarioManager()

    # campo de login
    USERNAME_FIELD = "cpf"

    REQUIRED_FIELDS = ["nome"]

    def __str__(self):
        return self.nome