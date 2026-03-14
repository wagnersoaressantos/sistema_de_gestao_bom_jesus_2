class Especialidade {

  final int id;
  final String nome;

  Especialidade({
    required this.id,
    required this.nome,
  });

  // Converte JSON da API para objeto
  factory Especialidade.fromJson(Map<String, dynamic> json) {

    return Especialidade(
      id: json['id'],
      nome: json['nome'],
    );
  }
}
