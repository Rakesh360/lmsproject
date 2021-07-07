import 'dart:io';

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
import 'package:wc_form_validators/wc_form_validators.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  late String phone;
  late String password;
  bool isChecked = false;
  GlobalKey<FormState> formkey = GlobalKey<FormState>();
  TextEditingController _phoneInput = TextEditingController();

  TextEditingController _passwordInput = TextEditingController();
  //bool isChecked = true;
  bool _showPassword = true;
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
                body: Form(
                  autovalidate: true, //check for validation while typing
                  key: formkey,
                  child: Container(
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
                          TextFormField(
                            controller: _phoneInput,
                            keyboardType: TextInputType.phone,
                            validator: (value) {
                              if (value!.isEmpty) {
                                return "please enter";
                              } else
                                return null;
                            },
                            onChanged: (value) {
                              setState(() {
                                phone = value;
                              });
                            },
                            decoration: InputDecoration(
                                prefixIcon: Icon(
                                  Icons.phone,
                                  color: AppColors.BorderColor,
                                ),
                                labelText: 'phone'),
                          ),

                          SizedBox(
                            height: 10,
                          ),

                          TextFormField(
                            keyboardType: TextInputType.text,
                            validator: (value) {
                              if (value!.isEmpty) {
                                return "please enter";
                              } else
                                return null;
                            },
                            obscureText: _showPassword,
                            onChanged: (value) {
                              setState(() {
                                password = value;
                              });
                            },
                            decoration: InputDecoration(
                              prefixIcon: Icon(
                                Icons.lock,
                                color: AppColors.BorderColor,
                              ),
                              suffixIcon: IconButton(
                                  icon: Icon(_showPassword
                                      ? Icons.remove_red_eye_outlined
                                      : Icons.visibility_off_outlined),
                                  onPressed: () {
                                    setState(() {
                                      _showPassword = !_showPassword;
                                    });
                                  }),
                              labelText: 'Password',
                            ),
                          ),
                          //),
                          SizedBox(
                            height: 20,
                          ),
                          ListTile(
                              horizontalTitleGap: 0,
                              contentPadding: EdgeInsets.all(0),
                              leading: Checkbox(
                                activeColor: AppColors.ButtonColor,
                                value: isChecked,
                                onChanged: (value) {
                                  setState(() {
                                    isChecked = value!;
                                  });
                                },
                              ),
                              title: Text(
                                'Remember Me',
                                style: rubikRegular.copyWith(
                                    color: AppColors.TextColor),
                              ),
                              trailing: InkWell(
                                onTap: () {},
                                child: Text('Forgot Password?',
                                    textAlign: TextAlign.left,
                                    style: rubikRegular.copyWith(
                                        color: AppColors.TextColor)),
                              )),
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
                                  if (formkey.currentState!.validate()) {
                                    context.read<LoginBloc>().add(
                                        LoginWithContactEvent(
                                            phone: _phoneInput.text,
                                            password: _passwordInput.text));
                                    print("Validated");
                                  } else {
                                    print("Not Validated");
                                  }
                                },
                                child: Text(
                                  'Login',
                                  style:
                                      rubikBold.copyWith(color: Colors.white),
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
                ),
              );
            } else if (state is LoginSuccess) {
              print('login $state');
              return UserProfile();
            }
            return HoldLoader();
          },
        ));
  }
}
