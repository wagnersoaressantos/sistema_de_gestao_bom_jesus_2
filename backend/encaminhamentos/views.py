from rest_framework.decorators import api_view
from django.shortcuts import render
from django.db.models import Count
from rest_framework import viewsets
from .models import Especialidade, Procedimento, Encaminhamento
from .serializers import (
    EspecialidadeSerializer,
    ProcedimentoSerializer,
    EncaminhamentoSerializer
)


# ---------------------------------------------------------
# View que calcula a demanda reprimida
# ---------------------------------------------------------
@api_view(['GET'])
def demanda_reprimida(request):

    # Busca todos os encaminhamentos que ainda não foram realizados
    encaminhamentos = Encaminhamento.objects.filter(
        status__in=["solicitado", "aguardando", "guia_disponivel"]
    )

    # Agrupa os dados por procedimento e conta quantos existem
    dados = encaminhamentos.values(
        'procedimento__nome'
    ).annotate(
        total=Count('id')
    ).order_by('-total')

    # Envia os dados para a página HTML
    return render(request, 'demanda_reprimida.html', {
        'dados': dados
    })




# API de especialidades
class EspecialidadeViewSet(viewsets.ModelViewSet):

    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializer


# API de procedimentos
class ProcedimentoViewSet(viewsets.ModelViewSet):

    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer


# API de encaminhamentos
class EncaminhamentoViewSet(viewsets.ModelViewSet):

    queryset = Encaminhamento.objects.all()
    serializer_class = EncaminhamentoSerializer


