import 'package:flutter/material.dart';
import 'package:lmsproject/utils/appColors.dart';
// ignore: unused_import
import 'package:lmsproject/utils/appImages.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class otpScreen extends StatefulWidget {
  const otpScreen({Key? key}) : super(key: key);

  @override
  _otpScreenState createState() => _otpScreenState();
}

class _otpScreenState extends State<otpScreen> {
  TextEditingController _emailInput = TextEditingController();
  TextEditingController _passwordInput = TextEditingController();
  //late FocusNode myFocusNode;
  bool otp_value  = false;
  bool textchange = true;
  
  /*@override
  void initState() {
    super.initState();

    myFocusNode = FocusNode();
  }

  @override
  void dispose() {
    // Clean up the focus node when the Form is disposed.
    myFocusNode.dispose();

    super.dispose();
  }
*/
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: SingleChildScrollView(
          child: Column(
            children: [
              SizedBox(
                height: 180,
              ),
              SizedBox(
                height: 40,
              ),
              Text("Verify through mobile",
                  style: rubikMedium.copyWith(
                      color: AppColors.TextColor, fontSize: 30)),
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
                  if (otp_value)
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

                                  style:
                                      rubikRegular.copyWith(color: Colors.red),
                                ),
                              ],
                            ),
                          ),
                          SizedBox(
                            height: 10,
                          ),
                                //Card(
                          //shape: OutlineInputBorder(),
                          //elevation: 9,
                          //child: 
                          TextField(
                            //focusNode: myFocusNode,
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
                          shape: StadiumBorder(
                          ),

                          primary: AppColors.ButtonColor,
                          onPrimary: Colors.white, 
                        ),
                        child: textchange ? Text("Get OTP") : Text("Verify OTP"),
                        //    style: TextStyle(fontSize: 14)

                        onPressed: () {
                          setState(() {
                            otp_value = true;
                          });
                          setState(() => textchange = false);
                          //setState(() => myFocusNode.requestFocus());
                          
                          
                        },
                      )),
                ],
              ),
              
            ],
          ),
        ),
      ),
    );
  }
}
