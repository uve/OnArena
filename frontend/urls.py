# Copyright 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from django.conf.urls.defaults import *
from settings import *

#from protorpc import service_handlers

#import logging

urlpatterns = patterns('',
)

from views.index import Index

from views.news import News
from views.team import Team


urlpatterns += patterns('views',              
          

    (r'^$', Index.as_view()),
              
    (r'^api/news/(?P<pk>[\da-f]+)/$', News.as_view()),
    (r'^api/team/(?P<pk>[\da-f]+)/$', Team.as_view()),    

    
    #To-do:
    
    #(r'^api/tournament/(?P<pk>[\da-f]+)/$', Tournament.as_view()),
    #(r'^api/season/(?P<pk>[\da-f]+)/$',  Season.as_view()),  
       
    #(r'^api/league/(?P<pk>[\da-f]+)/$',  League.as_view()),
    #(r'^api/league/(?P<pk>[\da-f]+)/stat/$', League.as_view(stat=True)),
    #(r'^api/league/(?P<pk>[\da-f]+)/print/$', League.as_view(print=True)),
       
    #(r'^api/match/(?P<pk>[\da-f]+)/$',   Match.as_view()),   
    #(r'^api/player/(?P<pk>[\da-f]+)/$',  Player.as_view()),   
    #(r'^api/referee/(?P<pk>[\da-f]+)/$', Referee.as_view()),        
    
    # (r'^api/image/(?P<pk>[\%\-\a-zA-Z0-9]+)$', 'Image'.as_view()),              
)


# TOURNAMENT
urlpatterns += patterns('tournament.views',
    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/$', 'tournament_item'),
    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/test/$', 'tournament_test'),
    (r'^tournament/(?P<tournament_id>[\da-f]+)/start/$', 'tournament_start'),
    


    
)



urlpatterns += patterns('common.user',                                                  
    (r'^login/$', 'login'),    
    (r'^logout/$', 'logout'),
)


    
    
###################################################3    
    
handler404 = 'common.views.common_404'
handler500 = 'common.views.common_500'




######## OLD #################

'''

urlpatterns += patterns('',
    (r'^i18n/', include('django.conf.urls.i18n'))
    )


urlpatterns += patterns('index.views',
    (r'^$', 'index'),   
)
# Image

urlpatterns += patterns('common.gsimage',
    (r'^image/add/$', 'image_add'),   
    (r'^image/upload/$',  'image_upload'),       
    (r'^image/remove/$',  'image_remove'),       
    
    (r'^image/uploaded/(?P<key>[\%\-\a-zA-Z0-9]+)/$', 'image_uploaded'),        
    (r'^image/remove/(?P<key>[\%\-\a-zA-Z0-9]+)/$',  'image_remove'),       
    
)
    
# TOURNAMENT
urlpatterns += patterns('tournament.views',
    (r'^_ah/start/$', 'tournament_index'),
    (r'^_ah/start$', 'tournament_index'),
    (r'^$', 'tournament_index'),
    (r'^tournament/browse/$', 'tournament_browse'),

    (r'^create/step1/$', 'tournament_create_step1'),    
    (r'^create/step2/$', 'tournament_create_step2'),            
    (r'^create/$', 'tournament_create'),
    
    (r'^search/$', 'tournament_search'),    
        
    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/$', 'tournament_item'),
    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/edit/$', 'tournament_edit'),    
    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/teams/$', 'tournament_team_browse'),    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/players/$', 'tournament_player_browse'),        
    
    (r'^tournament/(?P<tournament_id>[\da-f]+)/test/$', 'tournament_test'),
    (r'^tournament/(?P<tournament_id>[\da-f]+)/start/$', 'tournament_start'),
    


    (r'^tournament/(?P<tournament_id>[\da-f]+)/regulations/edit/$', 'regulations_edit'), 
    (r'^tournament/(?P<tournament_id>[\da-f]+)/regulations/$', 'regulations_item'),    
    
    

    (r'^weather/update/$', 'tournament_weather_update'),
    
    (r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/(?P<caption>[\%\-\_\a-zA-Z0-9]+).html$', 'tournament_spam'),
    (r'^search/label/(?P<caption>[\%\-\a-zA-Z0-9]+)$', 'tournament_spam'),
    (r'^search$', 'tournament_spam'),

    
    (r'^feeds/(?P<caption>[\%\-\a-zA-Z0-9]+)/comments/default$', 'tournament_spam'),

    (r'^ie6/$', 'tournament_ie6'),


    (r'^feeds/posts/default$', 'tournament_spam'),
    (r'^feeds/comments/default$', 'tournament_spam'),
    (r'^atom.xml$', 'tournament_spam'),
    #(r'^tournament/$', 'tournament_index'),
    
)

urlpatterns += patterns('common.deferred',
    (r'^service/deferred/$', 'deferred'),
)

urlpatterns += patterns('common.service',
    (r'^sitemap.xml$', 'sitemap'),
    (r'^terms/$', 'terms_of_service'),
    (r'^privacy/$', 'privacy'),        
    (r'^about/$', 'about_us'),
)

urlpatterns += patterns('common.widget',
    (r'^widget/$', 'widget'),
)



urlpatterns += patterns('django.views.generic.simple',       
    #(r'^$', 'redirect_to', {'url': '/tournament/'}),    
    (r'^tournament/$', 'redirect_to', {'url': '/'}),    
)
#http://178.49.10.142:8080/2010/06/sears-and-kmart-launch-streaming-video.html

# LEAGUE
urlpatterns += patterns('league.views',
    (r'^league/browse/$', 'league_browse'),
    (r'^league/create/$', 'league_create'),
    (r'^league/(?P<league_id>[\da-f]+)/remove/team/$', 'league_remove_team'),     
    (r'^league/(?P<league_id>[\da-f]+)/remove/$', 'league_remove'), 
    (r'^league/(?P<league_id>[\da-f]+)/test/$', 'league_test'),

    (r'^league/(?P<league_id>[\da-f]+)/stat/(?P<format>json|html)$', 'league_stat'),


    (r'^league/(?P<league_id>[\da-f]+)/stat/$', 'league_stat'),
    (r'^league/(?P<league_id>[\da-f]+)/print/$', 'league_print'),
    (r'^league/(?P<league_id>[\da-f]+)/$', 'league_item'),
    
    (r'^league/update/$', 'league_update'),        
    (r'^league/stat_update/$', 'league_stat_update'),    
    
    (r'^league/(?P<league_id>[\da-f]+)/playoff/create/$', 'league_playoff_create'),   
    (r'^league/(?P<league_id>[\da-f]+)/playoff/set/$', 'league_playoff_set'),    
            
    (r'^league/$', 'league_index'),   


    (r'^league/(?P<league_id>[\da-f]+)/upload/$', 'league_upload'),
)


# TEAM
urlpatterns += patterns('team.views',
    (r'^team/browse/$', 'team_browse'),
    (r'^team/create/$', 'team_create'),
    (r'^team/(?P<team_id>[\da-f]+)/edit/$', 'team_edit'),    
    (r'^team/(?P<team_id>[\da-f]+)/remove/$', 'team_remove'), 
    (r'^team/(?P<team_id>[\da-f]+)/(?P<format>json|html)$', 'team_item'),        
    (r'^team/(?P<team_id>[\da-f]+)/$', 'team_item'),
    
    (r'^team/$', 'team_index'),
)



# MATCH
urlpatterns += patterns('tournament.views2',
    (r'^api/tournament/(?P<item_id>[\da-f]+)/$', 'tournament'),   
)



# MATCH
urlpatterns += patterns('match.views2',
    (r'^api/match/(?P<item_id>[\da-f]+)/$', 'match'),   
)



# MATCH
urlpatterns += patterns('match.views', 
    (r'^match/browse/$', 'match_browse'),
    (r'^match/create/$', 'match_create'),
    (r'^match/edit/$', 'match_edit'),

    (r'^match/complete/$', 'match_complete'),

    (r'^match/(?P<match_id>[\da-f]+)/remove/$', 'match_remove'),    
    (r'^match/(?P<match_id>[\da-f]+)/edit/$', 'match_edit'),
    (r'^match/(?P<match_id>[\da-f]+)/$', 'match_item'),
    (r'^match/$', 'match_index'),
    (r'^match/(?P<nick>\w+)/settings/$', 'match_settings'),
)



# News
urlpatterns += patterns('news.views',
    (r'^news/(?P<news_id>[\da-f]+)/edit/$', 'news_edit'), 
    (r'^news/(?P<news_id>[\da-f]+)/remove/$', 'news_remove'),    
    (r'^news/(?P<news_id>[\da-f]+)/$', 'news_item'),
    
        
    (r'^tournament/(?P<tournament_id>[\da-f]+)/news/create/$', 'news_create'),
)


# PLAYER
urlpatterns += patterns('player.views',
    (r'^player/browse/', 'player_browse'),
    (r'^team/(?P<team_id>[\da-f]+)/player/create/$', 'player_create'),    
    (r'^player/create/$', 'player_create'),
    (r'^player/(?P<player_id>[\da-f]+)/disable/$', 'player_disable'),
    (r'^player/(?P<player_id>[\da-f]+)/remove/$', 'player_remove'),
    (r'^player/(?P<player_id>[\da-f]+)/edit/$', 'player_edit'),
     
    
    (r'^player/(?P<player_id>[\da-f]+)/$', 'player_item'),
    (r'^player/$', 'player_index'),
    (r'^player/(?P<nick>\w+)/settings/$', 'player_settings'),
)



# REFEREE
urlpatterns += patterns('referee.views',
    (r'^tournament/(?P<tournament_id>[\da-f]+)/referees/$', 'referee_browse'), 
     
    (r'^referee/create/$', 'referee_create'),
    (r'^referee/(?P<referee_id>[\da-f]+)/disable/$', 'referee_disable'),
    (r'^referee/(?P<referee_id>[\da-f]+)/remove/$', 'referee_remove'),
    (r'^referee/(?P<referee_id>[\da-f]+)/edit/$', 'referee_edit'),
  
    
    (r'^referee/(?P<referee_id>[\da-f]+)/$', 'referee_item'),
 
)


      
      

# COMMON
#urlpatterns += patterns('common.views',
#    (r'^error$', 'common_error'),
#    (r'^confirm$', 'common_confirm'),
#    (r'^(?P<path>.*)/$', 'common_noslash'),
#)

# i18n

# XMPP
#urlpatterns += patterns('',
#    (r'^i18n/setlang/', 'django.conf.urls.i18n')
#    )

# register auth urls depending on whether we use google or hybrid auth

'''




