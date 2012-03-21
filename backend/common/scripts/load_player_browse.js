

load_async({ 
            'key':           'player_browse_tournament_id_' + '{{ tournament.id }}',
            'last_modified': '{{ request.player_browse_tournament_id_ }}',
            'template':      '#template-player-browse', 
            'selector':      '#player-browse2',
            'data':          { 'name': 'player_browse', 'tournament_id': '{{ tournament.id }}' } 
            }, function(data) {
                           
                  var index = 0;
                  var all_players = new Array();

                  
                 $.each($(this), function(index, value) { 
                    
                   
                    personObj = new Object();
                    personObj.id = value.id;
                    personObj.value = value.full_name;
                                        
                    personObj.label = value.full_name + " ( ";
                    

                    $.each(value.teams, function(k, value2) { 
                          personObj.label += value2.name;
                          if (k < value.teams.length - 1 ){
                            personObj.label += ", ";
                          }                           
                    })
                  
                    personObj.label += " )";                                      
                    all_players[index] = personObj;                                 
                    index++;
                });  
                  
                                      
                                                            
                 $("input#autocomplete").autocomplete({ source: all_players,
                                                        minLength: 2,
                                                        select: function( event, ui ) {
					                                        
					                                      $("input#player_id").attr("value", ui.item.id);
			                                             }
			
			 });  
                                    
             
        });



