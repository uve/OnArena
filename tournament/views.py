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
from django.template import loader

from common import fix_path

from common import api

#import api as api2

from common import decorator
from common import user
from common import util

from common import models

from common import gsimage


import logging
import settings
from google.appengine.ext import db

from google.appengine.api import taskqueue

from common import deferred

import datetime



TOURNAMENT_HISTORY_PER_PAGE = 20
TOURNAMENTS_PER_INDEX_PAGE = 12
TOURNAMENTS_PER_PAGE = 24
CONTACTS_PER_PAGE = 24



def tournament_create(request, format='html'):  
        
        
    if request.method == 'POST':
        form = models.TournamentFormCreate(request.POST)
        if form.is_valid():             
            item = api.tournament_create(request = request, form = form)
            if item:
               return http.HttpResponseRedirect("/tournament/" + str(item) + "/")
            logging.info("Form is invalid")         
        else:
            logging.info("Form is invalid")            
    
    #form = models.TournamentForm() # An unbound form
    all_sports = api.sport_browse(limit = 1000)
    
    #logging.info("hes: %s", all_sports)
    
    try:
        lat, lon = request.META["HTTP_X_APPENGINE_CITYLATLONG"].split(",")
    except:
        lat, lon = ("", "")
    
    logging.info("lat: %s", lat)
    logging.info("lon: %s", lon)
    

    area = 'create'    
    is_map = True    
    
    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/create.html') 
            
            
def tournament_create_step1(request, format='html'):  

    return api.response_get(request, locals(), 'tournament/templates/create_step1.html') 
        
    if request.method == 'POST':
        form = models.TournamentFormStep1(request.POST)
        
        sport_id = request.POST.get("sport","")            
        sport = models.Sport.get_item(sport_id)
        
        if form.is_valid() and sport:             
            return api.response_get(request, locals(), 'tournament/templates/create_step1.html') 
        else:
            logging.info("Form is invalid")            
    
    return http.HttpResponseRedirect("/")
        
        
def tournament_create_step2(request, format='html'):  
        
    if request.method == 'POST':
        form = models.TournamentForm(request.POST)
        if form.is_valid():             
            item = api.tournament_create(request = request, form = form)
            return http.HttpResponseRedirect("/tournament/" + str(item) + "/")
        else:
            logging.info("Form is invalid")            
    
    form = models.TournamentForm() # An unbound form
    all_sports = api.sport_browse(limit = 1000)
    
    logging.info("hes: %s", all_sports)

    area = 'tournament'    
    
    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/create.html')                                         
        



def tournament_edit(request, tournament_id = None, format='html'):

    tournament = api.tournament_get(tournament_id = tournament_id)
    if not tournament:
        return http.HttpResponse()
        
    if not request.is_owner:
        return http.HttpResponseRedirect("/tournament/" + tournament_id + "/")         
        
    if request.method == 'POST':
        form = models.TournamentFormEdit(request.POST)
        if form.is_valid():             
            item = api.tournament_edit(form = form, tournament_id = tournament_id)
            return http.HttpResponseRedirect("/tournament/" + tournament_id + "/")
    else:
        form = models.TournamentFormEdit(tournament) # An unbound form

    area = 'team'
        
    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/edit.html')          


def tournament_index(request, format='html'):

    #all_tournaments = api.tournament_browse(sport_id = "1001")
    
    #all_tournaments = api.tournament_browse(limit=1000)
    
    #logging.info("request.META: %s",request.META)
    
    #form = models.TournamentForm() # An unbound form
    #all_sports = api.sport_browse(limit = 1000)
    
    #defers = {  "all_tournaments": deferred.group(api.tournament_browse,  sport_id = "1001")  }
    
    defers = {  "all_tournaments": deferred.group(api.tournament_browse,  limit = 1000)  }    
    
    #defers = {}

    
    main_page = True
    
    is_map = True

    area = 'index'    
    
    if format == 'html':
        return api.response_get(request, locals(), 'common/templates/index.html', defers = defers) 



def tournament_item(request, tournament_id = None, format='html'):

    #tournament = api.tournament_get(tournament_id)
    #all_leagues = api.league_browse(tournament_id = tournament_id)   
    
    tournament = api.tournament_get(tournament_id = tournament_id)
    
    defers = {  #"tournament": deferred.group(api.tournament_get, tournament_id = tournament_id),
                #"all_leagues": deferred.group(api.league_browse,  tournament_id = tournament_id)  
                }
    
    area = 'tournament'    
    
    is_map = True
        
    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/item.html', defers = defers) 


def tournament_ie6(request, format='html'):

    return api.response_get(request, locals(), 'common/templates/ie6.html') 



def tournament_browse(request, format='html'):
    
    all_tournaments = api.tournament_get_tournaments()
    
    area = 'tournament'
    c = template.RequestContext(request, locals())

    main_page = True

    # TODO(tyler): Other output formats.
    if format == 'html':
        t = loader.get_template('tournament/templates/browse.html')
        return http.HttpResponse(t.render(c))
        


def tournament_photo_upload(request, team_id = None, player_id = None, news_id = None, referee_id = None, match_id = None, format='html'):    

    item = request.POST.get("item", "")
    #logging.info("item: %s",item)
    item_id = request.POST.get("item_id", "")
    #logging.info("item_id: %s",item_id)    
    
    
    logging.info("Image uploading..  \t item: %s \t item_id: %s", item, item_id)    
    

    if request.method == "POST" and request.is_owner and item and item_id:# and request.is_owner:              
        
        #logging.info("POST upload: %s", request.FILES)        
        
        
        key = gsimage.image_upload(request = request, item = item, item_id = item_id)
        
        return http.HttpResponseRedirect("/uploaded/%s" % key)        
        
        
        return http.HttpResponse(status=301)
        
        return util.HttpJsonResponse(results, request)
        
        return http.HttpResponse('{"name":"picture1.jpg","size":902604,"url":"\/\/example.org\/files\/picture1.jpg","thumbnail_url":"\/\/example.org\/thumbnails\/picture1.jpg","delete_url":"\/\/example.org\/upload-handler?file=picture1.jpg","delete_type":"DELETE"}')         
        
        #logging.info("request: %s",request)
        
        blob_info_list = get_uploads(request)
        blob_info = blob_info_list[0]
        
        
        
        logging.info("Name: %s",blob_info.filename)
        logging.info("Size: %s",blob_info.size)        
        
        
        return http.HttpResponse('{"name":"picture1.jpg","size":902604,"url":"\/\/example.org\/files\/picture1.jpg","thumbnail_url":"\/\/example.org\/thumbnails\/picture1.jpg","delete_url":"\/\/example.org\/upload-handler?file=picture1.jpg","delete_type":"DELETE"},{"name":"picture2.jpg","size":841946,"url":"\/\/example.org\/files\/picture2.jpg","thumbnail_url":"\/\/example.org\/thumbnails\/picture2.jpg","delete_url":"\/\/example.org\/upload-handler?file=picture2.jpg","delete_type":"DELETE"}') 
      
        
        return
        
        img_load = request.FILES.get('files[]')
        if img_load:
            file_name = request.FILES['files[]'].name
            img = request.FILES['files[]'].read()
            results = api.image_set(path = item, id = item_id, content = img, file_name = file_name)
                
            return util.HttpJsonResponse(results, request)
        else:
            logging.error("No photo uploaded")
            
    logging.error("No Right for photo uploaded")            
            
    return http.HttpResponse('[]')
   
    
def tournament_team_browse(request, tournament_id = None, format='html'):
    

    tournament = api.tournament_get(tournament_id = tournament_id)
    all_teams = api.team_browse_rating(tournament_id = tournament_id)   
    
    area = 'tournament'    
    
    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/team_browse.html')         



def tournament_test(request,tournament_id=None, format='html'):

    #api.test()#:api.rating_update(tournament_id = "1001")
    
    #return http.HttpResponse(status = 200)    
    
    all_results = api.test()
    return api.response_get(request, locals(), 'tournament/templates/test.html') 
    
    if api.test():
        status_code = 200
    else:
        status_code = 301

    logging.info("Status Code: %s", status_code)        

    return http.HttpResponse(status = status_code)

def tournament_search(request, format='json'):

    lat = request.POST.get("lat","")
    lon = request.POST.get("lon","") 
    
    results = api.tournament_browse(lat = lat, lon = lon)
    
    #logging.info("results: %s",results)
    
    
    return util.HttpJsonResponse(str(results), request)

    


def tournament_start(request,tournament_id=None, format='html'):


    taskqueue.add(url='/tournament/1001/test/', method = 'GET')    

    return http.HttpResponse()



def tournament_spam(request, year=None, month=None, caption=None, format='html'):
    
    return http.HttpResponse('Spam')
    area = 'tournament'
    
    #c = template.RequestContext(request, locals())
    c = template.RequestContext(request, None)

    if format == 'html':
        t = loader.get_template('common/templates/spam.html')
        return http.HttpResponse(t.render(c))



def tournament_weather_update(request, format='html'):   
 
  actors = api.weather_update()

  area = 'weather'

  if format == 'html':
    return http.HttpResponse()
    
    
def regulations_edit(request, tournament_id=None, format='html'):

    if not request.is_owner:
        return http.HttpResponseRedirect("/tournament/" + tournament_id + "/")     
               
    regulations = api.regulations_get(tournament_id = tournament_id)
    
    if request.POST and request.is_owner:
        content = request.POST.get("content", "")
        logging.info("content: %s",content)
        item = api.regulations_edit(content = content, tournament_id = tournament_id)
            
        return http.HttpResponseRedirect("/tournament/" + tournament_id + "/regulations/")
        

    area = 'regulations'
        
    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/regulations_edit.html')     
        
      
           

def regulations_item(request, tournament_id=None, format='html'):

    regulations = api.regulations_get(tournament_id = tournament_id)
    
    if regulations is None and request.is_owner:
        return http.HttpResponseRedirect("/tournament/" + tournament_id + "/regulations/edit/")        

    if format == 'html':
        return api.response_get(request, locals(), 'tournament/templates/regulations_item.html') 


