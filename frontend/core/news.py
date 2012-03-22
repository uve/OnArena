import logging

from django.http import Http404
from common import models
from common import util

from core import Base 

t = 2

class News2(Base): 



    def get(self):        
                                                                   
        #logging.info("News GET %s", self.item_id)    
        
    
        
        return util.HttpJsonResponse('test', request)           
        
        key_name = "news_get_news_id_" + self.item_id
        result = models.StaticContent.get_by_key_name(key_name)
        
        if not result:       
            raise Http404
                         
        return util.HttpJsonResponse(result.content, request)   
                
             
    def create(self, request):        

                        
                    
        return http.HttpResponse(status = 200)                   
                
                
               
        
    def update(self, request):        

        logging.info("UPDATE request")                   
                    
        return http.HttpResponse(status = 200)         
        
        
    def delete(self):        
                    
        logging.info("DELETE request")                   
                            
        return http.HttpResponse(status = 200)        
        
        
               
