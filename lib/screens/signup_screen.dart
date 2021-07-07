import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:lmsproject/bloc/signup_bloc/signup_bloc.dart';
import 'package:lmsproject/screens/profile.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/loader.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({Key? key}) : super(key: key);

  @override
  _SignUpScreenState createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  late String username;
  late String email;
  late String password;
  GlobalKey<FormState> formkey = GlobalKey<FormState>();
  bool otpValue = false;
  bool textchange = true;
  TextEditingController _emailInput = TextEditingController();

  TextEditingController _passwordInput = TextEditingController();

  TextEditingController _usernameInput = TextEditingController();

  bool isChecked = false;
  void _doSomething() {
    // Navigator.push(
    //   context,
    //   MaterialPageRoute(builder: (context) => Profile()),
    // );
    if (formkey.currentState!.validate()) {
      context.read<SignupBloc>().add(SignupSuccessEvent(
          username: _usernameInput.text,
          password: _passwordInput.text,
          email: _emailInput.text,
          agreeTerms: isChecked));
    } else {
      print("Not Validated");
    }
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
        create: (context) => SignupBloc(),
        child: BlocBuilder<SignupBloc, SignupState>(builder: (context, state) {
          if (state is SignupInitial) {
            print('signup 45<<<<<<<<  $state');
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
                          height: 80,
                        ),
                        Text("Verify through mobile",
                            style: rubikMedium.copyWith(
                                color: AppColors.TextColor, fontSize: 20)),
                        SizedBox(
                          height: 30,
                        ),
                        TextInput(
                            iconData: Icons.phone,
                            lable: 'Your Number',
                            textEditingController: _emailInput),
                        SizedBox(
                          height: 10,
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Column(
                          children: <Widget>[
                            if (otpValue)
                              Column(
                                children: <Widget>[
                                  RichText(
                                    text: TextSpan(
                                      children: [
                                        /*WidgetSpan(
                                    child: Icon(Icons.check_box_outline_blank),
                                  ),*/
                                        TextSpan(
                                          text:
                                              'OTP sent on your mobile.. ENTER HERE!',
                                          style: rubikRegular.copyWith(
                                              color: Colors.red),
                                        ),
                                      ],
                                    ),
                                  ),
                                  SizedBox(
                                    height: 10,
                                  ),
                                  //Card(

                                  TextField(
                                    decoration: InputDecoration(
                                      border: OutlineInputBorder(),
                                      labelText: 'Enter Your OTP',
                                      labelStyle: rubikRegular.copyWith(
                                          color: AppColors.TextColor),
                                      prefixIcon: Icon(Icons.create,
                                          color: AppColors.BorderColor),
                                    ),
                                  ),
                                  //),
                                ],
                              ),
                            SizedBox(
                              height: 20,
                            ),
                            SizedBox(
                                width: 200,
                                height: 50,
                                child: ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      shape: StadiumBorder(),
                                      primary: AppColors.ButtonColor,
                                      onPrimary: Colors.white,
                                    ),
                                    child: textchange
                                        ? Text("Get OTP")
                                        : Text("Verify OTP"),
                                    onPressed: () {}
                                    //   textchange
                                    //       ? Navigator.push(
                                    //           context,
                                    //           MaterialPageRoute(
                                    //               builder: (context) =>
                                    //                   SignUpScreen()),
                                    //         )
                                    //       : setState(() {
                                    //           otpValue = true;
                                    //         });
                                    //   setState(() => textchange = false);
                                    // },
                                    )),
                            SizedBox(
                              height: 40,
                            )
                          ],
                        ),
                        TextFormField(
                          controller: _usernameInput,
                          keyboardType: TextInputType.phone,
                          validator: (value) {
                            if (value!.isEmpty) {
                              return "please enter";
                            } else
                              return null;
                          },
                          onChanged: (value) {
                            setState(() {
                              username = value;
                            });
                          },
                          decoration: InputDecoration(
                              prefixIcon: Icon(
                                Icons.person,
                                color: AppColors.BorderColor,
                              ),
                              labelText: 'username'),
                        ),
                        SizedBox(
                          height: 10,
                        ),
                        TextFormField(
                          controller: _emailInput,
                          keyboardType: TextInputType.phone,
                          validator: (value) {
                            if (value!.isEmpty) {
                              return "please enter";
                            } else
                              return null;
                          },
                          onChanged: (value) {
                            setState(() {
                              email = value;
                            });
                          },
                          decoration: InputDecoration(
                              prefixIcon: Icon(
                                Icons.email,
                                color: AppColors.BorderColor,
                              ),
                              labelText: 'email'),
                        ),
                        SizedBox(
                          height: 10,
                        ),
                        TextFormField(
                          controller: _passwordInput,
                          keyboardType: TextInputType.phone,
                          validator: (value) {
                            if (value!.isEmpty) {
                              return "please enter";
                            } else
                              return null;
                          },
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
                              labelText: 'password'),
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          mainAxisAlignment: MainAxisAlignment.start,
                          //mainAxisSize: MainAxisSize.max,
                          children: <Widget>[
                            Checkbox(
                              activeColor: AppColors.ButtonColor,
                              value: isChecked,
                              onChanged: (value) {
                                setState(() {
                                  isChecked = value!;
                                });
                              },
                            ),
                            Text(
                              'Agree to Terms & Conditions',
                              style: rubikRegular.copyWith(
                                  color: AppColors.TextColor),
                            ),
                          ],
                        ),
                        SizedBox(
                          height: 20,
                        ),
                        SizedBox(
                          width: 330,
                          height: 50,
                          child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                primary: AppColors.ButtonColor,
                                elevation: 10,
                                shape: StadiumBorder(),
                              ),
                              onPressed: isChecked ? _doSomething : null,
                              child: Text(
                                'Register',
                                style: rubikBold.copyWith(color: Colors.white),
                              )),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            );
          } else if (state is SignupSuccess) {
            print('>>>>>>>>>>>>>>>>>>>>>123 signup $state');
            return UserProfile();
          }
          return HoldLoader();
        }));
  }
}
