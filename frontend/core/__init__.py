from django import http
from django.http import Http404
import logging

from django.views.generic import View

class Base(View):

    status_code = 200

    template_name = 'manager/obj_add.html'
    
    def __init__(self, request, item_id): 

        self.request = request
        logging.info('starting Base:')        
            
        #return http.HttpResponse(status = 200)        

    def dispatch(request, *args, **kwargs):
        logging.info('starting Base:')      
        #return http.HttpResponse(status = 200)                
    #def __setitem__(self, key, value):
    #    logging.info('Setting %r to %r' % (key, value))
    #    return super().__setitem__(key, value) 
    
    

'''
class Base(db.Model):

    created  = db.DateTimeProperty(auto_now_add=True)
    _config_lock = threading.Lock()
    
    @classmethod
    def __init__(self, item_id):        
        
        if item_id:
                
            self.item_id = self.item_id

            with self._config_lock:
                        
                key_name = self.__name__ + "_" + str(item_id)        
                value = self.get_by_key_name(key_name)
                                            
                if value is not None:
                    logging.info("Get by key: %s", key_name)

                    return value
                else:
                    value = self.gql("WHERE id = :1", str(item_id)).get()
                                
                    if value is None:
                        logging.warning("Error get DB item: %s", key_name)
                        return None
                        
                    logging.info("Database: %s", key_name)

                    return value          
    
'''
    
