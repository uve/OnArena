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
from django import template
from django.conf import settings
from django.template import loader

from common import api
from common import decorator
from common import models

import logging

MATCH_HISTORY_PER_PAGE = 20
PLAYERS_PER_INDEX_PAGE = 12
PLAYERS_PER_PAGE = 24
CONTACTS_PER_PAGE = 24



def player_create(request, team_id = None, format='html'):

    load_async = 'player_create'   
    
    if not team_id:
        team_id = request.REQUEST.get('team_id', '')
        
        
    if not team_id:
        return http.HttpResponse()       
    #team = api.team_get(team_id = team_id)     
    #tournament_id = team["tournament_id"]["id"]
    #sport_id = team["tournament_id"]["sport_id"]["id"]

    
    return_url = request.REQUEST.get('return_url', '')
    
    if request.method == "POST" and request.is_owner:   
        item = api.player_create(request = request)
        
        if return_url:
            return http.HttpResponseRedirect(return_url)
            
        return http.HttpResponseRedirect("/team/" + team_id + "/")


    team = models.Team.get_item(team_id)
    if not team:
        return None   
   
    tournament    = team.tournament_id
    tournament_id = team.tournament_id.id        
    sport_id      = team.tournament_id.sport_id.id

    all_positions = api.positions_browse(sport_id = sport_id)
    all_teams = api.team_browse(tournament_id = tournament_id)
    
    area = 'player'
    
    if format == 'html':
        return api.response_get(request, locals(), 'player/templates/create.html')     



def player_disable(request, player_id = None, format='html'):

    area = 'player'

    team_id    = request.REQUEST.get('team_id', '')
    player_id  = request.REQUEST.get('player_id', '')
    

                
    is_checked = request.REQUEST.get('is_checked', '')
    
    logging.info("is_checked: %s",is_checked)    
        
    if is_checked == "true":
        is_checked = True
    else:
        is_checked = False    
    
    if request.POST and request.is_owner:
        player = api.player_disable(team_id = team_id, player_id = player_id, is_checked = is_checked)

    return http.HttpResponse()



def player_edit(request,player_id=None,  format='html'):


    team_id = request.REQUEST.get('team_id', '')
    if team_id:
        team = api.team_get(team_id = team_id)
        player = api.player_get(player_id = player_id, team_id = team_id)
    else:
        player = api.player_get(player_id = player_id)
        team_id = None
                
                        
    if not player:
        return http.HttpResponse()
      
    logging.info("player: %s", player)    
    #logging.info("player: %s", player["tournament_id"]["sport_id"]["id"])


    if not request.is_owner:
        return http.HttpResponseRedirect("/player/" + player_id + "/")        


    all_positions = api.positions_browse(sport_id = player["tournament_id"]["sport_id"]["id"])    
    
    if request.POST and request.is_owner:
        item = api.player_edit(request = request, player_id = player_id)
            
        return http.HttpResponseRedirect("/player/" + player_id + "/")


    area = 'player'
    
    if format == 'html':
        return api.response_get(request, locals(), 'player/templates/edit.html')     



def player_item(request, player_id = None, format='html'):

    player = api.player_get(player_id = player_id)
    
    team_id = request.REQUEST.get('team_id', '')
    
    if not player:
        return http.HttpResponse()
            
    player_stat = api.player_stat_get(player_id = player_id)
    
    area = 'player'

    if format == 'html':
        return api.response_get(request, locals(), 'player/templates/item.html') 



def player_remove(request, player_id=None, format='html'):

    area = 'player'
    team_id = request.REQUEST.get('team_id', '')
    
    if request.POST and request.is_owner:
        player = api.player_remove(player_id = player_id)
        if team_id:
            return http.HttpResponseRedirect("/team/" + team_id + "/")

    return http.HttpResponse()
    
    

def player_photo_upload(request, player_id, format='html'):
    

    if request.method == "POST" and request.is_owner:              

        img_load = request.FILES.get('file')
        if img_load:
            img = request.FILES['file'].read()
            item = api.image_set("player", player_id, img)
            logging.info("Small:\t %s", item)
  
                 
            return http.HttpResponse('{"name":"%s","type":"image/jpeg","size":"123456789"}' % item) 
        else:
            logging.error("No photo uploaded")
    
    return http.HttpResponse('{"name":"","type":"image/jpeg","size":"123456789"}')       
    

def player_photo_remove(request, player_id, format='html'):
    if request.POST and request.is_owner:              
        player = api.player_photo_remove(player_id = player_id)
    
    return http.HttpResponseRedirect("/player/" + str(player_id) + "/")        
 
