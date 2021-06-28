import 'package:flutter/material.dart';
import 'package:lmsproject/screens/login_screen.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/appImages.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({Key? key}) : super(key: key);

  @override
  _SignUpScreenState createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
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
                height: 40,
              ),
              Image.asset(
                AppImages.AppLogo,
                width: 400,
              ),
              SizedBox(
                height: 40,
              ),
              Text("Register here",
                  style: rubikMedium.copyWith(
                      color: AppColors.TextColor, fontSize: 30)),
              SizedBox(
                height: 20,
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
