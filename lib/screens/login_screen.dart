import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:lmsproject/bloc/login_bloc/login_bloc.dart';
import 'package:lmsproject/model/loginForm.dart';
import 'package:lmsproject/screens/otp.dart';
import 'package:lmsproject/screens/profile.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/appImages.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/loader.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  TextEditingController _phoneInput =
      TextEditingController(text: 'kartik jabreba');

  TextEditingController _passwordInput =
      TextEditingController(text: 'my password');
  //bool isChecked = true;
  bool _showPassword = false;
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
        create: (context) => LoginBloc(),
        child: BlocBuilder<LoginBloc, LoginState>(
          builder: (context, state) {
            if (state is LoginInitial) {
              print('login <<<<<<<<  $state');
              //   context.read<LoginBloc>().add(LoginInitialEvent());
              //   return HoldLoader();
              // } else if (state is LoginFailure) {
              //   print('login $state');
              return Scaffold(
                body: Container(
                  padding: EdgeInsets.symmetric(horizontal: 20),
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        SizedBox(
                          height: 40,
                        ),
                        Image.asset(
                          AppImages.AppLogo,
                          width: 400,
                        ),
                        SizedBox(
                          height: 40,
                        ),
                        Text("Welcome",
                            style: rubikMedium.copyWith(
                                color: AppColors.TextColor, fontSize: 30)),
                        SizedBox(
                          height: 20,
                        ),
                        TextInput(
                            iconData: Icons.phone,
                            lable: 'Phone Number',
                            textEditingController: _phoneInput),
                        SizedBox(
                          height: 10,
                        ),

                        TextFormField(
                          controller: _passwordInput,
                          validator: (value) {
                            if (value!.isEmpty) {
                              return "please enter";
                            } else
                              return null;
                          },
                          obscureText: !this._showPassword,
                          decoration: InputDecoration(
                            labelText: 'Password',
                            labelStyle: rubikRegular.copyWith(
                                color: AppColors.TextColor),
                            border: OutlineInputBorder(),
                            prefixIcon:
                                Icon(Icons.lock, color: AppColors.BorderColor),
                            suffixIcon: IconButton(
                              icon: Icon(
                                Icons.remove_red_eye,
                                color: this._showPassword
                                    ? AppColors.BorderColor
                                    : Colors.grey,
                              ),
                              onPressed: () {
                                setState(() =>
                                    this._showPassword = !this._showPassword);
                              },
                            ),
                          ),
                        ),
                        //),
                        SizedBox(
                          height: 20,
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: <Widget>[
                            RichText(
                              text: TextSpan(
                                children: [
                                  WidgetSpan(
                                    child: Icon(Icons.check_box_outline_blank),
                                  ),
                                  TextSpan(
                                    text: 'Remember Me',
                                    style: rubikRegular.copyWith(
                                        color: AppColors.TextColor),
                                  ),
                                ],
                              ),
                            ),
                            TextButton(
                              onPressed: () {},
                              child: Text('Forgot Password?',
                                  textAlign: TextAlign.left,
                                  style: rubikRegular.copyWith(
                                      color: AppColors.TextColor)),
                            )
                          ],
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        SizedBox(
                          width: 300,
                          height: 50,
                          child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                primary: AppColors.ButtonColor,
                                elevation: 10,
                                shape: StadiumBorder(),
                              ),
                              onPressed: () {
                                print(_phoneInput.text);
                                print(_passwordInput.text);
                                context.read<LoginBloc>().add(
                                    LoginWithContactEvent(
                                        phone: _phoneInput.text,
                                        password: _passwordInput.text));
                              },
                              child: Text(
                                'Login',
                                style: rubikBold.copyWith(color: Colors.white),
                              )),
                        ),
                        SizedBox(
                          height: 7,
                        ),
                        TextButton(
                          //padding: EdgeInsets.only(left: 0.0),
                          child: Text('Click here to Register ....',
                              style: rubikBold.copyWith(
                                  color: AppColors.TextColor, fontSize: 14)),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => OtpScreen()),
                            );
                          },
                        ),
                        SizedBox(
                          height: 20,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            } else if (state is LoginSuccess) {
              print('login $state');
              return Profile();
            }
            return HoldLoader();
          },
        ));
  }
}
