class SignupModel {
  String password;
  String username;
  String email;

  SignupModel(
      {required this.email, required this.password, required this.username});
  // factory SignupModel.fromJson(Map<String,dynamic> json)

  Map<String, dynamic> toJson() {
    Map<String, dynamic> map = {
      password: 'password'.trim(),
      username: 'username'.trim(),
      email: 'email'.trim()
    };
    return map;
  }

  static Future<SignupModel> fromJson(decode) {
    return decode;
  }
}
