{% load i18n %}

  var geocoder;
  var map;
  var markersArray = [];
  var beaches;
                
  
     /************************************************************************************/
     /******************           SET  MARKERS          *********************************/
 
  



             
        function addMarker(marker, content, url)
        {
        
            var infoWindow = new google.maps.InfoWindow({
                content: content,
                maxWidth: 300
            }); 
           google.maps.event.addListener(marker, 'click', function() {
                         /*  infoWindow.setContent(content);
                           infoWindow.open(map, marker);
                           */
                        window.location = url;
                           
         });
                 
        
            
           google.maps.event.addListener(marker, 'mouseover', function() {
                           infoWindow.setContent(content);
                           infoWindow.open(map, marker);
         });
         
            
           google.maps.event.addListener(marker, 'mouseout', function() {
                         infoWindow.close(map, marker);
         });
         
         
        };

        /**********************           SET MARKERS                   *******************************/        

        function setMarkers(map, locations) {
          // Add markers to the map
          
          
          // Marker sizes are expressed as a Size of X,Y
          // where the origin of the image (0,0) is located
          // in the top left of the image.

          // Origins, anchor positions and coordinates of the marker
          // increase in the X direction to the right and in
          // the Y direction down.
          var image_soccer = new google.maps.MarkerImage('http://commondatastorage.googleapis.com/cometip/images/soccer_ball.png',
              new google.maps.Size(45,48),
              new google.maps.Point(0,0),
              new google.maps.Point(0, 32));
              
          var image_basketball = new google.maps.MarkerImage('http://commondatastorage.googleapis.com/cometip/images/sport/basketball1.png',
              new google.maps.Size(45,48),
              new google.maps.Point(0,0),
              new google.maps.Point(0, 32));
              
          var image_volleyball = new google.maps.MarkerImage('http://commondatastorage.googleapis.com/cometip/images/sport/volleyball1.png',
              new google.maps.Size(45,48),
              new google.maps.Point(0,0),
              new google.maps.Point(0, 32));
              
          var image_hockey = new google.maps.MarkerImage('http://commondatastorage.googleapis.com/cometip/images/sport/hockey1.png',
              new google.maps.Size(45,48),
              new google.maps.Point(0,0),
              new google.maps.Point(0, 32));                                          
              // coordinate.
              
              
          var shape = {
              coord: [1, 1, 1, 90, 90, 90, 90 , 1],
              type: 'poly'
          };
          
          var markers = [];
          for (var i = 0; i < locations.length; i++) {
          
            var tournament = locations[i];
            
            if (!tournament){
                continue;
            }
            
            
            var myLatLng = new google.maps.LatLng(tournament['lat'], tournament['lon']);
            
            
            switch(tournament['sport_id'])
            {
                case '1001':
                  sport_name = "{% trans 'Football' %}";
                  marker_image = image_soccer;
                  break;
                case '1002':
                  sport_name = "{% trans 'Basketball' %}";
                  marker_image = image_basketball;                  
                  break;
                case '1003':
                  sport_name = "{% trans 'Volleyball' %}";
                  marker_image = image_volleyball;                  
                  break;
                case '1004':
                  sport_name = "{% trans 'Hockey' %}";
                  marker_image = image_hockey;                  
                  break;                                    
                default:
                  sport_name = "{% trans 'Football' %}";
                  marker_image = image_soccer;
                  break;      
            }
            
            tournament_url = '/tournament/'+ tournament['id'] + '/';
            
            var contentString = '<div id="info-content">'+
            '<h1>'+ tournament['name'] + '</h1>'+    
            '<p><b>{% trans "Sport" %}: </b> {% trans "Soccer" %}</p>' +
            '<p><b>{% trans "Address" %}: </b>'+  tournament['address'] + '</p>'+ 
            '<p><b>{% trans "Contacts" %}: </b>'+ tournament['contacts'] + '</p>'+ 
            '<p><b>{% trans "URL" %}: </b> <a href="'+ 
            tournament_url + '">'+ tournament_url +
            '</a></p></div>';
                

            var marker = new google.maps.Marker({
                'position': myLatLng,
                map: map,        
                icon:  marker_image,        
                shape: shape,
                title: '{% trans "Click to view Tournament" %}',
                /*shadow: shadow,*/
                zIndex: 1
            });
             
         
            addMarker(marker, contentString, tournament_url);
            markers.push(marker);
          }
          
          var markerClusterer = new MarkerClusterer(map, markers, {
              maxZoom: 9,
              gridSize: 50,
              styles: null
          });
        }
    
     /**********************                               *******************************/        
     /************************************************************************************/
     
     
  
  function placeMarker(location) {
  
    if (markersArray) {
      for (i in markersArray) {
        markersArray[i].setMap(null);
      }
      markersArray.length = 0;
    }

    $("#id_location").val(location);
    $("#id_lat").val(location.lat());
    $("#id_lon").val(location.lng());    
  
      var marker = new google.maps.Marker({
          position: location, 
          map: map
      });
      
      markersArray.push(marker);
      map.setCenter(location);
      
      geocoder.geocode( { 'location': location}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
      
        /*console.log(results);*/

        get_address(results[0]);
          
        
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
      
      /*console.log(location);*/
    }  
    
    var initialLocation;
    //ar siberia = new google.maps.LatLng(60, 105);
    //var newyork = new google.maps.LatLng(40.69847032728747, -73.9514422416687);
    var browserSupportFlag =  new Boolean();
    var zoom;
    
    
   function tournament_browse(map){
    
    /*console.log("start browse");*/
     var location = map.getCenter();
 
      for (i in beaches) {    

        beaches[i]["diff"] = (google.maps.geometry.spherical.computeDistanceBetween(location, beaches[i]["location"]) / 1000).toFixed(1);
        
         
      }
      
      beaches.sort(function(a,b){return a["diff"] - b["diff"]})      

     $( "#tournament-browse" ).empty();                         
         $( "#template-tournament-browse" ).tmpl( beaches ) 
        .appendTo( "#tournament-browse" );   

   } 
   
   

   function initialize() {
    
       
        {% if tournament.lat %}                       
            var place = new google.maps.LatLng( {{ tournament.lat }}, {{ tournament.lon }});
            
        var myOptions = {
            zoom: 17,
            maxZoom: 20,
            center: place,
            /*language: 'ja',*/
            mapTypeId: google.maps.MapTypeId.HYBRID
        };            

                     beaches = [

      
                    {'id': '{{ tournament.id }}', 'sport_id': '{{ tournament.sport_id.id }}',
                     'name': '{{ tournament.name }}', 'address': '{{ tournament.address }}',
                     'contacts': '{{ tournament.contacts }}', 'country': '{{ tournament.country }}',                     
                     'city': '{{ tournament.city }}',
                     'lat': {{ tournament.lat }}, 'lon': {{ tournament.lon }} }      
      
         
        ];
        
      
            
        {% else %}     
        
        var myOptions = {
            zoom: 12,
            maxZoom: 20,
            mapTypeId: google.maps.MapTypeId.ROADMAP
            /*language: 'ja',*/
        };
        
        {% endif %}                    

  
        map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

               
         {% if tournament.lat %} 
            setMarkers(map, beaches);             
            return;
         {% endif %}  
         
                 
        geocoder = new google.maps.Geocoder();
       
              

         beaches = [

          {% if all_tournaments|length %}
            {% for tournament in all_tournaments %}        
                {% if tournament.lat %}      
                    {'id': '{{ tournament.id }}', 'sport_id': '{{ tournament.sport_id.id }}',
                     'name': '{{ tournament.name }}', 'address': '{{ tournament.address }}',
                     'contacts': '{{ tournament.contacts }}', 'country': '{{ tournament.country }}',                     
                     'city': '{{ tournament.city }}',
                     'lat': {{ tournament.lat }}, 'lon': {{ tournament.lon }} }  {% if not forloop.last %},{% endif %}      
                {% endif %}            
            {% endfor %}
          {% endif %}
         
        ];
        
        
     for (i in beaches) {    
        beaches[i]["location"] = new google.maps.LatLng(beaches[i]["lat"],beaches[i]["lon"]);
      }  

        if (beaches.length){
            setMarkers(map, beaches);
        }            


 
        google.maps.event.addListener(map, 'bounds_changed', function(event){         
           tournament_browse(map);
        });        

        google.maps.event.addListener(map, 'click', function(event) {
           placeMarker(event.latLng);           
        });        
    
        //var defzoom = map.getZoom();
        
        var location_finded = false;
    
        {% if request.location %}
           initialLocation = new google.maps.LatLng({{ request.location.0 }},{{ request.location.1 }});
           map.setCenter(initialLocation);
           tournament_browse(map);   
           
           location_finded = true;
           
        {% else %}
           handleNoGeolocation(true);
        {% endif %}           
       
  
       // Try W3C Geolocation (Preferred)
       if(navigator.geolocation) {
           
           if (location_finded == false){
              handleNoGeolocation(true);
           }
       
           browserSupportFlag = true;

           navigator.geolocation.getCurrentPosition(function(position) {
           
           location_finded = true;
           
           initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
                                 
           map.setCenter(initialLocation);            
           tournament_browse(map);                                    
           //zoom = map.getZoom();  
                    
           //map.setZoom(defzoom - 1); 

       }, function() {
            handleNoGeolocation(browserSupportFlag);
        });
         // Try Google Gears Geolocation
       } else {
            browserSupportFlag = false;
            handleNoGeolocation(browserSupportFlag);
        }
  

  
        function handleNoGeolocation(errorFlag) 
        {
                                
            geocoder.geocode( { 'address': '{{ request.country_code }}' }, 
                             function(results, status)
             {
                  if (status == google.maps.GeocoderStatus.OK)
                  {
                         if (location_finded == true){
                            return;
                         }           
           
                        map.setCenter(results[0].geometry.location);
                        
                        tournament_browse(map);
                        
                         var ne = results[0].geometry.viewport.getNorthEast();
                         var sw = results[0].geometry.viewport.getSouthWest();

                         map.fitBounds(results[0].geometry.viewport);               

                         var boundingBoxPoints = [
                            ne, new google.maps.LatLng(ne.lat() , sw.lng()),
                            sw, new google.maps.LatLng(sw.lat(), ne.lng()), ne
                         ];

                         var boundingBox = new google.maps.Polyline({
                            path: boundingBoxPoints,
                            strokeColor: '#FF0000',
                            strokeOpacity: 1.0,
                            strokeWeight: 2
                         });

                         //boundingBox.setMap(map);
                         //map.setZoom(8);    
                         
                         zoom = map.getZoom();
                         map.setZoom(zoom + 1);                 
                  } 
                  else 
                  {
        alert("Geocode was not successful for the following reason: " + status);
                  }
            });
            


        }              
                      
                    
    }


    

   
   function get_address (result)
   {
        
     //console.log("form: " + result.formatted_address);
     //Doo something
         $.each(result.address_components, function (index,value) {
         
            $.each(value.types, function (item, type) {      
        
                if(type == 'street_number') { 
                    streetNumber = value.long_name; 
                    /*console.log("streetNumber: " + streetNumber);*/
                } 

                if(type == 'route') { 
                    streetName = value.long_name; 
                    /*console.log("streetName: " + streetName);*/
                } 
    
                if(type == 'country') { 
                    country = value.long_name;                     
                    /*console.log("Country: " + country);*/
                    $("#id_country").val(country);
                } 

                if(type == 'postal_code') { 
                    postalCode = value.long_name; 
                    /*console.log("postalCode: " + postalCode);*/                       
                } 

                if(type == 'locality') { 
                    city = value.long_name; 
                    /*console.log("city: " + city);*/  
                    $("#id_city").val(city);                                         
                } 

            });        
       
        });

   }     
  
   $("#search_submit").bind("click", function() {      
 
   var address = $("#search-query").val(); 
  
    //console.log("JSON Data: " + address); 
    // , 'region':   'uk'
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
            map: map, 
            position: results[0].geometry.location
        });
        
        markersArray.push(marker);
        //console.log(results[0]);        

        get_address(results[0]);
          
        
      } else {
        /*alert("Geocode was not successful for the following reason: " + status);*/
      }
    });

  });
  

      
   if ($("#map_canvas").length){

       initialize();

   }
