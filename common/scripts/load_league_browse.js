      
load_async({ 
            'key':           'league_browse_tournament_id_' + '{{ request.tournament.id }}',
            'last_modified': '{{ request.league_browse_tournament_id_ }}',
            'template':      '#template-list-league', 
            'selector':      '#list-league',
            'data':          { 'name': 'league_browse', 'tournament_id': '{{ request.tournament.id }}' } 
            }, function() {

        });
        
