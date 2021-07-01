part of 'login_bloc.dart';

abstract class LoginState extends Equatable {
  @override
  List<Object> get props => [];
}

class LoginInitial extends LoginState {}

class LoginSuccess extends LoginState {
  String? phone;
  LoginSuccess({@required this.phone});
}

class LoginFailure extends LoginState {
  String? message;
  LoginFailure({@required this.message});
}
