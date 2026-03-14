import 'package:app_bom_jesus/views/cadastro_encaminhamento_view.dart';
import 'package:app_bom_jesus/views/pacientes_view.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      // Define idioma padrão
      locale: Locale('pt', 'BR'),

       supportedLocales: [
        Locale('pt', 'BR'),
      ],
      localizationsDelegates: [

        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],

      home: CadastroEncaminhamentoView(),
    );
  }
}
