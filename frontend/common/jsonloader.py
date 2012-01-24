
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility classes and methods for use with json and appengine.

Provides both a specialized json encoder, GqlEncoder, designed to simplify
encoding directly from GQL results to JSON. A helper function, encode, is also
provided to further simplify usage.

  GqlEncoder: Adds support for GQL results and properties to json.
  encode(input): Direct method to encode GQL objects as JSON.
"""

import datetime
import json
import time

from django.utils.functional import Promise
from django.utils.translation import force_unicode

from google.appengine.ext import blobstore

from google.appengine.api import users
from google.appengine.ext import db
import logging

import struct

class GqlEncoder(json.JSONEncoder):
  
  """Extends JSONEncoder to add support for GQL results and properties.
  
  Adds support to json JSONEncoders for GQL results and properties by
  overriding JSONEncoder's default method.
  """
  #def __init__(self):
  #    self.exclude = ["access_token", "key", "created", "updated", "user_id"]
  
  include = []
  exclude = ["access_token", "key", "updated", "user_id"]
  

  
  # TODO Improve coverage for all of App Engine's Property types.

  def default(self, obj):
    
        
    
    """Tests the input object, obj, to encode as JSON."""
    #logging.info("Json obj: %s", obj)    

    if hasattr(obj, '__json__'):
      return getattr(obj, '__json__')()

    if isinstance(obj, db.GqlQuery):
      return list(obj)

    elif isinstance(obj, db.Model):
      output = {}      
      
      for field in obj.__dict__:
        #logging.info(field)
        
        if self.include:
            if not field in self.include:
                continue
        
        if field.startswith('_') or field in self.exclude:
            continue                                            
                    
        try:
            output[field] = getattr(obj, field)
            #logging.info("Name: %s",field)
            #pass#output[field] = unicode(getattr(obj, field))      
            
        except TypeError:
           logging.error("Json error: %s", obj) 
           pass     

      #logging.info("...VS...")

      properties = obj.properties().items()
      for field, value in properties:
        #logging.info(field)      
        
        if self.include:
            if not field in self.include:
                continue        
        
        if field.startswith('_') or field in self.exclude:
            continue
        
        try:    
            output[field] = getattr(obj, field)
        except TypeError:
           logging.error("Json error: %s", obj) 
           pass  

      return output

    elif isinstance(obj, datetime.datetime):

      try:
          output =  datetime.datetime.strftime(obj,"%Y-%m-%dT%H:%M:%S")
      except TypeError:
          logging.error("Json error: %s", obj) 
          pass           
          
      return output


    elif isinstance(obj, datetime.date):
      try:
          output =  datetime.datetime.strftime(obj,"%Y-%m-%d")
      except TypeError:
          logging.error("Json error: %s", obj) 
          pass           
          
      return output


    elif isinstance(obj, time.struct_time):
      try:
          output = list(obj)
      except TypeError:
          logging.error("Json error: %s", obj) 
          pass        
      return output

    elif isinstance(obj, users.User):
      output = {}
      methods = ['nickname', 'email', 'auth_domain']
      for method in methods:
          output[method] = getattr(obj, method)()
        
      try:            
          return output
      except TypeError:
          logging.error("Json error: %s", obj) 
          pass            


    elif isinstance(obj, Promise):
        logging.info("force_unicode: %s", obj) 
        return force_unicode(obj)
    #            else:
    #        return super(LazyEncoder, self).default(obj)


    elif isinstance(obj, blobstore.BlobInfo):
        try:
            output =   str(obj)
        except TypeError:
            logging.error("Json error: BlobInfo") 
            pass           
        
        return output                

    try:           
        results = json.JSONEncoder.default(self, obj)
    except TypeError:
        pass     
    
    return results


def encode(input = None, include = None):

  #logging.info("include: %s",include)
  """Encode an input GQL object as JSON

    Args:
      input: A GQL object or DB property.

    Returns:
      A JSON string based on the input object. 
      
    Raises:
      TypeError: Typically occurs when an input object contains an unsupported
        type.
    """
  ge = GqlEncoder()
  ge.include = include  
  
  return ge.encode(input)
    
  #return GqlEncoder().encode(input)  

