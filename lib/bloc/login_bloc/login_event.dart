part of 'login_bloc.dart';

@immutable
abstract class LoginEvent extends Equatable {
  @override
  List<Object> get props => [];
}

class LoginWithEmailEvent extends LoginEvent {
  String ?email;
  String ?password;
  LoginWithEmailEvent({this.email,this.password});

}
