part of 'login_bloc.dart';

@immutable
abstract class LoginState extends Equatable {
  @override
  List<Object> get props => [];
}

class LoginInitial extends LoginState {}

class LoginSuccess extends LoginState {
  String? userName;
  LoginSuccess({this.userName});
}

class LoginFailure extends LoginState {
  String? message;
  LoginFailure({this.message});
}
