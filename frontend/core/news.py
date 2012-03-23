#import logging

#from django.http import Http404
from django import http
#from common import util

from core import Base 


#from django.shortcuts import render_to_response
#from django.template import RequestContext
#from django.views.generic.base import TemplateView


from django.views.generic.base import View


class SomeView(View):

    def get(self, request, pk):                
        return http.HttpResponse("get: %s" % pk)
    
    def create(self, request, pk):                
        return http.HttpResponse("create: %s" % pk)
    
    def post(self, request, pk):                
        return http.HttpResponse("post: %s" % pk)      
    
    def put(self, request, pk):                
        return http.HttpResponse("put: %s" % pk)   
    
    def update(self, request, pk):                
        return http.HttpResponse("update: %s" % pk)         
    
    def delete(self, request, pk):                
        return http.HttpResponse("delete: %s" % pk)
     

               
