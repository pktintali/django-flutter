import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:flutterd/models/miscard.dart';
import 'package:localstorage/localstorage.dart';
import 'package:http/http.dart' as http;

class MiscardState with ChangeNotifier {
  LocalStorage storage = new LocalStorage('usertoken');

  List<MisCard> _miscards = [];

  Future<bool> getMisCards() async {
    String url = 'http://127.0.0.1:8000/api/miscards/';
    var token = storage.getItem('token');
    try {
      http.Response response =
          await http.get(url, headers: {'Authorization': "token $token"});
      print(response.body);
      var data = json.decode(response.body) as List;
      // print(data);
      List<MisCard> temp = [];
      data.forEach((element) {
        MisCard product = MisCard.fromMap(element);
        temp.add(product);
      });
      _miscards = temp;
      notifyListeners();
      return true;
    } catch (e) {
      print("e getProducts");
      print(e);
      return false;
    }
  }

  Future<bool> addMiscard(String title, String mistake,String lesson) async {
    String url = 'http://127.0.0.1:8000/api/miscards/';
    var token = storage.getItem('token');
    try {
      http.Response response = await http.post(url,
          headers: {
            "Content-Type": "application/json",
            'Authorization': "token $token"
          },
          body: json.encode({"title": title, "mistake": mistake,"lesson":lesson}));
      var data = json.decode(response.body) as Map;
      print(data);
      if (data["error"] == false) {
        return true;
      }
      return false;
    } catch (e) {
      print("e miscard adding");
      print(e);
      return false;
    }
  }

  List<MisCard> get miscards {
    return [..._miscards];
  }
}
