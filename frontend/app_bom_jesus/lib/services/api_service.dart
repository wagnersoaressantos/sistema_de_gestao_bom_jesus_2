import 'dart:convert';
import 'package:app_bom_jesus/models/especialidade.dart';
import 'package:app_bom_jesus/models/procedimento.dart';
import 'package:http/http.dart' as http;
import '../models/paciente.dart';

class ApiService {
  // URL da API Django
  static const String baseUrl = "http://127.0.0.1:8000/api";

  // Busca lista de pacientes
  static Future<List<Paciente>> getPacientes() async {
    final response = await http.get(Uri.parse('$baseUrl/pacientes/'));

    if (response.statusCode == 200) {
      List data = json.decode(response.body);

      return data.map((item) => Paciente.fromJson(item)).toList();
    } else {
      throw Exception('Erro ao carregar pacientes');
    }
  }

  // Método para cadastrar um novo paciente
static Future<bool> criarPaciente({
  required String nome,
  required String cpf,
  required String cns,
  required String dataNascimento,
  required String telefone,
  required String nomeMae,
  required String endereco,
  required String microarea,
}) async {

  final response = await http.post(
    Uri.parse('$baseUrl/pacientes/'),

    headers: {
      'Content-Type': 'application/json'
    },

    body: jsonEncode({
       'nome': nome,
      'cpf': cpf,
      'cns': cns,
      'data_nascimento': dataNascimento,
      'telefone': telefone,
      'nome_mae': nomeMae,
      'endereco': endereco,
      'microarea': microarea
    }),
  );

  if (response.statusCode == 201) {
    return true;
  } else {
    return false;
  }
}

// Busca lista de Especialidades
static Future<List<Especialidade>> getEspecialidades() async {

  final response = await http.get(
    Uri.parse('$baseUrl/especialidades/')
  );

  if (response.statusCode == 200) {

    List data = json.decode(response.body);

    return data.map((e) =>
        Especialidade.fromJson(e)).toList();

  } else {

    throw Exception("Erro ao carregar especialidades");
  }
}

// Busca lista de Procedimentos
static Future<List<Procedimento>> getProcedimentos() async {

  final response = await http.get(
    Uri.parse('$baseUrl/procedimentos/')
  );

  if (response.statusCode == 200) {

    List data = json.decode(response.body);

    return data.map((e) =>
        Procedimento.fromJson(e)).toList();

  } else {

    throw Exception("Erro ao carregar procedimentos");
  }
}



}
