{% load i18n %}

        $('.remove-match').bind('click', function() {   
  
                var $ttr = $( this );
                var $title = '<h2>' + $( this ).attr("title") + '</h2>';
                $('.inner').replaceWith($title);  
        

                 var $match_del = "/match/" + $( this ).attr("id") + "/remove/";

                 $( "#dialog-confirm" ).dialog({
	        	        resizable: false,
	                  	modal: true,
		              	buttons: {
				             '{% trans "Remove Match" %}': function()  {
				        
                                     $.post($match_del, { remove: "True" } );
                            		 $( this ).dialog( "close" );
     
                                     $('.inner').replaceWith($title); 
      
                                     $( "#dialog-message" ).dialog({
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
