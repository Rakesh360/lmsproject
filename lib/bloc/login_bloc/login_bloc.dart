import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:meta/meta.dart';

part 'login_event.dart';
part 'login_state.dart';

class LoginBloc extends Bloc<LoginEvent, LoginState> {
  LoginBloc() : super(LoginInitial());

  @override
  Stream<LoginState> mapEventToState(
    LoginEvent event,
  ) async* {
    if (event is LoginWithEmailEvent) {
      String? msg;
      try {
        if (event.email!.contains('kartik')) {
          msg = event.password;
          yield LoginSuccess(userName: msg);
        } else {
          yield LoginFailure(message: ' no user ');
        }
      } catch (e) {
        yield LoginFailure(message: 'Invalid exception called $e ');
      }
    }
  }
}
