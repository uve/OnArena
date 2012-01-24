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

import logging
#import traceback

#from google.appengine.api import memcache
from common import models
from common import user

#from django import http
#from django.utils.translation import ugettext as _

from google.appengine.api import users

#import logging

#import urllib
#from django.http import HttpResponse, HttpResponseRedirect, Http404
#from django.conf import settings

from google.appengine.api import rdbms
_INSTANCE_NAME = 'onarenacom'


import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http

#XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_ORIGINS = 'http://goapi.cometiphrd.appspot.com'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
        
    
def ip2int(ip):

    logging.info("ip: %s",ip)
    part = ip.split(".")
    result = 0
    if (len(part) == 4):
        result = int(part[3]) + 256 * (int(part[2]) + 
                 256 * (int(part[1]) + 256 * int(part[0])))

    return result

class UserLocation(object):
    def process_view(self, request, view_func, args, kw):

        if request.META["PATH_INFO"] == "/":
            try:
                
                if request.META["REMOTE_ADDR"] == "127.0.0.1":
                    logging.info("REMOTE_ADDR: 127.0.0.1")
                    return None
                    
                ip2 = ip2int(request.META["REMOTE_ADDR"])
                conn = rdbms.connect(instance="onarenacom:ipbase", database='ipbase')
                cursor = conn.cursor()

                cursor.execute("select * from (select * from net_ru where \
                     begin_ip<=%s order by begin_ip desc limit 1) \
                     as t where end_ip>=%s",(ip2,ip2))
                     
                res = cursor.fetchall()
                if len(res) == 0:
                
                    logging.info("second")          
                    cursor.execute("select * from (select * from net_city_ip where \
                         begin_ip<=%s order by begin_ip desc limit 1) \
                         as t where end_ip>=%s",(ip2,ip2))
                         
                    res = cursor.fetchall()              
                    if len(res) == 0:      
                        return None
                
                cursor.execute("select * from net_city where id=%s", res[0][0])    
                city = cursor.fetchall()[0]
                logging.info("lat: %s, lon: %s",city[6],city[7])    
                
                request.location = (city[6],city[7])
            
            except Exception, err:
                logging.warning("ERROR: %s", str(err))
                
            
        return None    
    

class UserAccess(object):
    def process_view(self, request, view_func, args, kw):

        user.current_user(request)
        
        request.is_global_admin = users.is_current_user_admin()
        
        request.country_code = request.META.get('HTTP_X_APPENGINE_COUNTRY',"") or "ru"        
        #logging.info("country_code: %s",request.country_code)
        
        url = request.META["PATH_INFO"]
        request.url = "http://www.onarena.com" + url
        request.local_url = url
        
        request.is_owner = False
        tournament_ref = None
                                     
        keys = {    "tournament_id": models.Tournament,
                    "league_id"    : models.League,
                    "team_id"      : models.Team,
                    "player_id"    : models.Player,
                    "match_id"     : models.Match,
                    "referee_id"   : models.Referee,                    
                    "news_id"      : models.News,                     
                    }
            
        for k in keys:
            item_id = None
                
            if request.REQUEST.has_key(k):
                item_id = request.REQUEST[k]
            elif kw.has_key(k):   
                item_id = kw[k]
                                      
                                                                        
            if item_id:
                value = keys[k].get_item(item_id)                    

                if not value:
                    break
                        
                try:
                    tournament_ref = value.tournament_id    
                except:
                    tournament_ref = value    
                    
                break                                 
                                                                                                     
                                    
        if tournament_ref:            
            request.tournament = tournament_ref           
            request.tournament_id = tournament_ref.id                 

            if request.user:                                           
                if tournament_ref.user_id.key() == request.user.key() or users.is_current_user_admin():
                    request.is_owner = True   
                elif tournament_ref.user_id.id == request.user.id:
                    tournament_ref.user_id = request.user.id
                    tournament_ref.put()
                    request.is_owner = True                         

            
        request.yahoo_login  = users.create_login_url(url,federated_identity="yahoo.com/")
        request.aol_login    = users.create_login_url(url,federated_identity="aol.com/")              
        request.google_login = users.create_login_url(url)
            
        return None






class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

        return response
