import logging
from django import http
from django.http import Http404

from django.views.generic.base import View

from common import models

class Base(View):

    def get(self, request, pk):                     # READ
        
        if not pk:
            raise Http404

        logging.info("GET request: %s", pk)    
        
        key_name = "team_get_team_id_" + pk
        content = models.StaticContent.get_by_key_name(key_name)
        
        if not content:       
            raise Http404
        
        #logging.info("content: %s",content.content)            
        
        response = http.HttpResponse(content.content)
        response['Content-type']  = "application/json; charset=utf-8"
        return response         
    
    
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
    
