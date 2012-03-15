#!/usr/bin/python
# -*- coding: utf-8 -*-




import datetime


#from django.conf import settings
#from django.template import loader
#from django.core.cache import cache

from django import template
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template


import json


from google.appengine.ext import db
from google.appengine.api import taskqueue
from google.appengine.api import memcache
from google.appengine.api import urlfetch


from google.appengine.datastore import entity_pb



from common import models
import settings


import time
import random
import logging

from django import http
from django import template
from django.template import loader

from google.appengine.api import images
#import facebook
import re

from common import jsonloader 
import json


import urllib2, urllib


from settings import CACHE_EXPIRES

from common import deferred


import os
import sys

import pickle
import types


import pyclbr

#from common.decorator import check_cache


from django.core.context_processors import csrf


from google.appengine.api import runtime




#######
#######
#######
HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"

DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT


import dateutil.parser




def decode_datetime(obj):
        
    if 'datetime' in obj:    	
        try:
            dt = dateutil.parser.parse(obj['datetime'])
            obj['datetime'] = dt
        except:
            pass
    
    if 'created' in obj:        
        try:
            dt = dateutil.parser.parse(obj['created'])
            obj['created'] = dt
        except:	        
            pass
	    
    return obj


def cache_delete(key_name):

    results = models.StaticContent.get_by_key_name(key_name)
    if results:     
        return db.delete(results)        

    return False
       
 

def cache_get(key_name):

    results = models.StaticContent.get_by_key_name(key_name) 
            
    if results and results.name:
    
        logging.info("Get from Cache: %s", key_name)       
    
        results = json.loads(results.content, object_hook=decode_datetime)       
         
    
        return results
    else:
        return None

def cache_set(key_name, value, include = [], commit = False):
    
    try:
        
        logging.info("Start encoding: %s", key_name)            
        
        logging.info("memory usage: %s",runtime.memory_usage().current())           
        value = jsonloader.encode(input = value, include = include)
        
        logging.info("Save to Cache: %s", key_name)            
        
        logging.info("memory usage: %s",runtime.memory_usage().current())           
        
        content = models.StaticContent( key_name = key_name, name = key_name, 
                            content = value, content_type = 'application/json')
                            
        content.put()       
        
        logging.info("Cache saved")             

        last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
        memcache.set(key_name, last_modified)             
        
        logging.info("memcache saved")                     
                                    
        logging.info("memory usage: %s",runtime.memory_usage().current())                                       
        
        if commit:
            del value
            return True
        
        logging.info("json.loads: %s", key_name)
    
        return json.loads(value, object_hook=decode_datetime) 
    except:
        logging.warning("Warning Cache Set!!   Json encode: %s", key_name)   
        return value     


def check_cache(handler):
    def _wrapper(*args, **kw):              
        key_name = _wrapper.__name__
     
        for k,v in kw.items():
            #logging.info("k: %s \t v: %s", k, v)
            if not k in ["is_reload", "memcache_delete", "get_key_name"]:
                key_name += '_' + k + '_' + unicode(v)

        kw["key_name"] = key_name
        
        if kw.has_key("get_key_name"):
            return key_name
        
        if kw.has_key("memcache_delete"):
            memcache.delete(key = key_name)
            cache_delete(key_name) 
            logging.info("Remove Memcache Key: %s", key_name)
            return None

        elif not kw.has_key("is_reload") and key_name != _wrapper.__name__:
            
            results = cache_get(key_name) 
            
            if results is not None:
                return results

                #return None                 
            
            #results = memcache.get(key = key_name)            
            #if results is not None:
            #    logging.info("Memcache: %s", key_name)
            #    return results            
                
        if key_name == _wrapper.__name__:
            logging.error("FUNCTION without args: %s", key_name)
        
        logging.info("Database: %s", key_name)

        return handler( *args, **kw)
    _wrapper.__name__ = handler.__name__
    return _wrapper



@check_cache
def eventtypes_browse(sport_id = None, limit = 100,
                 is_reload=None, memcache_delete=None, key_name=""):

    if not sport_id:
        return None

    sport = models.Sport.get_item(sport_id)

    results = models.EventType.gql("WHERE sport_id = :1", sport).fetch(limit)    
    
    for c in results:
        c.title = settings.SPORT_EVENTS[c.name][0] 
        c.img   = settings.SPORT_EVENTS[c.name][1]

    cache_set(key_name , results)    
    return results



########             GROUP            #########


@check_cache
def group_browse(league_id = None, limit=1000,
                 is_reload=None, memcache_delete=None, key_name=""):

    results = []

    league = models.League.get_item(league_id)
    
    if not league:
        return None

    if not league.league_seasons:
        return None
   
    all_groups = models.Group.gql("WHERE league_id = :1", league).fetch(limit)   

    for item in all_groups:
        group_id = item.id        
         
        all_teams = group_reload(league_id = league_id, group_id = group_id)        
        group = {"group": item, "all_teams": all_teams}        
        results.append(group)    


    all_teams = group_reload(league_id = league_id, group_id = None)        
    group = {"group": None, "all_teams": all_teams}        
    results.append(group)       



    include = ["id", "name", "group", "team", "match_played", "won", "drew",
               "loss", "scored", "conceded", "diff", "points", "all_teams", 
               "matches", "place"]
    
    
        
    return cache_set(key_name, results, include, commit = True)
    
    #return cache_set(key_name , results)   
    
    
    
    
def group_reload(league_id = None, group_id = None, limit = 1000):

    scoretype = models.ScoreType.get_item("1001").key()       

    scored_key   = models.ScoreType.get_item("1001").key()
    conceded_key = models.ScoreType.get_item("1002").key()

    won_key  = models.ResultType.get_item("1002").key()
    loss_key = models.ResultType.get_item("1003").key()
    drew_key = models.ResultType.get_item("1004").key()    

    league = models.League.get_item(league_id)
    
    logging.info("League_id: %s",league_id)
    logging.info("Group_id: %s",group_id)    
    
    all_scores = models.Score.gql("WHERE league_id = :1 and scoretype_id = :2 and group_id = :3 ORDER BY created", 
                                        league, scoretype, None).fetch(limit)   

    group = None
    group_key = None    
    
    if group_id:
        group = models.Group.get_item(group_id)
        group_key = group.key()
        
        all_seasons = models.Season.gql("WHERE league_id = :1 and group_id = :2", league, group).fetch(limit)
 
        all_scores_group = models.Score.gql("WHERE league_id = :1 and scoretype_id = :2 and group_id = :3 ORDER BY created", 
                                        league, scoretype, group).fetch(limit)   
                                        
        all_scores.extend(all_scores_group)                                 
    else:
        all_seasons = models.Season.gql("WHERE league_id = :1", league).fetch(limit)
             
    
 
    # 1001 = None    1002 = Wine    1003 = Lose   1004 = Draw   
    results = []
    
    for item in all_seasons:
        results.append(item.team_id)    
     
    team_ids = []    
    
    team_data = {}
       
    for item in results:
        team_ids.append(item.id)            
        
        team_data[item.id] =  {"won":      0,
                               "loss":     0,
                               "drew":     0,
                               "scored":   0,
                               "conceded": 0,}
        
                      
    results = sorted(results, key=lambda student: student.name, reverse=False)   

    for i, v in enumerate(results):           
        v.place = i + 1
        
        
    #logging.info("team_ids: %s",team_ids)

    c = {}        

    for team in results: 
        c[team.id] = {}

        for team2 in results: 
            if team.id == team2.id:
                c[team.id][team2.id] = []
            else:
                c[team.id][team2.id] = []#[None,None,0, 0, 0]

    new_scores = []
    for_del = []

    start = time.time()          
    
    for c1 in all_scores:
        for c2 in all_scores:
        
            #logging.info("c1: %s",c1.match_id.id)
        
            try:
                test = c[c1.team_id.id][c2.team_id.id]
            except:
                continue                      
               
            if not c1.team_id.id in team_ids:
                continue

            if not c2.team_id.id in team_ids:     
                continue                
             
            
            if c1.key() == c2.key():
                continue  
                       
            if not c1.created or not c2.created:      
                continue
                
            try:
                if c1.match_id.playoff_id:
                    continue
            except:
                pass
                
            try:
                if c2.match_id.playoff_id:
                    continue
            except:
                pass                
                    
            #if c1.match_id.playoff_id or c2.match_id.playoff_id:     
            #    continue         
            
            gametype = None

            try:
                value1 = int(c1.value)
                value2 = int(c2.value)   
                gametype = 2
                                          
                if value1 > value2:
                    game_result = 1
                elif value1 < value2:
                    game_result = 2
                else:
                    game_result = 0
            except:
                value1 = 0
                value2 = 0
                gametype = 1
                game_result = 0
            
            try:
                if c1.match_id.id == c2.match_id.id:
                    c[c1.team_id.id][c2.team_id.id].append(
                        [c1.match_id.id, gametype, value1, value2, game_result])
                    
                    if gametype == 2:
                        if game_result == 1:
                            team_data[c1.team_id.id]["won"]  += 1
                        if game_result == 2:
                            team_data[c1.team_id.id]["loss"] += 1
                        if game_result == 0:
                            team_data[c1.team_id.id]["drew"] += 1  
                                                       
                    team_data[c1.team_id.id]["scored"]   += value1 
                    team_data[c1.team_id.id]["conceded"] += value2    
            except:
                pass
                                

    #logging.info("##################################", )
    

    league_key = league.key()
        
    for team in results: 
        team_key   = team.key()
        
        '''
        team.won  = team_results(league_key, team_key, won_key,  
                                 group_key = group_key)
                                 
        team.loss = team_results(league_key, team_key, loss_key,  
                                 group_key = group_key)
                                 
        team.drew = team_results(league_key, team_key, drew_key,  
                                 group_key = group_key)    
        '''
        team.won  = team_data[team.id]["won"]
        team.loss = team_data[team.id]["loss"]
        team.drew = team_data[team.id]["drew"]
        
        team.match_played = team.won + team.loss + team.drew
        team.points = (team.won * 3) + team.drew           
        
        '''
        team.scored   = score_results(league_key, team_key, 
                                      scored_key, group_key = group_key)
                                      
        team.conceded = score_results(league_key, team_key, 
                                      conceded_key, group_key = group_key)   
        '''
        
        team.scored   = team_data[team.id]["scored"]
        team.conceded = team_data[team.id]["conceded"]
        team.diff = team.scored - team.conceded
    
    results = sorted(results, key=lambda student: student.points, reverse=True)   

    for i, v in enumerate(results):           
        v.place = i + 1
        
    for i, team1 in enumerate(results):           
        for j, team2 in enumerate(results): 
            t1 = results[i]
            t2 = results[j] 

            if t1.key() == t2.key():
                continue

            if t1.points == t2.points:
                team_score1 = 0
                team_score2 = 0

                
                team_score1 = 0
                team_score2 = 0

                '''
                try:                
                    team_score1 += c[t1.id][t2.id][2]
                except:
                    pass

                try:
                    team_score1 += c[t2.id][t1.id][3]
                except:
                    pass

                try:
                    team_score2 += c[t1.id][t2.id][3]
                except:
                    pass

                try:
                    team_score2 += c[t2.id][t1.id][2]
                except:
                    pass
                '''
                
                try:
                    for matches in c[t1.id][t2.id]:
                        team_score1 += matches[2]    
                        team_score2 += matches[3]                          
                except:
                    pass                                    
                
                try:
                    for matches in c[t2.id][t1.id]:
                        team_score1 += matches[3]    
                        team_score2 += matches[2]                          
                except:
                    pass                   

                replace = False
    
                if (team_score1 < team_score2 and t1.place < t2.place) or (team_score1 > team_score2 and t1.place > t2.place):
                    replace = True                 

                if team_score1 == team_score2:
                    if (t1.diff < t2.diff and t1.place < t2.place) or (t1.diff > t2.diff and t1.place > t2.place): 
                        replace = True

                    elif (t1.won < t2.won and t1.place < t2.place) or (t1.won > t2.won and t1.place > t2.place):            
                        replace = True

                if replace:
                    k = results[i].place
                    results[i].place = results[j].place
                    results[j].place = k       
                
    results = sorted(results, key=lambda student: student.place, reverse=False)              
            
    cross_table = []
    
    # Filling Cross Table 
    
    for item in results:
        item_table = {}
        item_table["team"] = item
        item_table["matches"] = []
        
        for item2 in results:        
            try:                              
                item_table["matches"].append(c[item.id][item2.id])
            except:  
                try:
                    item_table["matches"].append([])
                except:                    
                    t = 0

        #logging.info("item_table: %s", item_table)
        #logging.info("%s.\t%s", item.place, item.name)
        cross_table.append(item_table)

    end3 = round(time.time() - start, 6)  

    logging.info("Cross Table  all_scores  time: %s", end3)
                  
    return cross_table  


def group_create(league_id = None, size = 8, name = "PlayOff", limit = 1000):

    all_stages = models.GroupStage.all().count()
    if all_stages < 1:
    
        params = {   'name': 'final'    }  
        models.GroupStage.create(params)

        params = {   'name': 'semi-final'    }  
        models.GroupStage.create(params)    
    
        params = {   'name': 'quarter-final'    }  
        models.GroupStage.create(params)
        logging.info("Create Group Stages")
        

    league = models.League.get_item(league_id)
    tournament = league.tournament_id
    
    group = models.Group.gql("WHERE league_id = :1", league).get()    
    if group is None:  
    
        params = {    'tournament_id': tournament,
                      'league_id':     league,
                      'size':          size,
                      'name':          name,
                }
            
        group = models.Group.create(params)            
    
    if size >= 8:    
        stage = models.GroupStage.gql("WHERE name = :1", "quarter-final").get()    
        params = {    'tournament_id': tournament,
                      'league_id':     league,
                      'group_id':    group,
                      'groupstage_id':      stage,
                  }                               
        for i in xrange(4):       
            group_node = models.GroupNode.create(params)     
            
            params_node = {'tournament_id': tournament,
                      'league_id':     league,
                      'group_id':    group,
                      'groupstage_id':      stage,
                      'groupnode_id': group_node,                      
                  }    
            models.GroupCompetitor.create(params_node)
            models.GroupCompetitor.create(params_node)            

    if size >= 4:    
        stage = models.GroupStage.gql("WHERE name = :1", "semi-final").get()    
        params = {    'tournament_id': tournament,
                      'league_id':     league,
                      'group_id':    group,                      
                      'groupstage_id':      stage,
                  }                               
        for i in xrange(2):            
            group_node = models.GroupNode.create(params)
                
            params_node = {'tournament_id': tournament,
                      'league_id':     league,
                      'group_id':    group,
                      'groupstage_id':      stage,
                      'groupnode_id': group_node,                      
                  }    
            models.GroupCompetitor.create(params_node)
            models.GroupCompetitor.create(params_node)                 
            
    if size >= 1:
        stage = models.GroupStage.gql("WHERE name = :1", "final").get()    
        params = {    'tournament_id': tournament,
                      'league_id':     league,
                      'group_id':    group,                      
                      'groupstage_id':      stage,
                  }                               
        group_node = models.GroupNode.create(params)    
        
        
        params_node = {'tournament_id': tournament,
                      'league_id':     league,
                      'group_id':    group,
                      'groupstage_id':      stage,
                      'groupnode_id': group_node,                      
                  }    
        models.GroupCompetitor.create(params_node)
        models.GroupCompetitor.create(params_node)                      
                     
    group_browse(league_id = league_id, is_reload = True)                     
                                
    return True
    

def group_remove(group_id = None, league_id = None, limit = 1000):

    item = models.Group.get_item(group_id)
   
    
    if item:
        rem  = models.Match.gql("WHERE group_id = :1", item).fetch(limit)
        db.delete(rem)                
        rem = models.Competitor.gql("WHERE group_id = :1", item).fetch(limit)  
        db.delete(rem)
        rem = models.GroupCompetitor.gql("WHERE group_id = :1", item).fetch(limit)  
        db.delete(rem)
        rem = models.GroupNode.gql("WHERE group_id = :1", item).fetch(limit)  
        db.delete(rem)

        db.delete(item)

    models.Group.update(group_id)
    


    league_update_task(league_id = league_id)        

    
def group_get_nodeteams(groupnode_id = None, limit = 1000):

    groupnode = models.GroupNode.get_item(groupnode_id)
    
    if not groupnode:
        return False
        
    competitors = models.GroupCompetitor.gql("WHERE groupnode_id = :1 ORDER BY created ASC", groupnode).fetch(limit)
    
    results = []
    
    for item in competitors:
        try:
            results.append(item.team_id.id)
        except:
            pass
               
    return results

    
def group_set(league_id = None, request = None, limit = 1000):    

    team_id       = request.POST["team_id"]
    competitor_id = request.POST["competitor_id"]    
        
    logging.info("team_id: %s",team_id)
    logging.info("competitor_id: %s",competitor_id)

    competitor = models.GroupCompetitor.get_item(competitor_id)
    team =  models.Team.get_item(team_id)    
    
    competitor.team_id = team
    competitor.put()
    
    group_browse(league_id = league_id, is_reload = True)



def image_get(team_ref): 

    item = models.Image.gql("WHERE team_id = :1 ORDER BY created DESC", team_ref).get()    
    
    if item:
        return (settings.GOOGLE_BUCKET + item.photo_small)

    return (settings.GOOGLE_BUCKET + "images/anonymous_team.png")



@check_cache
def league_browse(tournament_id = None, limit = 100,
                 is_reload=None, memcache_delete=None, key_name=""):

    tournament = models.Tournament.get_item(tournament_id)
  
    if not tournament:    
        return None
        
    results = models.League.gql("WHERE tournament_id = :1 ORDER BY id ASC", tournament).fetch(limit)
            
    new_res = []
    
    include = ["id", "name", "ranking", "tournament_id", "sport_id"]    
    

    logging.info("settings.DEBUG: %s",settings.DEBUG)
    
    if settings.DEBUG == True:
        return cache_set(key_name, results, include)               
        
        
    if tournament_id == "1002":       
        for item in results:
            if int(item.id) >= int("1100"):
                new_res.append(item)    
                
        return cache_set(key_name, new_res, include)   
        
    if tournament_id == "1003":       
        for item in results:
            if int(item.id) >= int("1084"):
                new_res.append(item)    
                
        return cache_set(key_name, new_res, include)           
 

    if tournament_id == "1007":       
        for item in results:
            if int(item.id) >= int("1111"):
                new_res.append(item)    
                
        return cache_set(key_name, new_res, include)   
    
    if tournament_id in ["1001", "1003","1008"]:       
        for item in results:
            if int(item.id) >= int("1068"):
                new_res.append(item)    
                
        return cache_set(key_name, new_res, include)

    return cache_set(key_name, results, include)


def league_create(request, **kw):

    tournament_ref = models.Tournament.get_item(request.POST["tournament_id"])

    if not request.is_owner:
        return None
    
    params = {'name': request.POST["league_name"],
              'tournament_id': tournament_ref.key(),
            }
    new_league = models.League.create(params)
    league_id = new_league.id

    league_get(league_id = league_id, is_reload = True)
    league_browse(tournament_id = tournament_ref.id, is_reload = True)


    return new_league.id

   
@check_cache
def league_get(league_id = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
                 
                 
    results = models.League.get_item(league_id)

    #if league_id == "1002":
    #    models.League.update(league_id)
    #    logging.info("Updated league 1002")
    
    return cache_set(key_name , results)
    



def league_cross_table(league, limit=1000):
    
    if not league.league_seasons:
        return None

    c = {}
    all_competitors = models.Competitor.gql("WHERE league_id = :1", league).fetch(limit)
    for c1 in all_competitors:
        c[c1.team_id.id] = {}

        for c2 in all_competitors:
            if c1.key() == c2.key():               
                continue
            if c1.created > c2.created:
                continue

            if c1.match_id.key() == c2.match_id.key():
                c[c1.team_id.id][c2.team_id.id] = c1.match_id

    return c


def replace_items(value1, value2):
    value1 = k
    value1 = value2
    value2 - k
    

    
'''
@check_cache
def league_table(league_id = None, group_id = None, limit=1000,
                 is_reload=None, memcache_delete=None, key_name=""):

    league = models.League.get_item(league_id)

    if not league.league_seasons:
        return None

    c = {}     
        
    scoretype = models.ScoreType.get_item("1001")

    #rv = [season.team_id.key() for season in league.league_seasons]                        
    #results = models.Team.get(rv)
    
    if group_id:
        group = models.Group.get_item(group_id)
        all_seasons = models.Season.gql("WHERE league_id = :1 and group_id = :2", league).fetch(limit)
        all_scores = models.Score.gql("WHERE league_id = :1 and scoretype_id = :2 and group_id IN :3 ORDER BY created", 
                                        league, scoretype, [None, group]).fetch(limit)   
    else:
        all_seasons = models.Season.gql("WHERE league_id = :1", league).fetch(limit)
        all_scores = models.Score.gql("WHERE league_id = :1 and scoretype_id = :2 and group_id IN :3 ORDER BY created", 
                                        league, scoretype, [None]).fetch(limit)   
    
    
    
    for item in all_seasons:
        results.append(item.team_id)

    # 1001 = None    1002 = Wine    1003 = Lose   1004 = Draw   

    for team in results: 
        c[team.id] = {}

        for team2 in results: 
            if team.id == team2.id:
                c[team.id][team2.id] = None
            else:
                c[team.id][team2.id] = [None,None,0, 0, 0]

    new_scores = []
    for_del = []

    start = time.time()      
    
    
    for c1 in all_scores:
        for c2 in all_scores:
            if not c[c1.team_id.id][c2.team_id.id]:
                continue
            
            if c1.key() == c2.key():
                continue         
            if not c1.created or not c2.created:      
                continue
                
            if c1.match_id.playoff_id or c2.match_id.playoff_id:     
                #logging.info("Skip Playoff Match: %s\t%s",c1.match_id.id, c2.match_id.id)
                continue           
                
            #if c1.created > c2.created:
            #    continue

            
            gametype = None

            try:
                value1 = int(c1.value)
                value2 = int(c2.value)   
                gametype = 2
            
                if value1 > value2:
                    game_result = 1
                elif value1 < value2:
                    game_result = 2
                else:
                    game_result = 0
            except:
                value1 = 0
                value2 = 0
                gametype = 1
                game_result = 0

            if c1.match_id.key() == c2.match_id.key():                                     
                c[c1.team_id.id][c2.team_id.id] = [c1.match_id.id, gametype, value1, value2, game_result]
                
    for item in results:
        allp = ""
        for item2 in results:
            try:              
                #item_table.append(c[item.id][item2.id])
                allp += c[item.id][item2.id][0] + '\t'
            except:
                allp += '\t'


        #logging.info("%s", allp)


    #logging.info("##################################", )

    scored_key   = models.ScoreType.get_item("1001").key()
    conceded_key = models.ScoreType.get_item("1002").key()

    won_key  = models.ResultType.get_item("1002").key()
    loss_key = models.ResultType.get_item("1003").key()
    drew_key = models.ResultType.get_item("1004").key()
    
        
    for team in results: 
        
        team.won  = team_results(league.key(), team.key(), won_key)
        team.loss = team_results(league.key(), team.key(), loss_key)
        team.drew = team_results(league.key(), team.key(), drew_key)    
        team.match_played = team.won + team.loss + team.drew
        team.points = (team.won * 3) + team.drew           
        
        team.scored   = score_results(league.key(), team.key(), scored_key)
        team.conceded = score_results(league, team.key(), conceded_key)   
        team.diff = team.scored - team.conceded
    
    results = sorted(results, key=lambda student: student.points, reverse=True)   

    for i, v in enumerate(results):           
        v.place = i + 1
        
    for i, team1 in enumerate(results):           
        for j, team2 in enumerate(results): 
            t1 = results[i]
            t2 = results[j] 

            if t1.key() == t2.key():
                continue

            if t1.points == t2.points:
                team_score1 = 0
                team_score2 = 0

                
                team_score1 = 0#c[t1.id][t2.id][2] + c[t2.id][t1.id][3]
                team_score2 = 0#c[t1.id][t2.id][3] + c[t2.id][t1.id][2]
    


                try:
                    team_score1 += c[t1.id][t2.id][2]
                except:
                    pass

                try:
                    team_score1 += c[t2.id][t1.id][3]
                except:
                    pass

                try:
                    team_score2 += c[t1.id][t2.id][3]
                except:
                    pass

                try:
                    team_score2 += c[t2.id][t1.id][2]
                except:
                    pass
       

                replace = False
    
                if (team_score1 < team_score2 and t1.place < t2.place) or (team_score1 > team_score2 and t1.place > t2.place):
                    replace = True                 

                if team_score1 == team_score2:
                    if (t1.diff < t2.diff and t1.place < t2.place) or (t1.diff > t2.diff and t1.place > t2.place):                       
                        replace = True

                    elif (t1.won < t2.won and t1.place < t2.place) or (t1.won > t2.won and t1.place > t2.place):            
                        replace = True

                if replace:
                    k = results[i].place
                    results[i].place = results[j].place
                    results[j].place = k       
                
    results = sorted(results, key=lambda student: student.place, reverse=False)              
            
    cross_table = []
    
    for item in results:
        item_table = [item]
        allp = ""
        for item2 in results:
            try:              
                item_table.append(c[item.id][item2.id])

                #allp += c[item.id][item2.id][0] + '\t'
                t = 0
            except:
                t = 0
                allp += '\t'


        #logging.info("%s", allp)
        #logging.info("%s.\t%s", item.place, item.name)
        cross_table.append(item_table)

    end3 = round(time.time() - start, 6)  

    logging.info("Cross Table  all_scores  time: %s", end3)
        
    results = cross_table
                  
    return cache_set(key_name , results)
'''

def league_update(league_id = None, limit = 1000):

    league = models.League.get_item(league_id)
    tournament = league.tournament_id   
    tournament_id = tournament.id       
    
    deferred.defer(group_browse, league_id = league_id, is_reload = True)
    
    deferred.defer(stat_league, league_id = league_id, is_reload = True)

    deferred.defer(statistics, league_id = league_id, is_reload = True)
    deferred.defer(statistics, league_id = league_id, limit = 1000, is_reload = True)

    deferred.defer(match_browse, tournament_id = tournament_id, is_reload = True) 
    deferred.defer(match_browse, league_id = league_id, is_reload = True)
    deferred.defer(match_browse, tournament_id = tournament_id, league_id = league_id, is_reload = True)     
    

    deferred.defer(playoff_browse, league_id = league_id, is_reload = True)
    
    deferred.defer(team_browse_rating, tournament_id = tournament_id, is_reload = True)
    
    deferred.defer(referees_browse, tournament_id = tournament_id, stat = True, is_reload = True)    
    
    return True


def league_update_task(league_id = None):
    return taskqueue.add(url='/league/update/', method = 'POST', params=dict(league_id = league_id))
    
    
def league_upload(request, league = None, limit = 1000):

    tournament = league.tournament_id
    
    img = request.FILES['img'].read()
 

    tmp = img.decode('cp1251').split('table')[1]

    del_teams = []
        
    
    all_teams = models.Season.gql("WHERE league_id = :1", league).fetch(limit)
    '''
    for team in all_teams:
        
        #del_team = models.Team.gql("WHERE id = :1", team.team_id.id).fetch(limit)
        del_teams.append(team)

    models.db.delete(del_teams)

    return None
    all_teams = []
    '''





    all_players = tmp.split('<tr>')

    for item in all_players[2:]:

        value = item.split('<td>')

        try:
            player_full_name = value[2].split('<')[0]
            team_name = value[3].split('<')[0]

        except:
            continue

        '''
        if not team_name in all_teams:
            all_teams.append(team_name)
            logging.info("%s", team_name)
        '''

        team_id = None

        
        for team in all_teams:
            #logging.info("%s\t%s", team_name , team.team_id.name)
            if team_name == team.team_id.name:
                team_id = team.team_id.id
                #logging.info("%s", team.team_id.name)
                break
        if not team_id:
                logging.info("Team Not Found:\t%s", team_name)
        else:
            name = ""
            second_name = ""
            tmp = player_full_name.split(' ')
  
            try:
                second_name = tmp[0]
                second_name = second_name[0] + second_name[1:].lower()
            except:
                t = 0


            try:
                name = tmp[1]
            except:
                t = 0               


            #logging.info("%s\t%s\t%s",second_name, name,  team_name)
            all_players = models.PlayerTeam.gql("WHERE team_id = :1", team.team_id).fetch(limit)
                
            is_new = True        

            for player in all_players:
                if player.player_id.second_name == second_name:
                    is_new = False
                    break

            if is_new:
                try:
                    params = {
                                'tournament_id': tournament, 
                                'name': name,
                                'second_name': second_name,
                          }

                    player_ref = models.Player.create(params)
                


                    params = {
                                'tournament_id': tournament,
                                'player_id':     player_ref,
                                'team_id':      team.team_id,
                        }
                


                    teamplayer_ref = models.PlayerTeam(**params)
                    teamplayer_ref.put()
                    logging.info("Player Created:\t%s\t%s\t%s",second_name, name, team_name)
                except:
                    logging.error("Error  Player Created :\t%s\t%s\t%s",second_name, name, team_name)                    
            else:
                if not player.player_id.name and name:
                        edit_player = models.Player.gql("WHERE id = :1", player.player_id.id).get()
                        edit_player.name = name
                        edit_player.put()           
                        logging.info("Player Edit:\t%s\t%s\t%s",second_name, name, team_name)         
                else:
                     if name and len(player.player_id.name) < 3 and player.player_id.name[0] == name[0]:
                        edit_player = models.Player.gql("WHERE id = :1", player.player_id.id).get()
                        edit_player.name = name
                        edit_player.put()
                        logging.info("Player Edit:\t%s\t%s\t%s",second_name, name, team_name)
                
            


          

    '''
    for team_name in all_teams:
        
        params = {'name': team_name,
              'tournament_id': tournament,
                }
    
        team_ref = models.Team.create(params)
    
        params_season = {'tournament_id': tournament,
                     'league_id':     league,
                     'team_id':       team_ref.key(),
                }


        season_ref = models.Season(**params_season)
        season_ref.put()        
    '''
    #logging.info("%s\t%s\t%s", player_full_name, team_name, team_id)



    #print tmp
    #tmp = tmp.split(u'БОМБАРДИРЫ')[1].split("size=2")[1].split("</FONT>")[0]





    
def league_remove(league_id = None, limit=100):
    
    logging.info("DEl Value: %s", league_id)    

    del_mas = [ models.Image, models.Season, models.Competitor, models.Score, 
                models.PlayerMatch, models.StatPlayer, models.Group,
                models.Match, models.RefereeMatch, models.Playoff,  
                models.PlayoffNode, models.PlayoffCompetitor, models.Sanction ]
    
    del_value = models.League.get_item(league_id)

    tournament_id = del_value.tournament_id.id

    logging.info("DEl Value: %s", league_id)    
    
    hub = []
    
    if del_value:       
        for item in del_mas:
            try:
                rem  = item.gql("WHERE league_id = :1", del_value).fetch(limit)
                hub.append(db.delete_async(rem))
                #db.delete(rem)
            except:
                pass
            
        db.delete(del_value)

    for item in hub:
        item.get_result()
 
    logging.info("Legue Deleted")            
                
    league_browse(tournament_id = tournament_id, is_reload = True)

    models.League.update(league_id)

    return True
    

    
def league_remove_team(league_id = None, group_id = None, team_id = None, limit=5000):
    
    league = models.League.get_item(league_id)
    group  = models.Group.get_item(group_id)
    team   = models.Team.get_item(team_id) 
    
    if group is None:
        season = models.Season.gql("WHERE league_id = :1 and team_id = :2", league, team).get()
    else:
        season = models.Season.gql("WHERE league_id = :1 and team_id = :2 and group_id = :3", league, team, group).get()
        
        
        
    if league.tournament_id.id != team.tournament_id.id:
        return False                
        
    if not season:
        return False        
        
    del_mas = [  models.Match, models.RefereeMatch, models.Competitor, 
                 models.Score, models.PlayerMatch, models.Event,
                 models.Sanction, models.StatPlayer ]
    
    
    del_value = season
    hub = []
    
    if del_value:       
        for item in del_mas:
            try:
                rem  = item.gql("WHERE season_id = :1", del_value).fetch(limit)
                hub.append(db.delete_async(rem))
                #db.delete(rem)
            except:
                pass
                
                
        for item in hub:
            item.get_result()
            
        db.delete(del_value)

 
    logging.info("TeamSeason Deleted")         

    league_update_task(league_id = league.id)

    return True


#######

@check_cache
def match_browse(tournament_id = None, league_id = None, team_id = None, referee_id = None, limit=50, offset=0,
                 is_reload=None, memcache_delete=None, key_name=""):

    results = None

    if league_id and tournament_id:
        
        today =  datetime.date.today()
        league_ref = models.League.get_item(league_id)        

        results = models.Match.gql("WHERE league_id = :1 AND datetime >= :2 ORDER BY datetime ASC", league_ref, today).fetch(limit, offset)
        last = None
        for item in results:
            current_date = item.datetime.strftime("%d/%m/%y")
            if last != current_date:
                item.is_new_date = True
                last = current_date

            item.sanctions = models.Sanction.gql("WHERE match_id = :1", item).fetch(limit)
    
    elif league_id:
        
        league_ref = models.League.get_item(league_id)
        results = models.Match.gql("WHERE league_id = :1 ORDER BY datetime DESC", league_ref).fetch(limit, offset)
        
    elif team_id:
        

        team_ref = models.Team.get_item(team_id)
        team_competitors = models.Competitor.gql("WHERE team_id = :1 ORDER BY created DESC", team_ref).fetch(limit, offset)

        
        #team_ref = models.Team.get_item(team_id).team_competitors.fetch(limit, offset)
        
        rv = []    
        for c in team_competitors:
            try:
                rv.append(c.match_id.key()) 
            except:
                pass
                
                
        results = models.Match.get(rv)    
        results = sorted(results, key=lambda student: student.datetime, reverse=True)  
        #results = models.Match.gql("WHERE __key__ IN = :1 ORDER BY datetime DESC", rv).fetch(limit, offset)
            
    elif tournament_id:

        tournament = models.Tournament.get_item(tournament_id)               
        
        today =  datetime.datetime.now() - datetime.timedelta(hours=20)
        
        results = models.Match.gql("WHERE tournament_id = :1 AND datetime >= :2 ORDER BY datetime ASC", tournament, today).fetch(20, offset)
        last = None
        for item in results:
            current_date = item.datetime.strftime("%d/%m/%y")
            if last != current_date:
                item.is_new_date = True 
                last = current_date
                
    elif referee_id:                
        referee = models.Referee.get_item(referee_id)
        referee_matches = models.RefereeMatch.gql("WHERE referee_id = :1 ORDER BY created DESC", referee).fetch(limit, offset)
        
        
        #team_ref = models.Team.get_item(team_id).team_competitors.fetch(limit, offset)
        rv = []    
        for c in referee_matches:
            try:
                rv.append(c.match_id.key()) 
            except:
                pass
                
        results = models.Match.get(rv)    
        results = sorted(results, key=lambda student: student.datetime, reverse=True)  
        #results = models.Match.gql("WHERE __key__ IN = :1 ORDER BY datetime DESC", rv).fetch(limit, offset)    
       
    if results:
        
        #start = time.time()            
        #end1 = round(time.time() - start, 6)
        #start = time.time()                                                                   
        #end2 = round(time.time() - start, 6)
        
        for match in results:
            match.teams = []
            
            all_competitors = models.Competitor.gql("WHERE match_id = :1 ORDER BY created", match).fetch(limit)
            
            for team in all_competitors: #match.match_competitors.fetch(limit):
                #new_team = models.Team.get_item(team.team_id.id)
                new_team = team.team_id
                try:
                    #new_team.score = int(team.competitor_scores[0].value)
                    #new_team.played = True
                    
                    if team.competitor_scores[0].scoretype_id.id == "1001":
                        new_team.score = int(team.competitor_scores[0].value)
                        new_team.played = True
                
                    elif team.competitor_scores[1].scoretype_id.id == "1001":
                        new_team.score = int(team.competitor_scores[1].value)                    
                        new_team.played = True                        
                except:
                    t = 0
                    #logging.info("Except Team:  %s", team.team_id.name)
                '''
                if team.competitor_scores.count() > 1:
                    if team.competitor_scores[0].value:
                        logging.info("Team:  %s \t score: %s", team.team_id.name, int(team.competitor_scores[0].value))
                        new_team.score = int(team.competitor_scores[0].value)
                    new_team.played = True
                '''
                match.teams.append(new_team)           

            if team_id:
                try:
                    if match.teams[0].id == team_id:
                        if match.teams[0].score > match.teams[1].score:
                            match.result = 1

                        elif match.teams[0].score < match.teams[1].score:
                            match.result = 2

                    elif match.teams[1].id == team_id:
                        if match.teams[0].score > match.teams[1].score:
                            match.result = 2
    
                        elif match.teams[0].score < match.teams[1].score:
                            match.result = 1
                except:
                    t = 0
       
       
    include = ["id", "name", "datetime", "is_new_date","score", "played", "result", "teams", "sanctions"]
    
    
    return cache_set(key_name, results, include, commit = True)

 
    
    
def match_create_complete(league_id = None, team1_id = None, team2_id = None, full_datetime = None,
                                     referee_id = None, place = None, playoffnode_id = None, group_id = None,limit = 1000):    

   
    match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
    
    scoretype = models.ScoreType.get_item("1001")
    
    league_ref = models.League.get_item(league_id)

    season_ref = db.GqlQuery("SELECT __key__ FROM Season WHERE league_id = :1", league_ref).get()

    #if not season_ref:
    #    return None

    tournament_ref = league_ref.tournament_id

    if not tournament_ref:
        logging.error("No tournament")
        return None
        
    team1 = models.Team.get_item(team1_id)       
    team2 = models.Team.get_item(team2_id)           

    team_refs = [team1, team2]    
    
    playoff      = None
    playoffstage = None                   
    playoffnode  = None    
    
    if playoffnode_id:
        playoffnode  = models.PlayoffNode.get_item(playoffnode_id)
        playoff      = playoffnode.playoff_id
        playoffstage = playoffnode.playoffstage_id      
        
    group  = models.Group.get_item(group_id)              

    params = {'datetime' : match_datetime,
              'tournament_id': tournament_ref,
              
              'league_id': league_ref,
              'season_id': season_ref,
              
              'playoff_id':       playoff,         
              'playoffstage_id':  playoffstage,                         
              'playoffnode_id':   playoffnode,
              
              'group_id':         group,              
              
                  
              'place': place,
             }  
    
    match_ref = models.Match.create(params)
    
    
    values = []
    for team_ref in team_refs:



        params = {'match_id': match_ref,
                  'team_id' : team_ref,

                  'tournament_id': tournament_ref,
                  
                  'ranking': 0,                  
                  
                  'league_id': league_ref,
                  'season_id': season_ref,
                  
                  'playoff_id':       playoff,         
                  'playoffstage_id':  playoffstage,                         
                  'playoffnode_id':   playoffnode,
                  
                  'group_id':         group, 
                }

        competitor_ref = models.Competitor(**params)
        competitor_ref.put()
   
 

        params = {'match_id':      match_ref,
                  'team_id' :      team_ref,

                  'tournament_id': tournament_ref,
                  'league_id':     league_ref,
                  'season_id':     season_ref,
             
                  'competitor_id': competitor_ref,
                  'scoretype_id':  scoretype,
                  
                  'group_id':      group, 
                }
        score_ref = models.Score(**params)
        score_ref.put()


    
    new_playermatches = []
    teamplayers = models.PlayerTeam.gql("WHERE team_id IN :1 AND active = :2", [team1.key(), team2.key()], True).fetch(limit)

    for item in teamplayers:  
        
        params = {
                  'match_id': match_ref,
                  'team_id' : item.team_id.key(),

                  'tournament_id': tournament_ref,
                  'league_id': league_ref,
                  'season_id': season_ref,
                  
                  'ranking': 0,     
                      
                  'player_id': item.player_id.key(),
                      
               }
              
        playermatch_ref = models.PlayerMatch(**params)
        new_playermatches.append(playermatch_ref) 

    db.put(new_playermatches)

    if referee_id:
        new_referee = models.Referee.get_item(referee_id)
        if new_referee:
            if new_referee.tournament_id.key() == match_ref.tournament_id.key():
                params = {
                       
                      'match_id': match_ref,
                      'referee_id' : new_referee,
    
                      'tournament_id': tournament_ref,
                      'league_id': league_ref,
                      'season_id': season_ref,
    
                    }
    
            refereematch_ref = models.RefereeMatch(**params)
            refereematch_ref.put()  

        deferred.defer(referee_get,  referee_id = referee_id, is_reload = True)                   
        deferred.defer(match_browse, referee_id = referee_id, is_reload = True)                   

    league_update_task(league_id = league_id)         
    
    for team_ref in team_refs: 
        team_id = team_ref.id
        deferred.defer(match_browse, team_id = team_id, is_reload = True)          
        
    return True


def match_create(request):

    league_id  = request.POST["league_id"]
    playoffnode_id = request.POST["playoffnode_id"]    
    group_id = request.POST["group_id"]       

    team1_id = request.POST["team1"]
    team2_id = request.POST["team2"]
   
    match_date     = request.POST["datepicker"]
    match_time     = request.POST["timepicker"]
    referee_id        = request.POST["referee"]

    place        = request.POST["place"]
    
    match_date = match_date.replace("-",".")    
    
    match_time = match_time.replace(".",":")
    match_time = match_time.replace("-",":")    
    match_time = match_time.replace(",",":")    
    
    full_datetime  = str(match_date) + " " + str(match_time)
    #match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
    
    deferred.defer(match_create_complete, league_id = league_id, team1_id = team1_id, team2_id = team2_id, full_datetime = full_datetime,
                                     referee_id = referee_id, place = place, playoffnode_id = playoffnode_id, group_id = group_id)  
    
    return True


def match_edit(post_data, limit=1000):
        
   
       
    all_events = {}

    s = urllib.unquote(str(post_data["post_data"]))

    s = s.decode("utf-8")

    #logging.info(s)

    goals = []
    all_events["all-goals"] = []
    new_player = ""
    i = 0
    ss = s.split("&")   # it's correct
    for s in ss:
        p = s.split("=")
        if not p[0] in all_events:
            all_events[p[0]] = []
        
        if p[0].find("goals_") == 0:
            if len(p[1]) > 0:
                if int(p[1]) > 0:
                    for i in xrange(int(p[1])):
                        goals.append(p[0][6:])
                        all_events["all-goals"].append(p[0][6:])
               
        all_events[p[0]].append(p[1])           


    match_id  = all_events["match_id"][0]
    
    match = models.Match.get_item(match_id)


    league = match.league_id    
    league_id = league.id
       
    tournament = match.tournament_id
    tournament_id = tournament.id    

    match_ref = match
   
    match_date     = all_events["datepicker"][0]
    match_time     = all_events["timepicker"][0] 
    
    full_datetime  = str(match_date) + " " + str(match_time)
    match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
    

    match_ref.place = all_events["place"][0]
        
    match_ref.datetime = match_datetime
    match_ref.put()
    match_ref.update(match_ref.id)
       


    playoff      = None
    playoffstage = None                   
    playoffnode  = None    
    
    if match.playoff_id:
        playoff      = match.playoff_id
        playoffnode  = match.playoffnode_id        
        playoffstage = match.playoffstage_id    
        
    group  = None    
    
    if match.group_id:
        group  = match.group_id        
           

    ranking_for_match = 2
    if not match.ranking:
        match.ranking = 1
    
    ranking_team_win  =  match.ranking * league.ranking * ranking_for_match * 4
    ranking_team_drew =  match.ranking * league.ranking * ranking_for_match * 2 
    ranking_team_loss =  match.ranking * league.ranking * ranking_for_match

    ranking_for_goal = match.ranking * league.ranking
    
    
    
    logging.info("Ranking League: %s", league.ranking)
    logging.info("Ranking Match: %s",  match.ranking)
    
    logging.info("Ranking Team Win: %s",  ranking_team_win)
    logging.info("Ranking Team Drew: %s", ranking_team_drew)
    logging.info("Ranking Team Loss: %s", ranking_team_loss)        
    
    logging.info("Ranking For Goal: %s", ranking_for_goal)    
        
    
    #ranking_player = ranking_team +  match.ranking * league.ranking * ranking_for_goal * goals
    #ranking_player = ranking_team +  match.ranking * league.ranking * ranking_for_goal * goals    
  
    #****************************         REMOVE ALL     **************************************#
    

    old_competitors = db.GqlQuery("SELECT * FROM Competitor WHERE match_id = :1", match_ref.key()).fetch(limit)
    
    test_item = None
    
    update_teams = []        
    for item in old_competitors:    
        try:
            item.team_id.ranking -= item.ranking
            update_teams.append(item.team_id)    
            models.Team.update(item.team_id.id)      
        except:
            logging.error("No Team Ranking")                
       
    #db.put(update_teams)      
    s13 = db.put_async(update_teams)
         
    
    old_scores = db.GqlQuery("SELECT __key__ FROM Score WHERE match_id = :1", match_ref.key()).fetch(limit)
    old_events = db.GqlQuery("SELECT __key__ FROM Event WHERE match_id = :1", match_ref.key()).fetch(limit)
    old_referees = db.GqlQuery("SELECT __key__ FROM RefereeMatch WHERE match_id = :1", match_ref.key()).fetch(limit)

    old_sanctions = db.GqlQuery("SELECT __key__ FROM Sanction WHERE match_id = :1", match_ref.key()).fetch(limit)                
        
    old_playermatches = db.GqlQuery("SELECT * FROM PlayerMatch WHERE match_id = :1", match_ref.key()).fetch(limit)        

    update_players = []    
    for item in old_playermatches:
        try:
            #logging.info("Player: %s \t Last ranking: %s \t New Ranking: %s", item.player_id.name,
            #                         item.player_id.ranking, item.player_id.ranking - item.ranking)    
                                     
            item.player_id.ranking -= item.ranking           
            update_players.append(item.player_id)    
            models.Player.update(item.player_id.id)              
        except:
            logging.error("No Player Ranking")
                  
            

       
    
    '''
    db.put(update_players)
    
        
    db.delete(old_competitors)
    db.delete(old_scores)
    db.delete(old_events)
    db.delete(old_referees)
    db.delete(old_playermatches)
    db.delete(old_sanctions)
    '''
    
    s01 = db.put_async(update_players)
    
    s02 = db.delete_async(old_competitors)
    s03 = db.delete_async(old_scores)
    s04 = db.delete_async(old_events)
    s05 = db.delete_async(old_referees)
    s06 = db.delete_async(old_playermatches)
    s07 = db.delete_async(old_sanctions)    
    
    
    
    #****************************         REMOVE ALL     **************************************#    

    #for i in xrange(1001, 1006, )
    #ls_ResultType.append("1001": models.ResultType.get_item("1002"),  "1002": models.ResultType.get_item("1002"), ]
     

    team_refs = []
    
    
    team_refs.append(models.Team.gql("WHERE id = :1",all_events["teams0"][0]).get())
    team_refs.append(models.Team.gql("WHERE id = :1",all_events["teams1"][0]).get())    
    
    
    if team_refs[0] == team_refs[1] or not team_refs[0] or not team_refs[1]:
        return match_id

    team_refs[0].result = None
    team_refs[1].result = None
    
    team_refs[0].add_ranking = 0
    team_refs[1].add_ranking = 0  
        
    #Get Score
    is_played = False     
        
    if "team-score" in all_events and all_events["team-score"][0] and all_events["team-score"][1]:
        is_played = True
 
    if is_played == True:
        score0 = float(all_events["team-score"][0])
        score1 = float(all_events["team-score"][1])
        
                                    
        team_refs[0].score = [{"item": "1001" ,"value": score0}, {"item": "1002" ,"value": score1}]
        team_refs[1].score = [{"item": "1001" ,"value": score1}, {"item": "1002" ,"value": score0}]
        
        logging.info("team_refs[0].score: %s",team_refs[0].score)
        logging.info("team_refs[1].score: %s",team_refs[1].score)
        
        # 1001 = None    1002 = Wine    1003 = Lose   1004 = Draw
        if not team_refs[0].ranking:
            team_refs[0].ranking = 1

        if not team_refs[1].ranking:
            team_refs[1].ranking = 1            
  
           
        if score0 > score1:
            team_refs[0].result      = models.ResultType.get_item("1002")
            team_refs[0].ranking    += ranking_team_win
            team_refs[0].add_ranking = ranking_team_win
            
            team_refs[1].result      = models.ResultType.get_item("1003")
            team_refs[1].ranking    += ranking_team_loss
            team_refs[1].add_ranking = ranking_team_loss            
            
        elif score0 < score1:
            team_refs[0].result      = models.ResultType.get_item("1003")
            team_refs[0].ranking    += ranking_team_loss
            team_refs[0].add_ranking = ranking_team_loss              
            
            team_refs[1].result      = models.ResultType.get_item("1002")
            team_refs[1].ranking    += ranking_team_win     
            team_refs[1].add_ranking = ranking_team_win  
        else:
            team_refs[0].result      = models.ResultType.get_item("1004")
            team_refs[0].ranking    += ranking_team_drew
            team_refs[0].add_ranking = ranking_team_drew              
                        
            team_refs[1].result      = models.ResultType.get_item("1004")
            team_refs[1].ranking    += ranking_team_drew
            team_refs[1].add_ranking = ranking_team_drew              
            
    new_referee = None

    
    referee_id = all_events["referee"][0]
    if referee_id:
        new_referee = models.Referee.get_item(referee_id)
        if new_referee:
            if new_referee.tournament_id.key() == match_ref.tournament_id.key():
                params = {'match_id': match_ref.key(),
                      'referee_id' : new_referee.key(),
    
                      'tournament_id': match_ref.tournament_id,
                      'league_id': match_ref.league_id,
                      'season_id': match_ref.season_id,
                      
    
                    }
    
            refereematch_ref = models.RefereeMatch(**params)


            # Async
            #refereematch_ref.put()               
            s15 = db.put_async(refereematch_ref)
    
    
    #if not (team_refs[0].id == competitors[0].team_id.id and team_refs[1].id == competitors[1].team_id.id):
    new_competitors = []
    new_scores = []
    new_events = []
    new_playermatches = []
    new_sanctions = []

    team_keys = {}
        
    for team_ref in team_refs:    
    
        team_keys[team_ref.id] = team_ref.key()
        
    
        if not team_ref.add_ranking:
            team_ref.add_ranking = 1   

        params = {'match_id': match_ref.key(),
                  'team_id' : team_ref.key(),

                  'tournament_id': match_ref.tournament_id,
                  'league_id': match_ref.league_id,
                  'season_id': match_ref.season_id,
                  
                  'ranking': team_ref.add_ranking,                  
                  
                  'resulttype_id': team_ref.result,
                  
                  'playoff_id':       playoff,         
                  'playoffstage_id':  playoffstage,                         
                  'playoffnode_id':   playoffnode,  
                  
                  'group_id':         group,                  
                }

        competitor_ref = models.Competitor(**params)
        competitor_ref.put()
        
        logging.info("New TEAM: %s \t Ranking: %s", team_ref.name, team_ref.ranking)
        
        
        team_ref.put()
        models.Team.update(team_ref.id)        
        
        #new_competitors.append(competitor_ref)
        
        ######################################################################
        # 1001 = Scored  1002 = Conceded
        
        if is_played == True:        
            for res in team_ref.score:
                params = {'match_id': match_ref.key(),
                          'team_id' : team_ref.key(),
                          'league_id': match_ref.league_id,
                          'season_id': match_ref.season_id,                          
                          'tournament_id': match_ref.tournament_id,
                          'competitor_id': competitor_ref.key(),
                          'scoretype_id': models.ScoreType.get_item(res["item"]),
                          'value'   : res["value"],
                          
                          'group_id':         group,                             
                        }
        
                score_ref = models.Score(**params)
                new_scores.append(score_ref)
        else:

                params = {'match_id': match_ref.key(),
                          'team_id' : team_ref.key(),
                          'league_id': match_ref.league_id,
                          'season_id': match_ref.season_id,                          
                          'tournament_id': match_ref.tournament_id,
                          'competitor_id': competitor_ref.key(),
                          'scoretype_id': models.ScoreType.get_item("1001"),  # empty scored

                          'group_id':         group,                             
                        }
        
                score_ref = models.Score(**params)
                new_scores.append(score_ref)         
                
    s11 = db.put_async(new_scores)                   

    ########################   PlayerMatch  #############################################

    players = []

    if "is_played" in all_events:
        for item in all_events["is_played"]:
            try: 
                value = item.split("_")    
            
                team = models.Team.get_item(value[0])
                if not team:
                    continue
                     
                player = models.Player.get_item(value[1])
                if not player:
                    continue
                
                players.append(value[1])
            
                add_ranking = 0
            
            
                for item in team_refs:
                      # 1001 = None    1002 = Wine    1003 = Lose   1004 = Draw
                    if value[0] ==  item.id:
                        if not item.ranking:
                            item.ranking = 1
                        add_ranking += item.add_ranking 
            
                for goal in goals:
                    player_goal = goal.split("_")[1]
                    if player_goal == value[1]:
                        add_ranking += ranking_for_goal
       
            
                player.ranking += add_ranking
            
            #logging.info("Player: %s \t Last ranking: %s \t New Ranking: %s",
            # player.second_name, player.ranking - add_ranking, player.ranking)            
            
                params = {                                               
                          'match_id'     : match_ref,
                          'tournament_id': match_ref.tournament_id,
                          'league_id'    : match_ref.league_id,
                          'season_id'    : match_ref.season_id,
                          
                          'ranking'      : add_ranking,
                          
                          'team_id'      : team,    
                          'player_id'    : player,
                     }
                     
                playermatch_ref = models.PlayerMatch(**params)
                new_playermatches.append(playermatch_ref) 
                
                player.put()
                models.Player.update(player.id)
            
            except:
                logging.error("Error Save Match %s \t is_played %s", match_ref.id, value)
                pass 
    
    s09 = db.put_async(new_playermatches)
    
        
    if "sanction_player_id" in all_events:
        for item in all_events["sanction_player_id"]:
            try:         
                value = item.split("_")
                if len(value) < 2:
                    continue                          
                          
                team = models.Team.get_item(value[0])
                if not team:
                    continue
                                          
                player = models.Player.get_item(value[1])
                if not player:
                    continue            

                params = {                                               
                          'match_id'     : match_ref,
                          'tournament_id': match_ref.tournament_id,
                          'league_id'    : match_ref.league_id,
                          'season_id'    : match_ref.season_id,
                          
                          'team_id'      : team,    
                          'player_id'    : player,
                     }
                sanction_ref = models.Sanction(**params)
                new_sanctions.append(sanction_ref) 
            
            except:
                logging.error("Error Save Match %s \t Sanction: %s", match_ref.id, value)
                pass            

    s10 = db.put_async(new_sanctions)

    #####################################################################

    goal_key        = models.EventType.get_item("1001").key()
    yellow_card_key = models.EventType.get_item("1002").key()
    red_card_key    = models.EventType.get_item("1003").key()    
    
    
    all_event_types = { "all-goals":   goal_key,
                        "yellow-card": yellow_card_key,
                        "red-card":    red_card_key,
                      }   

 
    for item, event_key in all_event_types.iteritems():    
        if item in all_events:      
            for item in all_events[item]:            
                try:
                    value = item.split("_")                         
                    team = models.Team.get_item(value[0])
                    if not team:
                        continue
                        
                    player = models.Player.get_item(value[1])
                    if not player:
                        continue     
        
                    params = {#'minute'       : int(event_time),
                              'eventtype_id' : event_key,
                              
                              'match_id'     : match_ref,
                              'tournament_id': match_ref.tournament_id,
                              'league_id'    : match_ref.league_id,
                              'season_id'    : match_ref.season_id,
                              
                              'team_id'      : team,  
                              'player_id'    : player,
                           
                              'referee_id'   : new_referee,                           
                            }
                            
                    event_ref = models.Event(**params)
                    new_events.append(event_ref)  
                    
                except:
                    logging.error("Error Save Match %s \t Event: %s", match_ref.id, value)
                    pass             
     
    s12 = db.put_async(new_events)       

    #db.put(new_competitors)

    # Async
    '''
    db.put(new_playermatches)
    db.put(new_sanctions)

    db.put(new_scores)
    db.put(new_events)      
    '''

    try:
        s01.get_result()     
        s02.get_result()    
        s03.get_result()    
        s04.get_result()    
        s05.get_result()    
        s06.get_result()    
        s07.get_result()    

        s09.get_result()        
        s10.get_result()        
        s11.get_result()        
        s12.get_result()        
        s13.get_result()    
        
        s15.get_result()                  
    except:
        pass                                      

    logging.info("Start League Update")


    deferred.defer(match_get, match_id = match_id, is_reload = True)

    league_update_task(league_id = league_id)

    for team_ref in team_refs:   
        team_id = team_ref.id    
        
        #stat_update(league_id = league_id, team_id = team_ref.id)
        deferred.defer(stat_update, league_id = league_id, team_id = team_id)        
        deferred.defer(match_browse, team_id = team_id, is_reload = True) 

    logging.info("League Update Complete.")
    
    
    if is_played == True:        
        deferred.defer(rating_update, tournament_id = tournament_id, _target = "defworker")    

        for team_ref in team_refs: 
            team_id = team_ref.id
        
            deferred.defer(team_get, team_id = team_id, is_reload = True)  
            deferred.defer(team_get_players, team_id = team_id, stat = True, is_reload = True)        
        
        #######     Teams players update Statistics  ########
                
        for player_id in players:        
            deferred.defer(player_get, player_id = player_id, is_reload = True, _queue = "players")
            deferred.defer(player_stat_get, player_id = player_id, is_reload = True, _queue = "players")
            
            
    if referee_id:            
        deferred.defer(referee_get,  referee_id = referee_id, is_reload = True)                   
        deferred.defer(match_browse, referee_id = referee_id, is_reload = True)    

        
    return True

@check_cache
def match_get(match_id = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):

    #start = time.time()
  
    match_ref   = models.Match.get_item(match_id)

    if not match_ref:
        logging.warning("Match not found: %s", match_id)
        return None
            
    match_key   = match_ref.key()
    
    goal        = models.EventType.get_item("1001").key()
    yellow_card = models.EventType.get_item("1002").key()
    red_card    = models.EventType.get_item("1003").key()    

    
    match_ref.teams = []
       
    all_competitors = models.Competitor.gql("WHERE match_id = :1 ORDER BY created", match_ref).fetch(limit)

    for value in all_competitors:   
    
        #team = value.team_id 
        team = models.Team.get_item(value.team_id.id)
        team_key = team.key()
        
        logging.info("Team id: %s \t Name: %s", team.id, team.name)

        try:
            if value.competitor_scores[0].scoretype_id.id == "1001":
                team.scored = int(value.competitor_scores[0].value)
                
            elif value.competitor_scores[1].scoretype_id.id == "1001":
                team.scored = int(value.competitor_scores[1].value)
                
            #logging.info("competitor_scores[0] %s: %s",value.competitor_scores[0].scoretype_id.id, int(value.competitor_scores[0].value))
            #logging.info("competitor_scores[1] %s: %s",value.competitor_scores[1].scoretype_id.id, 
            #                                            int(value.competitor_scores[1].value))            
        except:
            t = 0
            logging.info("No Score")
            
        team.sanctions = models.Sanction.gql("WHERE match_id = :1 AND team_id = :2", match_key, team_key).fetch(limit)
        team.player = []
        
        match_ref.teams.append(team)        
        
                   
    for team in match_ref.teams:

        matchplayers = []        
        team_key = team.key()
                 
        teamplayers = models.PlayerMatch.gql("WHERE match_id = :1 AND team_id = :2", match_key, team_key).fetch(limit)        
                  
                  
        '''          
        #item = teamplayers[int(random.randint(0,len(teamplayers) - 1))]          
        
        for item in teamplayers:
            player = item.player_id            
            if player.id == "3645":
                logging.info("Player id: %s \t name: %s, n = ", player.id, player.name)        
                
                logging.info("date: %s",player.birthday)
                
                matchplayers.append(player)                   
        

                       
        '''                
        for item in teamplayers:
            try:                
                player = item.player_id
                                
                player_key = player.key()
            
                player.goals = int(models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND match_id = :3 AND team_id = :4", 
                                           player_key, goal, match_key, team_key).count(limit))
                                           
                if models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND match_id = :3 AND team_id = :4", 
                                           player_key, yellow_card, match_key, team_key).count(limit) > 0:                          
                        player.yellow_card = True                
                
                if models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND match_id = :3 AND team_id = :4", 
                                           player_key, red_card, match_key, team_key).count(limit) > 0:                          
                        player.red_card = True
                
                player.is_played = True
                
                matchplayers.append(player)         
            except:
                pass                                 
        
                   
        matchplayers = sorted(matchplayers, key=lambda student: student.full_name, reverse=False)                  
                   
        team.players = matchplayers                       

    match_datetime = match_ref.datetime

    match_ref.referees = models.RefereeMatch.gql("WHERE match_id = :1 ORDER BY created ASC", match_ref).fetch(limit)

    results = match_ref       
    return cache_set(key_name, results)



@check_cache
def match_get_events(match_id = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
    
    match = models.Match.get_item(match_id)       
    results = models.Event.gql("WHERE match_id = :1", match).fetch(limit)

    return cache_set(key_name , results)




#@check_cache
def match_get_players(match_id = None, team_id = None, limit=1000, offset=None,
                 is_reload=None, memcache_delete=None, key_name=""):
    match = models.Match.get_item(match_id)
    team = models.Team.get_item(team_id)
    
    results = models.PlayerMatch.gql('WHERE match_id = :1 AND team_id = :2', match, team).fetch(limit)
    
    #for item in results:
    #    item.
                      
    return cache_set(key_name , results)


def match_remove(match_id, limit=100):

    match = models.Match.get_item(match_id)

    league_id  = match.league_id.id
    tournament_id = match.tournament_id.id
    
    teams = []

    if match:
        rem  = models.Competitor.gql("WHERE match_id = :1", match).fetch(limit)
        
        for competitor in rem: 
            team_id = competitor.team_id.id
            teams.append(team_id)                     
                
        db.delete(rem)

        rem = models.Event.gql("WHERE match_id = :1", match).fetch(limit)  
        db.delete(rem)

        rem = models.Score.gql("WHERE match_id = :1", match).fetch(limit)  
        db.delete(rem)
                
        rem = models.RefereeMatch.gql("WHERE match_id = :1", match).fetch(limit)  
        db.delete(rem)                        
        db.delete(match)
               
    league_update_task(league_id = league_id)
    
    for team_id in teams:
        deferred.defer(match_browse, team_id = team_id, is_reload = True)   

    return True


#######
@check_cache
def news_browse(tournament_id = None, limit=5, offset=0,
                 is_reload=None, memcache_delete=None, key_name=""):
         
    tournament = models.Tournament.get_item(tournament_id)
    results = models.News.gql("WHERE tournament_id = :1 ORDER BY created DESC",
                                        tournament).fetch(limit, offset)
    
    logging.info("Last News From DataBase.")

    include = ["id", "name", "datetime", "created", "user_id"]    
    
    return cache_set(key_name, results, include, commit = True)   


def news_create_app(raw_post_data):
    
    tournament    = models.Tournament.get_item("1001")
    
    res = json.loads(raw_post_data)
    
    logging.info("raw: %s",res)
    
    
    
    name = res.get("name", "")
    content = res.get("content", "")

    params = {'name'          :    name,
              'content'       :    content,      

              'tournament_id' : tournament,
              'user_id'       : tournament.user_id,
             }

    
    news = models.News.create(params)
    
    news_get(news_id = news.id, is_reload = True)    
    news_browse(tournament_id = tournament.id, is_reload = True)    

    results = jsonloader.encode(input = news)
    
    return results
    
    
def news_create(request, **kw):

    tournament_id = request.POST.get("tournament_id", "")
    
    tournament    = models.Tournament.get_item(tournament_id)
    
    if not tournament:
        logging.error("No team: %s", team_id)
        return None
      
   

    name    = request.POST.get("name", "")
    content = request.POST.get("content", "")
    
    if name == "" or content == "":
        logging.error("Name and Content are empty")        
        return None


    params = {'name'          :    name,
              'content'       :    content,      

              'tournament_id' : tournament,
              'user_id'       : request.user,
             }

    
    news = models.News.create(params)
    
    logging.info("News id: %s", news.id)
    
    news_browse(tournament_id = tournament_id, is_reload = True)    

    return news.id


def news_edit(request, news_id, **kw):

    news = models.News.get_item(news_id)
    
    tournament    = news.tournament_id
    tournament_id = tournament.id

    name    = request.POST["name"]
    content = request.POST["content"]
    
    if name == "" or content == "":
        logging.error("Name and Content are empty") 
        
        if content == "1":
            return False
                   
        return None


    news.name    = name
    news.content = content

    news.put()

    news_get(news_id = news_id, is_reload = True)          
        
    #deferred.defer( news_browse, tournament_id = tournament_id, is_reload = True) 
    
    news_browse(tournament_id = tournament_id, is_reload = True) 
    
    
    return news.id


@check_cache
def news_get(news_id = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
    
    results = models.News.get_item(news_id)    
    if not results:
        return None
           
    all_images = models.Image.gql("WHERE news_id =:1", results).fetch(limit)   

    logging.info("Len images: %s",len(all_images))

    results.photos = []    
    results.photos = all_images

    include = ["id", "name", "content", "created", "tournament_id"]
    
    
    return cache_set(key_name, results, include)


'''
@check_cache
def new_get_photos(news_id = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""): 

    news = models.News.get_item(news_id)   
    results = models.Image.gql("WHERE news_id =:1", news).fetch(limit)   
    
    return cache_set(key_name, results)
'''        
   


def news_remove(news_id, limit=1000):

    news = models.News.get_item(news_id)
    
    tournament    = news.tournament_id
    tournament_id = tournament.id
    
    db.delete(news)
    
    news_browse(tournament_id = tournament_id, is_reload = True)      
    news_get(news_id = news_id, is_reload = True)        

    models.News.update(news_id)    
        
    return True



@check_cache
def playoff_browse(league_id = None, limit = 1000, is_reload = None, memcache_delete = None, key_name = ""):
    
    league = models.League.get_item(league_id)       
    
    results = models.Playoff.gql("WHERE league_id = :1", league).fetch(limit)   
    
    for item in results:
          
        item.nodes = models.PlayoffNode.gql("WHERE playoff_id = :1 ORDER BY playoff_id, created ASC", item).fetch(limit)
        
        for value in item.nodes:
            value.competitors = models.PlayoffCompetitor.gql("WHERE playoffnode_id = :1 ORDER BY created ASC", value).fetch(limit)

            value.matches     = models.Match.gql("WHERE playoffnode_id = :1 ORDER BY created ASC", value).fetch(limit)
                               
            for match in value.matches:
                match.teams = []
            
                all_competitors = models.Competitor.gql("WHERE match_id = :1 ORDER BY created", match).fetch(limit)
            
                for team in all_competitors:
                    new_team = team.team_id
                        
                    try:
    
                        if team.competitor_scores[0].scoretype_id.id == "1001":
                            new_team.score = int(team.competitor_scores[0].value)
                            new_team.played = True
                    
                        elif team.competitor_scores[1].scoretype_id.id == "1001":
                            new_team.score = int(team.competitor_scores[1].value)                    
                            new_team.played = True        
                        
                    except:
                        t = 0
                        #new_team.score = 0                                          
                    
                    match.teams.append(new_team)   
    
    
    include = ["id", "name", "playoffnode_id", "size", "playoffstage_id", "nodes", 
               "team_id", "score", "played", "competitors", "matches", "teams"]
    
    
    return cache_set(key_name, results, include, commit = True)



def playoff_create_nodes(stage_name, tournament, league, playoff, n_max):
       
    logging.info("stage_name: %s", stage_name)
            
    stage = models.PlayoffStage.gql("WHERE name = :1", stage_name).get()              
       
    params = {    'tournament_id': tournament,
                  'league_id':     league,
                  'playoff_id':    playoff,
                  'playoffstage_id':      stage,
              } 
    
    for i in xrange(1, n_max+1):    
        logging.info("1/%s  :%s", n_max, i)
               
        playoff_node = models.PlayoffNode.create(params)                
        params_node = {
                        'tournament_id':   tournament,
                        'league_id':       league,
                        'playoff_id':      playoff,
                        'playoffstage_id': stage,
                        'playoffnode_id':  playoff_node,                      
              }    
        models.PlayoffCompetitor.create(params_node)
        models.PlayoffCompetitor.create(params_node)
    
    return True
    

def playoff_create(league_id = None, name = "PlayOff", size = 8, third_place = False, limit = 1000):

    # Is Playoff pair valid?
    if size < 2 or size > 32:
        return None
        
    '''

    all_stages = models.PlayoffStage.all().count()
    if all_stages < 1:
    
        params = {   'name': 'final'    }  
        models.PlayoffStage.create(params)

        params = {   'name': 'semi-final'    }  
        models.PlayoffStage.create(params)    
    
        params = {   'name': 'quarter-final'    }  
        models.PlayoffStage.create(params)
        logging.info("Create Playoff Stages")
        
    if all_stages < 5:
    
        params = {   'name': '1/8'    }  
        models.PlayoffStage.create(params)

        params = {   'name': '1/16'    }  
        models.PlayoffStage.create(params)    
                 
    '''
    league = models.League.get_item(league_id)
    tournament = league.tournament_id
    
    #playoff = models.Playoff.gql("WHERE league_id = :1", league).get()    
    #if playoff is None:  
    
    params = {    'tournament_id': tournament,
                  'league_id':     league,
                  'size':          size,
                  'name':          name,
            }
        
    playoff = models.Playoff.create(params)    
  
        
    n_max = 2 
    k = 1
         
    while n_max < size:
        n_max *= 2   # iterator
        k += 1
        
    logging.info("#######################################\n")        

    logging.info("name: %s", name)
    logging.info("size: %s", size)
    logging.info("n_max: %s", n_max)
    logging.info("k: %s", k)    
        
    for j in xrange(0, k):

        n_max = n_max/2           
        
        if n_max == 16:
            stage_name = "1/16"
        if n_max == 8:
            stage_name = "1/8"
        if n_max == 4:
            stage_name = "quarter-final"
        if n_max == 2:
            stage_name = "semi-final"
        if n_max == 1:
            stage_name = "final"
                         
        playoff_create_nodes(stage_name, tournament, league, playoff, n_max)    
           
           
           
    if third_place == True:
        ''' Match For the Third_Place'''
        stage_name = "third-place"            
        playoff_create_nodes(stage_name, tournament, league, playoff, n_max)  
                       
                                                 
                     
    playoff_browse(league_id = league_id, is_reload = True)                     
                     
                                
    return True
    

def playoff_remove(playoff_id = None, league_id = None, limit = 1000):

    if playoff_id:        
        item = models.Playoff.get_item(playoff_id)
    else:
        league = models.League.get_item(league_id)
        item = models.Playoff.gql("WHERE league_id = :1", league).get()
   
    
    if item:
        rem  = models.Match.gql("WHERE playoff_id = :1", item).fetch(limit)
        db.delete(rem)                
        rem = models.Competitor.gql("WHERE playoff_id = :1", item).fetch(limit)  
        db.delete(rem)
        rem = models.PlayoffCompetitor.gql("WHERE playoff_id = :1", item).fetch(limit)  
        db.delete(rem)
        rem = models.PlayoffNode.gql("WHERE playoff_id = :1", item).fetch(limit)  
        db.delete(rem)

        db.delete(item)

    models.Playoff.update(playoff_id)
    


    league_update_task(league_id = league_id)        

    
def playoff_get_nodeteams(playoffnode_id = None, limit = 1000):

    playoffnode = models.PlayoffNode.get_item(playoffnode_id)
    
    if not playoffnode:
        return False
        
    competitors = models.PlayoffCompetitor.gql("WHERE playoffnode_id = :1 ORDER BY created ASC", playoffnode).fetch(limit)
    
    results = []
    
    for item in competitors:
        try:
            results.append(item.team_id.id)
        except:
            pass
               
    return results

    
def playoff_set(league_id = None, team_id = None, competitor_id = None, limit = 1000):    
        
    logging.info("team_id: %s",team_id)
    logging.info("competitor_id: %s",competitor_id)

    competitor = models.PlayoffCompetitor.get_item(competitor_id)
    team =  models.Team.get_item(team_id)    
    
    competitor.team_id = team
    competitor.put()
    
    #deferred.defer(playoff_browse, league_id = league_id, is_reload = True,
    #                                                 _target = "defworker")
    deferred.defer(playoff_browse, league_id = league_id, is_reload = True)    
    

################

@check_cache
def player_browse(tournament_id = None, limit=5000,
                 is_reload=None, memcache_delete=None, key_name=""):

    if not tournament_id:
        return None
               
    logging.info("memory usage: %s",runtime.memory_usage().current())

    tournament = models.Tournament.get_item(tournament_id)  
    results = models.Player.gql("WHERE tournament_id = :1 ORDER BY full_name ASC", tournament).fetch(limit)    
    
    logging.info("All Players len: %s",len(results))                 
    
    gql = 'SELECT * FROM PlayerTeam WHERE player_id = :1 ORDER BY created DESC' 
    qq = db.GqlQuery(gql) 

   
    for item in results:       
        item.teams = []               
        #all_teams = models.PlayerTeam.gql("WHERE player_id = :1 ORDER BY created DESC", item).fetch(limit)   
        qq.bind(item) 

        all_teams = qq.fetch(limit)      
        
        for value in all_teams:            
            item.teams.append(value.team_id)
                                                                    
                                                     
    logging.info("memory usage: %s",runtime.memory_usage().current())   	

    logging.info("cpu usage: %s",runtime.cpu_usage().total())   	    
   	           
    include = ["id", "name", "full_name", "rating", "ranking", "teams"]
    
                        
    return cache_set(key_name, results, include, commit = True)   

        
                 

def player_create(request, **kw):

    team_id  = request.POST["team_id"]
    team     = models.Team.get_item(team_id)
    
    if not team:
        return None

    tournament = team.tournament_id
    if not tournament:
        logging.error("No team: %s", team_id)
        return None
        
    tournament_id = tournament.id
        
    is_played_create = request.POST["player_create"]
    
    player = None
    
    if is_played_create == "false":

        player_id      = request.POST["player_id"]
        player = models.Player.get_item(player_id)
        
        if not player.tournament_id.id == tournament.id:
            logging.critical("No Rights!!!!: %s", player_id)
            return None        
                       
        
        if not player:
            logging.error("No Player: %s", player_id)
            return None
        
        is_teamplayed = models.PlayerTeam.gql("WHERE player_id = :1 AND team_id = :2", player, team).get()        
        
        if is_teamplayed:
            logging.error("Alreddy played. Player: %s \t Team: %s", player.id, team.id )
            return None
                
    else:        
    
        first_name = request.POST["player_name"]
        second_name = request.POST["player_second_name"]
        
        third_name = request.POST["player_third_name"]
    
        if first_name == "" and second_name == "":
            logging.error("First Name and Second Name are empty")        
            return None


        full_name = ""
        
        if second_name:
            if len(second_name) > 0:
                full_name = second_name + " "
            
        full_name += first_name

        params = {'name': first_name,
                  'second_name': second_name,
                  'third_name': third_name,
                  
                  'full_name':  full_name,             

                  'tournament_id': tournament,
                }

        position_id  = request.POST["player_position"]

        if position_id:
            params['position_id'] = models.Position.get_item(position_id)  

    
        height = request.POST["player_height"]
        if height:
            params['height'] = float(height)

        weight = request.POST["player_weight"]
        if weight:
            params['weight'] = float(weight)

        birthday_date     = request.POST["datepicker"]
        if birthday_date:    
            birthday = datetime.datetime.strptime(birthday_date, DATE_FORMAT)#.date()
            params['datetime'] = birthday


    
        player = models.Player.create(params)
    
    params = {'tournament_id': tournament,
                  'player_id':     player,
                  'team_id':       team,
                  'active':       True,
            }


    number = request.POST["player_number"]
    if number:
        params['number'] = int(number)

    teamplayer = models.PlayerTeam(**params)
    teamplayer.put()
    
    
    
    team_get_players(team_id = team_id, stat = True, is_reload = True)         
    team_get_players(team_id = team_id, is_reload = True) 
    team_get_players_active(team_id = team_id, is_reload = True)     

    deferred.defer( player_browse, tournament_id = tournament_id, is_reload = True, _target="defworker")   
    deferred.defer( player_get, player_id = player.id,  is_reload = True )       
    deferred.defer( player_stat_get, player_id = player.id,  is_reload = True )   
                        
    return player.id

def player_disable(team_id = None, player_id = None, is_checked = True):
        
    logging.info("Team: %s \t Player: %s \t is_checked: %s", team_id, player_id, is_checked)
    logging.info("New is_checked: %s", is_checked)

    team   = models.Team.get_item(team_id)
    player = models.Player.get_item(player_id)
        

    item = models.PlayerTeam.gql("WHERE team_id = :1 AND player_id = :2", team, player).get()
    if item:

        item.active = is_checked
        item.put()
        #return True                
    
    deferred.defer( team_get_players, team_id = team_id, stat = True, is_reload = True)    
    deferred.defer( team_get_players_active, team_id = team_id, is_reload = True)  
    
    return True
        

def player_edit(request, player_id, **kw):


    player = models.Player.get_item(player_id)

    if not player.tournament_id:
        item = models.PlayerTeam.gql("WHERE player_id = :1", player).get()
        if item:
            player.tournament_id = item.tournament_id

    tournament = player.tournament_id
    tournament_id = tournament.id
    
    first_name = request.POST["player_name"]
    second_name = request.POST["player_second_name"]
    
    if first_name == "" and second_name == "":
        logging.error("First Name and Second Name are empty")      
        return None

    third_name = request.POST["player_third_name"]



    player.name  = first_name
    player.second_name = second_name
    
    player.third_name = third_name
    
    player.full_name = ""
        
    if player.second_name:
        if len(player.second_name) > 0:
            player.full_name = player.second_name + " "
            
    player.full_name += player.name

    position_id  = request.POST["player_position"]

    if position_id:
        player.position_id = models.Position.get_item(position_id)  
    else:
        player.position_id = None
    
    height = request.POST["player_height"]
    if height:
        height = height.replace(",",".")    
        player.height = float(height)
    else:
        player.height = None

    weight = request.POST["player_weight"]
    if weight:
        weight = weight.replace(",",".")
        player.weight = float(weight)
    else:
        player.weight = None

    birthday_date     = request.POST["datepicker"]
    if birthday_date:    
        birthday = datetime.datetime.strptime(birthday_date, DATE_FORMAT)#.date()
        player.datetime = birthday
    else:
        player.datetime = None
     

    player.put()

    models.Player.update(player.id)


    number  = request.POST.get("player_number", "")
    team_id = request.POST.get("team_id", "")

    if number and team_id:
        team = team_get(team_id = team_id)
        playerteam = models.PlayerTeam.gql("WHERE team_id = :1 AND player_id = :2", team, player).get()
            
        logging.info("Number: %s", number)
        if playerteam:
            playerteam.number = int(number)
            playerteam.put()
            logging.info("Number Saved: %s", number)
            
    if team_id:        
        player = player_get(player_id = player_id, team_id = team_id, is_reload = True)           


        deferred.defer( team_get_players, team_id = team_id, stat = True, is_reload = True) 
        deferred.defer( team_get_players, team_id = team_id, is_reload = True)            
        deferred.defer( team_get_players_active, team_id = team_id, is_reload = True)                     

    player = player_get(player_id = player_id, is_reload = True)
    
    deferred.defer( player_browse, tournament_id = tournament_id, is_reload = True, _target="defworker")   
    deferred.defer( player_stat_get, player_id = player_id,  is_reload = True )  
        

    return player_id



@check_cache
def player_get(player_id = None, team_id = None,
                 is_reload=None, memcache_delete=None, key_name=""):
    
    player = models.Player.get_item(player_id)
    if not player:
        return None              

    #if player.birthday:
    #    new_age = datetime.date.today() - player.birthday
    #    player.age = int(new_age.days / (365.25))

    if player.position_id:
        player.position = settings.POSITIONS[player.position_id.name] 
        logging.info("player.position: %s",player.position)        

  

    if team_id:
        team = models.Team.get_item(team_id)
        playerteam = models.PlayerTeam.gql("WHERE team_id = :1 AND player_id = :2", team, player).get()

        if playerteam:
            if playerteam.number:
                player.number = playerteam.number 
                
    item = models.Image.gql("WHERE player_id = :1 ORDER BY created DESC", player).get()    
    
    if item:
        player.photo_small = settings.GOOGLE_BUCKET + item.photo_small
        player.photo_big = settings.GOOGLE_BUCKET + item.photo_big        
        player.photo_original = settings.GOOGLE_BUCKET + item.photo_original

    else:
        player.photo_small = settings.GOOGLE_BUCKET + "images/anonymous_avatar.png"
        player.photo_big = settings.GOOGLE_BUCKET + "images/anonymous_big.png"        
        player.photo_original = settings.GOOGLE_BUCKET + "images/anonymous_avatar.png"                


    results = player               
    return cache_set(key_name, results)        




@check_cache
def player_stat_get(player_id = None, limit=1000, offset=None,
                 is_reload=None, memcache_delete=None, key_name=""):

    if not player_id:
        return None

    player = models.Player.get_item(player_id)
    #player = player_get(player_id)
    
    goal        = models.EventType.get_item("1001").key()
    yellow_card = models.EventType.get_item("1002").key()
    red_card    = models.EventType.get_item("1003").key()

    if not player:
        return None
    
    player.goals = models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2", player, goal).count(limit)
                                           
    player.yellow_cards =  models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2", player, yellow_card).count(limit)
                
    player.red_cards = models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2", player, red_card).count(limit)        

    player.playermatches = models.PlayerMatch.gql("WHERE player_id = :1", player).count(limit)        

    '''
    logging.info("11:  %s", player.playermatches)
    logging.info("12:  %s", player.yellow_cards)
    logging.info("13:  %s", player.red_cards)
    logging.info("14:  %s", player.goals)
    '''

    all_player_teams = models.PlayerTeam.gql("WHERE player_id = :1 ORDER by created DESC", player).fetch(limit)

    player_key = player.key()
    
    for item in all_player_teams:
    
        team = item.team_id
        team_key = team.key()       

        all_team_seasons = models.Season.gql("WHERE team_id = :1 ORDER by created DESC", team).fetch(limit)        

        for season in all_team_seasons:          

            league_key = season.league_id.key()

            season.playermatches = models.PlayerMatch.gql("WHERE league_id = :1 AND team_id = :2 AND player_id = :3", 
                                                            league_key, team_key, player_key).count()
          
            season.yellow_cards = models.Event.gql("WHERE league_id = :1 AND team_id = :2 AND player_id = :3 AND eventtype_id = :4",
                                                            league_key, team_key, player_key, yellow_card).count(limit)

            season.red_cards    = models.Event.gql("WHERE league_id = :1 AND team_id = :2 AND player_id = :3 AND eventtype_id = :4",
                                                            league_key, team_key, player_key, red_card).count(limit)
            
            season.goals = models.Event.gql("WHERE league_id = :1 AND team_id = :2 AND player_id = :3 AND eventtype_id = :4",
                                                            league_key, team_key, player_key, goal).count(limit)



        item.all_team_seasons = all_team_seasons

        logging.info("All Team Seasons: \t %s", item.all_team_seasons)

    player.all_player_teams = all_player_teams

    logging.info("All Player Team: \t %s", player.all_player_teams)
        
    results = player   
    logging.info("key_name: %s",key_name)  
       
    return cache_set(key_name, results)


def player_remove(player_id, limit=1000):

    del_player = models.Player.get_item(player_id)
    if del_player:
        rem  = models.PlayerTeam.gql("WHERE player_id = :1", del_player).fetch(limit)
        db.delete(rem)                
        rem = models.Event.gql("WHERE player_id = :1", del_player).fetch(limit)  
        db.delete(rem)
        rem = models.StatPlayer.gql("WHERE player_id = :1", del_player).fetch(limit)  
        db.delete(rem)
        rem = models.Sanction.gql("WHERE player_id = :1", del_player).fetch(limit)  
        db.delete(rem)

        db.delete(del_player)

    models.Player.update(player_id)
    
        
    return True


def player_photo_remove(player_id = None, limit = 100):

  player = models.Player.get_item(player_id)
  
  all_images = models.Image.gql("WHERE player_id = :1 ORDER BY created DESC", player).fetch(limit)
  db.delete(all_images)
  
  models.Player.update(player_id)
  player = player_get(player_id = player_id, is_reload = True)      

  return True


def positions_browse(sport_id = None, limit = 100):
    
    sport = models.Sport.get_item(sport_id)
    
    results = models.Position.gql("WHERE sport_id = :1", sport).fetch(limit)
        
    for c in results:
        c.title = settings.POSITIONS[c.name] 
    return results


def increment_counter(key, amount):

    i = amount

    obj = db.get(key)
    obj.rating = i
    i += 1
    
    logging.info("Name: %s", obj.name)        
    obj.put()

def increment_counter2():
    tournament = models.Tournament.get_item("1001") 
    all_items = models.Player.gql("WHERE tournament_id = :1 ORDER BY ranking DESC", tournament)#.fetch(limit)
    i = 1
    for item in all_items:
        #logging.info("Player: %s \t Index: %s \t Ranking: %s", item.name, i, item.ranking)
        item.rating = i
        i += 1
    db.put(all_items)    

def rating_update(tournament_id = None, limit = 5000,
                 is_reload=None, memcache_delete=None, key_name=""):

    tournament = models.Tournament.get_item(tournament_id) 
    
    start = time.time()
    
    all_items = models.Player.gql("WHERE tournament_id = :1 ORDER BY ranking DESC", tournament).fetch(limit)
  
    i = 0
    logging.info("Len players full %s", len(all_items))
    newlist = []
    
    for item in all_items:
        i += 1

        if item.rating == i:
            continue
        else:     
            item.rating = i        
            newlist.append(item)
    

    logging.info("Len players update %s", len(newlist))
    db.put(newlist)

    
    end3 = round(time.time() - start, 6)  
    logging.info("Rating Players update time: %s", end3)    

        
    start = time.time()
    all_items = models.Team.gql("WHERE tournament_id = :1 ORDER BY ranking DESC", tournament).fetch(limit)
    i = 0
    logging.info("Len teams full %s", len(all_items))
    newlist = []
    
    for item in all_items:
        i += 1

        if item.rating == i:
            continue
        else:     
            item.rating = i        
            newlist.append(item)
    

    logging.info("Len teams update %s", len(newlist))
    db.put(newlist)
    
    end3 = round(time.time() - start, 6)   
    logging.info("Rating Teams update time: %s", end3)     

    return True


@check_cache
def referees_browse(tournament_id = None, stat = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
    if tournament_id == None:
        return none

    tournament = models.Tournament.get_item(tournament_id)    
    
    results = models.Referee.gql("WHERE tournament_id = :1 ORDER BY second_name ASC, name ASC",tournament).fetch(limit)
    
    if stat:
        yellow_card = models.EventType.get_item("1002").key() 
        red_card    = models.EventType.get_item("1003").key() 
        
        for item in results:
            item.matches = models.RefereeMatch.gql("WHERE referee_id = :1", item.key()).count()
            
            item.yellow_cards = models.Event.gql("WHERE referee_id = :1 AND eventtype_id = :2", item.key(), yellow_card).count()

            item.red_cards    = models.Event.gql("WHERE referee_id = :1 AND eventtype_id = :2", item.key(), red_card).count()            

    return cache_set(key_name , results)



def referee_create(request, **kw):

    tournament_id = request.POST["tournament_id"]
    tournament    = models.Tournament.get_item(tournament_id)


    if not tournament:
        logging.error("No tournament: %s", tournament_id)
        return None
   
    
    first_name  = request.POST["referee_name"]
    second_name = request.POST["referee_second_name"]
    
    if first_name == "" and second_name == "":
        logging.error("First Name and Second Name are empty")        
        return None

    full_name = ""
        
    if second_name:
        if len(second_name) > 0:
            full_name = second_name + " "
            
    full_name += first_name


    params = {'name': first_name,
              'second_name': second_name,
              'full_name':  full_name,              
              'tournament_id': tournament,
              }


    birthday_date     = request.POST["datepicker"]
    if birthday_date:    
        birthday = datetime.datetime.strptime(birthday_date, DATE_FORMAT)#.date()
        params['datetime'] = birthday

   
    referee = models.Referee.create(params)
    
    referees_browse(tournament_id = tournament_id, stat = True, memcache_delete = True)
    referees_browse(tournament_id = tournament_id, memcache_delete = True)

    return referee.id




def referee_edit(request, referee_id, **kw):

    referee = models.Referee.get_item(referee_id)
    tournament = referee.tournament_id
    tournament_id = tournament.id
    
    if not referee:
        logging.error("First Name and Second Name are empty")      
        return None
    
    
    first_name = request.POST["referee_name"]
    second_name = request.POST["referee_second_name"]
    
    if first_name == "" and second_name == "":
        logging.error("First Name and Second Name are empty")      
        return None


    referee.name  = first_name
    referee.second_name = second_name
    

    full_name = ""
        
    if second_name:
        if len(second_name) > 0:
            full_name = second_name + " "
            
    full_name += first_name
    
    referee.full_name = full_name


    birthday_date     = request.POST["datepicker"]
    
    logging.info("birthday: %s",birthday_date)
    
    if birthday_date:    
        birthday = datetime.datetime.strptime(birthday_date, DATE_FORMAT)#.date()
        referee.datetime = birthday
    else:
        referee.datetime = None
     

    referee.put()

    models.Referee.update(referee.id)

    referee_get(referee_id = referee_id, memcache_delete = True)
    referees_browse(tournament_id = tournament_id, stat = True, memcache_delete = True)
    referees_browse(tournament_id = tournament_id, memcache_delete = True)


    return referee.id


@check_cache
def referee_get(referee_id = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
    if not referee_id:
        return None
    
    referee = models.Referee.gql("WHERE id = :1", referee_id).get()
    
    yellow_card = models.EventType.get_item("1002").key() 
    red_card    = models.EventType.get_item("1003").key() 
        
    referee.matches = models.RefereeMatch.gql("WHERE referee_id = :1", referee.key()).count()
    referee.yellow_cards = models.Event.gql("WHERE referee_id = :1 AND eventtype_id = :2", referee.key(), yellow_card).count()
    referee.red_cards    = models.Event.gql("WHERE referee_id = :1 AND eventtype_id = :2", referee.key(), red_card).count()     
    
   
    item = models.Image.gql("WHERE referee_id = :1 ORDER BY created DESC", referee).get()    
    
    if item:
        referee.photo_small    = settings.GOOGLE_BUCKET + item.photo_small
        referee.photo_big      = settings.GOOGLE_BUCKET + item.photo_big        
        referee.photo_original = settings.GOOGLE_BUCKET + item.photo_original

    else:
        referee.photo_small = settings.GOOGLE_BUCKET + "images/anonymous_avatar.png"
        referee.photo_big = settings.GOOGLE_BUCKET + "images/anonymous_avatar.png"        
        referee.photo_original = settings.GOOGLE_BUCKET + "images/anonymous_avatar.png"       


    results = referee        
    return cache_set(key_name , results)
    
        
    
def referee_photo_remove(referee_id = None, limit = 100):

  referee = models.Referee.get_item(referee_id)
  
  all_images = models.Image.gql("WHERE referee_id = :1 ORDER BY created DESC", referee).fetch(limit)
  db.delete(all_images)
  
  models.Referee.update(referee_id)
  referee = referee_get(referee_id = referee_id, is_reload = True)      

  return True


def regulations_edit(content = "", tournament_id = None):    
    
    tournament = models.Tournament.get_item(tournament_id)
    if not tournament:
        return None                
    
    if content == "":
        logging.error("Name and Content are empty")        
        return None

    item = models.Regulations.gql("WHERE tournament_id = :1 ORDER BY created DESC", tournament).get()
    
    if not item:
        item = models.Regulations(tournament_id = tournament)
    
    item.content = content
    item.put()
    
    return True
    
    
    
    
def regulations_get(tournament_id = None):    
    
    tournament = models.Tournament.get_item(tournament_id)
    if not tournament:
        return None
        
    results = models.Regulations.gql("WHERE tournament_id = :1 ORDER BY created DESC", tournament).get()
    
    return results



def response_get(request, locals, template_path, tournament_id = None, defers = {}):
        
            
    c = template.RequestContext(request, locals)
    #c.update(csrf(request))
    t = loader.get_template(template_path)            
    result = http.HttpResponse(t.render(c))
    
    result['Access-Control-Allow-Origin'] = 'http://goapi.cometiphrd.appspot.com/'
                   
    return result
    
def response_index(request, template_path):
        
            
    c = template.RequestContext(request, locals())
    #c.update(csrf(request))
    t = loader.get_template(template_path)            
    result = http.HttpResponse(t.render(c))
       
    return result    
    

def fill_database(limit = 1000):

    results = models.EventType.all().fetch(limit)
    if len(results) < 1:        
        all_events = ["Goal", "Yellow Card", "Red Card", "Penalty", "Auto Goal", "Substitution", "5th foal"]
        sport_ref = models.Sport.all().get()
        
        for name in all_events:
            params = {'name': name, 'sport_id': sport_ref.key()}
            new_event_ref = models.EventType.create(params)
    
    results = models.ResultType.all().fetch(limit)
    if len(results) < 1:
        all_events = ["None", "Win", "Lose", "Draw"]
        sport_ref = models.ResultType.all().get()
        
        for name in all_events:
            params = {'name': name}
            new_event_ref = models.ResultType.create(params)
       
       
    results = models.ScoreType.all().fetch(limit)
    if len(results) < 1:
        all_events = ["Scored", "Conceded"]
        sport_ref = models.ScoreType.all().get()
        
        for name in all_events:
            params = {'name': name}
            new_event_ref = models.ScoreType.create(params)
            

@check_cache
def sport_browse(limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):

    results = models.Sport.all().fetch(limit)         
    if len(results) == 0:    
        sports = ["Soccer", "Basketball", "Volleyball", "Hockey"]
    if len(results) == 1:
        sports = ["Basketball", "Volleyball", "Hockey"]
    
    if len(results) < 2:          
        
        for item in sports:
            params = {'name': item}
            new_event_ref = models.Sport.create(params)

        results = models.Sport.all().fetch(limit)
        
        fill_database()
        
    #for c in results:
    #    c.title = settings.SPORT_EVENTS[c.name] 
                
    return cache_set(key_name, results)   
                


# depends on tournament_get's privacy
def sport_get_sports(limit = 100):#api_user, sports):

        
    #sport_refs = {}
    #sports = list(set(sports))
    #if not sports:
    #    return sport_refs


    """returns the tournaments the given actor is a member of"""
    #nick = clean.nick(nick)
    
    #user = models.Sport.all().get()
    
       
    #user.key_name="1"
    #user.id = "1"
    
    #user = user.put()
    
        
    results = models.Sport.all().fetch(limit)
    return results
    '''
    
    if len(results) < 1:
        memcache.flush_all()
        
        all_events = ["Football"]
                
        for name in all_events:
            params = {'name': name}
            new_event_ref = models.Sport.create(params)

        results = models.Sport.all().fetch(limit)
    
    for c in results:
        c.title = settings.SPORT_EVENTS[c.name] 
    
        
    results2 = results            
        
    results = models.EventType.all().fetch(limit)
    if len(results) < 1:        
        all_events = ["Goal", "Yellow Card", "Red Card", "Penalty", "Auto Goal", "Substitution", "5th foal"]
        sport_ref = models.Sport.all().get()
        
        for name in all_events:
            params = {'name': name, 'sport_id': sport_ref.key()}
            new_event_ref = models.EventType.create(params)
    
    results = models.ResultType.all().fetch(limit)
    if len(results) < 1:
        all_events = ["None", "Win", "Lose", "Draw"]
        sport_ref = models.ResultType.all().get()
        
        for name in all_events:
            params = {'name': name}
            new_event_ref = models.ResultType.create(params)
       
       
    results = models.ScoreType.all().fetch(limit)
    if len(results) < 1:
        all_events = ["Scored", "Conceded"]
        sport_ref = models.ScoreType.all().get()
        
        for name in all_events:
            params = {'name': name}
            new_event_ref = models.ScoreType.create(params)
                
    
    
    return results2
    '''



#######
#######

              
def score_results(league_key, team_key, type_key = None, group_key = None,limit = 1000):
    
    if type_key is None:
        return 0

    res = models.Score.all()
    res.filter('league_id =', league_key)         
    res.filter('team_id =', team_key)
    res.filter('scoretype_id =', type_key)     
    res.filter('group_id =', group_key)       
    results = res.fetch(limit)
    
    score = 0
    for val in results: 
        if val.value:
            score += val.value
                
    return int(score)


@check_cache              
def sitemap(name = None, limit = 10000, is_reload=None, memcache_delete=None, key_name="", get_key_name = None):

    if name == "tournaments":
        results = models.Tournament.gql("ORDER by created DESC").fetch(limit)

    if name == "leagues":
        results = models.League.gql("ORDER by created DESC").fetch(limit)

    if name == "matches":
        results = models.Match.gql("ORDER by created DESC").fetch(limit)

    if name == "teams":
        results = models.Team.gql("ORDER by created DESC").fetch(limit)

    if name == "players":
        results = models.Player.gql("ORDER by created DESC").fetch(limit)
    
    return cache_set(key_name , results)
    

def stat_update(league_id = None, team_id = None, limit = 1000):      
    
    league_ref = models.League.get_item(league_id)
    league_key = league_ref.key()
        
        
    team_key = models.Team.get_item(team_id).key()
    
    tournament_key = league_ref.tournament_id.key()
    
    season_key = models.Season.gql("WHERE league_id = :1 and team_id = :2", 
                                          league_key, team_key).get().key()
                                          
    ''' 
    season_key = None
    try:
        season_key = league_ref.league_seasons[0].key()
    except:
        pass        
    '''
    

    
    goal        = models.EventType.get_item("1001").key()    
    
    all_stat = []    
        
    all_players = models.PlayerTeam.gql("WHERE team_id = :1 AND active = :2",
                                                 team_key, True).fetch(limit)
                                                 
    for player in all_players:
       
        player_key = player.player_id.key()
       
        total_goals = models.Event.gql("WHERE player_id = :1 AND \
                                           eventtype_id = :2 AND \
                                              league_id = :3 AND \
                                                team_id = :4", 
                                 player_key, goal, league_key, team_key).count()


        params = {'player_id':  player_key,
                  'eventtype_id':  goal,
                  'score':         total_goals,
              
                  'team_id':       team_key,  
                  'tournament_id': tournament_key,
                  'league_id':     league_key,
                  'season_id':     season_key,
               }
    
    
        stat_player = models.StatPlayer.gql("WHERE league_id = :1 AND \
                                                eventtype_id = :2 AND \
                                                   player_id = :3 AND \
                                                     team_id = :4",
                                   league_key, goal, player_key, team_key).get()
                                   
        if stat_player:
            stat_player.score = total_goals            
        else: 
            stat_player = models.StatPlayer(**params)
        
        all_stat.append(stat_player)
           
    models.db.put(all_stat)  

    return True


@check_cache              
def statistics(league_id=None, limit = 10,
                 is_reload=None, memcache_delete=None, key_name=""):
    
        
    league  = models.League.get_item(league_id).key()
    goal        = models.EventType.get_item("1001").key() 
    yellow_card = models.EventType.get_item("1002").key() 
    red_card    = models.EventType.get_item("1003").key() 

    
    all_stat = models.StatPlayer.gql("WHERE league_id = :1 AND \
                                          eventtype_id = :2 \
                                          ORDER BY score DESC",
                                          league, goal).fetch(limit)
                
    results = []
    mas = []
    last_score = None

    s = len(all_stat) - 1 
    
    logging.info("Total strikers: %s", s)

    for i,item in enumerate(all_stat):
        
        try:
            
            item.yellow_cards = models.Event.gql("WHERE player_id = :1 AND \
                                                          team_id = :2 AND \
                                                        league_id = :3 AND \
                                                     eventtype_id = :4",
                     item.player_id, item.team_id, league, yellow_card).count()


            item.red_cards =    models.Event.gql("WHERE player_id = :1 AND \
                                                          team_id = :2 AND \
                                                        league_id = :3 AND \
                                                     eventtype_id = :4",
                     item.player_id, item.team_id, league, red_card).count()

                                                                
            if item.score != last_score or i >= s:
                
                if i >= s:
                    if item.score > 0 or item.yellow_cards > 0 or item.red_cards > 0:
                        mas.append(item)

                if mas:
                    mas = sorted(mas, key=lambda lv: lv.player_id.full_name,
                                                     reverse=False)
                    results.extend(mas)
                last_score = item.score
                mas = []

            if item.score > 0 or item.yellow_cards > 0 or item.red_cards > 0:
                mas.append(item)
                logging.info("Append: %s", item.score)

        except:
            continue
                

    logging.info("Result lenght: %s", len(results))                
                
    include = ["id", "name", "full_name", "score", "yellow_cards", "red_cards", "team_id", "player_id"]
        
    return cache_set(key_name, results, include)
 
'''      
@check_cache              
def statistics2(league_id=None, limit = 10,
                 is_reload=None, memcache_delete=None, key_name=""):
    
    #league_id = "1001"
    
    league  = models.League.get_item(league_id).key()
    goal        = models.EventType.get_item("1001").key() 
    yellow_card = models.EventType.get_item("1002").key() 
    red_card    = models.EventType.get_item("1003").key() 

      
    leagues = [league]
    
    if league_id == "1067":        
        res = models.League.gql("WHERE id IN :1", ["1056", "1057", "1058", "1059", "1067"]).fetch(limit)
        leagues = [x.key() for x in res]
        logging.info("leagues: %s",leagues)
        
       
        all_stat = []
        res = models.StatPlayer.gql("WHERE league_id IN :1 AND eventtype_id = :2 ORDER BY score DESC", leagues, goal).fetch(1000)
        
        for item in res:
            is_exist = False
            for value in all_stat:
                if value.player_id.key() == item.player_id.key():
                    value.score += item.score
                    is_exist = True
            if is_exist == False:
                all_stat.append(item)
        
        all_stat = sorted(all_stat, key=lambda student: student.score, reverse=True)        
        
        if limit == 10:   
            all_stat = all_stat[:9]
            
            
        
    else:
        if limit == 10:       
            all_stat = models.StatPlayer.gql("WHERE league_id IN :1 AND eventtype_id = :2 \
                                              AND score > 0 ORDER BY score DESC", leagues, goal).fetch(limit)
        else:        
            all_stat = models.StatPlayer.gql("WHERE league_id IN :1 AND eventtype_id = :2 \
                                              ORDER BY score DESC", leagues, goal).fetch(limit)

        

                
    results = []
    mas = []
    last_score = -1

    s = len(all_stat) - 1 

    for i,item in enumerate(all_stat):
        
        try:
            
            item.yellow_cards = models.Event.gql("WHERE player_id = :1 AND team_id = :2 \
                                                  AND league_id IN :3 AND eventtype_id = :4",
                                             item.player_id, item.team_id, leagues, yellow_card).count()

            item.red_cards    = models.Event.gql("WHERE player_id = :1 AND team_id = :2 \
                                                  AND league_id IN :3 AND eventtype_id = :4",
                                             item.player_id, item.team_id, leagues, red_card).count()
                
            #item.score    = models.Event.gql("WHERE player_id = :1 AND league_id IN :2 \
            #                                   AND eventtype_id = :3", item.player_id.key(), 
            #                                    leagues, goal).count()
                                                                
            if item.score != last_score or i == s:
                
                if i == s:
                    if item.score > 0 or item.yellow_cards > 0 or item.red_cards > 0:
                        mas.append(item)

                if mas:
                    mas = sorted(mas, key=lambda student: student.player_id.second_name, reverse=False)
                    results.extend(mas)
                last_score = item.score
                mas = []

            if item.score > 0 or item.yellow_cards > 0 or item.red_cards > 0:
                mas.append(item)

        except:
            #db.delete(item)
            continue
                
    include = ["id", "name", "full_name", "score", "yellow_cards", "red_cards", "team_id", "player_id"]
        
    return cache_set(key_name, results, include)     
'''

@check_cache  
def stat_league(league_id, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
    
    league = models.League.get_item(league_id)
    league_key = league.key()
    goal_key        = models.EventType.get_item("1001").key()
    yellow_card_key = models.EventType.get_item("1002").key()
    red_card_key    = models.EventType.get_item("1003").key()
    
    all = []
    all.append(models.ResultType.get_item("1002").key())
    all.append(models.ResultType.get_item("1003").key())
    all.append(models.ResultType.get_item("1004").key())
            
    league.teams = models.Season.gql("WHERE league_id = :1", league_key).count(limit)
    league.games = models.Match.gql("WHERE league_id = :1", league_key).count(limit)    
    
    league.played = models.Competitor.gql("WHERE league_id = :1 AND resulttype_id IN :2", league_key, all).count(limit)/2
    league.non_played = league.games - league.played
    
    
    
    league.goals = models.Event.gql("WHERE league_id = :1 AND eventtype_id = :2", league_key, goal_key).count(limit)
    
    
    scored_key = models.ScoreType.get_item("1001")
    all_scores = models.Score.gql("WHERE league_id = :1 AND scoretype_id = :2", league_key, scored_key).fetch(limit)
    league.goals = 0
    
    for item in all_scores:
        if item.value:
            league.goals += item.value    
    
    league.goals = int(league.goals)
    
    if league.played > 0:
        league.goals_avg = round(float(league.goals)/league.played, 2)
    else:
        league.goals_avg = 0
    
    league.yellow_cards = models.Event.gql("WHERE league_id = :1 AND eventtype_id = :2", league_key, yellow_card_key).count(limit)
    league.red_cards = models.Event.gql("WHERE league_id = :1 AND eventtype_id = :2", league_key, red_card_key).count(limit)
    results = league

    return cache_set(key_name , results)        



def team_scores(league_key, team_key, limit = 200):
    res = models.Score.all()
    res.filter('league_id =', league_key)         
    res.filter('team_id =', team_key)
    
    
    res.fetch(limit)
    total = 0
    
    for c in res:
        total = total + c.zab_id.value
        
    return total
    
def team_remove(team_id = None, limit=100):

    del_mas = [models.Image, models.Season, models.Competitor, models.Score, models.PlayerTeam, models.Event, models.StatPlayer]
    
    del_value = models.Team.get_item(team_id)
    
    if not del_value:
        return True
    
    tournament_id = del_value.tournament_id.id
         
    for item in del_mas:
        rem  = item.gql("WHERE team_id = :1", del_value).fetch(limit)
        db.delete(rem)
    
    db.delete(del_value)

    models.Team.update(team_id)
    
    deferred.defer(team_browse_rating, tournament_id = tournament_id, is_reload = True)          
    deferred.defer(team_browse, tournament_id = tournament_id, is_reload = True)      

    return True
    
    
def team_results(league_key, team_key, type_key = None, group_key = None, limit = 1000):
    
    if type_key is None:
        return 0

    res = models.Competitor.all()
    res.filter('league_id =', league_key)         
    res.filter('team_id =', team_key)
    res.filter('resulttype_id =', type_key)     
    #logging.info("group_key: %s",group_key)
    res.filter('group_id = ', group_key)       
    res.filter('playoff_id = ', None)            
    return res.count() 
            

@check_cache
def team_browse_rating(tournament_id = None, limit=1000,
                 is_reload=None, memcache_delete=None, key_name=""):

    tournament = models.Tournament.get_item(tournament_id)
        
    results = models.Team.gql("WHERE tournament_id = :1 ORDER BY ranking DESC", tournament).fetch(limit)
        
    include = ["id", "name", "rating", "ranking"]
        
    return cache_set(key_name, results, include)  
    

@check_cache
def team_browse(tournament_id = None, league_id = None, limit=1000,
                 is_reload=None, memcache_delete=None, key_name=""):

    if tournament_id:
        tournament = models.Tournament.get_item(tournament_id)  
        results = models.Team.gql("WHERE tournament_id = :1 ORDER BY name ASC", tournament).fetch(limit)    
               
        include = ["id", "name", "rating", "ranking"]
        
        return cache_set(key_name, results, include)            
    
    elif league_id:

        league = models.League.get_item(league_id)
    
        if not league.league_seasons:
            return None
    
        rv = [c.team_id.key() for c in league.league_seasons]                        
        results = models.Team.get(rv)
        # 1001 = None    1002 = Win    1003 = Lose   1004 = Draw   

        scored_key   = models.ScoreType.get_item("1001").key()
        conceded_key = models.ScoreType.get_item("1002").key()

        won_key  = models.ResultType.get_item("1002").key()
        loss_key = models.ResultType.get_item("1003").key()
        drew_key = models.ResultType.get_item("1004").key()
    
        
        for team in results: 
        
            team.won  = team_results(league.key(), team.key(), won_key)
            team.loss = team_results(league.key(), team.key(), loss_key)    
            team.drew = team_results(league.key(), team.key(), drew_key)        
            team.match_played = team.won + team.loss + team.drew
            team.points = (team.won * 3) + team.drew           
        
            team.scored   = score_results(league.key(), team.key(), scored_key)
            team.conceded = score_results(league, team.key(), conceded_key)  
 
            team.diff = team.scored - team.conceded  

            team.match_played = team.won + team.loss + team.drew
            team.points = (team.won * 3) + team.drew           
        
            team.diff = team.scored - team.conceded
         
        results = sorted(results, key=lambda student: student.points, reverse=True)
        
    else:
        return None
        
        
    return cache_set(key_name , results)



def team_create(request, **kw):
    #print "no"
    #return None
    
    
    league_id      = request.POST["league_id"]
    league_ref     = models.League.get_item(league_id)
  
    
    if not league_ref:
        return None

    tournament = league_ref.tournament_id
    if not tournament:
        return None

    tournament_id = tournament.id

    
    is_add = request.POST.get("team_add")
    
    if is_add:
        team_ref = models.Team.get_item(is_add)
        
        if team_ref.tournament_id.id != tournament_id:
            logging.error("No Access: %s",is_add)
            return False 
            
        tournament = models.Tournament.get_item(tournament_id)  
        
        is_exist = models.Season.gql("WHERE league_id = :1 AND team_id = :2", league_ref, team_ref).get()    
        if is_exist:
            logging.error("Team '%s' is alredy exists in league: %s", team_ref.name, league_ref.id)        
            return False           
    
    else:    
        params = {'name': request.POST["team_name"],
                  'tournament_id': tournament,
                }
    
        team_ref = models.Team.create(params)
    
    params_season = {'tournament_id': tournament,
                     'league_id':     league_ref.key(),
                     'team_id':       team_ref.key(),
            }


    season_ref = models.Season(**params_season)
    season_ref.put()


    deferred.defer(group_browse, league_id = league_id, is_reload = True)
    deferred.defer(team_browse, league_id = league_id, is_reload = True)
    deferred.defer(team_browse, tournament_id = tournament_id, is_reload = True)        


    return team_ref.id


def team_edit(form = None, team_id = None, limit = 100):

    team = models.Team.get_item(team_id)
    
    form.save(item = team)
    
    #return team

    team_get(team_id = team_id, is_reload = True)
    
    season = models.Season.gql("WHERE team_id = :1 ORDER BY created DESC", team).get()    
    if season:       
        deferred.defer(group_browse, league_id = season.league_id.id, is_reload = True)
        deferred.defer(team_browse,  league_id = season.league_id.id, is_reload = True)        
        deferred.defer(match_browse, league_id = season.league_id.id, is_reload = True)
    
      
    deferred.defer(team_browse,  tournament_id = team.tournament_id.id, is_reload = True)       
    deferred.defer(match_browse, tournament_id = team.tournament_id.id, is_reload = True)        
    deferred.defer(match_browse, team_id = team_id, is_reload = True)      
    
    
    playerteams = models.PlayerTeam.gql("WHERE team_id = :1", team).fetch(limit)
    for item in playerteams:
        deferred.defer( player_stat_get, player_id = item.player_id.id,
                        is_reload = True )                


    return team

@check_cache
def team_get(team_id = None,
                 is_reload=None, memcache_delete=None, key_name=""):

    team = models.Team.get_item(team_id)
    if not team:
        return None    
    
    item = models.Image.gql("WHERE team_id = :1 ORDER BY created DESC", team).get()    
    
    try:
        team.photo_small = settings.GOOGLE_BUCKET + item.photo_small
        team.photo_big   = settings.GOOGLE_BUCKET + item.photo_big        
        team.photo_original = settings.GOOGLE_BUCKET + item.photo_original

    except:
        team.photo_small    = settings.GOOGLE_BUCKET + "images/anonymous_team.png"
        team.photo_big      = settings.GOOGLE_BUCKET + "images/anonymous_team.png"        
        team.photo_original = settings.GOOGLE_BUCKET + "images/anonymous_team.png"
            
    results = team            
    
    return cache_set(key_name, results)    


@check_cache
def team_get_players_active(team_id = None, limit=1000, offset=None,
                 is_reload=None, memcache_delete=None, key_name=""):

    team_ref = models.Team.get_item(team_id)    
    team_key = team_ref.key()
    
    playerteams = models.PlayerTeam.gql('WHERE team_id = :1 and active = True', team_key).fetch(limit)
    results = []

    for item in playerteams:
        player        = item.player_id
        if item.number:
            player.number = item.number
        results.append(player)

        
    results = sorted(results, key=lambda student: student.full_name, reverse=False)                
                                                         
    return cache_set(key_name , results)                   
    
    
@check_cache
def team_get_players(team_id = None, stat = None, limit=1000, offset=None,
                 is_reload=None, memcache_delete=None, key_name=""):
      
    start = time.time()

    team_ref = models.Team.get_item(team_id)

    playerteams = models.PlayerTeam.gql('WHERE team_id = :1', team_ref).fetch(limit)
    
    team_key = team_ref.key()
    
    goal        = models.EventType.get_item("1001").key()
    yellow_card = models.EventType.get_item("1002").key()
    red_card    = models.EventType.get_item("1003").key()
    
    results = []
    if playerteams: 
        rv = [x.player_id.key() for x in playerteams]
        results = models.Player.get(rv)
        
        results = sorted(results, key=lambda student: student.full_name, reverse=False)
        
        
        for item in results:
                
            playerteam = models.PlayerTeam.gql("WHERE player_id = :1 AND team_id = :2", item.key(), team_key).get()

            item.active = playerteam.active             
            
            if playerteam.number:
                item.number = playerteam.number               
                 
            if stat:
   
                item.goals = models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND team_id = :3", 
                                           item.key(), goal, team_key).count(limit)
                                           
                item.yellow_cards =  models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND team_id = :3", 
                                           item.key(), yellow_card, team_key).count(limit)
                
                item.red_cards = models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND team_id = :3", 
                                           item.key(), red_card, team_key).count(limit)        

    end3 = round(time.time() - start, 6)  
    logging.info("Team get players  time: %s", end3)
                                                         
    return cache_set(key_name , results)



def team_photo_remove(team_id = None, limit = 100):

  team = models.Team.get_item(team_id)
  
  all_team_images = models.Image.gql("WHERE team_id = :1 ORDER BY created DESC", team).fetch(limit)
  db.delete(all_team_images)
  
  models.Team.update(team_id)
  team = team_get(team_id = team_id, is_reload = True)      

  return True
##############

def test_create(league_id = None, name = None, group_teams=[]):

    league = models.League.get_item(league_id)
    
    tournament = league.tournament_id
    
    params = {  "name":          name,
                "league_id":     league,
                "tournament_id": tournament,                    
    }

    new_group = models.Group.create(params)

    all_seasons = []
    
    for team_id in group_teams:
        team = models.Team.get_item(team_id)
        item = models.Season.gql("WHERE team_id = :1 and league_id = :2", team, league).get()
        item.group_id = new_group
        all_seasons.append(item)
    
    models.db.put(all_seasons)   

    deferred.defer(group_browse, league_id = league_id, is_reload = True)
    
    return True 


def test_create_confirm(league_id = None, group_id = None, name = None, group_teams=[]):

    league = models.League.get_item(league_id)
    

    new_group = models.Group.get_item(group_id)

    all_seasons = []
    
    for team_id in group_teams:
        team = models.Team.get_item(team_id)
        item = models.Season.gql("WHERE team_id = :1 and league_id = :2", team, league).get()
        item.group_id = new_group
        all_seasons.append(item)
    
    models.db.put(all_seasons)   

    deferred.defer(group_browse, league_id = league_id, is_reload = True)
    
    return True 

def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m
    


    
    
def test(league_id = "1004", limit = 1000):


    league_id = "1108"

    league = models.League.get_item(league_id)       
    
    nodes = models.PlayoffNode.gql("WHERE league_id = :1", league).fetch(limit)
    try:
        for node in nodes:
            logging.info(": %s", node.created)
    
    except:
        pass
    
    res = models.PlayoffCompetitor.gql("WHERE league_id = :1", league).fetch(limit)
    
    logging.info("competitors: %s", len(res))
    
    
    playoff = models.Playoff.gql("WHERE league_id = :1", league).fetch(limit)   


    db.delete(res)
    db.delete(nodes)
    db.delete(playoff)

        
    playoff_browse(league_id = league_id, is_reload = True)   
    
    return True    

    match_get(match_id = "5161", is_reload = True)

    match = match_get(match_id = "5161")
    
    logging.info(match["teams"][0]["name"])
    logging.info(match["teams"][1]["name"])    

    return True
    
    for item in ["1090","1091","1092","1093","1094","1095","1096","1097","1098","1099","1100","1101","1102","1103"]:
        match_browse(tournament_id = "1001", league_id = item, is_reload = True)     

    return True
    
    tournament = models.Tournament.get_item('1002')

    
    today =  datetime.datetime(2011, 11, 1)
        
    all_matches = models.Match.gql("WHERE tournament_id = :1 AND datetime >= :2 ORDER BY datetime ASC", tournament, today).fetch(limit)
    
    
    del_mas = [] 
    
    
    for match in all_matches:    
        deferred.defer(match_get, match_id = match.id, is_reload = True)

    return True 
    
        
    for match in all_matches:
    
        all_players = models.PlayerMatch.gql("WHERE match_id = :1", match).fetch(limit)
        for i, v in enumerate(all_players):
            for i2, v2 in enumerate(all_players): 
                if v.player_id.id == v2.player_id.id and v.team_id.id == v2.team_id.id and i < i2:
                    logging.info("team: %s \t player: %s \t datetime: %s",
                                   v.team_id.name, v.player_id.full_name, match.datetime)
                                   
                    del_mas.append(v2)
    


    models.db.delete(del_mas)  

    return True    
    
    for team in all_teams:
        deferred.defer(team_get_players, team_id = team.id, is_reload = True)
        deferred.defer(team_get_players_active,  team_id = team.id, is_reload = True)
        deferred.defer(team_get_players, team_id = team.id, stat=True, is_reload = True)


        
    for team in all_teams:    
        all_players = models.PlayerTeam.gql("WHERE team_id = :1", team).fetch(limit)
        for i, v in enumerate(all_players):
            for i2, v2 in enumerate(all_players): 
                if v.player_id.id == v2.player_id.id and i < i2:
                    logging.info("team: %s \t player: %s",
                                   team.name, v.player_id.full_name)
                                   
                    del_mas.append(v2)
    
    models.db.delete(del_mas)       
    
                 
    return True
            
    deferred.defer(statistics, league_id = "1085", is_reload=True)
    deferred.defer(statistics, league_id = "1085", limit = 1000, is_reload=True)
     
    
    deferred.defer(statistics, league_id = "1086", is_reload=True)
    deferred.defer(statistics, league_id = "1086", limit = 1000, is_reload=True)
     

    deferred.defer(statistics, league_id = "1094", is_reload=True)
    deferred.defer(statistics, league_id = "1094", limit = 1000, is_reload=True)
     

    deferred.defer(statistics, league_id = "1103", is_reload=True)
    deferred.defer(statistics, league_id = "1103", limit = 1000, is_reload=True)
                 
    return True
    
    goal        = models.EventType.get_item("1001").key() 
    
    team = models.Team.get_item("1535")
    player = models.Player.get_item("4795")
    league = models.League.get_item("1098")
    

    all_stat = models.StatPlayer.gql("WHERE league_id = :1 AND team_id = :2",
                                            league, team).fetch(limit)
     
    for item in all_stat:
        logging.info("score: %s \t name: %s", item.score, item.player_id.full_name) 
     
    models.db.delete(all_stat)
     
    deferred.defer(statistics, league_id = "1098", limit = 1000, is_reload=True)
     
    return True
    deferred.defer(league_get, league_id = "1025", is_reload=True)              
                        
    deferred.defer(league_browse, tournament_id = "1010", is_reload=True)
    
    return True
    
    
    team = models.Team.get_item("1116")
    league = models.League.get_item("1101")
    
    res = models.StatPlayer.gql("WHERE league_id = :1 and team_id = :2",
                                       league, team).fetch(limit)    

    db.delete(res)    
    deferred.defer(statistics, league_id = "1101", limit = 1000, is_reload = True)  

    return True

    league = models.League.get_item("1073")
    
    res = models.Season.gql("WHERE league_id = :1", league).fetch(limit)
    logging.info("season teams: %s", len(res))
  
    res = models.Group.gql("WHERE league_id = :1", league).fetch(limit)
    logging.info("groups: %s", len(res))        
    
    db.delete(res)
    
    deferred.defer(group_browse, league_id = "1073", is_reload=True)
  
    #deferred.defer(league_browse, tournament_id = "1002", is_reload=True)
    
    return True

    test_create(league_id = "1073", name=u'Высшая Лига 1-4 места',
                 group_teams=["1010", "1091", "1364", "1005"])

    test_create(league_id = "1073", name=u'Высшая Лига 5-8 места',
                 group_teams=["1004", "1001", "1022", "1006"])
                 
    return True

    test_create(league_id = "1084", name=u'Высшая Лига 1-6 места',
                 group_teams=["1178", "1174", "1359", "1366", "1170", "1321"])


    test_create(league_id = "1084", name=u'Высшая Лига 7-9 места',
                 group_teams=["1177", "1499", "1487"])
                 
                 
                 
    test_create(league_id = "1085", name=u'Первая Лига 1-6 места',
                 group_teams=[])
                 
    test_create(league_id = "1085", name=u'Первая Лига 7-10 места',
                 group_teams=[])
                 
                 
    test_create(league_id = "1086", name=u'Вторая Лига 1-6 места',
                 group_teams=["1324", "1370", "1373", "1485", "1358", "1475"])

    test_create(league_id = "1086", name=u'Вторая Лига 7-10 места',
                 group_teams=["1374", "1211", "1486", "1483"])
                 
    return True

    deferred.defer(player_browse, tournament_id = "1001", is_reload = True)  
    
    return True
    news_browse(tournament_id = "1003", is_reload = True)
    
    
    league_get(league_id = "1001", is_reload = True)
    league_get(league_id = "1002", is_reload = True)
    league_get(league_id = "1003", is_reload = True)
 
 
    return True    
    #deferred.defer(league_browse, tournament_id = "1003", is_reload = True)    
    
    '''
       Split several accounts for one player. Find all player_id and replace
       to original.       
    '''
    
    player = models.Player.get_item("1328")
    res = models.PlayerTeam.gql("WHERE player_id = :1", player).fetch(limit)
    logging.info(len(res))
    
    for item in res:
        logging.info("team: %s", item.team_id.name)
    team_get_players(team_id = "1076", is_reload = True)
    team_get_players_active(team_id = "1076", is_reload = True)
    team_get_players(team_id = "1076", stat=True, is_reload = True)
    
    return True
    
    
    player_original = models.Player.get_item("1328")
    player = models.Player.get_item("2681")
    
    
       
    

    all_refs = []
    
    res = pyclbr.readmodule('common.models')   
    for name, obj in res.items():        
        D = get_class("common.models." + name)
        try:
            if getattr(D, "player_id"):
                all_refs.append(D)
        except:
            pass             

    
    logging.info(all_refs)    
    
    for item in all_refs:
        res = item.gql("WHERE player_id = :1", player).fetch(limit)
        for value in res:
            value.player_id = player_original
        db.put(res) 
          
    
      
    #logging.info("modules: %s", res)  
      
    return True
    
    for item in xrange(1001, 1020):
        #logging.info(str(item))
        deferred.defer(league_get, league_id = str(item), is_reload = True)     
    
    return True
    
    goal      = models.EventType.get_item("1001")
    
    league_id = "1074"
    league    = models.League.get_item(league_id)        
    
    
    team_id   = "1023"
    team      = models.Team.get_item(team_id)    
    
    player    = models.Player.get_item("1754")         
     
    
    res = models.StatPlayer.gql("WHERE league_id = :1 AND player_id = :2 and team_id = :3",
                                            league, player, team).fetch(limit)

    logging.info("StatPlayer: %s", len(res))

    models.db.delete(res)                                                
            
    deferred.defer(stat_update, league_id = league_id, team_id = team_id)             
    deferred.defer(statistics, league_id = league_id, limit = 1000, is_reload = True)        
    
    
    
        
    #team_remove(team_id = "1540")
    #item = files.gs.create("/gs/arena/text.txt")   
    
    #logging.info("item: %s", item)
    
    #deferred.defer(player_browse, tournament_id = "1001", is_reload = True, _target="defworker")      

    #deferred.defer(team_remove, team_id = "1501")    
    #deferred.defer(group_browse, league_id = "1087", is_reload=True)    
       
    return True
    
    team = models.Team.get_item("1003")
    league = models.League.get_item("1073")
    
    all_items = models.Season.gql("WHERE team_id = :1 AND league_id = :2", team, league).fetch(1)
    
    models.db.delete(all_items)     
    
    team = models.Team.get_item("1065")

    
    all_items = models.Season.gql("WHERE team_id = :1 AND league_id = :2", team, league).fetch(1)
    
    models.db.delete(all_items)  
    
    
    league_update(league_id = "1073")
        
    return True
    
    
        
    tournament = models.Tournament.get_item("1002").key()
    
    #name = u'Интер'
    
    #name_s = '"' + name + '"'
    
    nn = [u'Интер']
    
    for name in nn:
        res = models.Team.gql("WHERE tournament_id = :1 and name = :2", tournament, name).fetch(limit)
        if len(res) > 1:
            break
    
    
    m = "9999"
    
    res2 = []
    
    for item in res:
        logging.info("id: %s",item.id)
        if int(item.id) < int(m):
            m = item.id
            value = item
    
    for item in res:
        if item.id != value.id:
            res2.append(item.key())      
        
    if len(res) < 2:
        return True
        
    logging.info("len(res): %s",len(res))
    
    logging.info("len(res2): %s",len(res2))    

    logging.info("min: %s", value.id)    
            
    
    mas = [ models.Season, models.PlayoffCompetitor, models.Competitor,  
            models.Score,  models.PlayerMatch, models.PlayerTeam, models.Event,
            models.Sanction, models.StatPlayer, models.Image, models.Vote]
    
    for item in mas:
        rem  = item.gql("WHERE tournament_id = :1 and team_id IN :2", tournament, res2).fetch(limit)
        for x in rem:
            x.team_id = value
                        
        db.put(rem)          
            
    '''
    mas = [ models.Season ]
    for item in mas:
        rem  = item.gql("WHERE tournament_id = :1 and team_id IN :2", tournament, res2).fetch(limit)
        db.delete(rem)         
    '''
    
    for item in res2:        
        db.delete(db.get(item))          
    
    
    deferred.defer(team_browse_rating, tournament_id = "1002", is_reload = True)  
    
    
    deferred.defer(team_browse, tournament_id = "1002", is_reload = True)      

    #deferred.defer(group_browse, league_id = 1078, is_reload = True)        
    
    #deferred.defer(tournament_browse, limit = 1000, is_reload = True)        
    
    

    return True      
    
    #deferred.defer(league_browse, tournament_id = "1007", is_reload=True)
    #league_update(league_id = "1067")
    
    deferred.defer(team_remove, team_id = "1484")    
    deferred.defer(group_browse, league_id = "1084", is_reload=True)
    
 
    return True
        
    deferred.defer(match_browse, tournament_id = "1004", is_reload=True)             
    
    tournament = models.Tournament.get_item("1004")
  
    if not tournament:    
        return None
        
    results = models.Team.gql("WHERE tournament_id = :1", tournament).fetch(limit)
    db.delete(results)
    
    results = models.Player.gql("WHERE tournament_id = :1", tournament).fetch(limit)
    db.delete(results)    
    
    deferred.defer(team_browse, tournament_id = "1004", is_reload=True)
    deferred.defer(team_browse_rating, tournament_id = "1004", is_reload=True)    
    
       
    return True    
    

    #deferred.defer(team_browse_rating, tournament_id = "1008", is_reload = True)
      
    deferred.defer(statistics, league_id = "1067", is_reload = True)
    #deferred.defer(statistics, league_id = "1067", limit = 1000, is_reload = True)
    
    #match_remove("3205")
    #league_browse(tournament_id = "1001", is_reload = True)
    #match_browse(league_id = "1067", is_reload = True)
    
    #match_browse(team_id = "1003", is_reload = True)

    return True    
    

    stage_name = 'third-place'
    
    stage = models.PlayoffStage.gql("WHERE name = :1", stage_name).get()      
    
    if stage:
        logging.info("created")
    
    league_id = "1067"
    
    league = models.League.get_item(league_id)
    
    tournament = league.tournament_id

    playoff = models.Playoff.gql("WHERE league_id = :1", league).get()  
    
    if not playoff:
        return False
    
           
    params = {    'tournament_id': tournament,
                  'league_id':     league,
                  'playoff_id':    playoff,
                  'playoffstage_id':      stage,
              } 
        

    is_third = models.PlayoffNode.gql("WHERE league_id = :1 and playoffstage_id = :2", league, stage).get()    
    
    if is_third:
        logging.info("Third Place ALready:")
        return False
            
    playoff_node = models.PlayoffNode.create(params)                
    params_node = {
                    'tournament_id':   tournament,
                    'league_id':       league,
                    'playoff_id':      playoff,
                    'playoffstage_id': stage,
                    'playoffnode_id':  playoff_node,                      
          }    
    models.PlayoffCompetitor.create(params_node)
    models.PlayoffCompetitor.create(params_node)     
                    
                     
    playoff_browse(league_id = league_id, is_reload = True)     

    return True

    
    res = models.Team.all().fetch(limit)    
    
    #for item in res:
    #    logging.info(": %s", item.id)
    
        
    
    x = [ 4, 19, 1, 56, 23]
    
    
    logging.info("Start MAP")
        
    m = reduce(lambda a,b: max((a or getattr(a,"id")), (getattr(b,"id") or b)), res)    
    logging.info("map results: %s",m)
    
    
    mas = []
    m = "0"
    
    logging.info("Start Manual")    
    for item in res:
        if item.id > m:
            m = item.id
        
        
    logging.info("map results: %s",m) 
    
        
    return True        

        
    return True         
        
    league_remove(league_id = "1069")      
    league_remove(league_id = "1070")      
    league_remove(league_id = "1071")              
    league_remove(league_id = "1076")          

    deferred.defer(league_browse, tournament_id = "1008", is_reload=True)

    #deferred.defer(statistics, league_id = "1040", limit = 1000, is_reload = True)

    return True 
    start = 1234
    
    while start <= 1248:

        
        n = str(start)
        
        logging.info("team: %s",str(n))
        
        deferred.defer(team_remove, team_id = n)
       
        
        start += 1
    

    deferred.defer(group_browse, league_id = "1025")

    return True

  
    
    #logging.info("os.environ: %s",os.environ)    
    
    return True       
       
    league = models.League.get_item("1041")       
    
    nodes = models.PlayoffNode.gql("WHERE league_id = :1", league).fetch(limit)
    for node in nodes:
        logging.info(": %s", node.created)
    
    logging.info("last: %s", node.created)
    
    res = models.PlayoffCompetitor.gql("WHERE playoffnode_id = :1", node).fetch(limit)
    
    logging.info("competitors: %s", len(res))
    
    db.delete(res)
    db.delete(node)
        
    playoff_browse(league_id = "1041", is_reload = True)    
        
    return True         
        
    #group_A = ["1321", "1170", "1178", "1173", "1320", "1175"]  
    

    #test_create_confirm(league_id = "1039", group_id = '1008', name=u'Высшая Лига 1-6 места',  
    #                    group_teams=["1321", "1170", "1178", "1173", "1320", "1175"])
    #                    
    #test_create_confirm(league_id = "1039", group_id = '1009', name=u'Высшая Лига 7-10 места',
    #                     group_teams=["1319", "1372", "1172", "1327"])
    
    
    test_create_confirm(league_id = "1040", group_id = '1010', name=u'Первая Лига 1-6 места',  
                          group_teams=["1359", "1332", "1366", "1331", "1187", "1185"])
                          
    test_create_confirm(league_id = "1040", group_id = '1011', name=u'Первая Лига 7-10 места', 
                          group_teams=["1184", "1376", "1186", "1375"])

       
    return True

    
    deferred.defer(group_browse, league_id = '1039', is_reload = True)    
    return True    
        
    
    player = models.Player.get_item("2064")
    team   = models.Team.get_item("1360")    
    
    all_players = models.PlayerTeam.gql("WHERE player_id = :1 AND team_id = :2", player, team).fetch(limit)
    models.db.delete(all_players)


    return True
    
    playoff_remove(league_id = "1049")
    playoff_remove(league_id = "1050")
    playoff_remove(league_id = "1051")    
     
    league_remove(league_id = "1052")      

    return True

    team = models.Team.get_item("1179")
    league = models.League.get_item("1040")
    
    all_items = models.Season.gql("WHERE team_id = :1 AND league_id = :2", team, league).fetch(1)
    
    models.db.delete(all_items)     
    
    
    return True

    memcache_name = 'person_start_cursor21'
    start = [memcache.get(memcache_name) or 0]      
    logging.info("Start: %s", start)

    new_events = []
    
    all_items = models.Player.gql("WHERE created > :1", start).fetch(limit)
    
    is_return = False
    
    if len(all_items) < 1:
          
        is_return = True
    
    for item in all_items:   
        if item.birthday:           
            item.datetime = datetime.datetime(year = item.birthday.year, month = item.birthday.month, day = item.birthday.day)              
        else:
            item.datetime = None
            
        
        deferred.defer(player_get, player_id = item.id, is_reload = True, _queue="default")               
                
    logging.info("Len Players events: %s",len(all_items))                
    models.db.put(all_items)
   
    
    if is_return == True:

        return True    
    
    last = all_items[-1].created
    memcache.set(memcache_name, last, 360)   


            
    
    return False     

    return True

    del_item = models.Tournament.get_item("1004")
    
    mas = [models.League, models.Team, models.Group, models.Season, models.Playoff, models.PlayoffNode, models.PlayoffCompetitor, 
            models.Match, models.RefereeMatch, models.Competitor, models.Score, models.Player, models.PlayerMatch, models.PlayerTeam, 
            models.Event, models.Sanction, models.StatPlayer]
    
    for item in mas:
        rem  = item.gql("WHERE tournament_id = :1", del_item).fetch(limit)
        db.delete(rem)                

    return True
       
 

    goal_key        = models.EventType.get_item("1001").key()
    yellow_card_key = models.EventType.get_item("1002").key()
    red_card_key    = models.EventType.get_item("1003").key()    
    
    
    all_event_types = { "all-goals":   goal_key,
                        "yellow-card": yellow_card_key,
                        "red-card":    red_card_key,
                      }   

 
    for item, event_key in all_event_types.iteritems():    
        logging.info("Item: %s \t event_key: %s",item, event_key)    
    
    return True
    
    for i in xrange(50):
        x = str(i + 1200)
        deferred.defer(team_get_players, team_id = x, stat = True, is_reload = True, _queue="default")
    
    
    return True
    t = models.Tournament.get_item("1001")        
    t.lat = "55.049035621789365"
    t.lon = "82.92583465576172"
    t.put()    
      
    tournament_get(tournament_id = "1010", is_reload = True)           
    
    
    
    tournament_browse(sport_id = "1001", is_reload = True) 
    
    return True
    u = models.User.get_item("100001809361460")
    logging.info("name: %s",u.name)
    
    t = models.Tournament.get_item("1008")        
    t.user_id = u
    t.put()
    
    t = models.Tournament.get_item("1009")        
    t.user_id = u
    t.put()    
    tournament_get(tournament_id = "1008", is_reload = True)
    tournament_get(tournament_id = "1009", is_reload = True)    
    
    return True   
    
    league_id = "1015"    
    league = models.League.get_item(league_id)
    
    tournament = league.tournament_id
    
    params = {  "name":          "Group A",
                "league_id":     league,
                "tournament_id": tournament,                    
    }

    new_group = models.Group.create(params)
    
    group_A = ["1177", "1174", "1176","1178","1172"]     
    
    all_seasons = []
    
    for team_id in group_A:
        team = models.Team.get_item(team_id)
        item = models.Season.gql("WHERE team_id = :1", team).get()
        item.group_id = new_group
        all_seasons.append(item)
    
    models.db.put(all_seasons)
    
    #***************************************************************#
    
    league_id = "1015"    
    league = models.League.get_item(league_id)
    
    tournament = league.tournament_id
    
    params = {  "name":          "Group B",
                "league_id":     league,
                "tournament_id": tournament,                    
    }

    new_group = models.Group.create(params)
    
    group_A = ["1171", "1175", "1170","1173"]     
    
    all_seasons = []
    
    for team_id in group_A:
        team = models.Team.get_item(team_id)
        item = models.Season.gql("WHERE team_id = :1", team).get()
        item.group_id = new_group
        all_seasons.append(item)
    
    models.db.put(all_seasons)    
    
    #***************************************************************#
    
    league_id = "1016"    
    league = models.League.get_item(league_id)
    
    tournament = league.tournament_id
    
    params = {  "name":          "Group A",
                "league_id":     league,
                "tournament_id": tournament,                    
    }

    new_group = models.Group.create(params)
    
    group_A = ["1183", "1182", "1184","1179","1185"]     
    
    all_seasons = []
    
    for team_id in group_A:
        team = models.Team.get_item(team_id)
        item = models.Season.gql("WHERE team_id = :1", team).get()
        item.group_id = new_group
        all_seasons.append(item)
    
    models.db.put(all_seasons)
    
    #***************************************************************#
    
    league_id = "1016"    
    league = models.League.get_item(league_id)
    
    tournament = league.tournament_id
    
    params = {  "name":          "Group B",
                "league_id":     league,
                "tournament_id": tournament,                    
    }

    new_group = models.Group.create(params)
    
    group_A = ["1211", "1180", "1181","1186","1187","1210"]     
    
    all_seasons = []
    
    for team_id in group_A:
        team = models.Team.get_item(team_id)
        item = models.Season.gql("WHERE team_id = :1", team).get()
        item.group_id = new_group
        all_seasons.append(item)
    
    models.db.put(all_seasons)    
    
    '''
    #league 1015    
    group_A = ["1177", "1174", "1176","1178","1172"]    
    group_B = ["1171", "1175", "1170","1173"]
    
    #league 1016    
    group_C = ["1183", "1182", "1184","1179","1185"]    
    group_D = ["1211", "1180", "1181","1186","1187","1210"]
    '''
    
    
    return True  
    
    won_key  = models.ResultType.get_item("1002").key()
        
    league  = models.League.get_item("1004").key()
    team    = models.Team.get_item("1010").key()            
        
    test  = team_results(league, team, won_key)    
    logging.info("Count : %s",test)
        

    

    return True  
    
    playoff_remove(playoff_id = "1003", league_id = "1015")
    
    return True    

    
    
    memcache_name = 'person_start_cursor13'
    start = [memcache.get(memcache_name) or 0]      
    logging.info("Start: %s", start)

    new_events = []
    
    all_items = models.Competitor.gql("WHERE created > :1", start).fetch(limit)
    
    is_return = False
    
    if len(all_items) < 1:
          
        is_return = True
    
    for item in all_items:    
        if item.match_id.playoff_id:
            item.playoff_id      = item.match_id.playoff_id
            item.playoffstage_id = item.match_id.playoffstage_id
            item.playoffnode_id  = item.match_id.playoffnode_id   
            logging.info("set planode")        
        else:
            item.playoff_id = None
            item.playoffstage_id = None
            item.playoffnode_id = None               
                
    logging.info("Len Players events: %s",len(all_items))                
    models.db.put(all_items)
    
    
    if is_return == True:

        return True    
    
    last = all_items[-1].created
    memcache.set(memcache_name, last, 360)   


            
    
    return False

    team = models.Team.gql("WHERE id = :1", "1169").get()
    if team:
       models.db.delete(team)
    return True
    
    pls = ["1001","3265","3266"]
    
    for item in pls:    
        player = models.Player.get_item(item)
        if player:
            all_players = models.PlayerTeam.gql("WHERE player_id = :1", player).fetch(limit)
            models.db.delete(all_players)
            models.db.delete(player)
            models.Player.update(item)
            logging.info("Player %s is deleted", player.second_name)

    return True
    
    key_name = "last_competitor_id57"

    last = memcache.get(key = key_name)                     
    
    type_goal = models.EventType.get_item("1001").key()        
        
    all_items = models.PlayerTeam.gql("WHERE created > :1 ORDER BY created ASC", last).fetch(limit)  
    if len(all_items) < 1:
        return True
        
    all_players = []
        
    for item in all_items:
    
        player = item.player_id
        team   = item.team_id        
    
        goals = models.Event.gql("WHERE player_id =:1 AND team_id = :2 AND eventtype_id = :3", player, team, type_goal).count(1000)
        test = models.Event.gql("WHERE player_id =:1 AND team_id = :2 AND eventtype_id = :3", player, team, type_goal).get()
        value = 2
        try:
            league = test.league_id
            value =  test.league_id.ranking
        except:
            value = 2

            
        player.ranking += team.ranking + goals * value
        
        all_players.append(player)
        
        last = item.created
    
 
    db.put(all_players)      
           
              

    logging.info("Count items: %s", len(all_items))        
    memcache.set(key = key_name, value = last)
    
    

    return False
    
    user = models.User.get_item("102990095653693255899")
    if user:
        tournament = models.Tournament.get_item("1005")
        tournament.user_id = user
        tournament.put()
        models.Tournament.update("1005")

    #team_id = models.User.get_item("100002144359648")
    #team_id = models.Team.get_item(team_id)
    #100002144359648
    #t = memcache.flush_all()
    #logging.info("Flush ALL: %s",t)
    #models.Team.update("1030")

    match_browse(team_id = "1030", is_reload = True)

    return

    tournament_id = models.Tournament.get_item("1001")
    
    all_players = models.Player.gql("WHERE tournament_id = :1 ORDER BY second_name", tournament_id).fetch(3000)

    last = all_players[0]      
    last.second_name = ""
    mas = ""

    for player in all_players:
            
        if last.second_name == player.second_name: 
            if last.name == player.name:

                team1 = models.PlayerTeam.gql("WHERE player_id = :1", last).get()
                team2 = models.PlayerTeam.gql("WHERE player_id = :1", player).get()
                
                try:                
                    logging.info("\n%s %s: %s ( %s ) - %s ( %s )", player.second_name, player.name, team1.team_id.name, team1.league_id.name,
                                  team2.team_id.name, team2.league_id.name)
                except:
                    pass

        last = player
    
    #logging.info("%s %s: %s - %s", player.second_name, player.name, team1.team_id.name, team2.team_id.name)

    return

    logging.info("Dobule !!!!!!!!!!!!!!1")

    doubles = [
        (u'Виноградов Никита', u'Затулинка', u'Лидер'), 
        (u'Белых Артем', u'Затулинка', u'Атлетик'),
        (u'Мишнев Артем', u'Затулинка', u'Спартак'),
        (u'Шатунов Александр', u'Затулинка', u'Спартак'),
        (u'Морозов Игорь', u'Затулинка', u'АТОМ-ОХРАНА'),
        (u'Семенов Александр', u'ФК Чемской', u'Новосибирск'),
        (u'Семиненко Юрий', u'ФК Чемской', u'Крафт'),
        (u'Ростовцев Александр', u'ФК Чемской', u'Крафт'),
        (u'Щукин Андрей', u'Комета', u'АТОМ-ОХРАНА'),
        (u'Алексеев Антон', u'Рассвет', u'Транссиб'),
        (u'Артюхов Андрей', u'Рассвет', u'Нефрит'),
        (u'Комаров Алексей', u'Рассвет', u'Транссиб'),
        (u'Реутов Федор', u'Рассвет', u'Атлетик'),
        (u'Соломатов Дмитрий', u'Рассвет', u'Транссиб'),
        (u'Коваленко Денис', u'Система Косметикс', u'АТОМ-ОХРАНА'),
        (u'Лычко Сергей', u'Восток', u'Нефрит'),
    ]

    tournament_id = models.Tournament.get_item("1003")

    for item in doubles:
      

        value = item[0].split(" ")

        all_players = models.Player.gql("WHERE tournament_id = :1 AND second_name = :2 AND  name = :3 ORDER BY created ASC", 
                                 tournament_id, value[0], value[1] ).fetch(limit)

        if len(all_players) < 2:
            logging.info("Len small %s", value[1])   
            continue

        player_id = all_players[0]
        double_player_id = all_players[1]

        #logging.info("Name: %s \t id: %s \t id: %s", item[0], all_players[0].id, all_players[1].id)        
      
        mod_items = [models.PlayerTeam, models.Event, models.Sanction, models.StatPlayer, models.PlayerMatch]
        for item in mod_items:
            all_values = item.gql("WHERE tournament_id = :1 AND player_id = :2", tournament_id, double_player_id ).fetch(limit)
            for value in all_values:
                value.player_id = player_id

                logging.info("Original: %s %s \t\t Double: %s %s ", player_id.id, player_id.second_name, double_player_id.id, double_player_id.second_name)                   
            #db.put(all_values)
                

    return

    t = "%D0%9F%D0%BE%D0%BB%D0%B51"

    #urllib.urlencode(u'a unicode string'.encode('utf-8'))

    logging.info(urllib.unquote(t))
    logging.info(t.decode('utf-8'))

    return    
    t = memcache.flush_all()
    logging.info("Flush ALL: %s",t)
    return

    # Start a query for all Person entities.
    #people = models.PlayerTeam.all().count()
    #logging.info("Active True:  %s", people)

    # If the app stored cursors during a previous request, use them.
    return True
    
    start = [memcache.get('person_start_cursor') or 0]
    all_competitors = models.Competitor.gql("WHERE created > :1", start).fetch(100)
        
    #last = all_competitors[-1].created
    #memcache.set('person_start_cursor', last, 360)        

    if len(all_competitors) == 0:
        return True

    new_playermatches = []
        
    for competitor in all_competitors:
        
        if db.GqlQuery("SELECT __key__ FROM PlayerMatch WHERE match_id = :1 AND team_id = :2", competitor.match_id.key(), competitor.team_id.key()).get():
            logging.info("Exist: Continue")
            continue        

        teamplayers = models.PlayerTeam.gql("WHERE team_id = :1", competitor.team_id.key()).fetch(limit)

        for item in teamplayers:  
        
            params = {
                  'match_id': competitor.match_id,
                  'team_id' : item.team_id,

                  'tournament_id': item.tournament_id,
                  'league_id': competitor.league_id,
                  'season_id': competitor.season_id,
                      
                  'player_id': item.player_id,
                }
              
            playermatch_ref = models.PlayerMatch(**params)
            new_playermatches.append(playermatch_ref) 

    last = all_competitors[-1].created
    memcache.set('person_start_cursor', last, 360)

    logging.info("Active Last:  %s", last)
    db.put(new_playermatches)

    c = models.PlayerMatch.all().count()
    logging.info("Active All:  %s", c)
    
    


    return False


    soccer = {
              "1001": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=453",
              "1002": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=454",
              "1003": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=455",
              "1004": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=456",
              "1005": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=457",
              "1006": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=459",
              "1007": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=460",
              "1008": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=461",
              "1009": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=462",
              "1010": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=463",
              "1010": "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=464",
              }
    
    
    name_replace = {
                    u'42-й регион Кемеровская обл.' :   u'42-й регион',
                    u'Медицинский Центр Биовэр'     :   u'М.Ц. Биовэр',
                    u'Мебельная фабрика Золушка'    :   u'М.Ф. Золушка', 
                    u'Вип-сервис'                   :   u'VIP-сервис',
                    u'Жд/экспедиция'                :   u'Желдорэкспедиция',
                    u'Некст'                        :   u'Next',
                    u'ВБД'                          :   u'ВиммБилльДанн',
                    u'Прагма'                       :   u'Прагма Краснозерское',
                    u'Г/Ривард'                     :   u'Гранд-Ривард',                    
                }
    

    league = models.League.get_item(league_id)
    league_link = soccer[league_id]
    
    #league = models.League.get_item("1004")
    #league_link = "http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=456"
    
    #all_matches = models.Match.gql("WHERE league_id =:1", league).fetch(limit)
    #models.db.delete(all_matches)
    #all_competitors = models.Competitor.gql("WHERE league_id =:1", league).fetch(limit)
    #models.db.delete(all_competitors)
    
    tournament = league.tournament_id
    
    
    result = urlfetch.fetch(url=league_link, deadline=10)
    
    tmp1 = result.content
    #tmp = unicode(tmp, 'cp1251').decode('utf-8')
    #tmp = unicode(tmp, 'cp1251')
    tmp = result.content.decode('cp1251')
    tmp = tmp.split("resultable")[1]
    tmp = tmp.split("<tr bgcolor=#ffffff>")
    
    for item in tmp[1:]:
        
        item = item.replace("<b>", "")
        item = item.replace("</b>", "")        
        
        item = item.split("<td>")
        
        teams = item[1].split("</td>")[0].split(" - ")
        team1_name = teams[0]
        #p = unicode(team1_name, 'cp1251')   
        #team1_name = unicode(team1_name, 'cp1251')#.encode('utf-8')    
        for value in name_replace:
            if team1_name == value:
                logging.info("Team1 name is changed") 
                team_name1 = name_replace[value]
            
        #team1_name = unicode(team1_name, 'cp1251').encode('utf-8')  
        logging.info("Team1: %s", team1_name)    
        team1_names = models.Team.gql("WHERE name = :1", team1_name).fetch(limit)
        
        
        team1 = None        
           
        for team in team1_names:
            team_season = models.Season.gql("WHERE league_id = :1 AND team_id = :2", league, team).count()
            if team_season > 0:
                team1 = team 
                break
                        
        if not team1:
            continue    
        
                   
        
        team2_name = teams[1]
        for value in name_replace:
            if team2_name == value:
                logging.info("Team2 name is changed") 
                team_name2 = name_replace[value]
                
        #team2_name = unicode(team2_name, 'cp1251').encode('utf-8')                     
            
        team2_names = models.Team.gql("WHERE name = :1", team2_name).fetch(limit)
        
        team2 = None        
           
        for team in team2_names:
            team_season = models.Season.gql("WHERE league_id = :1 AND team_id = :2", league, team).count()
            if team_season > 0:
                team2 = team 
                break
                        
        if not team2:
            continue    
        
        score = item[2].split("</td>")[0]
        if len(score) > 2:
            score = score.split("-")
            score1 = score[0]
            score2 = score[1]
        
        match_date  = item[3].split("</td>")[0]
        match_time  = item[4].split("</td>")[0]
        
    
        full_datetime  = str(match_date) + " " + str(match_time)
        match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
        
        match = None
        
        all_matches = models.Match.gql("WHERE league_id =:1 AND datetime = :2 ORDER BY datetime DESC", league, match_datetime).fetch(limit)
        
        for match_item in all_matches:
            is_team1 = False
            is_team2 = False
        
            for competitor in match_item.match_competitors:
                if competitor.team_id.key() == team1.key():
                    is_team1 = True
                elif competitor.team_id.key() == team2.key():
                    is_team2 = True
                    
            if is_team1 and is_team2:
                match = match_item
                break                        
        
        if not match:
            # Create
            match_id = match_create_complete(league, team1, team2, match_datetime)            

                
        #all_competitors1 = models.Competitor.gql("WHERE league_id =:1 AND team_id = :2", league, team1_id).fetch(limit)
        #all_competitors2 = models.Competitor.gql("WHERE league_id =:1 AND team_id = :2", league, team2_id).fetch(limit)
        #
        #for comp1 in all_competitors1:
        #    for comp2 in all_competitors2:
        #        if comp1.match_id == comp1.match_id:
        #            match = comp1.match_id
    

    #Soccer-Arena
    #3th  league 
    #1004    
    #http://soccer.ossib.ru/groups.php?act=kalendar&turnirs=83&groups=456
    


def test2(league_id = "1003", limit = 100):
       

    
    soccer = {
              "1003": "http://soccer.ossib.ru/groups.php?act=statistic&turnirs=83&groups=455",
              "1004": "http://soccer.ossib.ru/groups.php?act=statistic&turnirs=83&groups=456",
              "1005": "http://soccer.ossib.ru/groups.php?act=statistic&turnirs=83&groups=457",
              "1006": "http://soccer.ossib.ru/groups.php?act=statistic&turnirs=83&groups=459",
              "1007": "http://soccer.ossib.ru/groups.php?act=statistic&turnirs=83&groups=460",
              "1008": "http://soccer.ossib.ru/groups.php?act=statistic&turnirs=83&groups=461",
              "1009": "",
              "1010": "",
              "1011": "",
              }
    
    
    name_replace = {
                    u'42-й регион Кемеровская обл.' :   u'42-й регион',
                    u'Медицинский Центр Биовэр'     :   u'М.Ц. Биовэр',
                    u'Мебельная фабрика Золушка'    :   u'М.Ф. Золушка', 
                    u'Вип-сервис'                   :   u'VIP-сервис',
                    u'Жд/экспедиция'                :   u'Желдорэкспедиция',
                    u'Некст'                        :   u'Next',
                    u'ВБД'                          :   u'ВиммБилльДанн',
                    u'Прагма'                       :   u'Прагма Краснозерское',
                    u'Г/Ривард'                     :   u'Гранд-Ривард',    
                    u'КДВ'                          :   u'КДВ Новосибирск',
                    u'Д/город'                      :   u'Добрый город',
                    u'С/троллейбус'                 :   u'Сибирский троллейбус',
                    u'Н/энерго'                     :   u'Новосибирскэнерго',
                    u'Кока Кола'                    :   u'Coca Cola',
                    u'Ч/туман'                      :   u'Черный туман',
                    u'МЛК'                          :   u'Моя любимая команда',
                    u'Домоцентр'                    :   u'Домоцентр-Розница',
                    u'ГВК'                          :   u'Горводоканал',
                    u'Машук'                        :   u'Машук-Нск',
                    u'Арчибальд'                    :   u'Арчибальд!',
                    u'Гр.здоровья'                  :   u'Группа здоровья',
                    u'Сокол'                        :   u'Сокол-Эфес',
                    u'С/энергосервис'               :   u'Сибирьэнергосервис',                    
                    u'С/гипротранспуть'             :   u'Сибгипротранспуть',
                    u'Центр'                        :   u'ФК Центр',
                    u'Фортуна'                      :   u'ФК Фортуна', 
                    u'Ю/Запад'                      :   u'Юго-Запад',
                    u'Петрович'                     :   u'ФК Петрович',
                    u'Ост-ком'                      :   u'Ost-com',
                    u'Брайтком'                     :   u'БрайтКом',
                    u'НЭВЗ'                         :   u'НЭВЗ-Союз',
                    u'Форвард-2'                    :   u'Forward-2',
                }   
    

    league = models.League.get_item(league_id)
    league_link = soccer[league_id]
    
    tournament = league.tournament_id
    
    
    result = urlfetch.fetch(url=league_link, deadline=10)
    
    tmp1 = result.content
    tmp = result.content.decode('cp1251')
    tmp = tmp.split(u'БОМБАРДИРЫ')[1].split("size=2")[1].split("</FONT>")[0]
    
    
    #m = re.match('>\d+', tmp)

    all_ratings = []
    
    #object = re.compile( ur"(?P<section>{[^}\n]+})|(?:(?P<name>[^=\n]+)=(?P<value>[^\n]+))", re.M | re.S | re.U )
    object = re.compile(">[\d+]")
    result = object.finditer( tmp )
    for match in result :
        y = match.group(0)[1:]
        all_ratings.append(y)
        continue

    
    
    m = re.split('>\d+', tmp)
    
    #tmp = tmp.split("<tr bgcolor=#ffffff>")
    all_players = []
    
    for index, item in enumerate(m[1:]):
        
        item = item.replace("<BR>", "")
        item = item.replace("<STRONG>", "")
        item = item.replace("</STRONG>", "")
        item = item.replace("<STRONG", "")    
        item = item.replace("<BR", "")
        item = item.replace(u'голов', "")
        item = item.replace(" - ", "")       
        item = item.replace(")", "(")  
        
        
        list_item = item.split(", ")
        
        for player_item in list_item:
            content = player_item.split("(")
            try:
                player_team_name = content[1]#.split(")")[0]
            except:
                logging.info("Error split player:  %s", content[0])
                continue
            
            for value in name_replace:
                if player_team_name == value:                     
                    player_team_name = name_replace[value]
                    #logging.info("Team name is changed:  %s  to   %s", value, player_team_name)
            
            player_full_name = content[0]
            if player_full_name[0] == " ":
                player_full_name = player_full_name[1:]
                
            player_full_name = player_full_name.replace(" ", ".")
            player_full_name = player_full_name.replace("..", ".")
            
            if player_full_name[0] == ".":
                player_full_name = player_full_name[1:]            
            
            s1 = player_full_name.split(".")
            if len(s1) == 1:
                first_name = ""
                second_name = s1[0]
            
            elif len(s1) == 2:
                first_name = s1[0] + '.'
                second_name = s1[1]
            
            elif len(s1) == 3:
                first_name = s1[0] + '.' + s1[1] + '.'
                second_name = s1[2]
        
        
            t = 2
            
            people = [first_name, second_name, player_team_name, all_ratings[index]]
            all_players.append(people)
        continue
    
    
    t = 1
    
    for item in all_players:
        first_name = item[0]
        second_name = item[1]
        
        team = models.Team.gql("WHERE name = :1", item[2]).get()
        if not team:
            logging.info("No Team found:  %s", item[2] )
            continue
        
        season = models.Season.gql("WHERE league_id = :1 AND team_id = :2", league, team).get()
        if not season:
            continue
        
        is_player_exist = False
        
        if second_name == u'Леваков':
            t = 1

        players = models.Player.gql("WHERE second_name = :1", second_name).fetch(100)   
        
        for player in players: 
                    
            player_team = models.PlayerTeam.gql("WHERE player_id = :1 AND team_id = :2", player, team).get()
            #db.delete(player_team)
            #continue
            if player_team:
                if len(first_name) == 0:
                    is_player_exist = True
                    break
                
                
                if player.name[0] == " ":
                    player.name = player.name[1:]
                
                if len(first_name) > 0:
                    if player.name[0] == first_name[0]: 
                        #logging.info("Player is exist:  %s  %s  (%s)", item[1], item[0], item[2] )
                        is_player_exist = True
                        break
        
        #db.delete(players)        
        if is_player_exist:
            continue        
        
        logging.info("New Player:  %s  %s  (%s)", item[1], item[0], item[2] )
        
        params = {'name': first_name,
              'second_name': second_name,
              'tournament_id': team.tournament_id,
            }
    
        player_ref = models.Player.create(params)
    
        params = {'tournament_id': team.tournament_id,
              'player_id':     player_ref,
              'team_id':       team,
            }

        teamplayer_ref = models.PlayerTeam(**params)
        teamplayer_ref.put()
        
        

    
    '''
        item = item.split("<td>")
        
        teams = item[1].split("</td>")[0].split(" - ")
        team1_name = teams[0]
        #p = unicode(team1_name, 'cp1251')   
        #team1_name = unicode(team1_name, 'cp1251')#.encode('utf-8')    
        for value in name_replace:
            if team1_name == value:
                logging.info("Team1 name is changed") 
                team_name1 = name_replace[value]
            
        #team1_name = unicode(team1_name, 'cp1251').encode('utf-8')  
        #logging.info("Team1: %s", team1_name)    
        #team1_names = models.Team.gql("WHERE name = :1", team1_name).fetch(limit)
    '''

    

###############
def tournament_create(request = None, form = None):

    logging.info("request: %s",request.POST)

    sport_id = request.POST.get("sport","")            
    name = request.POST.get("name","")   
    lat = request.POST.get("lat","")   
    lon = request.POST.get("lon","")  
        
    if not name:
        logging.info("not name")
        return None
        
    if not sport_id:
        logging.info("not sport_id")
        return None

    if not request.user:
        logging.info("not request.user")
        return None
        
    if lat is None or lon is None:
        logging.info("not location")
        return None        
  
    sport_ref = models.Sport.get_item(sport_id)
     
        
    params = {'name':     name,
              'user_id':  request.user.key(),
              'sport_id': sport_ref,
            }

    tournament = models.Tournament.create(params)
    
    form.save(item = tournament)
    
    deferred.defer(tournament_browse, limit = 1000, is_reload = True)

    return tournament.id

def tournament_edit(form = None, tournament_id = None, limit = 100):

    tournament = models.Tournament.get_item(tournament_id)
    
    form.save(item = tournament)
 

    tournament_get(tournament_id = tournament_id, is_reload = True)
    deferred.defer(tournament_browse, limit = 1000, is_reload = True)    
    
    return tournament.id


@check_cache
def tournament_browse(limit=1000,
                 is_reload=None, memcache_delete=None, key_name=""):
                 
    results = models.Tournament.gql("ORDER BY created ASC").fetch(limit)
    
    #logging.info("len(results): %s",len(results))
        
    return cache_set(key_name, results)
    
'''                     
#def tournament_browse(lat = None, lon = None, sport_id = None, limit=1000, offset=None,
#                 is_reload=None, memcache_delete=None, key_name=""):

    
    results = models.Tournament.gql("ORDER BY created ASC").fetch(limit)
    
    
    return cache_set(key_name , results)
        
        
    #for item in value:
    #    logging.info("Tournament: %s", item.name)    
    
    include = ["id", "sport_id", "name", "lat", "lon", "location",
               "country", "city", "address", "contacts", "url", "email"]
    
    results = jsonloader.encode(input = value, include = include)
    
    return cache_set(key_name , results, include = include)
''' 



def tournament_get_tournaments(limit=48, offset=None):

    query = models.Tournament.all()
    rv = query.fetch(limit)

    return rv


@check_cache
def tournament_get(tournament_id = None, limit=1000, offset=None,
                 is_reload=None, memcache_delete=None, key_name=""):
    
    results = models.Tournament.get_item(tournament_id)
    
    return cache_set(key_name , results)



#######
#######
#######

#@public_owner_or_contact
def user_get_tournaments_admin(user, limit=48, offset=None):

    results = models.Tournament.all().filter('actor_id = :1', user).fetch(limit)
    #user.user_tournaments

    return results


def weather_get(match):
    return models.Weather.gql("WHERE date = :1", match.datetime.date()).get()    
        
    

def weather_update():

    result = urlfetch.fetch(url="http://www.foreca.ru/Russia/Novosibirsk?tenday&lang=en", deadline=10)
    tmp = result.content.decode('utf-8').split("<!-- START -->")[1]

    all_days = tmp.split("c1 ")
    for day_item in all_days[1:]:
        
            
        item = day_item.split('"')
        overcast = item[0]
        strdate = item[2].split("=")[1]
        title = item[4]
           
        date = datetime.datetime.strptime(strdate, "%Y%m%d").date()
            
        
        #return
        image     = item[10].split('/')[3]
        windimage = item[16].split('/')[3]
        windtype  = item[18]

        day   = day_item.split('<strong>')[1].split('</strong>')[0]
        night = day_item.split('<strong>')[2].split('</strong>')[0]
        wind  = day_item.split('<strong>')[3].split('</strong>')[0]



        day = day.replace('&deg;', '')
        night = night.replace('&deg;', '')

        logging.info("%s: %s  %s",strdate, float(day), float(night))

        new_weather = models.Weather.gql("WHERE date = :1", date).get()
            
        if not new_weather:
            new_weather = models.Weather()
    
        new_weather.overcast  = overcast
        new_weather.date      = date
        new_weather.title     = title
        new_weather.image     = image
        new_weather.day       = float(day)
        new_weather.night     = float(night)
        new_weather.wind      = float(wind)
        new_weather.windimage = windimage
        new_weather.windtype  = windtype

        new_weather.put()
            
        





























