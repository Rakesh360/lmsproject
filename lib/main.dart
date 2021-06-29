import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:lmsproject/bloc/login_bloc/login_bloc.dart';
import 'package:lmsproject/screens/login_screen.dart';
import 'package:lmsproject/screens/otp.dart';

void main() {
  runApp(Main());
}

class Main extends StatelessWidget {
  const Main({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        home: MultiBlocProvider(
          providers: [
            BlocProvider(
              create: (context) => LoginBloc(),
            )
          ],
          child: LoginScreen(),
        ));
  }
}
