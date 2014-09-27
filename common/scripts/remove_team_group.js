{% load i18n %}

        $('.remove-team-group').bind('click', function() {   
  
                var $ttr = $( this );
                

                
                var team_id   = $( this ).attr("data-team_id");
                var team_name = $( this ).attr("data-team_name");                
                var league_id = $( this ).attr("data-league_id");
                var group_id  = $( this ).attr("data-group_id");
                
                var $title = '<h2>' + team_name + '</h2>';
                $('.inner').replaceWith($title);                  
                
                /*console.log(team_id + "  " + team_name + "  " + league_id + "  " + group_id + "  " );*/
                
                var url = "/league/" + league_id + "/remove/team/";
                
                $( "#dialog-remove-team-group-confirm" ).dialog({
	        	        resizable: false,
	                  	modal: true,
	                  	minWidth: 400,
		              	buttons: {
				             '{% trans "Remove Team" %}': function()  {
				        
                                     $.post(url, { 
                                                            'team_id':  team_id,
                                                            'league_id':league_id,
                                                            'group_id': group_id
                                                                                                                                      
                                      } );
                            		 $( this ).dialog( "close" );
     
                                     $('.inner').replaceWith($title); 
      
                                     $( "#dialog-remove-team-group-message" ).dialog({
			                             modal: true,
                               			 buttons: {
                        				            Ok: function() {
                                        					$( this ).dialog( "close" );
                                    		          	  }
                                		          	}
                              		});           

                                    $ttr.parent().parent().remove();
			        	          },
            	        	'{% trans "Cancel" %}': function() {
		                     	     $( this ).dialog( "close" );
                       				}
                            }
                		});        
                     });
                     
                     
               
