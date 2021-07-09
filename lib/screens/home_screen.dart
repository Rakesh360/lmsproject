import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:lmsproject/bloc/home_screen_bloc/bloc/home_screen_bloc.dart';
import 'package:lmsproject/utils/appColors.dart';
import 'package:lmsproject/utils/styles.dart';
import 'package:lmsproject/widgets/loader.dart';
import 'package:lmsproject/widgets/login/textInput.dart';
import 'package:page_indicator/page_indicator.dart';

class Profile extends StatefulWidget {
  const Profile({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<Profile> {
  late PageController controller;

  GlobalKey<PageContainerState> key = GlobalKey();
  int i = 0;
  TextEditingController textEditingController = TextEditingController();
  @override
  void initState() {
    super.initState();
    controller = PageController();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
        create: (context) => HomeScreenBloc(),
        child: BlocBuilder<HomeScreenBloc, HomeScreenState>(
            builder: (context, state) {
          if (state is HomeScreenInitial) {
            print('homeScreen <<<<<<<<  $state');
            return Scaffold(
                body: SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.only(top: 30),
                        child: Container(
                          height: 200,
                          child: ListView(
                            scrollDirection: Axis.horizontal,
                            children: new List.generate(5, (int index) {
                              return new Card(
                                child: new Container(
                                  width: 240.0,
                                  height: 50.0,
                                  decoration: new BoxDecoration(
                                    image: new DecorationImage(
                                      image: new AssetImage(
                                          "assets/images/leaf_" +
                                              index.toString() +
                                              ".jpeg"),
                                      fit: BoxFit.fill,
                                    ),
                                  ),
                                ),
                              );
                            }),
                          ),
                        ),
                      ),
                      Container(
                          padding: EdgeInsets.only(
                              top: 10, bottom: 8, left: 8, right: 8),
                          height: 110,
                          color: Colors.white,
                          child: Column(
                            children: [
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                mainAxisAlignment: MainAxisAlignment.start,
                                children: [
                                  Spacer(),
                                  Icon(
                                    Icons.notifications,
                                    color: Colors.white,
                                    size: 30,
                                  )
                                ],
                              ),
                              Spacer(),
                              TextInput(
                                  iconData: Icons.search,
                                  lable: 'Search Course Here',
                                  textEditingController: textEditingController),
                            ],
                          )),
                      Container(
                        padding: EdgeInsets.only(
                            top: 30, bottom: 8, left: 8, right: 8),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            GestureDetector(
                              onTap: () {
                                setState(() {
                                  i = 0;
                                });
                              },
                              child: Container(
                                decoration: BoxDecoration(
                                    color: Colors.cyan[50],
                                    borderRadius:
                                        BorderRadius.all(Radius.circular(8))),
                                height: 100,
                                width: 100,
                                child: Center(
                                    child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Image.asset(
                                      'assets/images/course.png',
                                      height: 50,
                                      width: 50,
                                    ),
                                    Text('Course',
                                        style: rubikRegular.copyWith(
                                            color: Colors.black)),
                                  ],
                                )),
                              ),
                            ),
                            GestureDetector(
                              onTap: () {
                                setState(() {
                                  i = 1;
                                });
                              },
                              child: Container(
                                decoration: BoxDecoration(
                                    color: Colors.red[50],
                                    borderRadius:
                                        BorderRadius.all(Radius.circular(8))),
                                height: 100,
                                width: 100,
                                child: Center(
                                    child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Image.asset(
                                      'assets/images/course.png',
                                      height: 50,
                                      width: 50,
                                    ),
                                    Text('My Course',
                                        style: rubikRegular.copyWith(
                                            color: Colors.black)),
                                  ],
                                )),
                              ),
                            ),
                            GestureDetector(
                              onTap: () {
                                setState(() {
                                  i = 2;
                                });
                              },
                              child: Container(
                                decoration: BoxDecoration(
                                    color: Colors.blue[50],
                                    borderRadius:
                                        BorderRadius.all(Radius.circular(8))),
                                height: 100,
                                width: 103,
                                child: Center(
                                    child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Image.asset(
                                      'assets/images/course.png',
                                      height: 50,
                                      width: 50,
                                    ),
                                    Text('Announcement',
                                        style: rubikRegular.copyWith(
                                            color: Colors.black)),
                                  ],
                                )),
                              ),
                            ),
                          ],
                        ),
                      ),
                      SizedBox(
                        height: 10,
                      ),
                      if (i == 0)
                        Container(
                          padding: EdgeInsets.all(8),
                          width: MediaQuery.of(context).size.width,
                          child: GridView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              gridDelegate:
                                  SliverGridDelegateWithMaxCrossAxisExtent(
                                      maxCrossAxisExtent: 200,
                                      mainAxisSpacing: 30,
                                      crossAxisSpacing: 6),
                              itemCount: 4,
                              itemBuilder: (BuildContext ctx, index) {
                                return Container(
                                  padding: EdgeInsets.only(bottom: 8),
                                  child: Column(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Image.asset('assets/images/leaf.jpeg'),
                                      Text('Course Name'),
                                      Text('1200/-'),
                                      Align(
                                        alignment: Alignment.centerRight,
                                        child: Container(
                                            child: Center(
                                                child: Text(
                                              'Buy Now',
                                              style: TextStyle(
                                                  color: Colors.white),
                                            )),
                                            width: 70,
                                            height: 20,
                                            decoration: BoxDecoration(
                                                borderRadius: BorderRadius.all(
                                                    Radius.circular(5)),
                                                color: AppColors.ButtonColor)),
                                      )
                                    ],
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.cyan[50],
                                  ),
                                );
                              }),
                        )
                      else if (i == 1)
                        Container(
                          padding: EdgeInsets.all(8),
                          width: MediaQuery.of(context).size.width,
                          child: GridView.builder(
                              shrinkWrap: true,
                              physics: NeverScrollableScrollPhysics(),
                              gridDelegate:
                                  SliverGridDelegateWithMaxCrossAxisExtent(
                                      maxCrossAxisExtent: 200,
                                      mainAxisSpacing: 30,
                                      crossAxisSpacing: 6),
                              itemCount: 4,
                              itemBuilder: (BuildContext ctx, index) {
                                return Container(
                                  padding: EdgeInsets.only(bottom: 8),
                                  child: Column(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Image.asset('assets/images/leaf.jpeg'),
                                      Text('Course Name'),
                                      Text('Status - 45%'),
                                    ],
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.red[50],
                                  ),
                                );
                              }),
                        )
                      else if (i == 2)
                        Container(
                            width: MediaQuery.of(context).size.width,
                            height: 300,
                            child: Center(
                                child: Text('Today is no announcement !',
                                    style: rubikRegular.copyWith(
                                        color: AppColors.TextColor,
                                        fontSize: 25,
                                        fontWeight: FontWeight.bold)))),
                      Card(
                        elevation: 8,
                        child: Container(
                          padding: EdgeInsets.all(8),
                          width: MediaQuery.of(context).size.width,
                          decoration: BoxDecoration(
                              borderRadius:
                                  BorderRadius.all(Radius.circular(5)),
                              color: Colors.white),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Contact Here:',
                                style: rubikRegular.copyWith(
                                    color: AppColors.TextColor, fontSize: 20),
                              ),
                              Text(
                                'Ph: +911234554321',
                                style: rubikRegular.copyWith(
                                    color: AppColors.TextColor),
                              ),
                              Text(
                                'Address: BHU Varanasi',
                                style: rubikRegular.copyWith(
                                    color: AppColors.TextColor),
                              ),
                            ],
                          ),
                        ),
                      )
                    ],
                  ),
                ),
                bottomNavigationBar: BottomNavigationBar(
                  backgroundColor: AppColors.BorderColor,
                  items: const <BottomNavigationBarItem>[
                    BottomNavigationBarItem(
                      backgroundColor: AppColors.BorderColor,
                      icon: Icon(
                        Icons.home,
                        color: AppColors.ButtonColor,
                      ),
                      title: Text(
                        'Home',
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                    BottomNavigationBarItem(
                      backgroundColor: AppColors.BorderColor,
                      icon: Icon(
                        Icons.work,
                        color: AppColors.ButtonColor,
                      ),
                      title: Text(
                        'Test',
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                    BottomNavigationBarItem(
                      backgroundColor: AppColors.BorderColor,
                      icon: Icon(
                        Icons.person,
                        color: AppColors.ButtonColor,
                      ),
                      title: Text(
                        'Profile',
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  ],
                ));
          }
          ;
          return HoldLoader();
        }));
  }
}
