

load_async({ 
            'key':           'player_browse_tournament_id_' + '{{ tournament.id }}',
            'last_modified': '{{ request.player_browse_tournament_id_ }}',
            'template':      '#template-player-browse', 
            'selector':      '#player-browse2',
            'data':          { 'name': 'player_browse', 'tournament_id': '{{ tournament.id }}' } 
            }, function(data) {
                           
                  var index = 0;
                  window.all_players = this;//new Array();

                  //console.log(this);
                  
                  for (var i=0;i<all_players.length;i++)
                  {       
                	  
                	  all_players[i].label = all_players[i].full_name + " (";
                	  

                	  if (all_players[i].teams){
	                	  for (var j=0;j<all_players[i].teams.length;j++)
	                      {   
	                		  all_players[i].label += all_players[i].teams[j].name;
	                		  
	                            if (j < all_players[i].teams.length - 1 ){
	                            	all_players[i].label += ", ";
	                            }                           
	                      }
                	  }
                      
                      all_players[i].label += ")";    
                      
                  }
                
                                    
                                                            
                 $("input#autocomplete").autocomplete({ source: all_players,
                                                        minLength: 2,
                                                        select: function( event, ui ) {
					                                        
					                                      $("input#player_id").attr("value", ui.item.id);
			                                             }
			
			 });  
                                    
             
        });



