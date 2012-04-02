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

from django import http
from django.http import Http404

from django import template
#from django.conf import settings
from django.template import loader

from common import api
from common import decorator

from common import deferred


import datetime

import settings
import logging
from google.appengine.api import taskqueue

MATCH_HISTORY_PER_PAGE = 20
MATCHES_PER_INDEX_PAGE = 12
MATCHES_PER_PAGE = 24
CONTACTS_PER_PAGE = 24


#
def match_create(request, format='html'):

    if request.POST and request.is_owner:
        item = api.match_create(request)

        item = request.POST["league_id"]
        
        
        
        return http.HttpResponseRedirect("/league/" + str(item) + "/")
        
    league_id = request.REQUEST.get('league_id', '')
    playoffnode_id = request.REQUEST.get('playoffnode_id', '')    
    group_id = request.REQUEST.get('group_id', '')    
       
    league = api.league_get(league_id = league_id)
    
    tournament = league.tournament_id    
    tournament_id = tournament.id

   
    all_teams = api.team_browse(league_id = league_id)#, is_reload = True)
    #all_teams = api.team_browse(tournament_id = tournament_id)#, is_reload = True)
    
    if playoffnode_id:
        playoff_teams = api.playoff_get_nodeteams(playoffnode_id = playoffnode_id)
        all_teams = api.team_browse(tournament_id = tournament_id)#, is_reload = True)    
    
    all_referees = api.referees_browse(tournament_id = tournament_id)

    # FIXME:   new create

        
    area = 'match'
    c = template.RequestContext(request, locals())

    #if format == 'html':
    #    t = loader.get_template('match/templates/create.html')
    #    return http.HttpResponse(t.render(c))
    if format == 'html':
        return api.response_get(request, locals(), 'match/templates/create.html') 



def match_complete(request, format='html'):
   
    if request.method == "POST":
        #logging.info("POST: \t %s", request)
        
        #item = api.match_edit(post_data = request.POST)
        
        deferred.defer(api.match_edit, post_data = request.POST)
        


    return http.HttpResponse(status = 200)


 
def match_item(request, match_id = None, format='html'):    

    match = api.match_get(match_id = match_id)
    
    if not match:
        raise Http404

    team0 = api.team_get(team_id = match["teams"][0]["id"])    
    team1 = api.team_get(team_id = match["teams"][1]["id"])    
    
    
    league    = match["league_id"]
    league_id = league["id"]
    
    tournament    = match["tournament_id"]
    tournament_id = tournament["id"]    

                
    area = 'match'    
    
    
    if not request.is_owner:  
        return api.response_get(request, locals(), 'match/templates/item.html')
    

    if request.method == "POST" and request.is_owner:        


        #for i,v in request.POST.items():
        #    logging.info("i: %s", i)    
        #    logging.info("v: %s", v) 

        s = request._raw_post_data
        taskqueue.add(url='/match/complete/', method = 'POST', params={ 'post_data': s })        
        return http.HttpResponseRedirect("/league/" + str(league_id) + "/")

     
    if request.method == "GET" and request.is_owner:
           
        is_edit_match = True        
  
        #all_teams = api.team_browse(league_id = league_id)
        all_teams = api.team_browse(tournament_id = tournament_id)     
        
             
        all_referees = api.referees_browse(tournament_id = tournament_id)    
        
        team0_players_active = api.team_get_players_active(team_id = match["teams"][0]["id"])    
        team1_players_active = api.team_get_players_active(team_id = match["teams"][1]["id"]) 
        
        for match_item in match["teams"][0]["players"]:   
            for item in team0_players_active:
                if item["id"] == match_item["id"]:
                    team0_players_active.remove(item)                 
                    
        for match_item in match["teams"][1]["players"]:   
            for item in team1_players_active:
                if item["id"] == match_item["id"]:
                    team1_players_active.remove(item)            

        # %Y-%m-%d %H:%M:%S
        # data = str(datetime.datetime.now())
        logging.info("Data: %s", match["datetime"])                 

        if format == 'html':
            return api.response_get(request, locals(), 'match/templates/edit.html')


def match_print(request, match_id = None, format='html'):  
   
    match = api.match_get(match_id = match_id)
    
    if not match:
        raise Http404

    team0 = api.team_get(team_id = match["teams"][0]["id"])    
    team1 = api.team_get(team_id = match["teams"][1]["id"])    
    
    
    league    = match["league_id"]
    league_id = league["id"]
    
    tournament    = match["tournament_id"]
    tournament_id = tournament["id"]    


    team0_players_active = api.team_get_players_active(team_id = match["teams"][0]["id"])    
    team1_players_active = api.team_get_players_active(team_id = match["teams"][1]["id"]) 


    #all_groups = api.group_browse(league_id = league_id)
 

    area = 'match'
    c = template.RequestContext(request, locals())

    # TODO(tyler): Other output formats.
    if format == 'html':
        t = loader.get_template('match/templates/print.html')
        return http.HttpResponse(t.render(c))


def match_remove(request, match_id=None, format='html'):

    area = 'match'
    
    if request.POST and request.is_owner:
        match = api.match_remove(match_id = match_id)
    else:
        logging.error("Match Remove NO Rights")

    return http.HttpResponse()
