import webapp2

from google.appengine.api import memcache

import datetime

import logging

import zlib


from google.appengine.ext import db

class StaticContent(db.Model):
    name = db.StringProperty(required=False)
    content = db.TextProperty(required=False)
    last_modified = db.DateTimeProperty(required=True, auto_now=True)
    
    content_type = db.StringProperty(required=False)
    #etag = aetycoon.DerivedProperty(lambda x: hashlib.sha1(x.content).hexdigest())
    etag = db.StringProperty(required=False)

    compressed = db.BlobProperty(required=False)
    

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

class StaticContentHandler(webapp2.RequestHandler):
    
    def output_content(self, content, serve=True):
        self.response.headers['Content-Type'] = 'application/json'#content.content_type    
        
        try:
            last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
            self.response.headers['Last-Modified'] = last_modified                
            self.response.headers['ETag'] = str(content.etag)
            
            #logging.info("content.content: %s",content.content)
            #logging.info("content.compressed: %s",content.compressed)
                
            if serve:
                
                result = content.content
                
                #logging.info("content.content: %s",content.content)
                            
                if hasattr(content, 'compressed') and content.compressed:      
                    logging.info("is_compressed: %s", True)   
                    result = zlib.decompress(content.compressed).decode('utf-8')
                else: 
                    self.response.headers['ETag'] = '' 
                
                
                self.response.out.write(result)
            else:
                self.response.set_status(304)        
                    
        except Exception as e:           
            logging.warning("Exception: %s", e)
            self.response.set_status(200) 
            return

  
    def get(self, path):

        self.response.headers['Content-Type'] = 'application/json'
          
        name = self.request.get("name") 
        if name is None:
            raise Http404
            
        #key_name = 'api.' + name
                
        key_name = name
    
        mas = ['tournament_id', 'league_id', 'team_id', 
                                'match_id', 'referee_id', 'player_id']
        
        for k in mas:
            v = self.request.get(k)
            if v:
                key_name += '_' + k + '_' + unicode(v)    
            
        
        logging.info("key_name: %s", key_name)    
    
        last_seen = None#memcache.get(key_name)   
        #logging.info("last_seen: %s",last_seen)    
            
        if last_seen and 'If-Modified-Since' in self.request.headers:
            #logging.info("If-Modified-Since: %s", self.request.headers['If-Modified-Since'])
            if last_seen == self.request.headers['If-Modified-Since']:
        
                logging.info("Get From Memcache key_name: %s", key_name)         
                self.response.set_status(304)       
                return
            
            
        content = StaticContent.get_by_key_name(key_name)   
        if not content:
            self.response.out.write('[]')
            return
            
            
        last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
        
                           
        #if not last_seen:  
        logging.info("Set Memcache key_name: %s \t value: %s", key_name, last_modified)     
        memcache.set(key_name, last_modified)    
                     
        serve = True
        
        try:        
            if 'If-Modified-Since' in self.request.headers:
                last_seen = datetime.datetime.strptime(
                          self.request.headers['If-Modified-Since'],
                          HTTP_DATE_FMT)
                if last_seen >= content.last_modified.replace(microsecond=0):
                    serve = False
                
            if 'If-None-Match' in self.request.headers:
                etags = [x.strip()
                       for x in self.request.headers['If-None-Match'].split(',')]
                if content.etag in etags:
                    serve = False
            
        except Exception as e:           
            logging.warning(e)   
            serve = True        
            
        self.output_content(content, serve)
   
   

class ErrorHandler(webapp2.RequestHandler):  
    def post(self, path):   
        logging.info("errorMsg: %s",   self.request.get("errorMsg"))
        logging.info("url: %s",        self.request.get('url'))
        logging.info("lineNumber: %s", self.request.get('lineNumber'))        
           
        self.response.set_status(200) 
        return

app = webapp2.WSGIApplication([('(/api/*)', StaticContentHandler),
                                      ('(/error/*)', ErrorHandler)])



