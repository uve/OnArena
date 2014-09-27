from google.appengine.ext import db
from google.appengine.tools import bulkloader

class Net_country(db.Model):
    id2 = db.IntegerProperty()
    name_ru = db.StringProperty()
    name_en = db.StringProperty()
    code    = db.StringProperty()

class Net_country_ip(db.Model):
    country_id2 = db.IntegerProperty()
    begin_ip = db.IntegerProperty()
    end_ip = db.IntegerProperty()
    
    


class Net_city_ip(db.Model):
    city_id2 = db.IntegerProperty()
    begin_ip = db.IntegerProperty()
    end_ip = db.IntegerProperty()
    

class AlbumLoader4(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Net_country',
                                   [('id2', int),
                                    ('name_ru', lambda x: x.decode('utf-8')),
                                    ('name_en', lambda x: x.decode('utf-8')),
                                    ('name_code', lambda x: x.decode('utf-8'))
                                   ])

class AlbumLoader3(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Net_country_ip',
                                   [('country_id2', int),
                                    ('begin_ip', int),
                                    ('end_ip', int)
                                   ])

class AlbumLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Net_city_ip',
                                   [('city_id2', int),
                                    ('begin_ip', int),
                                    ('end_ip', int)
                                   ])
        

loaders = [AlbumLoader3]    