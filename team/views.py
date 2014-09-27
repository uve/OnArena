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
from django.conf import settings
from django.template import loader

from google.appengine.ext import blobstore

from common import api
from common import decorator
from common import util
import logging

from common import models

from django.utils.translation import ugettext_lazy as _

TEAM_HISTORY_PER_PAGE = 20
TEAMS_PER_INDEX_PAGE = 12
TEAMS_PER_PAGE = 24
CONTACTS_PER_PAGE = 24



def team_create(request, format='html'):

    league_id = request.REQUEST.get('league_id', '')    
    league = api.league_get(league_id = league_id) 
    
    group_id = request.REQUEST.get('group_id', '')
     
        
    
    if request.POST and request.is_owner:
        item = api.team_create(request)
        return http.HttpResponseRedirect("/league/" + league_id + "/")
    
    
    all_teams = api.team_browse(tournament_id = request.tournament.id)   
    
    '''    
    owned_leagues = []
    owned_tournaments = request.user.user_tournaments
    for c in owned_tournaments:
        for c2 in c.tournament_leagues:
            owned_leagues.append(c2)
    '''
            
    area = 'team'

    
    #c = template.RequestContext(request, locals())
    #if format == 'html':
    #    t = loader.get_template('team/templates/create.html')
    #    return http.HttpResponse(t.render(c))
    
    if format == 'html':
        return api.response_get(request, locals(), 'team/templates/create.html')     
   

#@admin
def team_edit(request, team_id = None, format='html'):

    team = api.team_get(team_id = team_id)
    if not team:
        return http.HttpResponse()
        
    if not request.is_owner:
        return http.HttpResponseRedirect("/team/" + team_id + "/")         
        
    if request.method == 'POST':
        form = models.TeamForm(request.POST)
        if form.is_valid():             
            item = api.team_edit(form = form, team_id = team_id)
            return http.HttpResponseRedirect("/team/" + team_id + "/")
    else:
        form = models.TeamForm(team) # An unbound form
          


    area = 'team'
        
    if format == 'html':
        return api.response_get(request, locals(), 'team/templates/edit.html')    



def team_item(request, team_id = None, format='html'):
    
    area = 'team'
    load_async = 'team_item'        
   
  
    if format == 'html':
        team = api.team_get(team_id = team_id, is_reload=True)
 
        if not team:
            raise Http404    

     
        all_players = api.team_get_players(team_id = team_id, stat = True)
        #all_matches = api.match_browse(team_id = team_id)        
   
        return api.response_get(request, locals(), 'team/templates/item.html')         
        
    if format == 'json':
        jsoncallback = request.REQUEST.get("jsoncallback")
        limit = request.REQUEST.get("limit")
        logging.info("CALLBACK: %s", jsoncallback)
        
        all_players = api.team_get_players(team_id = team_id)    
        c = template.RequestContext(request, locals())    
        t = loader.get_template('team/templates/item.json')
        return util.HttpJsonResponse(t.render(c), request)

def team_browse(request, format='html'):


  actors = api.models.Team.all().fetch(100)
  ourpicks_teams = actors
  owned_nicks  = actors

  area = 'team'
  c = template.RequestContext(request, locals())

  # TODO(tyler): Other output formats.
  if format == 'html':
    t = loader.get_template('team/templates/browse.html')
    return http.HttpResponse(t.render(c))



def team_members(request, nick=None, format='html'):
  nick = clean.team(nick)

  view = api.actor_lookup_nick(request.user, nick)

  if not view:
    raise exception.UserDoesNotExistError(nick, request.user)

  handled = common_views.handle_view_action(
      request,
      { 'actor_add_contact': request.path,
        'actor_remove_contact': request.path, })
  if handled:
    return handled

  per_page = CONTACTS_PER_PAGE
  offset, prev = util.page_offset_nick(request)

  follower_nicks = api.team_get_members(request.user,
                                           view.nick,
                                           limit=(per_page + 1),
                                           offset=offset)
  actor_nicks = follower_nicks
  actors = api.actor_get_actors(request.user, actor_nicks)
  # clear deleted actors
  actors = dict([(k, v) for k, v in actors.iteritems() if v])
  per_page = per_page - (len(follower_nicks) - len(actors))

  whose = "%s's" % view.display_nick()

  # here comes lots of munging data into shape
  actor_tiles = [actors[x] for x in follower_nicks if x in actors]

  actor_tiles_count = view.extra.get('member_count', 0)
  actor_tiles, actor_tiles_more = util.page_actors(request,
                                                   actor_tiles,
                                                   per_page)

  area = 'teams'

  c = template.RequestContext(request, locals())

  # TODO: Other output formats.
  if format == 'html':
    t = loader.get_template('team/templates/members.html')
    return http.HttpResponse(t.render(c))



def team_photo_upload(request, team_id = None, format='html'):
    

    if request.method == "POST" and request.is_owner:           
    
        logging.info("request: %s",request)   

        return 
        img_load = request.FILES.get('file')
        if img_load:
            img = request.FILES['file'].read()
            item = api.image_set("team", team_id, img)
            logging.info("Small:\t %s", item)
  
                 
            return http.HttpResponse('{"name":"%s","type":"image/jpeg","size":"123456789"}' % item) 
        else:
            logging.error("No photo uploaded")
    
    return http.HttpResponse('{"name":"","type":"image/jpeg","size":"123456789"}')       
    

def team_photo_remove(request, team_id, format='html'):
    if request.POST and request.is_owner:              
        team = api.team_photo_remove(team_id)
    
    return http.HttpResponseRedirect("/team/" + str(team_id) + "/")    



def team_remove(request, team_id=None, format='html'):

    area = 'team'
    
    if request.is_owner:
        team = api.team_remove(team_id = league_id)
    return http.HttpResponse()

