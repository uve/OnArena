
from django import http
from django.http import Http404
import logging

from common import models

from core import Base 


class Team(Base):
  

    def get(self):        
                    
        logging.info("GET request: %s", self.item_id)    
        
        key_name = "team_get_team_id_" + self.item_id
        content = models.StaticContent.get_by_key_name(key_name)
                    
        #logging.info("content: %s",content.content)            
 
        response = http.HttpResponse(content.content)
        response['Content-type']  = "application/json; charset=utf-8"
        return response                    
                
             
    def create(self, request):        

                        
                    
        return http.HttpResponse(status = 200)                   
                
                
               
        
    def update(self, request):        

        logging.info("UPDATE request")                   
                    
        return http.HttpResponse(status = 200)         
        
        
    def delete(self):        
                    
        logging.info("DELETE request")                   
                            
        return http.HttpResponse(status = 200)        
        
        
               
