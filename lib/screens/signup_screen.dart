import 'package:flutter/material.dart';
import 'package:lmsproject/screens/login_screen.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({Key? key}) : super(key: key);

  @override
  _SignUpScreenState createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  //late FocusNode myFocusNode;
  bool otpValue = false;
  bool textchange = true;
  TextEditingController _emailInput = TextEditingController();

  TextEditingController _passwordInput = TextEditingController();

  TextEditingController _usernameInput = TextEditingController();
  bool isChecked = false;
  void _doSomething() {
    Navigator.push(
        context, MaterialPageRoute(builder: (context) => LoginScreen()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
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
                  lable: 'Enter Your Number',
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
                                text: 'OTP sent on your mobile.. ENTER HERE!',
                                style: rubikRegular.copyWith(color: Colors.red),
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
                        child:
                            textchange ? Text("Get OTP") : Text("Verify OTP"),
                        //    style: TextStyle(fontSize: 14)

                        onPressed: () {
                          textchange
                              ? Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                      builder: (context) => SignUpScreen()),
                                )
                              : setState(() {
                                  otpValue = true;
                                });
                          setState(() => textchange = false);
                        },
                      )),
                  SizedBox(
                    height: 40,
                  )
                ],
              ),
              TextInput(
                  iconData: Icons.person,
                  lable: 'Username',
                  textEditingController: _usernameInput),
              SizedBox(
                height: 10,
              ),
              TextInput(
                  iconData: Icons.mail,
                  lable: 'E-Mail',
                  textEditingController: _emailInput),
              SizedBox(
                height: 10,
              ),
              TextInput(
                  iconData: Icons.lock,
                  lable: 'Password',
                  textEditingController: _passwordInput),
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
                    style: rubikRegular.copyWith(color: AppColors.TextColor),
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
    );
  }
}
