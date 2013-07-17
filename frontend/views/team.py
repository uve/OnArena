import logging
from views import Base

from common import models 
from common import api

class Team(Base):
    
    def create(self, request, pk):                  
        return ("post: %s" % pk)      
    
    def save(self, request, pk):
        
        #request['name'] += '_1'                 
        
        form = models.TeamForm(request)
        
        if form.is_valid():
            item = api.team_edit(form = form, team_id = pk)
                              
        return ("put: %s" % pk)        
        
    def remove(self, request, pk):                  
        return ("delete: %s" % pk)
