import 'package:flutter/material.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/appImages.dart';
import 'package:lmsproject/utils/styles.dart';

class UserProfile extends StatefulWidget {
  const UserProfile({Key? key}) : super(key: key);

  @override
  _ProfileState createState() => _ProfileState();
}

class _ProfileState extends State<UserProfile> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.red,
        // padding: EdgeInsets.symmetric(horizontal: 20),
        // child: SingleChildScrollView(
        //   child: Column(
        //     children: [
        //       SizedBox(
        //         height: 50,
        //       ),
        //       Row(
        //         children: [
        //           CircleAvatar(
        //             child: Image.asset(
        //               AppImages.AppProfile,
        //             ),
        //           ),
        //           Text
        //         ],
        //       )
        //     ],
        //   ),
        //  )
      ),
    );
  }
}
