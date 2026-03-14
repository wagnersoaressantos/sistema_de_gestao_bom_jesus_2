import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CadastroPacienteView extends StatefulWidget {
  const CadastroPacienteView({super.key});

  @override
  State<CadastroPacienteView> createState() => _CadastroPacienteViewState();
}

class _CadastroPacienteViewState extends State<CadastroPacienteView> {
  // Controladores para os campos de texto
  final TextEditingController nomeController = TextEditingController();
  final TextEditingController cpfController = TextEditingController();
  final TextEditingController cnsController = TextEditingController();
  final TextEditingController nascimentoController = TextEditingController();
  final TextEditingController telefoneController = TextEditingController();
  final TextEditingController maeController = TextEditingController();
  final TextEditingController enderecoController = TextEditingController();
  final TextEditingController microareaController = TextEditingController();

  bool carregando = false;

  // Função que envia os dados para API
  void salvarPaciente() async {
    setState(() {
      carregando = true;
    });

    bool sucesso = await ApiService.criarPaciente(
      nome: nomeController.text,
      cpf: cpfController.text,
      cns: cnsController.text,
      dataNascimento: nascimentoController.text,
      telefone: telefoneController.text,
      nomeMae: maeController.text,
      endereco: enderecoController.text,
      microarea: microareaController.text,
    );

    setState(() {
      carregando = false;
    });

    if (sucesso) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Paciente cadastrado com sucesso")),
      );

      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erro ao cadastrar paciente")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Cadastrar Paciente")),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: ListView(
          children: [
            Column(
              children: [
                TextField(
                  controller: nomeController,
                  decoration: const InputDecoration(
                    labelText: "Nome do paciente",
                  ),
                ),

                const SizedBox(height: 20),

                TextField(
                  controller: cpfController,
                  decoration: const InputDecoration(labelText: "CPF"),
                ),

                const SizedBox(height: 20),
                TextField(
                  controller: cnsController,
                  decoration: const InputDecoration(labelText: "CNS"),
                ),

                const SizedBox(height: 20),
                TextField(
                  controller: nascimentoController,
                  decoration: const InputDecoration(
                    labelText: "Data de Nascimento",
                  ),
                ),

                const SizedBox(height: 20),
                TextField(
                  controller: telefoneController,
                  decoration: const InputDecoration(labelText: "Telefone"),
                ),

                const SizedBox(height: 20),
                TextField(
                  controller: maeController,
                  decoration: const InputDecoration(labelText: "Nome mãe"),
                ),

                const SizedBox(height: 20),
                TextField(
                  controller: enderecoController,
                  decoration: const InputDecoration(labelText: "Endereço"),
                ),
                const SizedBox(height: 20),
                TextField(
                  controller: microareaController,
                  decoration: const InputDecoration(labelText: "Microárea"),
                ),

                const SizedBox(height: 20),

                ElevatedButton(
                  onPressed: carregando ? null : salvarPaciente,

                  child: carregando
                      ? const CircularProgressIndicator()
                      : const Text("Salvar"),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
