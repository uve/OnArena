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
REFEREES_PER_INDEX_PAGE = 12
REFEREES_PER_PAGE = 24
CONTACTS_PER_PAGE = 24


def referee_browse(request, tournament_id = None, format='html'):

    logging.info("Tournament: %s", tournament_id)

    tournament = api.tournament_get(tournament_id = tournament_id)

    all_referees = api.referees_browse(tournament_id = tournament_id, stat = True)
    
    area = 'referee'
    
    if format == 'html':
        return api.response_get(request, locals(), 'referee/templates/browse.html')   


def referee_create(request, format='html'):

    tournament_id = request.REQUEST.get('tournament_id', '')
    tournament = api.tournament_get(tournament_id = tournament_id)

    if request.POST and request.is_owner:
        item = api.referee_create(request = request)
        #return http.HttpResponseRedirect("/referee/" + str(item) + "/")
        #item = request.POST["team_id"]
            
        return http.HttpResponseRedirect("/tournament/" + tournament_id + "/referees/")
    
    area = 'referee'
    
    if format == 'html':
        return api.response_get(request, locals(), 'referee/templates/create.html')     



def referee_disable(request, referee_id = None, format='html'):

    area = 'referee'

    team_id    = request.REQUEST.get('team_id', '')
    referee_id  = request.REQUEST.get('referee_id', '')
    is_checked = request.REQUEST.get('is_checked', '')
    
    if request.POST and request.is_owner:
        referee = api.referee_disable(team_id = team_id, referee_id = referee_id, is_checked = is_checked)

    return http.HttpResponse()



def referee_edit(request,referee_id = None,  format='html'):



    referee = api.referee_get(referee_id = referee_id)
    if not referee:
        return http.HttpResponse()


    if not request.is_owner:
        return http.HttpResponseRedirect("/referee/" + referee_id + "/")        
        
    if request.POST and request.is_owner:
        item = api.referee_edit(request = request, referee_id = referee_id)
            
        return http.HttpResponseRedirect("/referee/" + referee_id + "/")

    area = 'referee'
    
    if format == 'html':
        return api.response_get(request, locals(), 'referee/templates/edit.html')     


def referee_item(request,referee_id = None, format='html'):

    referee = api.referee_get(referee_id = referee_id, is_reload = True)
   
    if not referee:
        return http.HttpResponse()
    
    
    area = 'referee'
    load_async = "referee_item"
    

    if format == 'html':
        return api.response_get(request, locals(), 'referee/templates/item.html') 


def referee_remove(request, referee_id=None, format='html'):

    area = 'referee'
    team_id = request.REQUEST.get('team_id', '')
    
    if request.POST and request.is_owner:
        referee = api.referee_remove(referee_id = referee_id)
        if team_id:
            return http.HttpResponseRedirect("/team/" + team_id + "/")

    return http.HttpResponse()
    
    

def referee_photo_upload(request, referee_id, format='html'):
    

    if request.method == "POST" and request.is_owner:              

        img_load = request.FILES.get('file')
        if img_load:
            img = request.FILES['file'].read()
            item = api.image_set("referee", referee_id, img)
            logging.info("Small:\t %s", item)
  
                 
            return http.HttpResponse('{"name":"%s","type":"image/jpeg","size":"123456789"}' % item) 
        else:
            logging.error("No photo uploaded")
    
    return http.HttpResponse('{"name":"","type":"image/jpeg","size":"123456789"}')       
    

def referee_photo_remove(request, referee_id, format='html'):
    if request.POST and request.is_owner:              
        referee = api.referee_photo_remove(referee_id = referee_id)
    
    return http.HttpResponseRedirect("/referee/" + str(referee_id) + "/")        
 
