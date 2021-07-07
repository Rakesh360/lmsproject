part of 'signup_bloc.dart';

abstract class SignupEvent extends Equatable {
  const SignupEvent();

  @override
  List<Object> get props => [];
}

class SignupInitialEvent extends SignupEvent {
  SignupInitialEvent();
}

class GetOtpEvent extends SignupEvent {
  final String phone;
  GetOtpEvent({required this.phone});
}

class VerifyOtpEvent extends SignupEvent {
  VerifyOtpEvent();
}

class SignupSuccessEvent extends SignupEvent {
  final String username;
  final String password;
  final String email;
  bool agreeTerms = false;
  SignupSuccessEvent(
      {required this.username,
      required this.password,
      required this.email,
      required this.agreeTerms});
}
