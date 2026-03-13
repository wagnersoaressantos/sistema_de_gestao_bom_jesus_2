"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from encaminhamentos.views import demanda_reprimida
from rest_framework.routers import DefaultRouter
from pacientes.views import PacienteViewSet
from encaminhamentos.views import (
    EspecialidadeViewSet,
    ProcedimentoViewSet,
    EncaminhamentoViewSet
)
from django.urls import path, include


router = DefaultRouter()

router.register(r'pacientes', PacienteViewSet)
router.register(r'especialidades', EspecialidadeViewSet)
router.register(r'procedimentos', ProcedimentoViewSet)
router.register(r'encaminhamentos', EncaminhamentoViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # Página de relatório de demanda reprimida
    path('demanda/', demanda_reprimida, name='demanda_reprimida'),
]
