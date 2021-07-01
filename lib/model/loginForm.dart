import 'dart:core';

import 'package:equatable/equatable.dart';

class LoginForm extends Equatable {
  LoginForm(this.phone, this.password);

  String phone;
  String password;

  @override
  List<Object> get props => [];
}
