from encaminhamentos.models import Encaminhamento,STATUS_FILA


def obter_fila_especialidades(especialidades_id):
    fila = Encaminhamento.objects.filter(
        especialidade__id=especialidades_id,
        status__in = STATUS_FILA
    ).order_by(
        "prioridade",
        "data_solicitacao"
    )

    return fila