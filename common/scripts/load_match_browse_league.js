{% load i18n %}

load_async({ 
            'key':           'match_browse_league_id_' + '{{ league.id }}',
            'last_modified': '{{ request.match_browse_league_id_ }}',
            'template':      '#template-match-browse', 
            'selector':      '#match-browse',
            'data':          { 'name': 'match_browse', 'league_id': '{{ league.id }}' } 
            }, function() {
            
                  {% include 'common/scripts/match_remove.js' %} 
             
        });

