    $("#search-submit-site").bind("click", function(e, data) { 
           
      /*
       $.ajax({                         
                type: "GET",
                dataType: 'JSONP', 
                url: "https://www.googleapis.com/customsearch/v1",
                data: ({ 'key': '{{ GOOGLE_SIMPLE_API }}',
                         'cx':  '{{ GOOGLE_CUSTOM_SEARCH }}',
                         'alt':  'json',
                         'q':  $("#search-query").val(),
                      }),                  
                jsonp: "$callback",                 
                success: function( e, data ) {                                    
                    console.log("Hello");
                }
        });     
        */
        window.location = "http://www.google.ru/search?q=site:www.onarena.com+" +
                           $("#search-query").val();
        
  
	});
