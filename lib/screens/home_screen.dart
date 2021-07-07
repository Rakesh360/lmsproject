import 'package:flutter/material.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/login/textInput.dart';

class Profile extends StatefulWidget {
  const Profile({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<Profile> {
  int i = 0;
  Color _courseContainer = AppColors.BorderColor;
  Color _myCourseContainer = AppColors.BorderColor;
  Color _announceContainer = AppColors.BorderColor;
  TextEditingController textEditingController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        drawer: Drawer(
          // Add a ListView to the drawer. This ensures the user can scroll
          // through the options in the drawer if there isn't enough vertical
          // space to fit everything.
          child: ListView(
            // Important: Remove any padding from the ListView.
            padding: EdgeInsets.zero,
            children: <Widget>[
              DrawerHeader(
                decoration: BoxDecoration(
                  color: Colors.blue,
                ),
                child: Text('Drawer Header'),
              ),
              ListTile(
                title: Text('Item 1'),
                onTap: () {
                  // Update the state of the app
                  // ...
                  // Then close the drawer
                  Navigator.pop(context);
                },
              ),
              ListTile(
                title: Text('Item 2'),
                onTap: () {
                  // Update the state of the app
                  // ...
                  // Then close the drawer
                  Navigator.pop(context);
                },
              ),
            ],
          ),
        ),
        appBar: AppBar(
          backgroundColor: AppColors.ButtonColor,
          actions: [
            Icon(Icons.message),
            SizedBox(
              width: 10,
            )
          ],
        ),
        body: Padding(
          padding: EdgeInsets.all(10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              TextInput(
                  iconData: Icons.search,
                  lable: 'Search Course Here',
                  textEditingController: textEditingController),
              SizedBox(
                height: 10,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _courseContainer = AppColors.OnTapButtonColor;
                        i = 0;
                      });
                    },
                    child: Container(
                      decoration: BoxDecoration(
                          color: _courseContainer,
                          borderRadius: BorderRadius.all(Radius.circular(8))),
                      height: 60,
                      width: MediaQuery.of(context).size.width * 0.25,
                      child: Center(
                          child: Text(
                        'Course',
                        style: TextStyle(
                          color: Colors.white,
                        ),
                      )),
                    ),
                  ),
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _myCourseContainer = AppColors.OnTapButtonColor;
                        i = 1;
                      });
                    },
                    child: Container(
                      decoration: BoxDecoration(
                          color: _myCourseContainer,
                          borderRadius: BorderRadius.all(Radius.circular(8))),
                      height: 60,
                      width: MediaQuery.of(context).size.width * 0.25,
                      child: Center(
                          child: Text(
                        'My Course',
                        style: TextStyle(
                          color: Colors.white,
                        ),
                      )),
                    ),
                  ),
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _announceContainer = AppColors.OnTapButtonColor;
                        i = 2;
                      });
                    },
                    child: Container(
                      decoration: BoxDecoration(
                          color: _announceContainer,
                          borderRadius: BorderRadius.all(Radius.circular(8))),
                      height: 60,
                      width: MediaQuery.of(context).size.width * 0.25,
                      child: Center(
                          child: Text(
                        'Announcment',
                        style: TextStyle(
                          color: Colors.white,
                        ),
                      )),
                    ),
                  ),
                ],
              ),
              SizedBox(
                height: 10,
              ),
              if (i == 0)
                Container(
                  width: MediaQuery.of(context).size.width,
                  height: 300,
                  child: GridView.builder(
                      gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
                          maxCrossAxisExtent: 200,
                          childAspectRatio: 3 / 2,
                          crossAxisSpacing: 20,
                          mainAxisSpacing: 20),
                      itemCount: 4,
                      itemBuilder: (BuildContext ctx, index) {
                        return Container(
                          alignment: Alignment.center,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text('Course Name'),
                              SizedBox(
                                height: 10,
                              ),
                              Text('1200/-')
                            ],
                          ),
                          decoration: BoxDecoration(
                              color: Colors.amber,
                              borderRadius: BorderRadius.circular(15)),
                        );
                      }),
                )
              else if (i == 1)
                Container(
                  width: MediaQuery.of(context).size.width,
                  height: 300,
                  child: GridView.builder(
                      gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
                          maxCrossAxisExtent: 200,
                          childAspectRatio: 3 / 2,
                          crossAxisSpacing: 20,
                          mainAxisSpacing: 20),
                      itemCount: 4,
                      itemBuilder: (BuildContext ctx, index) {
                        return Container(
                          alignment: Alignment.center,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              Text('Course Name'),
                              SizedBox(
                                height: 10,
                              ),
                              Text('Status- 45 %')
                            ],
                          ),
                          decoration: BoxDecoration(
                              color: Colors.amber,
                              borderRadius: BorderRadius.circular(15)),
                        );
                      }),
                )
              else if (i == 2)
                Container(
                    width: MediaQuery.of(context).size.width,
                    height: 300,
                    child: Center(
                        child: Text(
                      'Today is no announcement !',
                      style: TextStyle(
                          color: AppColors.TextColor,
                          fontSize: 25,
                          fontWeight: FontWeight.bold),
                    ))),
              Container(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Contact Here:',
                      style: rubikRegular.copyWith(color: AppColors.TextColor),
                    ),
                    Text(
                      'Ph: +911234554321',
                      style: rubikRegular.copyWith(color: AppColors.TextColor),
                    ),
                    Text(
                      'Address: BHU Varanasi',
                      style: rubikRegular.copyWith(color: AppColors.TextColor),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        bottomNavigationBar: BottomNavigationBar(
          backgroundColor: AppColors.ButtonColor,
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              backgroundColor: AppColors.ButtonColor,
              icon: Icon(
                Icons.home,
                color: Colors.white,
              ),
              title: Text(
                'Home',
                style: TextStyle(color: Colors.white),
              ),
            ),
            BottomNavigationBarItem(
              backgroundColor: AppColors.ButtonColor,
              icon: Icon(
                Icons.work,
                color: Colors.white,
              ),
              title: Text(
                'Test',
                style: TextStyle(color: Colors.white),
              ),
            ),
            BottomNavigationBarItem(
              backgroundColor: AppColors.ButtonColor,
              icon: Icon(
                Icons.person,
                color: Colors.white,
              ),
              title: Text(
                'Profile',
                style: TextStyle(color: Colors.white),
              ),
            ),
          ],
        ));
  }
}
