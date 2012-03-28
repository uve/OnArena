{% load i18n %}

load_async({ 
            'key':           'match_browse_referee_id_' + '{{ referee.id }}',
            'last_modified': '{{ request.match_browse_referee_id_ }}',
            'template':      '#template-match-browse', 
            'selector':      '#match-browse',
            'data':          { 'name': 'match_browse', 'referee_id': '{{ referee.id }}' } 
            }, function() {
            
                  {% include 'common/scripts/match_remove.js' %} 
             
        });

