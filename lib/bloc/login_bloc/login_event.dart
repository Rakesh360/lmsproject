part of 'login_bloc.dart';

abstract class LoginEvent extends Equatable {
  @override
  List<Object> get props => [];
}

class LoginInitialEvent extends LoginEvent {
  LoginInitialEvent();
}

class LoginWithContactEvent extends LoginEvent {
  final String phone;
  final String password;
  LoginWithContactEvent({required this.phone, required this.password});
}
