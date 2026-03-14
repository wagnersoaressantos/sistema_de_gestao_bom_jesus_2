class Paciente {
  final int id;
  final String nome;
  final String cpf;
  final String cns;
  final String dataNascimento;
  final String telefone;
  final String nomeMae;
  final String endereco;
  final String microarea;

  Paciente({
    required this.id,
    required this.nome,
    required this.cpf,
    required this.cns,
    required this.dataNascimento,
    required this.telefone,
    required this.nomeMae,
    required this.endereco,
    required this.microarea,
  });

  // Converte JSON da API em objeto Paciente
  factory Paciente.fromJson(Map<String, dynamic> json) {
    return Paciente(
      id: json['id'],
      nome: json['nome'],
      cpf: json['cpf'],
      cns: json['cns'],
      dataNascimento: json['data_nascimento'],
      telefone: json['telefone'],
      nomeMae: json['nome_mae'],
      endereco: json['endereco'],
      microarea: json['microarea'],
    );
  }
}
