from django import http
from django.http import Http404
import logging

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


class Base():

    def __init__(self, item_id): 
    
        if item_id:
            self.item_id = item_id
            logging.info("INIT item_id: %s", item_id)
