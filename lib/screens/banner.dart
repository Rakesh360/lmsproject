// import 'dart:convert';
// import 'package:flutter_test_app/propery_details_widget.dart';
// import 'package:carousel_slider/carousel_slider.dart';
// import 'package:flutter/material.dart';
// import 'package:flutter/services.dart';

// class _PropertyDetailsState extends State<PropertyDetails> {
//   late List properties;
//   int index = 1;

//   Future<void> loadJsonData() async {
//     var jsonText = await rootBundle.loadString("assets/home.json");
//     setState(() {
//       properties = json.decode(jsonText);
//     });
//   }

//   @override
//   void initState() {
//     super.initState();
//     loadJsonData();
//   }

//   @override
//   Widget build(BuildContext context) {
//     Widget carousel = properties == null
//         ? CircularProgressIndicator()
//         : CarouselSlider(
//             items: properties[index]["image"].map((it) {
//               return new Container(
//                 width: MediaQuery.of(context).size.width,
//                 decoration: new BoxDecoration(),
//                 child: new Image.asset(it),
//               );
//             }).toList(),
//           //  autoPlay: true,
//            // autoPlayDuration: new Duration(seconds: 2),
//             //height: 200,
//              options: CarouselOptions(),
//           );

//     return Scaffold(
//       appBar: AppBar(
//         centerTitle: true,
//         title: Text("Test App"),
//       ),
//       body: Container(
//         height: MediaQuery.of(context).size.height,
//         width: MediaQuery.of(context).size.width,
//         child: Column(
//           children: <Widget>[
//             carousel,
//             Flexible(
//               fit: FlexFit.tight,
//               child: Container(
//                // child: Details(),
//               ),
//             )
//           ],
//         ),
//       ),
//     );
//   }
// }
