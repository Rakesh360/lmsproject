part of 'signup_bloc.dart';

abstract class SignupState extends Equatable {
  const SignupState();

  @override
  List<Object> get props => [];
}

class SignupInitial extends SignupState {}

class GetOtp extends SignupState {
  String? phone;
  GetOtp({required String phone});
}

class VerifyOtp extends SignupState {
  String? phone;
  VerifyOtp();
}

class AlreadySignup extends SignupState {
  String? message;
  AlreadySignup({
    @required this.message,
  });
}

class SignupSuccess extends SignupState {
  String? username;
  String? email;
  String? password;
  bool? agreeTerms = false;

  SignupSuccess(
      {@required this.username,
      @required this.email,
      @required this.password,
      @required this.agreeTerms});
}
