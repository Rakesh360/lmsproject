import 'package:flutter/material.dart';
import 'package:lmsproject/screens/home_screen.dart';
import 'package:lmsproject/screens/login_screen.dart';
import 'package:lmsproject/screens/otp.dart';

import 'package:lmsproject/screens/signup_screen.dart';

void main() {
  runApp(Main());
}

class Main extends StatelessWidget {
  const Main({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(debugShowCheckedModeBanner: false, home: Profile());
  }
}