import 'package:app_bom_jesus/models/especialidade.dart';
import 'package:app_bom_jesus/models/procedimento.dart';
import 'package:app_bom_jesus/services/api_service.dart';
import 'package:flutter/material.dart';

class CadastroEncaminhamentoView extends StatefulWidget {
  const CadastroEncaminhamentoView({super.key});

  @override
  State<CadastroEncaminhamentoView> createState() =>
      _CadastroEncaminhamentoViewState();
}

class _CadastroEncaminhamentoViewState
    extends State<CadastroEncaminhamentoView> {
  // Lista de especialidades vindas da API
  List<Especialidade> especialidades = [];

  // Lista completa de procedimentos
  List<Procedimento> procedimentos = [];

  // Lista filtrada de procedimentos
  List<Procedimento> procedimentosFiltrados = [];

  // Especialidade selecionada no dropdown
  Especialidade? especialidadeSelecionada;

  // Procedimento selecionado
  Procedimento? procedimentoSelecionado;

  // Controller para profissional solicitante
  final TextEditingController profissionalController = TextEditingController();

  // Controller para observação
  final TextEditingController observacaoController = TextEditingController();

  // Variável que guarda o tipo de encaminhamento
  // Pode ser "especialista" ou "exame"
  String tipoEncaminhamento = "exame";

  // --------------------------------------------------
  // Função executada quando a tela é aberta
  // --------------------------------------------------
  @override
  void initState() {
    super.initState();

    // Carrega dados da API
    carregarDados();
  }

  // --------------------------------------------------
  // Carrega especialidades e procedimentos da API
  // --------------------------------------------------
  Future<void> carregarDados() async {
    try {
      // Busca especialidades
      final listaEspecialidades = await ApiService.getEspecialidades();

      // Busca procedimentos
      final listaProcedimentos = await ApiService.getProcedimentos();

      setState(() {
        especialidades = listaEspecialidades;

        procedimentos = listaProcedimentos;
      });
    } catch (e) {
      print("Erro ao carregar dados: $e");
    }
  }

  // --------------------------------------------------
  // Filtra procedimentos pela especialidade escolhida
  // --------------------------------------------------
  void filtrarProcedimentos(int especialidadeId) {
    setState(() {
      procedimentosFiltrados = procedimentos
          .where((proc) => proc.especialidade == especialidadeId)
          .toList();

      // Limpa procedimento selecionado
      procedimentoSelecionado = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Novo Encaminhamento")),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          children: [
            // -------------------------------------
            // Seleção do tipo de encaminhamento
            // -------------------------------------
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,

              children: [
                const Text(
                  "Tipo de encaminhamento",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),

                Row(
                  children: [
                    // Radio para especialista
                    Radio<String>(
                      value: "especialista",

                      groupValue: tipoEncaminhamento,

                      onChanged: (valor) {
                        setState(() {
                          tipoEncaminhamento = valor!;
                        });
                      },
                    ),

                    const Text("Especialista"),

                    // Radio para exame
                    Radio<String>(
                      value: "exame",

                      groupValue: tipoEncaminhamento,

                      onChanged: (valor) {
                        setState(() {
                          tipoEncaminhamento = valor!;
                        });
                      },
                    ),

                    const Text("Exame"),
                  ],
                ),
              ],
            ),

            // -------------------------------
            // Campo de especialidade
            // -------------------------------
            DropdownButtonFormField<Especialidade>(
              hint: const Text("Selecione a especialidade"),

              initialValue: especialidadeSelecionada,

              items: especialidades.map((esp) {
                return DropdownMenuItem(value: esp, child: Text(esp.nome));
              }).toList(),

              onChanged: (valor) {
                setState(() {
                  especialidadeSelecionada = valor;
                });

                // Filtra procedimentos
                if (valor != null) {
                  filtrarProcedimentos(valor.id);
                }
              },
            ),
            const SizedBox(height: 20),

            // -------------------------------
            // Campo de procedimento
            // -------------------------------
            // Só mostra procedimentos se for exame
            if (tipoEncaminhamento == "exame")
              DropdownButtonFormField<Procedimento>(
                hint: const Text("Selecione o procedimento"),

                initialValue: procedimentoSelecionado,

                items: procedimentosFiltrados.map((proc) {
                  return DropdownMenuItem(value: proc, child: Text(proc.nome));
                }).toList(),

                onChanged: (valor) {
                  setState(() {
                    procedimentoSelecionado = valor;
                  });
                },
              ),

            const SizedBox(height: 20),

            // -------------------------------
            // Profissional solicitante
            // -------------------------------
            TextField(
              controller: profissionalController,

              decoration: const InputDecoration(
                labelText: "Profissional solicitante",
              ),
            ),

            const SizedBox(height: 20),

            // -------------------------------
            // Observação
            // -------------------------------
            TextField(
              controller: observacaoController,

              decoration: const InputDecoration(labelText: "Observação"),
            ),

            const SizedBox(height: 30),

            // -------------------------------
            // Botão salvar
            // -------------------------------
            ElevatedButton(
              onPressed: () {
                print("Tipo: $tipoEncaminhamento");
                print("Especialidade: ${especialidadeSelecionada?.nome}");
                print("Procedimento: ${procedimentoSelecionado?.nome}");
                print("Profissional: ${profissionalController.text}");
              },

              child: const Text("Salvar Encaminhamento"),
            ),
          ],
        ),
      ),
    );
  }
}
