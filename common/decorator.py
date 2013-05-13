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


#from django.conf import settings

#from common import exception
#from common import user
#from common import models
#from common import util
import logging
from google.appengine.api import memcache
import models
import api

def check_cache(handler):
    def _wrapper(*args, **kw):              
        key_name = _wrapper.__name__
     
        for k,v in kw.items():
            #logging.info("k: %s \t v: %s", k, v)
            if not k in ["is_reload", "memcache_delete"]:
                key_name += '_' + k + '_' + unicode(v)

        kw["key_name"] = key_name
        
        if kw.has_key("memcache_delete"):
            memcache.delete(key = key_name)
            api.cache_delete(key_name) 
            logging.info("Remove Memcache Key: %s", key_name)
            return None

        elif not kw.has_key("is_reload") and key_name != _wrapper.__name__:
            
            results = api.cache_get(key_name) 
            
            if results is not None:
                return results

                #return None                 
            
            #results = memcache.get(key = key_name)            
            #if results is not None:
            #    logging.info("Memcache: %s", key_name)
            #    return results            
                
        if key_name == _wrapper.__name__:
            logging.error("FUNCTION without args: %s", key_name)
        
        logging.info("Database: %s", key_name)

        return handler( *args, **kw)
    _wrapper.__name__ = handler.__name__
    return _wrapper

'''
from django import http
import urllib


def login_required(handler):
    def _wrapper(request, *args, **kw):   
        if not request.user:
            args={}
            args["redirect_to"] = request.path
            return http.HttpResponseRedirect("/login?" + urllib.urlencode(args))            
            #raise exception.LoginRequiredException()
   
        return handler(request, *args, **kw)
    _wrapper.__name__ = handler.__name__
    return _wrapper

def debug_only(handler):
  def _wrapper(request, *args, **kw):
    if not settings.DEBUG:
      raise http.Http404()
    return handler(request, *args, **kw)
  _wrapper.__name__ = handler.__name__
  return _wrapper



def add_caching_headers(headers):
  def _cache(handler):
    def _wrap(request, *args, **kw):
      rv = handler(request, *args, **kw)
      return util.add_caching_headers(rv, headers)
    _wrap.func_name == handler.func_name
    return _wrap
  return _cache

# TOOD(termie): add caching headers to cache response forever
cache_forever = add_caching_headers(util.CACHE_FOREVER_HEADERS)

# TOOD(termie): add caching headers to cache response never
cache_never = add_caching_headers(util.CACHE_NEVER_HEADERS)

'''
