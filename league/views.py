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
from common import util

from common import deferred

from google.appengine.ext import db

import logging


LEAGUE_HISTORY_PER_PAGE = 20
LEAGUES_PER_INDEX_PAGE = 12
LEAGUES_PER_PAGE = 24
CONTACTS_PER_PAGE = 24



def league_create(request, format='html'):

    if request.POST and request.is_owner:
        item = api.league_create(request)
        return http.HttpResponseRedirect("/league/" + str(item) + "/")
        
    owned_tournaments = request.user.user_tournaments

    area = 'league'
    c = template.RequestContext(request, locals())

    #if format == 'html':
    #    t = loader.get_template('league/templates/create.html')
    #    return http.HttpResponse(t.render(c))
    
     
    if format == 'html':
        return api.response_get(request, locals(), 'league/templates/create.html') 


def league_index(request, format='html'):

    if not request.user:
        return league_index_signedout(request, format='html')

    owned_leagues = api.actor_get_leagues_admin(
        request.user,
        request.user.nick,
        limit=(LEAGUES_PER_INDEX_PAGE + 1))

    for c in owned_leagues:
        c.i_am_admin = True

    all_leagues = api.actor_get_leagues(
        request.user,
        request.user.nick,
        limit=(LEAGUES_PER_INDEX_PAGE + 1))

    creator_ref = db.GqlQuery("SELECT __key__ FROM Actor WHERE nick = :1", request.user.nick).get()

    for c in all_leagues:
        if c.actor == creator_ref:
            c.i_am_admin = True

 
    area = 'league'
    c = template.RequestContext(request, locals())

    if format == 'html':
        t = loader.get_template('league/templates/index.html')
        return http.HttpResponse(t.render(c))




def league_item(request, league_id = None, format='html'):

    area = 'league'
    load_async = 'league_item'  
    
    league = models.League.get_item(league_id)
    if not league:
        return http.HttpResponse()    
    
    
    defers = {  "league":       deferred.group(api.stat_league,    league_id = league_id),
                "all_goals":    deferred.group(api.statistics,     league_id = league_id),
                
                
                #"all_teams":    deferred.group(api.team_browse,    league_id = league_id),
                
                #"all_matches":  deferred.group(api.match_browse,   league_id = league_id),
                #"all_playoffs": deferred.group(api.playoff_browse, league_id = league_id), 
                }   
                
    '''    
    if request.REQUEST.get("is_reload"):
        all_groups = api.group_browse(league_id = league_id, is_reload = True)   
    else:
        defers["all_groups"] = deferred.group(api.group_browse,   league_id = league_id)
    '''                            
                
    #if request.is_owner:
    #    defers["all_playoff_teams"] = deferred.group(api.team_browse, tournament_id = request.tournament_id)
                        
                             
        
    #logging.info("request: %s",request)
    
    items = {'area': area, 'load_async': load_async, 'league': league, 'league_id': league_id}

    if format == 'html':
        return api.response_get(request, items, 'league/templates/item.html', defers = defers) 



def league_stat(request,league_id=None, format='html'):


    league = api.league_get(league_id)
    if not league:
        return http.HttpResponse()   
            
    tournament = league.tournament_id
  

    logging.info("format:   %s", format)

    area = 'league'
     
    if format == 'html':
        all_goals = api.statistics(league_id = league_id, limit = 1000)
        return api.response_get(request, locals(), 'league/templates/stat.html') 

    league = api.stat_league(league_id = league_id)

    jsoncallback = request.REQUEST.get("jsoncallback")

    limit = request.REQUEST.get("limit")

    logging.info("%s", jsoncallback)

    all_goals = api.statistics(league_id = league_id, limit = limit)
    c = template.RequestContext(request, locals())

    if format == 'json':
  
        t = loader.get_template('league/templates/stat.json')
        return util.HttpJsonResponse(t.render(c), request)

def league_browse(request, format='html'):

  actors = api.models.League.all().fetch(100)
  ourpicks_leagues = actors
  owned_nicks  = actors

  area = 'league'
  c = template.RequestContext(request, locals())

  # TODO(tyler): Other output formats.
  if format == 'html':
    t = loader.get_template('league/templates/browse.html')
    return http.HttpResponse(t.render(c))





def league_playoff_create(request, league_id = None, format='html'):

    if request.POST and request.is_owner:
        name = request.POST.get("name") 
        size = int(request.POST.get("size"))    
             
        logging.info("request.POST: %s",request.POST)
        
        is_third_place = request.POST.get("third_place","")
        if is_third_place == "true":
            third_place = True
        else:
            third_place = False
                               

        #item = api.playoff_create(league_id = league_id, name = name, size = size)  
        
        deferred.defer( api.playoff_create, league_id = league_id, name = name, size = size, third_place = third_place)      
        
    return http.HttpResponseRedirect("/league/" + str(league_id) + "/")



def league_playoff_set(request, league_id = None, format='html'):
    
    if request.method == "POST" and request.is_owner:
        #item = api.playoff_set(league_id = league_id, request = request)  

        team_id       = request.POST["team_id"]
        competitor_id = request.POST["competitor_id"]                   
        
        api.playoff_set( league_id = league_id, team_id = team_id, competitor_id = competitor_id )    
        
    return http.HttpResponse()


def league_print(request, league_id = None, format='html'):  
   
    league = api.league_get(league_id)
    tournament = league.tournament_id
    tournament_id = tournament.id    


    all_groups = api.group_browse(league_id = league_id)
    #all_teams = api.league_table(league_id = league_id)
    all_goals = api.statistics(league_id = league_id, limit = 1000)

    last_matches = api.match_browse(tournament_id = tournament_id, league_id = league_id) 

    area = 'league'
    c = template.RequestContext(request, locals())

    # TODO(tyler): Other output formats.
    if format == 'html':
        t = loader.get_template('league/templates/print.html')
        return http.HttpResponse(t.render(c))


def league_stat_update(request, format='html'):

    if request.method == "POST":    
        league_id = request.POST["league_id"]
        team_id   = request.POST["team_id"]
        api.stat_update(league_id, team_id)
        return http.HttpResponse()
    
    

def league_update(request, format='html'):

    if request.method == "POST":    
        league_id = request.POST["league_id"]
        result = api.league_update(league_id = league_id)
        return http.HttpResponse()    



def league_test(request,league_id=None, format='html'):
  
 
  actors = api.test2(league_id)
 

  area = 'league'
  #c = template.RequestContext(request, locals())

  # TODO(tyler): Other output formats.
  if format == 'html':
    return http.HttpResponse()


def league_upload(request,league_id=None, format='html'):   
        
    league = models.League.get_item(league_id)
    tournament = league.tournament_id


    if request.POST:
        actors = api.league_upload(request, league)
        #return http.HttpResponseRedirect("/league/" + str(league_id) + "/")


    area = 'league'
    c = template.RequestContext(request, locals())
    # TODO(tyler): Other output formats.
    if format == 'html':
        t = loader.get_template('league/templates/upload.html')
        return http.HttpResponse(t.render(c))


def league_remove(request, league_id=None, format='html'):

    area = 'league'
    
    team_id   = request.REQUEST.get_item('team_id','')
    league_id = request.REQUEST.get_item('league_id','')
    group_id  = request.REQUEST.get_item('group_id','')  
    
    logging.info("team_id: %s",team_id)
    logging.info("league_id: %s",league_id)
    logging.info("group_id : %s",group_id )
    
    #if request.is_owner:
    #    team = api.league_remove(league_id)
    return http.HttpResponse()
    

def league_remove_team(request, league_id=None, format='html'):

    area = 'league'

    team_id   = request.POST.get('team_id') or None
    league_id = request.POST.get('league_id','') or None
    group_id  = request.POST.get('group_id') or None
    
    logging.info("team_id: %s",team_id)
    logging.info("league_id: %s",league_id)
    logging.info("group_id : %s",group_id )    
    
    if request.method == "POST" and request.is_owner:
        result = api.league_remove_team(league_id = league_id, group_id = group_id, team_id = team_id)
        
    return http.HttpResponse(status=200)    

