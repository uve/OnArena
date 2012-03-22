
from django import http
from django.http import Http404
import logging


from core import Base 


class Match(Base):
  

    def get(self):        
                    
        logging.info("GET request")                                       
                    
        return http.HttpResponse(status = 200)      
             
                     
    def create(self, request):        

    
        league_id      = request.REQUEST.get('league_id', '')
        playoffnode_id = request.REQUEST.get('playoffnode_id', '')    
        group_id       = request.REQUEST.get('group_id', '')
    
    
        team1_id = request.REQUEST.get("team1", '')
        team2_id = request.REQUEST.get("team2", '')
   
    
        match_date = request.REQUEST.get("datepicker", '')
        match_time = request.REQUEST.get("timepicker", '')
        referee_id = request.REQUEST.get("referee", '')
        
        place      = request.REQUEST.get("place", '')
    
        match_date = match_date.replace("-",".")    
    
        match_time = match_time.replace(".",":")
        match_time = match_time.replace("-",":")    
        match_time = match_time.replace(",",":")    
    
        full_datetime  = str(match_date) + " " + str(match_time)    
    
        logging.info("POST request")                          
                    
        return http.HttpResponse(status = 200)                   
                                              
        
    def update(self, request):        

        logging.info("UPDATE request")                   
                    
        return http.HttpResponse(status = 200)         
        
        
    def delete(self):        
                    
        logging.info("DELETE request")                   
                            
        return http.HttpResponse(status = 200)        
        
        
               
