from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    # campos exibidos na lista
    list_display = (
        "cpf",
        "nome",
        "cargo",
        "unidade",
        "is_active",
        "is_staff",
    )

    # campos editáveis
    fieldsets = (
        (None, {"fields": ("cpf", "password")}),

        ("Informações pessoais", {
            "fields": ("nome", "email", "cargo", "unidade")
        }),

        ("Permissões", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("cpf", "nome", "password1", "password2", "is_staff", "is_active")
        }),
    )

    search_fields = ("cpf", "nome")

    ordering = ("cpf",)