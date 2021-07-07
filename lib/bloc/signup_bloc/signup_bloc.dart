import 'dart:async';
import 'dart:math';

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

part 'signup_event.dart';
part 'signup_state.dart';

class SignupBloc extends Bloc<SignupEvent, SignupState> {
  SignupBloc() : super(SignupInitial());

  @override
  Stream<SignupState> mapEventToState(
    SignupEvent event,
  ) async* {
    if (event is SignupInitialEvent) {
      yield* mapSignupInitialState(event);
    } else if (event is GetOtpEvent) {
      yield* mapGetOtpState(event);
    } else if (event is VerifyOtpEvent) {
      yield* mapVerifyOtpState(event);
    } else if (event is SignupSuccessEvent) {
      yield* mapSignupSuccessState(event);
    }
  }
}

Stream<SignupState> mapSignupSuccessState(SignupSuccessEvent event) async* {
  try {
    yield SignupSuccess(
      username: event.username,
      email: event.email,
      password: event.password,
      agreeTerms: event.agreeTerms,
    );
  } catch (e) {
    yield AlreadySignup(message: e.toString());
  }
}

mapVerifyOtpState(VerifyOtpEvent event) {}

mapGetOtpState(GetOtpEvent event) {}

Stream<SignupState> mapSignupInitialState(SignupInitialEvent event) async* {
  yield SignupInitial();
}
