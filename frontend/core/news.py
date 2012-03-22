import logging

from django.http import Http404
from common import models
from common import util

from core import Base 

from django.views.generic import DetailView
t = 2

class News2(DetailView): 


    def get_context_data(self, **kwargs):
    
        return http.HttpResponse(status = 200)        
        '''
        meetup = Meetup.objects.get(pk=self.kwargs['pk'])
        if self.request.user.is_authenticated():
            try:
                user_section_vote = SectionVote.objects.filter(user=self.request.user) \
                                        .get(section__meetup=meetup) \
                                        .section
            except SectionVote.DoesNotExist:
                user_section_vote = None
        else:
            user_section_vote = None
            
        context = super(MeetupDetailView, self).get_context_data(**kwargs)
        context['USER_VOTE'] = user_section_vote
        
        return context
        '''

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
        
        
               
