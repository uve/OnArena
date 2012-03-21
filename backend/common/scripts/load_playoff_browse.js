{% load i18n %}

load_async({ 
            'key':           'playoff_browse_league_id_' + '{{ league.id }}',
            'last_modified': '{{ request.playoff_browse_league_id_ }}',
            'template':      '#template-playoff-browse', 
            'selector':      '#playoff-browse',
            'data':          { 'name': 'playoff_browse', 'league_id': '{{ league.id }}' } 
            }, function() {
            
                        {% if request.is_owner %}
                        
                        load_async({ 
                                    'key':           'team_browse_tournament_id_' + '{{ request.tournament.id }}',
                                    'last_modified': '{{ request.team_browse_tournament_id_ }}',
                                    'template':      '#template-team-browse', 
                                    'selector':      '.playoff-select-competitors',
                                    'data':          { 'name': 'team_browse', 'tournament_id': '{{ request.tournament.id }}' } 
                                    }, function() {

                                });

                                                
                                                
                        
                            $('.playoff-select-competitors').change(function() {
                        
                            
                                $.ajax({
                                       type: "POST",
                                       url: "/league/{{ league.id }}/playoff/set/",
                                       data: ({ team_id : $(this).val(), 
                                                competitor_id : this.getAttribute('name') }),
                                       success: function(msg){
                                         /*alert( "Data Saved: " + msg );*/
                                       }
                                }); 
                            
                        });   
                        
                       
                           
                     {% endif %}  
             
        });


  
