import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

part 'login_event.dart';
part 'login_state.dart';

class LoginBloc extends Bloc<LoginEvent, LoginState> {
  LoginBloc() : super(LoginInitial());

  @override
  Stream<LoginState> mapEventToState(
    LoginEvent event,
  ) async* {
    if (event is LoginInitialEvent) {
      yield* mapLoginInitialState(event);
    } else if (event is LoginWithContactEvent) {
      yield* mapLoginWithContactState(event);
    }
  }
}

Stream<LoginState> mapLoginInitialState(LoginInitialEvent event) async* {
  yield LoginInitial();
}

Stream<LoginState> mapLoginWithContactState(
    LoginWithContactEvent event) async* {
  try {
    print('<<<<<<<<< in bloc login line 58');
    print(event.phone);
    print(event.password);
    yield LoginSuccess(phone: event.phone);
  } catch (e) {
    yield LoginFailure(message: e.toString());
  }
}
