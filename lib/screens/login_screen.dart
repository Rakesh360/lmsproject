import 'package:flutter/material.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/appImages.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  TextEditingController _emailInput = TextEditingController();

  TextEditingController _passwordInput = TextEditingController();
  bool isChecked = true;
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
              Text("Welcome",
                  style: rubikMedium.copyWith(
                      color: AppColors.TextColor, fontSize: 30)), SizedBox(
                height: 20,
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
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                //mainAxisSize: MainAxisSize.max,
                children: <Widget>[
                  RichText(
                    text: TextSpan(
                      children: [
                        WidgetSpan(
                          child: Icon(Icons.check_box_outline_blank),
                        ),
                        TextSpan(
                          text: 'Remember Me',
                          style:
                              rubikRegular.copyWith(color: AppColors.TextColor),
                        ),
                      ],
                    ),
                  ),
                  TextButton(
                    onPressed: () {},
                    child: Text('Forgot Password?',
                        textAlign: TextAlign.left,
                        style:
                            rubikRegular.copyWith(color: AppColors.TextColor)),
                  )
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
                    onPressed: () {},
                    child: Text(
                      'Sign In',
                      style: rubikBold.copyWith(color: Colors.white),
                    )),
              ),
              SizedBox(
                height: 20,
              ),
               Text('Click here for Register......',
                    style: rubikBold.copyWith(color: AppColors.TextColor,fontSize: 16)),
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
                    onPressed: () {},
                    child: Text(
                      'Sign up',
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
