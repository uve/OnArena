#!/usr/bin/env python
#
# Copyright 2010 Google Inc.
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
#


from common import api

from datetime import datetime
import logging

from django import http

from common import deferred
from common import util
from common import models


from django.http import Http404
HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

'''
import datetime
import hashlib

import fix_path
import aetycoon


HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"


class StaticContent(db.Model):
  """Container for statically served content.
  
  The serving path for content is provided in the key name.
  """
  body = db.BlobProperty(required=True)
  content_type = db.StringProperty(required=True)
  last_modified = db.DateTimeProperty(required=True, auto_now=True)
  etag = aetycoon.DerivedProperty(lambda x: hashlib.sha1(x.body).hexdigest())


def get(path):
  """Returns the StaticContent object for the provided path.
  
  Args:
    path: The path to retrieve StaticContent for.
  Returns:
    A StaticContent object, or None if no content exists for this path.
  """
  return StaticContent.get_by_key_name(path)


def set(path, body, content_type, **kwargs):
  """Sets the StaticContent for the provided path.
  
  Args:
    path: The path to store the content against.
    body: The data to serve for that path.
    content_type: The MIME type to serve the content as.
    **kwargs: Additional arguments to be passed to the StaticContent constructor
  Returns:
    A StaticContent object.
  """
  content = StaticContent(
      key_name=path,
      body=body,
      content_type=content_type,
      **kwargs)
  content.put()
  return content


class StaticContentHandler(webapp.RequestHandler):
  def output_content(self, content, serve=True):
    self.response.headers['Content-Type'] = content.content_type
    last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
    self.response.headers['Last-Modified'] = last_modified
    self.response.headers['ETag'] = content.etag
    if serve:
      self.response.out.write(content.body)
    else:
      self.response.set_status(304)
  
  def get(self, path):
    content = get(path)
    if not content:
      self.error(404)
      return

    serve = True
    if 'If-Modified-Since' in request:
      last_seen = datetime.datetime.strptime(
          request['If-Modified-Since'],
          HTTP_DATE_FMT)
      if last_seen >= content.last_modified.replace(microsecond=0):
        serve = False
    if 'If-None-Match' in request:
      etags = [x.strip()
               for x in request['If-None-Match'].split(',')]
      if content.etag in etags:
        serve = False
    self.output_content(content, serve)

'''



def output_content(response, content, serve=True):



    response['Content-Type'] = 'application/json'#content.content_type
    last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
    
    response['Last-Modified'] = last_modified
    
    logging.info("etag start")
    response['ETag'] = '"%s"' % (content.etag,)
    
    logging.info("etag: %s",response['ETag'])
    return http.HttpResponse(status = 304)     
 
    if serve:
        return content.content    

    return http.HttpResponse(status = 304)      
      

def protoprc(request):

    logging.info("request: %s",request)
    
    name = request.REQUEST.get("name") 
    if name is None:
        raise Http404
        
    #key_name = 'api.' + name
    key_name = name

    mas = ['tournament_id', 'league_id']
    
    for k in mas:
        v = request.REQUEST.get(k)
        if v is not None:
            key_name += '_' + k + '_' + unicode(v)    
        
    
    logging.info("key_name: %s", key_name)    
    
    content = models.StaticContent.get_by_key_name(key_name) 
        
    logging.info("request: %s",request)
        
    
    serve = True
    
    '''
    if request['If-Modified-Since']:
        last_seen = datetime.strptime(  request['If-Modified-Since'],  HTTP_DATE_FMT)
        if last_seen >= content.last_modified.replace(microsecond=0):
            serve = False
    if request['If-None-Match']:
        etags = [x.strip()
               for x in request['If-None-Match'].split(',')]
        if content.etag in etags:
            serve = False
    '''    
    response = http.HttpResponse(content)        
    return output_content(response, content, serve)
     




def sitemap(request, format='html'):

    deferred.defer(api.sitemap, name = "tournaments")      
    deferred.defer(api.sitemap, name = "leagues")  
    deferred.defer(api.sitemap, name = "teams")  
    #deferred.defer(api.sitemap, name = "players")  
    #deferred.defer(api.sitemap, name = "matches")      
    

    defers = {  "all_tournaments": deferred.group(api.sitemap, name = "tournaments"),
                "all_leagues":     deferred.group(api.sitemap, name = "leagues"),
                "all_teams":       deferred.group(api.sitemap, name = "teams"),
                #"all_matches":     deferred.group(api.sitemap, name = "matches"),                
                #"all_players":     deferred.group(api.sitemap, name = "players"),  
                }    
  
  

    
    today = datetime.today()
    
    if format == 'html':
        return api.response_get(request, locals(), 'common/templates/sitemap.html')
        
        
def terms_of_service(request, format='html'):
    if format == 'html':
        return api.response_get(request, locals(), 'common/templates/terms_of_service.html')    
        
def privacy(request, format='html'):
    if format == 'html':
        return api.response_get(request, locals(), 'common/templates/privacy.html')    
        
def about_us(request, format='html'):
    if format == 'html':
        return api.response_get(request, locals(), 'common/templates/about_us.html')    
        
                        
        
        
        
        
