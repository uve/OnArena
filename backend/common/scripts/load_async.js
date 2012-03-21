
function load_async(item, callback) {

  var key = item['key'];
  
  var etag_browse = item['last_modified'];
  
  var last_modified = 'last_modified_' + key;  
    
  var etag_local = '';
  var item_local = '';
  
  if (is_localStorage == true){  
    etag_local = window.localStorage.getItem(last_modified);     
    item_local = window.localStorage.getItem(key)  
  }
  
  if (is_localStorage == true && etag_local != '' && etag_local == etag_browse && item_local)
  {
        {% if request.is_global_admin %}
            console.time(key);
            console.log("LocalStorage: " + key + " lenght: " + item_local.length);            
        {% endif %}          
        
        values = JSON.parse(item_local);     

        $.each(values, function(index, value) { 
           value.index = index + 1 ;
        });  
                                
        //$( item['selector'] ).empty();                         
        $( item['template'] ).tmpl( values ) 
        .appendTo( item['selector'] );  
        
        {% if request.is_global_admin %}        
            console.timeEnd(key);        
        {% endif %}            
        callback.call(values);    
  }
  else{

    var geturl = $.ajax({                         
                type: "GET",
                url: "/api/",
                data: ( item['data'] ),  
                                        
                jsonp: "$callback",                 
                success: function( data ) {                                    
                    var values = data;      
       
                    if (values.length > 0) {                                                
                                                                                     
                        {% if request.is_global_admin %}
                            console.time(key);                        
                            console.log("Ajax: " + key + " lenght: " + values.length);
                        {% endif %}          
        
                        
                        $.each(values, function(index, value) { 
                           value.index = index + 1 ;
                        });   
                        
                        //$( item['selector'] ).empty();                         
                        $( item['template'] ).tmpl( values ) 
                        .appendTo( item['selector'] );    
             
                    
                        if (is_localStorage == true){  
                        
                            try {
                            window.localStorage.removeItem(key);
                            window.localStorage.setItem(last_modified, geturl.getResponseHeader('Last-Modified'));                        
                            window.localStorage.setItem(key, JSON.stringify(values, 
                                        function(k, v) { return v === "" ? "" : v }));        

                            } catch (e) {
	                            
	                             	 console.log('Quota exceeded!');
	                           
                            }                                                                                     
                        }
                                    
                                   
                        {% if request.is_global_admin %}        
                            console.timeEnd(key);        
                        {% endif %} 
                        
                        callback.call(values); 
                                                
                    }
                    else {
             
                        if (item['template'] == '#template-group-browse'){
                                                    
                            $( '#template-group-browse-empty' ).tmpl() 
                            .appendTo( item['selector'] );   
                        }
                    }
                }
                
        });     
  };
}  
