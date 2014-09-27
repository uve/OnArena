{% load i18n %}


$( "#dialog-playoff-form" ).dialog({
		autoOpen: false,
		height: 400,
		width: 600,
		modal: true,
		buttons: {
			"{% trans 'Create Playoff' %}": function() {
			    
			    var bValid = true;
				/*allFields.removeClass( "ui-state-error" );*/
				
				var playoff_name  = $( "#playoff-name" );
				var playoff_teams = $( "#playoff-teams" );
				
				 
				var third_place;
        		if ($('#id-third-place').is(':checked')){ 
        		    third_place = true; } else { third_place = false; }
				
																		   
			    bValid = bValid && checkLength( playoff_name, "name", 5, 40 );
        	    bValid = bValid && checkLength( playoff_teams, "teams", 1, 2 );

				if ( bValid ) {
				
        			//console.log(third_place);
                    
                    /*				
					$.post("/league/{{ league_id }}/playoff/create/", 
					    { 'name': playoff_name.val(), 'size': playoff_teams.val() } );
				    */
					    
			        $.ajax({
                       type: "POST",
                       url: "/league/{{ league_id }}/playoff/create/",
                       data: ({ 'name': playoff_name.val(), 
                                'size': playoff_teams.val(),
                                'third_place': third_place }),                                
                       success: function(msg){

                       }
                    }); 
					
					$( this ).dialog( "close" );
				}
			},
			"{% trans 'Cancel' %}": function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			/*allFields.val( "" ).removeClass( "ui-state-error" );*/
		}
	});



    $("#playoff-create").click(function () { 
        $( "#dialog-playoff-form" ).dialog( "open" );
    });
	
