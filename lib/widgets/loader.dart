import 'package:flutter/material.dart';

class HoldLoader extends StatelessWidget {
  const HoldLoader({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}
