from __future__ import with_statement
from google.appengine.api import app_identity

from google.appengine.api import files
try:
  files.gs
except AttributeError:
  import gs
  files.gs = gs
  
  
import cgi
import logging
import json

from django import http

from common import util
from common import models
from common import deferred

from google.appengine.ext import blobstore
from google.appengine.api import images


from random import randint

import api


    
def get_uploads(request, field_name=None, populate_post=False):
    """Get uploads sent to this handler.
    Args:
      field_name: Only select uploads that were sent as a specific field.
      populate_post: Add the non blob fields to request.POST
    Returns:
      A list of BlobInfo records corresponding to each upload.
      Empty list if there are no blob-info records for field_name.
    """
    
    if hasattr(request,'__uploads') == False:
        request.META['wsgi.input'].seek(0)
        fields = cgi.FieldStorage(request.META['wsgi.input'], environ=request.META)
        
        request.__uploads = {}
        if populate_post:
            request.POST = {}
        
        for key in fields.keys():
            field = fields[key]
            if isinstance(field, cgi.FieldStorage) and 'blob-key' in field.type_options:
                request.__uploads.setdefault(key, []).append(blobstore.parse_blob_info(field))
            elif populate_post:
                request.POST[key] = field.value
    if field_name:
        try:
            return list(request.__uploads[field_name])
        except KeyError:
            return []
    else:
        results = []
        for uploads in request.__uploads.itervalues():
            results += uploads
        return results
        

def image_add(request):    
    upload_url  = blobstore.create_upload_url('/image/upload/')       
    results = '"' + upload_url + '"'  
         
    return util.HttpJsonResponse(results, request)
    

def image_remove(request, key = None, limit = 100, format='html'):  

    item = request.POST.get("item", "")
    logging.info("item: %s",item)
    item_id = request.POST.get("item_id", "")
    logging.info("item_id: %s",item_id)    

    logging.info("key: %s",key)    
    
    name = None   
            
    if request.method == "DELETE" and key:

        blob_info = blobstore.get(key)
        logging.info("blob_info: %s",blob_info.key())
        results = models.Image.gql("WHERE blob_key = :1", blob_info.key()).get() 
        if results:
            logging.info("yes: %s",results)
            item_id = results.news_id.id
            models.db.delete(results)
            deferred.defer(api.news_get, news_id = item_id, is_reload = True)  
    
        return http.HttpResponse(status = 200)
        
    
    if item == "team":  
        name = 'team_id'    
        value = models.Team.get_item(item_id)

    elif item == "player":
        name = 'player_id'          
        value = models.Player.get_item(item_id)
  
    elif item == "referee":
        name = 'referee_id'            
        value = models.Referee.get_item(item_id)   
  
    elif item == "news":  
        name = 'news_id'            
        value = models.News.get_item(item_id)     
  
    elif item == "match":  
        name = 'match_id'              
        value = models.Match.get_item(item_id)      
        
    if request.method == "POST":# and request.is_owner:             
        
        results = models.Image.gql("WHERE %s = :1" % name, value).fetch(limit)             
            
        models.db.delete(results)
        
        if item == "team":  
            deferred.defer(api.team_get, team_id = item_id, is_reload = True) 

        elif item == "player":
            deferred.defer(api.player_get, player_id = item_id, is_reload = True) 
  
        elif item == "referee":
            deferred.defer(api.referee_get, referee_id = item_id, is_reload = True)       
  
        elif item == "news":  
            deferred.defer(api.news_get, news_id = item_id, is_reload = True)       
  
        elif item == "match":  
            deferred.defer(api.match_get, match_id = item_id, is_reload = True)         
        
    else:
        logging.error("No Rights!!  Image Remove: %s \t %s", item, item_id)        
        
    
    return http.HttpResponseRedirect("/" + item + "/" + item_id + "/")        
    
      
def image_send(img = None, path = None, width = None, height = None):
      
    if width and height:    
        if img.width > width or img.height > height:              
            img.resize(width, height)
            
    img.im_feeling_lucky()  
    content = img.execute_transforms(output_encoding=images.JPEG)
              
    logging.info("app_identity: %s",app_identity.get_service_account_name()) 
    
    filename='/gs/cometip/' + path
    
    write_path = files.gs.create(filename=filename,
                                 acl='public-read',
                                 cache_control='public,max-age=29030400', 
                                 mime_type='image/jpeg')
                                 
    with files.open(write_path, 'a') as fp:
        fp.write(content)

    files.finalize(write_path)      
    
    '''
    try:
        uri.new_key().set_contents_from_string(content,  headers=header_new, policy="public-read")  
        return path
    except:
        logging.info("Size is too large")     
    '''        
     
    return None
  
                
                
def image_process(blob_key = None, item = None, item_id = None):

    output_encoding = images.JPEG
    format = 'jpeg' 


    id_gen = item_id + "_" + str(randint(1000,9999))        
        
    blob_info = blobstore.get(blob_key)
    if not blob_info:
        return None
        
    filename = blob_info.filename        
    img = images.Image(blob_key=blob_key)
    
    img.im_feeling_lucky()  
    img.execute_transforms(output_encoding=output_encoding)
    
    ##############    Image Original    #################################     
    
    path_original = 'image/%s/%s/%s_%s_original.%s' % (item, item_id, item, id_gen, format)  
    image_send(img = img, path = path_original, width = 1920, height = 1080)                 
         
    ##############    Image Big  1024x786  ##############################     
         
    path_big = 'image/%s/%s/%s_%s_big.%s' % (item, item_id, item, id_gen, format)  
    image_send(img = img, path = path_big, width = 1024, height = 768)         
          
    ##############    Image Small  300x  ##############################     

    path_small = 'image/%s/%s/%s_%s_small.%s' % (item, item_id, item, id_gen, format)  
    image_send(img = img, path = path_small, width = 300, height = 500)          
               
    name = None
  
    if item == "team":  
        name = 'team_id'    
        value = models.Team.get_item(item_id)

    elif item == "player":
        name = 'player_id'          
        value = models.Player.get_item(item_id)
  
    elif item == "referee":
        name = 'referee_id'            
        value = models.Referee.get_item(item_id)   
  
    elif item == "news":  
        name = 'news_id'            
        value = models.News.get_item(item_id)     
  
    elif item == "match":  
        name = 'match_id'              
        value = models.Match.get_item(item_id)      


    if name:
        logging.info("Create Image in DB: %s",filename)
        params = {#'key_name': 'image/%s/%s' % (item, id),
                   ###   Link to Item ###
                   name:              value,            
           
                   'name':            filename,
            
                   'photo_original':  path_original,            
                   'photo_big':       path_big,
                   'photo_small':     path_small,
                   
                   'blob_key':        blob_key,
        }
            
        image = models.Image.create(params)                      
 
        if item == "team":  
            deferred.defer(api.team_get, team_id = item_id, is_reload = True) 

        elif item == "player":
            deferred.defer(api.player_get, player_id = item_id, is_reload = True) 
  
        elif item == "referee":
            deferred.defer(api.referee_get, referee_id = item_id, is_reload = True)       
  
        elif item == "news":  
            deferred.defer(api.news_get, news_id = item_id, is_reload = True)       
  
        elif item == "match":  
            deferred.defer(api.match_get, match_id = item_id, is_reload = True)                  
       
    return  


        
def image_upload(request = None, item = None, item_id = None):

    blob_info_list = get_uploads(request)    
    #logging.info("blob_info_list: %s", blob_info_list)           
    blob_info = blob_info_list[0]    
    
    item = request.POST["item"]
    item_id = request.POST["item_id"]
    
    #image_process(blob_key = blob_info.key(), item = item, item_id = item_id)    
    deferred.defer(image_process, blob_key = blob_info.key(), item = item, item_id = item_id, _queue = "images", _countdown = 5)    
    
    return http.HttpResponseRedirect("/image/uploaded/%s/" % blob_info.key() )         
    
        
def image_uploaded(request, key = None):

    if not key:
        util.HttpJsonResponse('', request)
    
    blob_info = blobstore.get(key)
    thumbnail_url = images.get_serving_url(blob_info.key(), size=80, crop=False)       
    
    small_url = images.get_serving_url(blob_info.key(), size=300, crop=False)               
    big_url   = "."#images.get_serving_url(blob_info.key(), size=1024, crop=False)                       

    results = { 'name':          blob_info.filename,
                'size':          blob_info.size,
                'thumbnail_url': thumbnail_url,
                'small_url':     small_url,
                'big_url':       big_url,                                        
                'delete_url':    '/image/remove/%s/' % blob_info.key(),   
                'delete_type':   'DELETE',
    }
    
    results = json.dumps([results])     
       
    logging.info("results: %s",results)
    
    return util.HttpJsonResponse(results, request)
        
  
    

    

    

