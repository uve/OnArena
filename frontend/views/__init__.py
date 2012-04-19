import logging
from django import http
from django.http import Http404

from django.views.generic.base import View

from common import models

import json


from google.appengine.ext import db

class Base(View):
    
    @classmethod
    def output(cls, content):
                
        if not content:       
            raise Http404
                                                
        response = http.HttpResponse(content)
        response['Content-type']  = "application/json; charset=utf-8"
        return response  

    
    def get(self, request, pk):                     # READ
        
        if not pk: raise Http404
       
        key_name = "team_get_team_id_" + pk
        
        k = db.Key.from_path('StaticContent', key_name) 
        content = db.get_async(k).get_result()        
        #content = models.StaticContent.get_by_key_name(key_name)
        
        return self.output(content.content)
    
    def post(self, request):                          # CREATE
                
        request = json.loads( request.raw_post_data )                
        content = self.create(request) 
                               
        content = json.dumps(content)                                       
        return self.output(content)     
    
    def put(self, request, pk):                       # UPDATE
        
        if not pk: raise Http404
       
        request = json.loads( request.raw_post_data )                
        content = self.save(request, pk)               
        
        content = json.dumps(content)        
        return self.output(content)              
        
    def delete(self, request, pk):                    # DELETE
        
        if not pk: raise Http404
                
        content = self.remove(request, pk)
               
        content = json.dumps(content)        
        return self.output(content)  
    
    
'''
class Base(db.Model):

    created  = db.DateTimeProperty(auto_now_add=True)
    _config_lock = threading.Lock()
    
    @classmethod
    def __init__(self, item_id):        
        
        if item_id:
                
            self.item_id = self.item_id

            with self._config_lock:
                        
                key_name = self.__name__ + "_" + str(item_id)        
                value = self.get_by_key_name(key_name)
                                            
                if value is not None:
                    logging.info("Get by key: %s", key_name)

                    return value
                else:
                    value = self.gql("WHERE id = :1", str(item_id)).get()
                                
                    if value is None:
                        logging.warning("Error get DB item: %s", key_name)
                        return None
                        
                    logging.info("Database: %s", key_name)

                    return value          
    
'''
    
