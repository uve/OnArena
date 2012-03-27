import logging
from django import http

from views import Base 

class News(Base):
    
    def post(self, request, pk):                    # CREATE
        return http.HttpResponse("post: %s" % pk)      
    
    def put(self, request, pk):                     # UPDATE  
        return http.HttpResponse("put: %s" % pk)        
        
    def delete(self, request, pk):                  # DELETE
        return http.HttpResponse("delete: %s" % pk)
