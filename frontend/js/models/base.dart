#import('dart:html');
#import('../JsonObject.dart');

interface BaseInterface extends JsonObject {

    String id;
    String name;      
    String item_id;
    String item_name;  
    
    String created;
}


class Base {

  String class_name; 
    
  Base() {
     
  }
  
  read(var data) {
  }

  void get(String id) {
    
      var url = "/api/" + class_name + "/$id/"; 
                             
      XMLHttpRequest request = new XMLHttpRequest();
      
      request.open("GET", url, true);
      request.setRequestHeader('Content-Type', 'application/json');

      
      request.on.readyStateChange.add((Event e) {
        if (request.readyState == XMLHttpRequest.DONE &&
              (request.status == 200 || request.status == 0)) {
                  //Map data = JSON.parse(request.responseText);  
                  
                  Map data = new JsonObject.fromJsonString(request.responseText);
                  
                  read(data);                  
            }
        });
       
      
      request.send();    
    
    
  }
  
  void write(String message) {
    // the HTML library defines a global "document" variable
    document.query('#status').innerHTML = document.query('#status').innerHTML + "<br/>" + message;
  }  
    
  
}  
