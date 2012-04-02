# Copyright 2009 Google Inc.
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

#import datetime
import logging

from google.appengine.ext import db
from google.appengine.api import memcache

from google.appengine.ext import blobstore

import aetycoon
import hashlib

try:
  #from google.appengine.ext.db import djangoforms
  import djangoforms
  from django.utils.translation import ugettext_lazy as _
except ImportError:
  pass

#from settings import CACHE_EXPIRES
CACHE_EXPIRES = 0

class CustomModel(db.Model):
    
    created  = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def get_item(self, item):        

        if item is None:
            return None
        
        key_name = self.__name__ + "_" + str(item)        
        value = self.get_by_key_name(key_name)
                 
                
        if value is not None:
            return value
        else:
            value = self.gql("WHERE id = :1", str(item)).get()
            #logging.info("Value: %s\t%s",value, item)
            
            if value is None:
                logging.warning("Error get DB item: %s", key_name)
                return None
        
            return value           
            
            
        #########  New !!!  CAS
        ''''
        def bump_counter(key): 
            client = memcache.Client() 
            while True: # Retry loop 
                counter = client.gets(key) 
                assert counter is not None, 'Uninitialized counter' 
                if client.cas(key, counter+1): 
                    break          
        '''        
        '''
        value = memcache.get(key = key_name)
        if value is not None:
            logging.info("Memcache: %s", key_name)
            return value
        else:
            value = self.get_by_key_name(item)
            if not value:
                value = self.gql("WHERE id = :1", str(item)).get()
            if not value:
                return None
            if not memcache.set(key = key_name, value = value):
                logging.error("Memcache set failed.")

            logging.info("Database: %s", key_name)
            return value
        '''
        
    @classmethod
    def update(self, item):
        key_name = self.__name__ + "_" + str(item)
        t = memcache.delete(key = key_name)
        t = t
    
    @classmethod 
    def create(self, params):
        key_name = self.__name__ + "_last"
        
        if memcache.get(key = key_name):
            value = memcache.incr(key = key_name)
            
        else:
            last = self.all().order('-created').get()
            try:#if last.id:
                value = int(last.id) + 1
                logging.warning("Memcache Counter from DataBase for: %s\t%s", key_name, value)
            except:#else:
                if self.__name__ == "Image":
                    value = 1100001
                else:                
                    value = 1001
                logging.error("Memcache Counter from DataBase for: %s\t%s", key_name, value)
            if not memcache.set(key = key_name, value = value, time = 0):#CACHE_EXPIRES):
                logging.error("Memcache set failed.")
            
            
        key_name = self.__name__ + "_" + str(value)            
            
        params["id"] = str(value)
        params["key_name"] = key_name
        
        new_ref = self(**params)
        new_ref.put()
        return new_ref  



class CustomForm(djangoforms.ModelForm):
    #error_css_class = 'error'
    #required_css_class = 'required'
    
    def save(self, item = None, commit=True):
        #logging.info("data: %s",self)
        data = self._cleaned_data()
        if item is not None:            
            for k,v in data.items():
                setattr(item, k, v)
            
            item.put()                        
            return item
                
        return None  

    def _cleaned_data(self):
        """Helper to retrieve the cleaned data attribute.

        In Django 0.96 this attribute was called self.clean_data.  In 0.97
        and later it's been renamed to self.cleaned_data, to avoid a name
        conflict.  This helper abstracts the difference between the
        versions away from its caller.
        """
        try:
          return self.cleaned_data
        except AttributeError:
          return self.clean_data                  
        
               
                           
class StaticContent(CustomModel):
    name = db.StringProperty(required=False)
    content = db.TextProperty()
    last_modified = db.DateTimeProperty(required=True, auto_now=True)
    
    content_type = db.StringProperty(required=False)
    etag = aetycoon.DerivedProperty(lambda x: hashlib.sha1(x.content).hexdigest())
    

class User(CustomModel):
    id = db.StringProperty(required=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=False)
    access_token = db.StringProperty(required=False)
    

class Sport(CustomModel):
    id       = db.StringProperty(required=True)
    name     = db.StringProperty(required=True)
    
    #@classmethod
    #def create(self):
           
    
class Tournament(CustomModel):
    id       = db.StringProperty(required=True)
    name     = db.StringProperty(required=True, verbose_name=_('Tournament Name'))  # ref - entry
    user_id  = db.ReferenceProperty(User, collection_name='user_tournaments', required=True)
    sport_id = db.ReferenceProperty(Sport, collection_name='sport_tournaments', required=True)
    
    #geopt    = db.GeoPtProperty() # the count of the number of reports so f ar
    lat      = db.StringProperty()
    lon      = db.StringProperty()            

    #country  = db.StringProperty()
    
    #rules    = db.TextProperty()
    #info     = db.StringProperty()
    #contacts = db.StringProperty()

    about    = db.TextProperty(required=False,   verbose_name=_('About Tournament'))
    contacts = db.StringProperty(required=False, verbose_name=_('Contacts'))    
    
    url     = db.StringProperty(required=False,   verbose_name=_('URL'))
    email   = db.StringProperty(required=False,   verbose_name=_('E-mail'))   
    
     
    country = db.StringProperty(required=False, verbose_name=_('Country'))  
    city    = db.StringProperty(required=False, verbose_name=_('City'))          
    
    postal_code = db.StringProperty(required=False, verbose_name=_('ZIP Code'))      
    
    formatted_address = db.StringProperty(required=False, verbose_name=_('Full Address'))      
    street            = db.StringProperty(required=False, verbose_name=_('Street'))      
    address           = db.StringProperty(required=False, verbose_name=_('Address'))   
    

    #logo    = db.LinkProperty(required=False)

    
class TournamentFormEdit(CustomForm):
    class Meta:
        model=Tournament
        fields = ('name','about','country','city','contacts','address','url','email')         
    
class TournamentFormCreate(CustomForm):
    class Meta:
        model=Tournament
        fields = ('name','about','country','city','contacts','address','url','email','lat','lon')         
      
class TournamentAddressForm(CustomForm):
    class Meta:
        model=Tournament
        fields = ('country','postalcode','address','formatted_address','lat','lon') 
        
class TournamentFormStep1(CustomForm):
    class Meta:
        model=Tournament
        fields = ('name','address')  
        
        
        

class League(CustomModel):
    id            = db.StringProperty(required=True)
    name          = db.StringProperty(required=True)
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_leagues', required=True)
    ranking = db.IntegerProperty(required=True, default = 1)  

class Team(CustomModel):
    id   = db.StringProperty(required=True)
    name = db.StringProperty(required=True, verbose_name = _('Team Name'))
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_teams', required=True)
    
    rating = db.IntegerProperty()
    ranking = db.IntegerProperty(default = 1)
    
    manager  = db.StringProperty(required=False, verbose_name=_('Manager'))
    coach    = db.StringProperty(required=False, verbose_name=_('Coach'))  
    captain  = db.StringProperty(required=False, verbose_name=_('Captain'))
    contacts = db.StringProperty(required=False, verbose_name=_('Contacts'))
    about    = db.TextProperty(required=False,   verbose_name=_('About Team'))
    
    sponsor_name    = db.StringProperty(required=False, verbose_name=_('Team Sponsor'))
    sponsor_about   = db.TextProperty(required=False,   verbose_name=_('About Sponsor'))
    sponsor_url     = db.StringProperty(required=False, verbose_name=_('URL'))
    sponsor_email   = db.StringProperty(required=False, verbose_name=_('Sponsor E-mail'))    
    sponsor_address = db.StringProperty(required=False, verbose_name=_('Address'))
    sponsor_contact = db.StringProperty(required=False, verbose_name=_('Sponsor Contacts'))   

    #logo    = db.LinkProperty(required=False)

class TeamForm(CustomForm):   
    class Meta:
        model=Team
        #fields=('name')        
        exclude = ('id','tournament_id','rating','ranking') 

                 

class Group(CustomModel):
    id          = db.StringProperty(required=True)
    name        = db.StringProperty()    
        
    league_id     = db.ReferenceProperty(League,     collection_name='league_groups', required=True)
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_groups', required=True)  

class Season(CustomModel):
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_seasons', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_seasons',     required=True)
    team_id       = db.ReferenceProperty(Team,       collection_name='team_seasons',       required=True)
        
    group_id      = db.ReferenceProperty(Group,      collection_name='group_seasons')     
        



class Playoff(CustomModel):
    id          = db.StringProperty(required=True)
    name        = db.StringProperty()    
    size        = db.IntegerProperty()    
        
    league_id     = db.ReferenceProperty(League,     collection_name='league_playoffs', required=True)
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_playoffs', required=True)    
    
    
class PlayoffStage(CustomModel):
    id          = db.StringProperty(required=True)    
    name        = db.StringProperty(required=True)    

class PlayoffNode(CustomModel):
    id              = db.StringProperty(required=True)    

    league_id     = db.ReferenceProperty(League,     collection_name='league_playoffnodes', required=True)
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_playoffnodes', required=True)  
        
    playoff_id      = db.ReferenceProperty(Playoff,      collection_name='playoff_playoffnodes', required=True)
    playoffstage_id = db.ReferenceProperty(PlayoffStage, collection_name='playoffstage_playoffnodes', required=True)    
    

class PlayoffCompetitor(CustomModel):

    id          = db.StringProperty(required=True)
    team_id  = db.ReferenceProperty(Team,   collection_name='team_playoffcompetitors',    required=False)

    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_playoffcompetitors', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_playoffcompetitors',     required=True)
    
    playoff_id      = db.ReferenceProperty(Playoff,      collection_name='playoff_playoffcompetitors', required=True)
    playoffstage_id = db.ReferenceProperty(PlayoffStage, collection_name='playoffstage_playoffcompetitors', required=True)       
    playoffnode_id  = db.ReferenceProperty(PlayoffNode,  collection_name='playoffnode_playoffcompetitors', required=True)   

class Match(CustomModel):
    id            = db.StringProperty(required=True)
    datetime      = db.DateTimeProperty(required=True)
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_matches', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_matches',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_matches',     required=False)
     
    place         = db.StringProperty(required=False)

    ranking = db.IntegerProperty(default = 1)
    
    playoff_id      = db.ReferenceProperty(Playoff,      collection_name='playoff_matches')
    playoffstage_id = db.ReferenceProperty(PlayoffStage, collection_name='playoffstage_matches')       
    playoffnode_id  = db.ReferenceProperty(PlayoffNode,  collection_name='playoffnode_matches')    
    
    
    group_id      = db.ReferenceProperty(Group ,      collection_name='group_matches')     
    
    #referee       = db.ReferenceProperty(Referee,     collection_name='referee_matches')

class Referee(CustomModel):
    id            = db.StringProperty(required=True)
    name          = db.StringProperty()
    second_name   = db.StringProperty()
    full_name     = db.StringProperty()    
    birthday      = db.DateProperty()    
    datetime      = db.DateTimeProperty()        
    tournament_id = db.ReferenceProperty(Tournament,   collection_name='tournament_referees', required=True)
    
    

class RefereeMatch(CustomModel):
    match_id      = db.ReferenceProperty(Match,      collection_name='match_refereematches', required=True)
    referee_id    = db.ReferenceProperty(Referee,    collection_name='referee_refereematches', required=True)
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_refereematches', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_refereematches',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_refereematches',     required=False)

class ResultType(CustomModel):
    id       = db.StringProperty(required=True)
    name     = db.StringProperty(required=True)
    

class Regulations(CustomModel):
    content       = db.TextProperty(required=False)    
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_regulations', required=True)    
 

class Competitor(CustomModel):
    match_id = db.ReferenceProperty(Match,  collection_name='match_competitors',   required=True)
    team_id  = db.ReferenceProperty(Team,   collection_name='team_competitors',    required=True)

    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_competitors', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_competitors',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_competitors',     required=False)

    ranking = db.IntegerProperty(default = 0)   
    
    resulttype_id = db.ReferenceProperty(ResultType, collection_name='resulttype_competitors')
    
    
    playoff_id      = db.ReferenceProperty(Playoff,      collection_name='playoff_competitors',)
    playoffstage_id = db.ReferenceProperty(PlayoffStage, collection_name='playoffstage_competitors',)       
    playoffnode_id  = db.ReferenceProperty(PlayoffNode,  collection_name='playoffnode_competitors',)       
    
    group_id      = db.ReferenceProperty(Group,      collection_name='group_competitors')          

class ScoreType(CustomModel):
    id       = db.StringProperty(required=True)
    name     = db.StringProperty(required=True)

    
class Score(CustomModel):    
    match_id      = db.ReferenceProperty(Match,      collection_name='match_scores',      required=True)
    team_id       = db.ReferenceProperty(Team,       collection_name='team_scores',       required=True)
    competitor_id = db.ReferenceProperty(Competitor, collection_name='competitor_scores', required=True)
    scoretype_id  = db.ReferenceProperty(ScoreType,  collection_name='scoretype_scores',  required=True)
    
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_scores', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_scores',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_scores',     required=False)
    
    group_id      = db.ReferenceProperty(Group,      collection_name='group_scores')      
    
    value         = db.FloatProperty()

class Position(CustomModel):
    id          = db.StringProperty(required=True)
    name        = db.StringProperty(required=True)
    sport_id    = db.ReferenceProperty(Sport, collection_name='sport_positions', required=True)

    
   

class Player(CustomModel):
    id          = db.StringProperty(required=True)
    name        = db.StringProperty()
    second_name = db.StringProperty()
    third_name  = db.StringProperty()
    full_name   = db.StringProperty()
    
    
    height = db.FloatProperty()
    weight = db.FloatProperty()
    
    position_id   = db.ReferenceProperty(Position,     collection_name='position_players', ) 
    tournament_id = db.ReferenceProperty(Tournament,   collection_name='tournament_players', required=True) 
    
    birthday = db.DateProperty()
    datetime = db.DateTimeProperty()   
        
    rating = db.IntegerProperty()
    ranking = db.IntegerProperty(default = 1)    
    


class PlayerMatch(CustomModel):
    
    match_id      = db.ReferenceProperty(Match,      collection_name='match_playermatches',      required=True)
    team_id       = db.ReferenceProperty(Team,       collection_name='team_playermatches',       required=True)
    
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_playermatches', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_playermatches',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_playermatches',     required=False)

    player_id     = db.ReferenceProperty(Player, collection_name='player_playermatches',     required=True)


    ranking = db.IntegerProperty(default = 0)   

class PlayerTeam(CustomModel):
    player_id     = db.ReferenceProperty(Player, collection_name='player_playerteams',     required=True)
    team_id       = db.ReferenceProperty(Team,   collection_name='team_playerteams',       required=True)
    tournament_id = db.ReferenceProperty(Tournament,   collection_name='tournament_playerteams', required=True)    
    number        = db.IntegerProperty()

    active        = db.BooleanProperty(required=False)



class EventType(CustomModel):
    id       = db.StringProperty(required=True)
    name     = db.StringProperty(required=True)
    sport_id = db.ReferenceProperty(Sport, collection_name='sport_eventtypes', required=True)

class Event(CustomModel):
    minute      = db.IntegerProperty()

    eventtype_id = db.ReferenceProperty(EventType,   collection_name='eventtype_events',  required=True)
    player_id    = db.ReferenceProperty(Player,      collection_name='player_events',     )
    
    playermatch  = db.ReferenceProperty(PlayerMatch, collection_name='playermatch_events',     )    

    match_id      = db.ReferenceProperty(Match,      collection_name='match_events',      required=True)
    team_id       = db.ReferenceProperty(Team,       collection_name='team_events',       )
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_events', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_events',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_events',     required=False)
    
    referee_id    = db.ReferenceProperty(Referee,    collection_name='referee_events',    required=False)    



class Sanction(CustomModel):
      
    match_id      = db.ReferenceProperty(Match,      collection_name='match_sanctions',      required=True)
    team_id       = db.ReferenceProperty(Team,       collection_name='team_sanctions',       required=True)
    
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_sanctions', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_sanctions',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_sanctions',     required=False)

    player_id     = db.ReferenceProperty(Player,     collection_name='player_sanctions',     required=True)


class StatPlayer(CustomModel):
      
    eventtype_id = db.ReferenceProperty(EventType,   collection_name='eventtype_statplayers',  required=True)
    player_id    = db.ReferenceProperty(Player,      collection_name='player_statplayers',     required=True)
    score        = db.IntegerProperty(required=True)

    team_id       = db.ReferenceProperty(Team,       collection_name='team_statplayers',       )
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_statplayers', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_statplayers',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_statplayers',     required=False)
    
   

class News(CustomModel):
    id       = db.StringProperty(required=True)
    name     = db.StringProperty(required=True)
    content  = db.TextProperty(required=True)
    
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_news', required=True)
    user_id       = db.ReferenceProperty(User,       collection_name='user_news',       required=True)
    
   
    
class Image(CustomModel):
    id             = db.StringProperty(required=False)
    name           = db.StringProperty(required=False)
    
    team_id        = db.ReferenceProperty(Team,    collection_name='team_photos')         
    player_id      = db.ReferenceProperty(Player,  collection_name='player_photos')         
    referee_id     = db.ReferenceProperty(Referee, collection_name='referee_photos')   
    news_id        = db.ReferenceProperty(News,    collection_name='news_photos')         
    match_id       = db.ReferenceProperty(Match,   collection_name='match_photos')       
              
    photo_original = db.StringProperty()            
    photo_big      = db.StringProperty()   
    photo_small    = db.StringProperty()   
    
    blob_key       = blobstore.BlobReferenceProperty()
        

class Vote(CustomModel):
    match_id      = db.ReferenceProperty(Match,      collection_name='match_votes',      required=True)
    team_id       = db.ReferenceProperty(Team,       collection_name='team_votes',       required=True)
    competitor_id = db.ReferenceProperty(Competitor, collection_name='competitor_votes', required=True)
    
    tournament_id = db.ReferenceProperty(Tournament, collection_name='tournament_votes', required=True)
    league_id     = db.ReferenceProperty(League,     collection_name='league_votes',     required=True)
    season_id     = db.ReferenceProperty(Season,     collection_name='season_votes',     required=False)

    player_id     = db.ReferenceProperty(Player, collection_name='player_votes',     required=True)


class Weather(CustomModel):
    date     = db.DateProperty()
    title     = db.StringProperty()
    overcast = db.StringProperty()
    image    = db.StringProperty()
    day      = db.FloatProperty()
    night    = db.FloatProperty() 
    wind     = db.FloatProperty() 
    windtype = db.StringProperty()
    windimage = db.StringProperty()

