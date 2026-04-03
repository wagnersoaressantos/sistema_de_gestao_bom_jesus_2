from django.shortcuts import render
import tempfile

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Paciente, MicroArea
from .serializers import PacienteSerializer, MicroAreaSerializer, ImportacaoPacienteSerializer
from .services.importador_csv import importar_pacientes_csv





# ======================================================
# API MICROÁREA
# ======================================================

class MicroAreaViewSet(viewsets.ModelViewSet):

    """
    API responsável por gerenciar microáreas da unidade
    """

    queryset = MicroArea.objects.all()

    serializer_class = MicroAreaSerializer

    permission_classes = [IsAuthenticated]

# ======================================================
# API PACIENTES
# ======================================================

class PacienteViewSet(viewsets.ModelViewSet):

    """
    API responsável por gerenciar pacientes
    """

    queryset = Paciente.objects.select_related("microarea")

    serializer_class = PacienteSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ["nome","cpf","cns"]
    ordering_fields = ["nome","data_nascimento"]
    ordering = ["nome"]

# class ImportarPacientesView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#
#         arquivo = request.FILES.get("arquivo")
#
#         if not arquivo:
#
#             return Response(
#                 {"erro": "Arquivo não enviado"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # salva temporariamente
#         with tempfile.NamedTemporaryFile(delete=False) as temp:
#
#             for chunk in arquivo.chunks():
#                 temp.write(chunk)
#
#             caminho = temp.name
#
#         # executa importação
#         importar_pacientes_csv(caminho)
#
#         return Response({
#             "mensagem": "Importação realizada com sucesso"
#         })
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser
#
# import tempfile
#
# from .services.importador_csv import importar_pacientes_csv
#
#
# class ImportarPacientesView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     parser_classes = [MultiPartParser, FormParser]
#
#     def post(self, request):
#
#         arquivo = request.FILES.get("arquivo")
#
#         if not arquivo:
#
#             return Response(
#                 {"erro": "Arquivo não enviado"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         with tempfile.NamedTemporaryFile(delete=False) as temp:
#
#             for chunk in arquivo.chunks():
#                 temp.write(chunk)
#
#             caminho = temp.name
#
#         importar_pacientes_csv(caminho)
#
#         return Response({
#             "mensagem": "Importação realizada com sucesso"
#         })

#
#
# class ImportarPacientesView(APIView):
#
#     permission_classes = [IsAuthenticated]
#
#     parser_classes = [MultiPartParser, FormParser]
#
#     def post(self, request):
#
#         serializer = ImportacaoPacienteSerializer(data=request.data)
#
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         arquivo = serializer.validated_data["arquivo"]
#
#         with tempfile.NamedTemporaryFile(delete=False) as temp:
#
#             for chunk in arquivo.chunks():
#                 temp.write(chunk)
#
#             caminho = temp.name
#
#         importar_pacientes_csv(caminho)
#
#         return Response({
#             "mensagem": "Importação realizada com sucesso"
#         })
#


class BuscarPacienteView(GenericAPIView):

    def get(self, request):

        termo = request.GET.get("q", "").strip()

        if len(termo) < 3:
            return Response({
                "mensagem": "Digite pelo menos 3 caracteres"
            })

        pacientes = (
            Paciente.objects
            .filter(
                Q(nome__icontains=termo) |
                Q(cpf__icontains=termo) |
                Q(cns__icontains=termo)
            )
            .select_related("microarea")
            .order_by("nome")[:10]
        )

        dados = [
            {
                "id": p.id,
                "nome": p.nome,
                "cpf": p.cpf,
                "cns": p.cns,
                "label": f"{p.nome} - CPF: {p.cpf or '---'}"
            }
            for p in pacientes
        ]

        return Response(dados)

class ImportarPacientesView(GenericAPIView):

    serializer_class = ImportacaoPacienteSerializer

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        arquivo = serializer.validated_data["arquivo"]

        with tempfile.NamedTemporaryFile(delete=False) as temp:

            for chunk in arquivo.chunks():
                temp.write(chunk)

            caminho = temp.name

        resultado = importar_pacientes_csv(caminho)

        return Response({
            "mensagem": "Importação realizada com sucesso",
            "resultado": resultado
        })


def tela_busca_paciente(request):
    return render(request, "buscar_paciente.html")