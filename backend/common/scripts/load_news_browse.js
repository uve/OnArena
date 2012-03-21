
load_async({ 
            'key':           'news_browse_tournament_id_' + '{{ request.tournament.id }}',
            'last_modified': '{{ request.news_browse_tournament_id_ }}',
            'template':      '#template-news-browse', 
            'selector':      '#list-news',
            'data':          { 'name': 'news_browse', 'tournament_id': '{{ request.tournament.id }}' } 
            }, function() {

        });

