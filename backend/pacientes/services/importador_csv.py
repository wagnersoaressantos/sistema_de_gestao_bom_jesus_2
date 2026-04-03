import csv

import re
from datetime import datetime

from pacientes.models import MicroArea, Paciente

def encontrar_paciente(cpf,cns, nome,data_nascimento):
    paciente = None
    if cns:
        paciente = Paciente.objects.filter(cns=cns).first()
    if not paciente and cpf:
        paciente = Paciente.objects.filter(cpf=cpf).first()
    if not paciente and nome and data_nascimento:
        paciente = Paciente.objects.filter(nome__iexact=nome.strip(),data_nascimento=data_nascimento).first()
    return paciente

def possivel_duplicidade(nome,data_nascimento):
    if not nome or not data_nascimento:
        return None
    return Paciente.objects.filter(nome__icontains=nome.split()[0],data_nascimento=data_nascimento).first()

def converter_data(data_str):

    if not data_str:
        return None

    try:
        return datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        return None


def limpar_numero(valor):

    if not valor:
        return None

    return re.sub(r'\D', '', valor)


def importar_pacientes_csv(caminho_arquivo):
    pacientes_novos = 0
    pacientes_atualizados = 0
    detalhe_importacao = []

    # -------------------------------------------------
    # MARCAR TODOS COMO NÃO SINCRONIZADOS
    # -------------------------------------------------

    Paciente.objects.update(
        sincronizado=False
    )

    with open(caminho_arquivo, encoding="latin-1") as arquivo:

        linhas = arquivo.readlines()

        # encontrar a linha do cabeçalho
        indice_cabecalho = None

        for i, linha in enumerate(linhas):

            if "Nome equipe" in linha:
                indice_cabecalho = i
                break

        if indice_cabecalho is None:
            raise Exception("Cabeçalho do CSV não encontrado")

        # pegar apenas a tabela
        linhas_csv = linhas[indice_cabecalho:]

        leitor = csv.DictReader(linhas_csv, delimiter=";")

        for linha in leitor:

            nome = linha.get("Nome")

            if not nome:
                continue

            documento = limpar_numero(linha.get("CPF/CNS"))

            cpf = None
            cns = None

            if documento:

                if len(documento) == 11:
                    cpf = documento

                elif len(documento) == 15:
                    cns = documento

            telefone = (
                linha.get("Telefone celular")
                or linha.get("Telefone de contato")
                or linha.get("Telefone residencial")
            )

            telefone = limpar_numero(telefone)

            endereco = linha.get("Endereço")
            microarea_nome = linha.get("Microárea")
            data_nascimento = converter_data(
                linha.get("Data de nascimento")
            )

            microarea = None

            if microarea_nome:
                microarea, _ = MicroArea.objects.get_or_create(
                    microarea=microarea_nome
                )

            paciente = encontrar_paciente(cpf,cns,nome,data_nascimento)



            if paciente:
                paciente.nome = nome
                paciente.cns = cns
                paciente.telefone = telefone
                paciente.endereco = endereco
                paciente.microarea = microarea
                paciente.sincronizado = True

                paciente.save()

                detalhe_importacao.append({
                    "nome": paciente.nome,
                    "cpf": paciente.cpf,
                    "sus": paciente.cns,
                    "acao": "atualizado"
                })
                pacientes_atualizados += 1
            else:

                if not paciente:
                    duplicado = possivel_duplicidade(nome,data_nascimento)
                    if duplicado:
                        print("Possível duplicidade",nome)

                paciente = Paciente.objects.create(
                    nome=nome,
                    cpf=cpf,
                    cns=cns,
                    telefone=telefone,
                    endereco=endereco,
                    microarea=microarea,
                    sincronizado=True
                )
                detalhe_importacao.append({
                    "nome": paciente.nome,
                    "cpf": paciente.cpf,
                    "sus": paciente.cns,
                    "acao": "criado"
                })

                pacientes_novos += 1


    #=====================================================
    # PACIENTES QUE NÃO APARECERAM NA NOVA LISTA
    #=====================================================

    pacientes_sem_vinculo = Paciente.objects.filter(sincronizado=False)
    for paciente in pacientes_sem_vinculo:
        detalhe_importacao.append({
            "nome": paciente.nome,
            "cpf": paciente.cpf,
            "sus": paciente.cns,
            "acao": "marcado sem vinculo"
        })
    quantidade_sem_vinculo = pacientes_sem_vinculo.count()

    pacientes_sem_vinculo.update(vinculo="sem_vinculo")

    return {
        "pacientes_novos": pacientes_novos,
        "pacientes_atualizados": pacientes_atualizados,
        "pacientes_sem_vinculo": quantidade_sem_vinculo,
        "detalhes": detalhe_importacao
    }



