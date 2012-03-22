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
from django.http import Http404

from common import api
from common import decorator
from common import util

from common import models


import logging
import json


from core.news import News 

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

    news = api.news_get(news_id = news_id)
    if not news:
        return http.HttpResponse()


    if not request.is_owner:
        return http.HttpResponseRedirect("/news/" + news_id + "/")        
   

    if request.POST and request.is_owner:
        item = api.news_edit(request = request, news_id = news_id)
            
        return http.HttpResponseRedirect("/news/" + news_id + "/")

    area = 'news'
    
    if format == 'html':
        return api.response_get(request, locals(), 'news/templates/edit.html')  

def app_news_item(request, news_id = None, format='html'):
    
    
    return News(request, news_id)
    
    if request.method == "GET":
        logging.info("READ - GET")     
        
        #news = api.news_get(news_id = news_id, is_reload = True)
                 
        key_name = "news_get_news_id_" + news_id 
        
        result = models.StaticContent.get_by_key_name(key_name) 
        if not result:       
            raise Http404
        
                
        return util.HttpJsonResponse(result.content, request)
    
    if request.method == "POST":
        logging.info("CREATE - POST")   
        key_name = "news_get_news_id_1002" 
        
        result = api.news_create_app(request.raw_post_data)
        
        return util.HttpJsonResponse(result, request) 
        #return http.HttpResponse("")   

    if request.method == "PUT":
        logging.info("UPDATE - PUT")    
        logging.info("request: %s", request.raw_post_data)   
        pass   
      
    if request.method == "DELETE":
        logging.info("DELETE - DELETE")                
        pass
            

    return http.HttpResponse("")
            

                   
        
        

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
      
