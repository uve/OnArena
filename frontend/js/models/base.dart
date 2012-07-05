#library('base');

#import('dart:html');
#import("dart:json");

interface BaseInterface extends Object{

    String id;
    String name;
    String created;
}


class Base {

  String class_name;

  Base() {

  }


  abstract void read(var data);

  void get(String id) {

      var url = "/api/$class_name/$id/";

      print(url);

      XMLHttpRequest request = new XMLHttpRequest();

      request.open("GET", url, true);
      request.setRequestHeader('Content-Type', 'application/json');


      request.on.readyStateChange.add((Event e) {
        if (request.readyState == XMLHttpRequest.DONE &&
              (request.status == 200 || request.status == 0)) {

                  var data = JSON.parse(request.responseText);
                  read(data);
            }
        });


      request.send();


  }

  void write(String message) {
    // the HTML library defines a global "document" variable
   // document.query('#status').innerHTML = document.query('#status').innerHTML + "<br/>" + message;
  }


}
