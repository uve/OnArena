{% load i18n %}

load_async({ 
            'key':           'match_browse_team_id_' + '{{ team.id }}',
            'last_modified': '{{ request.match_browse_team_id_ }}',
            'template':      '#template-match-browse', 
            'selector':      '#match-browse',
            'data':          { 'name': 'match_browse', 'team_id': '{{ team.id }}' } 
            }, function() {
            
                  {% include 'common/scripts/match_remove.js' %} 
             
        });

