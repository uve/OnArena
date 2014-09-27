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

import datetime
import logging

from google.appengine.api import urlfetch

#from common import api
from common import models
import settings

from django import http
#from django import template
import base64
import cgi
import Cookie
import email.utils
import hashlib
import hmac
import time
import urllib

import json

from google.appengine.api import users

#@property
def current_user(request):
    """Returns the logged in Facebook user, or None if unconnected."""

    logging.info("start. cheking for login")
    
    google_user = users.get_current_user()
    
    if google_user:
        request.user = models.User.get_item(google_user.user_id())
        if not request.user:
            user = models.User(key_name=str(google_user.user_id()), id=str(google_user.user_id()),
                name=google_user.email())
            user.put()
            request.user = models.User.get_item(google_user.user_id())
                         
        return request.user            

    user = getattr(request, "user", None)
    if not user:
        request.user = None
        user_id = parse_cookie(request.COOKIES.get("fb_user"))        
   
        if user_id:
            request.user = models.User.get_item(user_id)                             

    return request.user



def login(request):
    #verification_code = request.code
    
    #redirect_to = request.REQUEST.get("redirect_to")
    #if not redirect_to:
    #    redirect_to = request.META.get('HTTP_REFERER', None) or '/'
    #    request.redirect_to = redirect_to
    
              
    redirect_to = "/"   
        
    redirect_uri = settings.DOMAIN + "/login/"
        
    args = dict(client_id=settings.FACEBOOK_API_KEY, redirect_uri=redirect_uri, scope="publish_stream,create_event,rsvp_event,sms,publish_checkins")
    
    code = request.REQUEST.get("code")   
        
    if not code:
        form_data = urllib.urlencode(args)
        return http.HttpResponseRedirect("https://www.facebook.com/dialog/oauth" + form_data+"&scope=publish_stream")        
    else:        
        #,create_event,rsvp_event,publish_checkins
        #redirect_uri = settings.DOMAIN + "/login/"        
        #args = dict(client_id=settings.FACEBOOK_API_KEY, redirect_uri=redirect_uri)
        
        args["client_secret"] = settings.FACEBOOK_SECRET_KEY
        args["code"] = code        
        
        
        #response = cgi.parse_qs(urllib.urlopen(
        #    "https://graph.facebook.com/oauth/access_token?" +
        #    urllib.urlencode(args)).read())
        #access_token = response["access_token"][-1]
        form_data = urllib.urlencode(args)
        
        result = urlfetch.fetch(url="https://graph.facebook.com/oauth/access_token",
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        deadline=10,
                        )
        
        response = cgi.parse_qs(result.content)
        access_token = response["access_token"][-1]

        # Download the user profile and cache a local instance of the
        # basic profile info
        #profile = json.load(urllib.urlopen(
        #    "https://graph.facebook.com/me?" +
        #    urllib.urlencode(dict(access_token=access_token))))
        
        form_data = urllib.urlencode(dict(access_token=access_token))
        result = urlfetch.fetch(url="https://graph.facebook.com/me?" + form_data,
                        method=urlfetch.GET,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        deadline=10,
                        )
        profile = json.loads(result.content)

        user = models.User(key_name=str(profile["id"]), id=str(profile["id"]),
                    name=profile["name"], access_token=access_token,
                    profile_url=profile["link"])
        request.user = user.put()
        
        response = http.HttpResponseRedirect(redirect_to)
        #response = user.set_user_cookie(response, current_user, rememberme)
        #profile = {}
        #profile["id"] = 500
     
        
        set_cookie(response, "fb_user", str(profile["id"]))
        
        #return http.HttpResponseRedirect()
   
        
        return response


#class LogoutHandler(BaseHandler):
#    def get(self):
#        set_cookie(self.response, "fb_user", "", expires=time.time() - 86400)
#        self.redirect("/")

def set_cookie(response, name, value):
    """Generates and signs a cookie for the give name/value"""
    timestamp = str(int(time.time()))
    value = base64.b64encode(value)
    signature = cookie_signature(value, timestamp)
    cookie = Cookie.BaseCookie()
    cookie[name] = "|".join([value, timestamp, signature])
    cookie[name]["path"] = settings.COOKIE_PATH
    cookie[name]["domain"] = settings.COOKIE_DOMAIN
            
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    cookie[name]['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
    

    #response._headers.append(("Set-Cookie", cookie.output()[12:]))
    fb_user = cookie.output().split('=')[1].split(';')[0]

    response.set_cookie(key=name, value=fb_user, max_age=None, expires=cookie[name]["expires"], path='/', domain=None)
    


def parse_cookie(value):
    """Parses and verifies a cookie value from set_cookie"""
    if not value: 
        return None
    parts = value.split("|")
    if len(parts) != 3: 
        return None
    if cookie_signature(parts[0], parts[1]) != parts[2]:
        logging.warning("Invalid cookie signature %r", value)
        return None
    timestamp = int(parts[1])
    if timestamp < time.time() - 30 * 86400:
        logging.warning("Expired cookie %r", value)
        return None
    try:
        return base64.b64decode(parts[0]).strip()
    except:
        return None


def cookie_signature(*parts):
    """Generates a cookie signature.

    We use the Facebook app secret since it is different for every app (so
    people using this example don't accidentally all use the same secret).
    """
    hash = hmac.new(settings.FACEBOOK_SECRET_KEY, digestmod=hashlib.sha1)
    for part in parts: hash.update(part)
    return hash.hexdigest()
    

def logout(request):
    request.user = None
    
    redirect_to = request.REQUEST.get("redirect_to")
    
    logging.info("redirect_to: %s",redirect_to)
    if not redirect_to:
        redirect_to = "/" 
 
    response = http.HttpResponseRedirect(users.create_logout_url(redirect_to))
    response.delete_cookie(key="fb_user", path=settings.COOKIE_PATH)
    #response = user.clear_user_cookie(response)

    return response
      
