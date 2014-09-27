
load_async({ 
            'key':           'group_browse_league_id_' + '{{ league.id }}',
            'last_modified': '{{ request.group_browse_league_id_ }}',
            'template':      '#template-group-browse', 
            'selector':      '#group-browse',
            'data':          { 'name': 'group_browse', 'league_id': '{{ league.id }}' } 
            }, function() {
                        
            var $tabs1 = $( "#tabs1" ).tabs();
            $tabs1.tabs('select', 0); 
            
            var $tabs2 = $( "#tabs2" ).tabs();
            $tabs2.tabs('select', 0); 
            
            var $tabs3 = $( "#tabs3" ).tabs();
            $tabs3.tabs('select', 0);        
            
            {% include 'common/scripts/remove_team_group.js' %}         
             
        });

