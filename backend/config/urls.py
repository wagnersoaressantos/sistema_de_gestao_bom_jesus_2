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
from encaminhamentos.views import AnexoEncaminhamentoViewSet, demanda_reprimida, painel_fila, tempo_medio_espera
from rest_framework.routers import DefaultRouter
from pacientes.views import PacienteViewSet
from encaminhamentos.views import (
    EspecialidadeViewSet,
    ProcedimentoViewSet,
    EncaminhamentoViewSet
)
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




router = DefaultRouter()

router.register(r'pacientes', PacienteViewSet)
router.register(r'especialidades', EspecialidadeViewSet)
router.register(r'procedimentos', ProcedimentoViewSet)
router.register(r'encaminhamentos', EncaminhamentoViewSet)
router.register(r'anexos',AnexoEncaminhamentoViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/demanda/', demanda_reprimida),
    path('api/tempo-espera/', tempo_medio_espera),
    path('api/painel/', painel_fila),
]

# -------------------------------------------------
# Permite acessar arquivos enviados
# -------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
