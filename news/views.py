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
from common import util

import logging



MATCH_HISTORY_PER_PAGE = 20
PLAYERS_PER_INDEX_PAGE = 12
PLAYERS_PER_PAGE = 24
CONTACTS_PER_PAGE = 24



def news_create(request, tournament_id = None, format='html'):  
        
    if request.is_owner:    
        if request.POST:
            item = api.news_create(request)
            return http.HttpResponseRedirect("/news/" + str(item) + "/")
    
        else:
            tournament = request.tournament

            area = 'news'

            if format == 'html':
                return api.response_get(request, locals(), 'news/templates/create.html')                 
                
                
    else:
        logging.critical("No Access!!!")
        return http.HttpResponse()                    



def news_edit(request, news_id = None,  format='html'):

    if not request.is_owner:
        return http.HttpResponseRedirect("/news/" + news_id + "/")        
   

    if request.POST and request.is_owner:

        name    = request.POST.get("name")
        content = request.POST.get("content")   
        
        item = api.news_edit(news_id = news_id, name = name, content = content)
            
        return http.HttpResponseRedirect("/news/" + news_id + "/")


    news = api.news_get(news_id = news_id)
    if not news:
        return http.HttpResponse()

    area = 'news'
    
    if format == 'html':
        return api.response_get(request, locals(), 'news/templates/edit.html')  
                      

def news_item(request, news_id = None, format='html'):
    
    area = 'news'    
        
    news = api.news_get(news_id = news_id)

    if format == 'html':
        return api.response_get(request, locals(), 'news/templates/item.html') 
        
        
def news_remove(request, news_id = None, format='html'):

    area = 'news'
    news = api.news_get(news_id = news_id)
    tournament_id = news["tournament_id"]["id"]
    
    if request.POST and request.is_owner:
        api.news_remove(news_id = news_id)
        
    return http.HttpResponseRedirect("/tournament/"+ tournament_id + "/")
      
