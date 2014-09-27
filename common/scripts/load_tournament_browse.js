     $.ajax({                         
            type: "GET",
            url: "/api/",
            data: ({ 'name': 'tournament_browse' }),                                          
            
            jsonp: "$callback",                 
            success: function( data ) {                                    
                var values = data;      
                
                if (values) {
                    $( "#tournament-browse" ).empty();                         
                    $( "#template-tournament-browse" ).tmpl( values ) 
                    .appendTo( "#tournament-browse" );     
                }
            }
    });     
