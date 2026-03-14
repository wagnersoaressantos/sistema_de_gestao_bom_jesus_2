import 'package:app_bom_jesus/views/cadastro_paciente_view.dart';
import 'package:flutter/material.dart';
import '../models/paciente.dart';
import '../services/api_service.dart';

class PacientesView extends StatefulWidget {
  const PacientesView({super.key});

  @override
  State<PacientesView> createState() => _PacientesViewState();
}

class _PacientesViewState extends State<PacientesView> {
  late Future<List<Paciente>> pacientes;

  @override
  void initState() {
    super.initState();

    // Carrega pacientes da API
    pacientes = ApiService.getPacientes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Pacientes")),

      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),

        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const CadastroPacienteView(),
            ),
          );
        },
      ),

      body: FutureBuilder<List<Paciente>>(
        future: pacientes,

        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text("Erro: ${snapshot.error}"));
          }

          final lista = snapshot.data!;

          return ListView.builder(
            itemCount: lista.length,

            itemBuilder: (context, index) {
              final paciente = lista[index];

              return Card(
                child: ListTile(
                  title: Text(
                    paciente.nome,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),

                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,

                    children: [
                      Text("CPF: ${paciente.cpf}"),
                      Text("Telefone: ${paciente.telefone}"),
                      Text("Microárea: ${paciente.microarea}"),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
