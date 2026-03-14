class Procedimento {

  final int id;
  final String nome;
  final int especialidade;

  Procedimento({
    required this.id,
    required this.nome,
    required this.especialidade,
  });

  factory Procedimento.fromJson(Map<String, dynamic> json) {

    return Procedimento(
      id: json['id'],
      nome: json['nome'],
      especialidade: json['especialidade'],
    );
  }
}
