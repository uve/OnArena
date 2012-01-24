
from django import http
from django.http import Http404
import logging


from core import Base 

from common import models

class Tournament(Base):
  
  
    def get(self):        
                    
        logging.info("GET request")    
                
        key_name = "tournament_get_tournament_id_" + self.item_id
        
        logging.info("key_name: %s", key_name)
   
        content = models.StaticContent.get_by_key_name(key_name)   
        
        logging.info("content: %s",content.content)
                    
        return http.HttpResponse(status = 200)     
        
        
    def create(self, request):        

    
        logging.info("POST request")                          
                    
        return http.HttpResponse(status = 200)                   
                
                
               
        
    def update(self, request):        

        logging.info("UPDATE request")                   
                    
        return http.HttpResponse(status = 200)         
        
        
    def delete(self):        
                    
        logging.info("DELETE request")                   
                            
        return http.HttpResponse(status = 200)         
