import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:lmsproject/model/signup_model.dart';

class APIService {
  Future<SignupModel> signup(SignupModel signupModel) async {
    String url = "http://127.0.0.1:8000/api/accounts/";
    final response =
        await http.post(Uri.parse(url), body: signupModel.toJson());
    if (response.statusCode == 200 || response.statusCode == 400) {
      return SignupModel.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load Data');
    }
  }
}
