#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement


#import fix_path

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
import sys, inspect

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
#from google.appengine.ext import deferred

import os
import pickle
import types

#from common.decorator import check_cache


from django.core.context_processors import csrf


from google.appengine.api import runtime



from google.appengine.datastore import datastore_query


from google.appengine.api.logservice import logservice
#######
#######
#######
HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"

DATETIME_FORMAT = DATE_FORMAT + " " + TIME_FORMAT

US_FORMAT = "%m/%d/%Y" + " " + TIME_FORMAT

import dateutil.parser

import hashlib
import aetycoon

import zlib
COMPRESSION_LEVEL = 1

MAX_LIMIT = 10000


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
        
        content = results.content
        
        if hasattr(results, 'compressed') and results.compressed:
            logging.info("is_compressed: %s", True)            
            content = zlib.decompress(results.compressed).decode('utf-8')        

        results = json.loads(content, object_hook=decode_datetime)       

        return results
    else:
        return None

def cache_set(key_name, value, include = [], commit = False):
    
    try:
        
        
        logging.info("Start encoding: %s", key_name)
        
        logging.info("memory usage: %s",runtime.memory_usage().current())
           
        #value = jsonloader.encode(input = value, include = include)
                  
        
        e1 = jsonloader.encode(input = value, include = include)
        
        etag = hashlib.sha1(e1).hexdigest()
        logging.info("etag: %s", etag)
        #logging.info("e1: %s", e1)
        e2 = e1.encode('utf-8')
        #logging.info("e2: %s", e2)
        e3 = zlib.compress( e2, COMPRESSION_LEVEL)
        #logging.info("e3: %s", e3)
        
        value = e3                           
        #value = zlib.compress( jsonloader.encode(input = value, include = include).encode('utf-8'), COMPRESSION_LEVEL)
                
        logging.info("Content len: %s", len(value))
                     
            
        content = models.StaticContent( key_name = key_name, name = key_name, 
                            compressed = value, content_type = 'application/json', etag = etag)
                            
        content.put()       
        
        logging.info("Cache saved")             

        last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
                  
        logging.info("memory usage: %s",runtime.memory_usage().current())               
        
        if commit:
            #del value
            return True
        
        logging.info("json.loads: %s", key_name)
                
    
        return cache_get(key_name)
     
    except Exception as e:
        logging.warning("Warning Cache Set!!  Json encode: %s", key_name)
        logging.warning("Exception: %s", e)   
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
            #memcache.delete(key = key_name)
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


    # Не выводить общую таблицу    
    if not league_id in ["1236", "1251"]:
        all_teams = group_reload(league_id = league_id, group_id = None)        
        group = {"group": None, "all_teams": all_teams}        
        results.append(group)   


    include = ["id", "name", "group", "team", "match_played", "won", "drew",
               "loss", "scored", "conceded", "diff", "points", "all_teams", 
               "matches", "place"]
    
    
        
    return cache_set(key_name, results, include, commit = True)
    
    #return cache_set(key_name , results)   
    
    
    
def group_reload(league_id = None, group_id = None, limit = 5000):

    scoretype = models.ScoreType.get_item("1001").key()       

    scored_key   = models.ScoreType.get_item("1001").key()
    conceded_key = models.ScoreType.get_item("1002").key()

    won_key  = models.ResultType.get_item("1002").key()
    loss_key = models.ResultType.get_item("1003").key()
    drew_key = models.ResultType.get_item("1004").key()    

    league = models.League.get_item(league_id)    
    
    tournament_id = league.tournament_id.id
    
    
    logging.info("League_id: %s",league_id)
    logging.info("Group_id: %s",group_id)    
    
    all_leagues = [league.key()]
    
    
    # Удалить!!
    #if league_id in ["1220", "1221"]:
    #    all_leagues.append( models.League.get_item("1198").key() )
    #    all_leagues.append( models.League.get_item("1199").key() )
    
    if league_id in ["1302", "1302", "1304"]:
        all_leagues.append( models.League.get_item("1286").key() )
        all_leagues.append( models.League.get_item("1287").key() )
        
    
    
    group = None
    group_key = None
    if group_id:
        group = models.Group.get_item(group_id)
        group_key = group.key()
        
           
        
    if len(all_leagues) <= 1:  
    
        all_scores = models.Score.gql("WHERE league_id IN :1 and scoretype_id = :2 and group_id = NULL ORDER BY created", 
                                            all_leagues, scoretype).fetch(limit)   
         
        if group_id:

            all_seasons = models.Season.gql("WHERE league_id IN :1 and group_id = :2", all_leagues, group_key).fetch(limit)
            all_scores_group = models.Score.gql("WHERE league_id IN :1 and scoretype_id = :2 and group_id = :3 ORDER BY created", 
                                        all_leagues, scoretype, group_key).fetch(limit)               
                                            
            all_scores.extend(all_scores_group)                                 
        else:
            all_seasons = models.Season.gql("WHERE league_id IN :1", all_leagues).fetch(limit)
                 
    
    else:

        logging.info("all_seasons_pre. starting...")
        
        all_seasons = models.Season.gql("WHERE league_id = :1", all_leagues[0]).fetch(limit)
        all_teams = []
        
        for item in all_seasons:
            all_teams.append(item.team_id.key())         
        
        
        logging.info("len all_teams: %s", len(all_teams) )
        
        all_scores = models.Score.gql("WHERE league_id IN :1 and team_id IN :2 and scoretype_id = :3 ORDER BY created", 
                                            all_leagues, all_teams, scoretype).fetch(limit)   
        
        
        logging.info("len all_scores: %s", len(all_scores) )


                     
 
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
    results = sorted(results, key=lambda student: student.rating, reverse=False)      

    for i, v in enumerate(results):           
        v.place = i + 1
        
 
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
                    
                    all_mas = [ v[0] for v in c[c1.team_id.id][c2.team_id.id] ]
                    
                    #logging.info( all_mas )
                    
                    if c1.match_id.id in all_mas:
                        continue
                    
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
    total_list = {}

    league_key = league.key()
        
    for team in results: 
        team.key   = team.key()
        
        team.won  = team_data[team.id]["won"]
        team.loss = team_data[team.id]["loss"]
        team.drew = team_data[team.id]["drew"]
        
        team.match_played = team.won + team.loss + team.drew
        team.points = (team.won * 3) + team.drew           
        
        team.scored   = team_data[team.id]["scored"]
        team.conceded = team_data[team.id]["conceded"]
        team.diff = team.scored - team.conceded
        
        team.equal_score = 0
        
            
    results = sorted(results, key=lambda student: student.scored, reverse=True) 
    results = sorted(results, key=lambda student: student.points, reverse=True)   


    logging.info("Step 2")

    for i, team in enumerate(results, 1): 

        team.place = i
        # For recurse
        if not team.points in total_list:
            total_list[team.points] = []
       
        total_list[team.points].append(team)  
         
    for points, teams in total_list.items():
        
        points = points #To don't show errors
        i = len(teams)


        while i > 0: 
            
            logging.info("Differ: %s", teams[i-1].name) 
            for j in xrange(i - 1):
                
                replace = False    
                
                t1 = teams[j]
                t2 = teams[j+1]
                
                #logging.info("Points: %s \t Compare ... team %s: %s \t team %s: %s", points, t1.place, t1.name, t2.place, t2.name) 
    
                if t1.key == t2.key:
                    continue
    
                if t1.points == t2.points:
                    team_score1 = 0
                    team_score2 = 0
                    
                    team_score1 = 0
                    team_score2 = 0
                    
                    
                    try:
                        for matches in c[t1.id][t2.id]:
                            team_score1 += matches[2]    
                            team_score2 += matches[3]                         
                    except:
                        pass                                    
                    
                    '''
                    try:
                        for matches in c[t2.id][t1.id]:
                            team_score1 += matches[3]    
                            team_score2 += matches[2]                          
                    except:
                        pass                   
                    '''
    
                    teams[j].equal_score   += team_score1 - team_score2
                    teams[j+1].equal_score += team_score2 - team_score1
                    
                    
                    team_score1 = teams[j].equal_score
                    team_score2 = teams[j+1].equal_score
                    
                        
                    if (team_score1 < team_score2 and t1.place < t2.place) or (team_score1 > team_score2 and t1.place > t2.place):
                        replace = True                 
    
                    if team_score1 == team_score2:
                        if (t1.diff < t2.diff and t1.place < t2.place) or (t1.diff > t2.diff and t1.place > t2.place): 
                            replace = True
                            
                        elif (t1.diff == t2.diff):    
                            if (t1.won < t2.won and t1.place < t2.place) or (t1.won > t2.won and t1.place > t2.place):            
                                replace = True
    
                                   
                    '''
                    if tournament_id == "1001" and not league_id in ["1263", "1257", "1258", "1260", "1261"]:
                        replace = False

                        if (t1.diff < t2.diff and t1.place < t2.place) or (t1.diff > t2.diff and t1.place > t2.place): 
                            replace = True
    
                        elif (t1.diff == t2.diff):
                            if (t1.scored < t2.scored and t1.place < t2.place) or (t1.scored > t2.scored and t1.place > t2.place):            
                                replace = True

       
                        elif (t1.won < t2.won and t1.place < t2.place) or (t1.won > t2.won and t1.place > t2.place):            
                            replace = True
                    '''
                    
                    logging.info("team %s: %s (%s - %s), \t team %s: %s (%s - %s)\t, is_replace: %s", t1.place, t1.name, team_score1, t1.diff, t2.place, t2.name, team_score2, t2.diff, replace)
    
                                        
                    # Change team places in the table
                    if replace:                                         
                        teams[j].place, teams[j+1].place = teams[j+1].place, teams[j].place
                        
                        t = teams[j]
                        teams[j] = teams[j+1]
                        teams[j+1] = t
    
            i -= 1  #Iterate i
            
            for item in teams:
                for v in results:
                    if item.key == v.key:
                        v = item
            
            
                
    results = sorted(results, key=lambda student: student.place, reverse=False)              
            
    cross_table = []
    
    # Filling Cross Table 
    
    for item in results:
        item_table = {}
        item_table["team"] = item
        item_table["matches"] = []
        
        for item2 in results:        
            try:                    
                #all_mas = list(set(c[item.id][item2.id]))
                
                #logging.info(all_mas )
                
                #if not c[item.id][item2.id][0] in all_mas:
                item_table["matches"].append( c[item.id][item2.id] )
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
        
        rem = models.Season.gql("WHERE group_id = :1", item).fetch(limit)  
        db.delete(rem)
        
        #rem = models.GroupCompetitor.gql("WHERE group_id = :1", item).fetch(limit)  
        #db.delete(rem)
        #rem = models.GroupNode.gql("WHERE group_id = :1", item).fetch(limit)  
        #db.delete(rem)

        db.delete(item)

    #models.Group.update(group_id)
    


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
        
    results = models.League.gql("WHERE tournament_id = :1 and active = :2 ORDER BY id ASC", tournament, True).fetch(limit)
            
    new_res = []
    
    include = ["id", "name", "ranking", "tournament_id", "sport_id"]    
    

    logging.info("settings.DEBUG: %s",settings.DEBUG)
    
    if settings.DEBUG == True:
        return cache_set(key_name, results, include)               
        
    if tournament_id == "1002":       
        for item in results:
            if int(item.id) >= int("1146"):
                new_res.append(item)    
                
        return cache_set(key_name, new_res, include)   

    if tournament_id == "1007":       
        for item in results:
            if int(item.id) >= int("1162"):
                new_res.append(item)  
                
        return cache_set(key_name, new_res, include)   
        
    if tournament_id == "1001":       
        for item in results:
            if int(item.id) > int("1248"):
                new_res.append(item)    
                
        return cache_set(key_name, new_res, include)           
    
    if tournament_id in ["1003"]:       
        
        #res2 = ["1244", "1239", "1241", "1242", "1243", "1251"]
        #new_res = [models.League.get_item(item) for item in res2]
        
        
        for item in results:
            if int(item.id) >= int("1271"):# and not item.id in res2:
                new_res.append(item)        
        

        
        return cache_set(key_name, new_res, include)     
                
    if tournament_id in ["1008"]:     
        #res2 = ["1191", "1192", "1170", "1139", "1138", "1137"]
        
        #new_res = [models.League.get_item(item) for item in res2]

        for item in results:
            if int(item.id) >= int("1245") and not int(item.id) in [1291, 1292, 1293]:
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
    new_ref = models.League.create(params)


    league_browse(tournament_id = tournament_ref.id, is_reload = True)


    return new_ref.id

  
def league_get(league_id):
  

    league_ref = models.League.get_item(league_id)

    #if league_id == "1002":
    #    models.League.update(league_id)
    #    logging.info("Updated league 1002")

    return league_ref



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





def league_update(league_id = None, limit = 1000):
 
    league = models.League.get_item(league_id)
    tournament = league.tournament_id   
    tournament_id = tournament.id       
    
    logging.info("League_update League_id: %s  \t  Tournament_id: %s", league_id, tournament_id)
    
    deferred.defer(group_browse, league_id = league_id, is_reload = True)
    
    deferred.defer(match_browse, tournament_id = tournament_id, is_reload = True) 
    deferred.defer(match_browse, league_id = league_id, is_reload = True)
    deferred.defer(match_browse, tournament_id = tournament_id, league_id = league_id, is_reload = True)  

    deferred.defer(team_browse,  league_id = league_id, is_reload = True)     

    deferred.defer(playoff_browse, league_id = league_id, is_reload = True)
    
    deferred.defer(stat_league, league_id = league_id, is_reload = True)

    deferred.defer(statistics, league_id = league_id, is_reload = True)
    deferred.defer(statistics, league_id = league_id, limit = 1000, is_reload = True)



    deferred.defer(rating_player_update, tournament_id = tournament_id)
    deferred.defer(rating_team_update, tournament_id = tournament_id)
    
        
    deferred.defer(referees_browse, tournament_id = tournament_id, stat = True, is_reload = True)    
    
    return True


def league_update_task(league_id = None):

    #deferred.defer(league_update, league_id = league_id)
    league_update(league_id = league_id)
    
    return True
    #return taskqueue.add(url='/league/update/', method = 'POST', params=dict(league_id = league_id))
    
    
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





def league_hide(league_id = None, limit=100):
    
    league = models.League.get_item(league_id)

    league.active = False
    db.put(league)
                

    tournament_id = league.tournament_id.id
    logging.info("League hide Value: %s", league_id)    
                
    league_browse(tournament_id = tournament_id, is_reload = True)

    return True


    
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
    
    # Удалить!!!!!!!!!!!!!!!!
    #if not group:
    #    logging.error("No group found: %s", group_id)
    #    return False  
    
    
    
    if not league:
        logging.error("No league found: %s", league_id)
        return False
        
    if not team:
        logging.error("No team found: %s", team_id)
        return False  
    
    season = models.Season.gql("WHERE league_id = :1 and team_id = :2 and group_id = :3", league, team, group).get()
        

    #return True        
        
    if league.tournament_id.id != team.tournament_id.id:
        logging.error("League tournament != team tournament")
        return False                
        
    if not season:
        logging.error("No season found")
        return False        
        
 
    '''  
    all_matches = models.Match.gql("WHERE league_id = :1 and team_id = :2 and season_id = :3", league, team, season).fetch(limit)


    #Removinf all season team matches!!
    for match in all_matches:        
        remove_by_model(match, "match_id")
    
        
        
    #Removinf all season team!!
    remove_by_model(season, "season_id")
    '''

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


def match_create_complete(post = None, limit = 5000):

    

    league_id  = post["league_id"]
    playoffnode_id = post["playoffnode_id"]    
    group_id = post["group_id"]       

    team1_id = post["team1"]
    team2_id = post["team2"]
   
    match_date = post["datepicker"]
    match_time = post["timepicker"]
    
    
    referee_id = post["referee"]

    place = post["place"]
    
    match_date = match_date.replace("-",".")    
    
    match_time = match_time.replace(".",":")
    match_time = match_time.replace("-",":")    
    match_time = match_time.replace(",",":")    
    
    full_datetime  = str(match_date) + " " + str(match_time)
    
    if str(match_time) == "":       
        logging.error("No Match time: %s", full_datetime)
        return False
    
        
    #################################  old
    

    try:
        match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
    except: 
        match_datetime = datetime.datetime.strptime(full_datetime, US_FORMAT)
    
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
    group        = None
    
    if playoffnode_id:
        playoffnode  = models.PlayoffNode.get_item(playoffnode_id)
        playoff      = playoffnode.playoff_id
        playoffstage = playoffnode.playoffstage_id      
        
    if group_id:        
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
        deferred.defer(team_get_players, team_id = team_id, stat = True, is_reload = True)
        deferred.defer(team_get_players_active, team_id = team_id, is_reload = True)          
        
    return True



def match_create(request):

    deferred.defer(match_create_complete, post = request.POST)  
    return True


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
    
    if str(match_time) == "":       
        logging.error("No Match time: %s", full_datetime)
        return False
    
    
    #match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
    
    deferred.defer(match_create_complete, league_id = league_id, team1_id = team1_id, team2_id = team2_id, full_datetime = full_datetime,
                                     referee_id = referee_id, place = place, playoffnode_id = playoffnode_id, group_id = group_id)  
    
    return True


def match_edit(post_data, limit=5000):
        
   
       
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

    if not match:
        return None

    league = match.league_id    
    league_id = league.id
       
    tournament = match.tournament_id
    tournament_id = tournament.id    

    match_ref = match
   
    match_date     = all_events["datepicker"][0]
    match_time     = all_events["timepicker"][0] 
    
    full_datetime  = str(match_date) + " " + str(match_time)
    #match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)

    try:
        match_datetime = datetime.datetime.strptime(full_datetime, DATETIME_FORMAT)
    except: 
        match_datetime = datetime.datetime.strptime(full_datetime, US_FORMAT)    

    match_ref.place = all_events["place"][0]
        
    match_ref.datetime = match_datetime
    match_ref.put()
    match_ref.update(match_ref.id)
    
    match = match_ref
       
           

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

    all_results = []    

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
       
   
    all_results.append(db.put_async(update_teams))    
    
     
    all_results.append(db.delete_async(old_competitors))    
    
    # Remove all data    
    
    old_scores = db.GqlQuery("SELECT __key__ FROM Score WHERE match_id = :1", match_ref.key()).fetch(limit)
    all_results.append(db.delete_async(old_scores))         
    
    old_events = db.GqlQuery("SELECT __key__ FROM Event WHERE match_id = :1", match_ref.key()).fetch(limit)
    all_results.append(db.delete_async(old_events))  
    
    old_referees = db.GqlQuery("SELECT __key__ FROM RefereeMatch WHERE match_id = :1", match_ref.key()).fetch(limit)
    all_results.append(db.delete_async(old_referees))      

    old_sanctions = db.GqlQuery("SELECT __key__ FROM Sanction WHERE match_id = :1", match_ref.key()).fetch(limit)                
    all_results.append(db.delete_async(old_sanctions))      
        
    old_playermatches = db.GqlQuery("SELECT __key__ FROM PlayerMatch WHERE match_id = :1", match_ref.key()).fetch(limit)        
    all_results.append(db.delete_async(old_playermatches))      
    
    
    

    update_players = []    
    for item in old_playermatches:
        try:
            #logging.info("Player: %s \t Last ranking: %s \t New Ranking: %s", item.player_id.name,
            #                         item.player_id.ranking, item.player_id.ranking - item.ranking)    
                                     
            item.player_id.ranking -= item.ranking           
            update_players.append(item.player_id)    
            #models.Player.update(item.player_id.id)              
        except:
            #logging.warning("No Player Ranking")
            pass
                  
            

    all_results.append(db.put_async(update_players))    
    
     
    all_results.append(db.delete_async(old_playermatches))         
      
    
        
    
    
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


            all_results.append(db.put_async(refereematch_ref))    
    
    
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
                  
                  'playoff_id':       match_ref.playoff_id,         
                  'playoffstage_id':  match_ref.playoffstage_id,                         
                  'playoffnode_id':   match_ref.playoffnode_id,  
                  
                  'group_id':         match_ref.group_id,                  
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
                          
                          'group_id':         match_ref.group_id,                             
                        }
        
                score_ref = models.Score(**params)
                #new_scores.append(score_ref)
                #score_ref
                all_results.append(db.put_async(score_ref))                                
                
        else:
            
                params = {'match_id': match_ref.key(),
                          'team_id' : team_ref.key(),
                          'league_id': match_ref.league_id,
                          'season_id': match_ref.season_id,                          
                          'tournament_id': match_ref.tournament_id,
                          'competitor_id': competitor_ref.key(),
                          'scoretype_id': models.ScoreType.get_item("1001"),  # empty scored

                          'group_id':         match_ref.group_id,                             
                        }
        
                score_ref = models.Score(**params)
                #new_scores.append(score_ref)         
                all_results.append(db.put_async(score_ref))
       
    #all_results.append(db.put_async(new_scores))   

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
                
                all_results.append(db.put_async(playermatch_ref))   
                all_results.append(db.put_async(player))   
            
            except:
                logging.error("Error Save Match %s \t is_played %s", match_ref.id, value)
                pass 

        
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
                
                all_results.append(db.put_async(sanction_ref))                                   
            
            except:
                logging.error("Error Save Match %s \t Sanction: %s", match_ref.id, value)
                pass            


    

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
                    all_results.append(db.put_async(event_ref))     
                    
                except:
                    logging.error("Error Save Match %s \t Event: %s", match_ref.id, value)
                    pass             
         
  
    for item in all_results:
        try:
            res = item.get_result()                     
            logging.info("Edit async: %s:" % res)
        except:
            logging.error("Match_edit async put")        
            pass                                      
  
    
    logging.info("Start League Update")

    deferred.defer(match_get, match_id = match_id, is_reload = True)

    #league_update_task(league_id = league_id)

    for team_ref in team_refs:   
        stat_update(league_id = league_id, team_id = team_ref.id)

    league_update(league_id = league_id)


    for team_ref in team_refs:   
        team_id = team_ref.id
       
        #stat_update(league_id = league_id, team_id = team_ref.id)
        #deferred.defer(stat_update, league_id = league_id, team_id = team_id)
        deferred.defer(match_browse, team_id = team_id, is_reload = True) 
        
        deferred.defer(team_get, team_id = team_id, is_reload = True)  
        deferred.defer(team_get_players, team_id = team_id, stat = True, is_reload = True)
        deferred.defer(team_get_players_active, team_id = team_id, is_reload = True)        
    
    
        

    logging.info("League Update Complete.")
    
    
    for player_id in players:        
        deferred.defer(player_get, player_id = player_id, is_reload = True)
        deferred.defer(player_stat_get, player_id = player_id, is_reload = True)
                     
            
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
                
            logging.info("Team scored: %s", team.scored)
                
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
                    
        
        #remove_by_model(match, "match_id")
        
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
    results = models.News.gql("WHERE tournament_id = :1 ORDER BY created DESC", tournament).fetch(limit, offset)
    logging.info("Last News From DataBase.")

    include = ["id", "name", "datetime", "created", "user_id"]    
    
    return cache_set(key_name, results, include, commit = True)   


def news_create(request, **kw):

    tournament_id = request.POST.get("tournament_id", "")
    
    tournament    = models.Tournament.get_item(tournament_id)
    
    if not tournament:
        logging.error("No tournament_id: %s", tournament_id)
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


def news_edit(news_id = None, name = None, content = None):

    news = models.News.get_item(news_id)
    
    tournament    = news.tournament_id
    tournament_id = tournament.id
    
    if name == "" or content == "":
        logging.error("Name and Content are empty")        
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

    return cache_set(key_name, results)


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

            value.competitors = []
            
            value.competitors = models.PlayoffCompetitor.gql("WHERE playoffnode_id = :1 ORDER BY created ASC", value).fetch(limit)
            
            
            '''
            value.competitors = []
            
            for competitor in competitors:
                
                logging.info(competitor.id)
                logging.info(competitor.key())
                
                value.competitors.append(competitor.team_id)
            '''

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
                    
                    for competitor in value.competitors:
                        if not competitor.team_id:                                                
                            competitor.team_id = new_team
                            break
    
    
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

    logging.info("playoff_get_nodeteams id: %s", playoffnode_id)
    
    playoffnode = models.PlayoffNode.get_item(playoffnode_id)
    
    if not playoffnode:
        return False
        
    competitors = models.PlayoffCompetitor.gql("WHERE playoffnode_id = :1 ORDER BY created ASC", playoffnode).fetch(limit)
    
    results = []
    
    logging.info("len(competitors) id: %s", len(competitors))
    
    for item in competitors:        
        #try:
            logging.info("Playoff competitior id: %s", item.team_id.id)
            results.append(item.team_id.id)
        #except:
        #    pass
               
    return results

    
def playoff_set(league_id = None, team_id = None, competitor_id = None, limit = 1000):    
        
    logging.info("team_id: %s",team_id)
    logging.info("competitor_id: %s",competitor_id)

    competitor = models.PlayoffCompetitor.get_item(competitor_id)
    team =  models.Team.get_item(team_id)    
    
    competitor.team_id = team
    competitor.put()
    
    
    deferred.defer(playoff_browse, league_id = league_id, is_reload = True)    
    

################
@check_cache
def player_browse(tournament_id = None, limit=500,
                 is_reload=None, memcache_delete=None, key_name=""):


    taskqueue.add(url='/api/v1/tournament/%s/player/' % tournament_id, #params={'tournament_id': '1001'}
                      target='goworker', method="PUT")
    return []

    name = "offset_player_browse_" + tournament_id
    
    
    
    if not tournament_id:
        return None
               
    logging.info("memory usage: %s",runtime.memory_usage().current())

    tournament = models.Tournament.get_item(tournament_id)
    
    
    limit = 10000
    batch_limit = 500
    
    new_players = {}
    new_playerteams = {}
    new_teams = {}
      
         
    
    logging.info("iterate all_playerteams")
    
    query =  models.PlayerTeam.all().filter("tournament_id", tournament)
    
    count = query.count(limit)
    
    for i in xrange(0, count, batch_limit):
        
        for item in query.run(config=datastore_query.QueryOptions(deadline=60, offset=i, limit=batch_limit)):
            
            value = str(item.player_id.key())     
            if not value in new_teams:
                new_playerteams[value] = []
            new_playerteams[value].append(str(item.team_id.key()))
    
    
    
    logging.info("iterate all_players")
    
    query = models.Player.all().filter("tournament_id", tournament).order("full_name")
    count = query.count(limit)
    
    for i in xrange(0, count, batch_limit):
        for item in query.run(config=datastore_query.QueryOptions(deadline=60, offset=i, limit=batch_limit)):
            
            new_players[str(item.key())] = { "id": item.id, "full_name" : item.full_name }


    logging.info("iterate all_teams")
    
    for item in models.Team.all().filter("tournament_id", tournament).run(config=datastore_query.QueryOptions(limit=limit)):
                
        new_teams[str(item.key())] = { "id": item.id, "name" : item.name }
    
    
    logging.info("Updating results")    
    
    results = []
    
    for k,v in new_players.iteritems():
        
        v["teams"] = []
        if str(k) in new_playerteams:
            for value in new_playerteams[str(k)]:
                v["teams"].append( new_teams[value] )
   
        results.append(v)
    
    
    logging.info("all_players len: %s", len(results))
    
    
    include = ["id", "name", "full_name", "teams"]
    results = cache_set(key_name, results, include, commit = False)
    
    return results

        
                 

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
    is_teamplayed = None
    
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



    if is_teamplayed:
        logging.error("Alreddy played. Player: %s \t Team: %s", player.id, team.id )        
    else:
        teamplayer = models.PlayerTeam(**params)
        teamplayer.put()
    
    
    
    team_get_players_active(team_id = team_id, is_reload = True)
        
    
    deferred.defer( team_get_players, team_id = team_id, stat = True, is_reload = True)         
    deferred.defer( team_get_players, team_id = team_id, is_reload = True) 
             
    
    deferred.defer( player_browse, tournament_id = tournament_id, is_reload = True)

       
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
    team = models.Team.get_item(team_id)

    if number and team:
        logging.info("Number: %s", number)
        logging.info("Player_id: %s", player.id)
        logging.info("Team_id: %s", team.id)        
        playerteam = models.PlayerTeam.gql("WHERE team_id = :1 AND player_id = :2", team, player).get()
            
        
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
    

    deferred.defer( player_browse, tournament_id = tournament_id, is_reload = True)  
       
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


def rating_player_update(tournament_id = None, limit = 5000):

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
    
    

    deferred.defer( player_browse, tournament_id = tournament_id, is_reload = True)
          
    
    return True

def rating_team_update(tournament_id = None, limit = 5000):

    tournament = models.Tournament.get_item(tournament_id) 
        
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
    
    
    deferred.defer(team_browse, tournament_id = tournament_id, is_reload = True)  
    deferred.defer(team_browse_rating, tournament_id = tournament_id, is_reload = True)

    return True


@check_cache
def referees_browse(tournament_id = None, stat = None, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):
    if tournament_id == None:
        return None

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
       
    all_keys = []           
    
    tournament_id = None    
   
    if hasattr(request, "tournament"):
        
        try:   
            locals["tournament"] = request.tournament
            tournament_id = request.tournament_id
                               
        except:
            pass            

    for item, value in defers.items():          
        all_keys.append(value["key_name"])            
        
        
    cached_values = {}
        
    if tournament_id:
        cached_values.update({'match_browse_tournament_id_':  tournament_id})
        cached_values.update({'league_browse_tournament_id_': tournament_id})
        cached_values.update({'news_browse_tournament_id_':   tournament_id})            
        
        cached_values.update({'player_browse_tournament_id_':   tournament_id})     
                
        if request.is_owner:
            cached_values.update({'team_browse_tournament_id_':   tournament_id})  
        
                    

    if "team_id" in locals:
        cached_values.update({ 'match_browse_team_id_':    locals["team_id"] })
        
    if "league_id" in locals:
        cached_values.update({ 'match_browse_league_id_':   locals["league_id"] })        
        cached_values.update({ 'group_browse_league_id_':   locals["league_id"] })   
        cached_values.update({ 'playoff_browse_league_id_': locals["league_id"] })                   
            
    if "referee_id" in locals:
        cached_values.update({ 'match_browse_referee_id_': locals["referee_id"] })            

    '''
    memcached_values = memcache.get_multi([(k+v) for k, v in cached_values.iteritems()])
        
    for k, v in cached_values.iteritems():
        try:
            setattr(request, k, memcached_values[k+v])
        except:
            pass            
    '''

  
    logging.info("caching complete")
    
            
    all_static = models.StaticContent.get_by_key_name(all_keys)
    #logging.info("keys: %s",all_static)    
    
    i = -1    
    for item, value in defers.items():        
        i += 1    

        logging.info("item: %s \t static: %s", item, value["key_name"])         
        if all_static[i] is None:
            #logging.info("None: %s", value["key_name"])
            try:
                func, args, kwds = pickle.loads(value["pickled"])    
    
            except Exception, err:
                logging.warning("ERROR: %s", str(err))
            else:
                locals[item] = func(*args, **kwds)
        
        else:
            #locals[item] = json.loads(all_static[i].content, object_hook=decode_datetime)
            locals[item] = cache_get(value["key_name"])      

    start = time.time()   
    
        
    c = template.RequestContext(request, locals)
    #c.update(csrf(request))
    t = loader.get_template(template_path)            
    result = http.HttpResponse(t.render(c))
    
    stop = round(time.time() - start, 6)       
    logging.info("HttpResponse \t time: %s", stop)         

        
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
    
    team_key = models.Team.get_item(team_id).key()
    
    tournament_key = league_ref.tournament_id.key()
    
    
    season_key = None
    try:
        season_key = league_ref.league_seasons[0].key()
    except:
        pass        
    
    league_key = league_ref.key()
    
    goal        = models.EventType.get_item("1001").key()    
    
    all_stat = []    
        
    all_players = models.PlayerTeam.gql("WHERE team_id = :1 AND active = :2", team_key, True).fetch(limit)
    for player in all_players:
       
        player_key = player.player_id.key()
       
        total_goals = models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND league_id = :3 AND team_id = :4", 
                                       player_key, goal, league_key, team_key).count(limit)


        params = {'player_id':  player_key,
                  'eventtype_id':  goal,
                  'score':         total_goals,
              
                  'team_id':       team_key,  
                  'tournament_id': tournament_key,
                  'league_id':     league_key,
                  'season_id':     season_key,
               }
    
    
        stat_player = models.StatPlayer.gql("WHERE league_id = :1 AND eventtype_id = :2 AND player_id = :3 AND team_id = :4",
                                            league_key, goal, player_key, team_key).get()
        if stat_player:
            stat_player.score = total_goals            
        else: 
            stat_player = models.StatPlayer(**params)
        
        all_stat.append(stat_player)
           
    models.db.put(all_stat)  

    return



@check_cache              
def statistics(league_id=None, limit = 10,
                 is_reload=None, memcache_delete=None, key_name=""):
    
        
    #league  = models.League.get_item(league_id).key()
    goal        = models.EventType.get_item("1001").key() 
    yellow_card = models.EventType.get_item("1002").key() 
    red_card    = models.EventType.get_item("1003").key() 

    leagues = [league_id]
    
    league_ref = models.League.get_item(league_id)
    
    #### Few leagues stats ###
    
    if league_id == "1164" or league_id == "1165":
        leagues.extend(["1146", "1147", "1148", "1149"])


    if league_id == "1166":
        leagues.extend(["1143", "1144", "1145", "1150"])
        
    
    all_leagues = [models.League.get_item(item).key() for item in leagues]
    
            
    #all_leagues = models.db.GqlQuery("SELECT __key__ FROM League WHERE id IN :1", leagues).fetch(limit)
    
    all_stat = models.StatPlayer.gql("WHERE league_id IN :1 AND \
                                          eventtype_id = :2 \
                                          ORDER BY score DESC",
                                          all_leagues, goal).fetch(5000)
                
    results = []      

    for item in all_stat:        
        try:
            
            if len(all_leagues) > 1:                
                                          
                total_goals = models.Event.gql("WHERE player_id = :1 AND \
                                                              team_id = :2 AND \
                                                            league_id = :3 AND \
                                                         eventtype_id = :4",
                         item.player_id, item.team_id, league_ref, goal).count()                                          
                
                #logging.info("Player id: %s, goals: %s", item.player_id.id, total_goals)
                
                if total_goals <= 0:
                    continue
                         
            item.yellow_cards = models.Event.gql("WHERE player_id = :1 AND \
                                                          team_id = :2 AND \
                                                        league_id IN :3 AND \
                                                     eventtype_id = :4",
                     item.player_id, item.team_id, all_leagues, yellow_card).count()


            item.red_cards =    models.Event.gql("WHERE player_id = :1 AND \
                                                          team_id = :2 AND \
                                                        league_id IN :3 AND \
                                                     eventtype_id = :4",
                     item.player_id, item.team_id, all_leagues, red_card).count()

            #logging.info("%s: %s", item.player_id.full_name, item.score)
            
            
            if item.score > 0 or item.yellow_cards > 0 or item.red_cards > 0:
                                                                
                if not hasattr(item, 'teams'):
                    item.teams = []
                                                                        
                is_new = True
                
                for value in results:
                    if value.player_id.id == item.player_id.id:
                        is_new = False
                        
                        value.score        += item.score
                        value.yellow_cards += item.yellow_cards
                        value.red_cards    += item.red_cards
                        
                        if not item.team_id.id in [x.id for x in value.teams]:
                            value.teams.append(item.team_id)                            
                            logging.info('Another team detected: %s', item.team_id.id)
                            logging.info('For player: %s', item.player_id.id)
                        else:                            
                            logging.info('Double team detected: %s', item.team_id.name)            
                                                                                        
                if is_new:
                    item.teams.append(item.team_id)
                    results.append(item)
                            
        except Exception, err:
                logging.warning("ERROR: %s", str(err))
        
    results = sorted(results, key=lambda lv: lv.player_id.full_name, reverse=False)    
    results = sorted(results, key=lambda lv: lv.score, reverse=True)
    
    results = results[:limit]

    logging.info("Result lenght: %s", len(results))                
                
    include = ["id", "name", "full_name", "score", "yellow_cards", "red_cards", "team_id", "teams", "player_id"]
        
    return cache_set(key_name, results, include)



 

@check_cache  
def stat_league(league_id, limit = 1000,
                 is_reload=None, memcache_delete=None, key_name=""):


    fill_database()
        
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
    
    
    league_id      = request.POST.get("league_id")
    league_ref     = models.League.get_item(league_id)
    
    group_id      = request.POST.get("group_id")
    group_ref = models.Group.get_item(group_id)
    
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
        
        is_exist = models.Season.gql("WHERE league_id = :1 AND group_id = :2 AND team_id = :3",
                                                    league_ref, group_ref, team_ref).get()    
        if is_exist:
            logging.error("Team '%s' is alredy exists in league: %s, group: %s", 
                                                team_ref.name, league_id, group_id)        
            return False           
    
    else:    
        team_name = request.POST.get("team_name")
        
        if not team_name:
            return None
            
        params = {'name': team_name ,
                  'tournament_id': tournament,
                }
    
        team_ref = models.Team.create(params)
    
    params_season = {'tournament_id': tournament,
                     'league_id':     league_ref.key(),
                     'group_id':      group_ref,
                     'team_id':       team_ref.key(),
            }


    season_ref = models.Season(**params_season)
    season_ref.put()


    deferred.defer(league_update, league_id = league_id)


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
    
        if item:    
            item.group_id = new_group
            all_seasons.append(item)
        else:               
            params_season = {'tournament_id': tournament,
                             'league_id':     league,
                             'team_id':       team,
                             'group_id':      new_group
            }
        
            item = models.Season(**params_season)
            item.put()        
    
    models.db.put(all_seasons)   

    deferred.defer(group_browse, league_id = league_id, is_reload = True)
    
    return True 


def test_create_confirm(league_id = None, group_id = None, group_teams=[]):

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
    




def remove_by_model(removing_item = None, name = 'something_id', limit=5000):
         
    all_mas = []
    
    if not removing_item:
        logging.error("Model for removing was not found")
        return False
        
    removing_key = removing_item.key()
    
    
    for class_name, model in inspect.getmembers(sys.modules["common.models"]):
        if not inspect.isclass(model):
            continue

        if not name in dir(model):
            continue
    
        logging.info("Removing all: %s \t with %s=%s", class_name, name, removing_key)
        
        
        
        res = model.all().filter(name+' = ', removing_key).fetch(limit)
                    
        all_mas.append(db.delete_async(res))
    
        
    all_mas.append(db.delete_async(removing_item))        
            
            
    for item in all_mas:
        item.get_result()
    
        
        

def test(limit = 5000):
    
    league_id = "1329"
    
    #logging.info("Tos rassvet 2224")
    #logging.info("Tos rassvet 2224")
    
        
    logging.info("Tournament browse GITHUB upload working!!!")
    tournament_browse(limit = 1000, is_reload = True)
    
    
    
    return []
    
    
    league_id = "1329"
    
    
    group_remove(group_id = "1062", league_id = league_id)
    group_remove(group_id = "1063", league_id = league_id)
    
    
          
    test_create(league_id = league_id, name=u'Группа А',
                 group_teams=["1953", "1861", "1873", "1370", "1680"])
    
    test_create(league_id = league_id, name=u'Группа Б',
                 group_teams=["1358", "1957", "1673", "2089", "1860"])
       
    
    #tournament_browse(limit = 1000, is_reload = True)
    
    return []
    
    
    logging.info("Tos rassvet 2224")
    
    
    league_id = "1317"

    league = models.League.get_item(league_id)

    res = models.Event.gql("WHERE league_id = :1", league).count(limit)
    logging.info("Event: %d", res)

    res = models.Match.gql("WHERE league_id = :1", league).count(limit)
    logging.info("Match: %d", res)

    res = models.PlayerMatch.gql("WHERE league_id = :1", league).count(limit)
    logging.info("PlayerMatch: %d", res)

    res = models.Score.gql("WHERE league_id = :1", league).count(limit)
    logging.info("Score: %d", res)

    res = models.Sanction.gql("WHERE league_id = :1", league).count(limit)
    logging.info("Sanction: %d", res)
    

        
        
    return []


    p1 = models.Player.get_item("1252")
    p2 = models.Player.get_item("1190")
    
    if not p1 or not p2:
        logging.error("Player not found")
        return []
        
    
    for name, item in inspect.getmembers(sys.modules["common.models"]):
        if not inspect.isclass(item):
            continue

        if not 'player_id' in dir(item):
            continue
    
        logging.info(item)
        
        all_results  = item.gql("WHERE player_id = :1", p1).fetch(limit)
        
        for value in all_results:            
            value.player_id = p2
            
        db.put(all_results)
        
    
    
    #player_browse(tournament_id = "1001", is_reload = True)
    #league_update_task(league_id = "1272")
    
    return []
    
    league_id = "1256"
    league = models.League.get_item(league_id)
    
    team   = models.Team.get_item("1091")
    player = models.Player.get_item("2984")


    goal        = models.EventType.get_item("1001").key()    
    

    total_goals = models.Event.gql("WHERE player_id = :1 AND eventtype_id = :2 AND league_id = :3 AND team_id = :4", 
                                   player, goal, league, team).fetch(limit)

    db.delete(total_goals)
    
   
    
    stat_player = models.StatPlayer.gql("WHERE league_id = :1 AND eventtype_id = :2 AND player_id = :3 AND team_id = :4",
                                            league, goal, player, team).fetch(limit)

    db.delete(stat_player)
    
    
    playermatches = models.PlayerMatch.gql("WHERE player_id = :1 and team = :2", player, team).fetch(limit)
    
    db.delete(playermatches)
    
    
    
    deferred.defer(stat_league, league_id = league_id, is_reload = True)

    deferred.defer(statistics, league_id = league_id, is_reload = True)
    deferred.defer(statistics, league_id = league_id, limit = 1000, is_reload = True)


    #item = models.PlayerTeam.gql("WHERE player_id = :1 AND team_id = :2", player, team).get()
    
    #db.delete(item)
    
    
    #player_browse(tournament_id = "1001", is_reload = True)
    #league_browse(tournament_id = "1003", is_reload = True)
    
    #league_id = "1251"
    #group_browse(league_id = league_id, is_reload = True)

    
    #tournament = models.Tournament.get_item("1003")
    
    
    #league_update(league_id = "1001")
    

    return []
    
    '''
    to_disable = models.Tournament.gql("ORDER BY created ASC").fetch(limit)
    for tournament in to_disable:
                
        tournament.active = True
        
        tournament.put()
        
    to_disable = ["1014", "1005", "1009", "1004", "1007", "1010", "1034", "1031", "1018", "1033", "1006"]    
    '''
    
    to_disable = ["1039"] 
    
    for item in to_disable:
        tournament = models.Tournament.get_item(item)
        
        tournament.active = False
        
        tournament.put()
        
    tournament_browse(limit = 1000, is_reload = True)
    
    
    #league_id = "1251"
    #group_browse(league_id = league_id, is_reload = True)

    
    tournament = models.Tournament.get_item("1003")
    

    return []
    
    
    '''    
    group_remove(group_id = "1045", league_id = "1239")
    group_remove(group_id = "1046", league_id = "1242")
    
    
  
    test_create(league_id = league_id, name=u'Группа А',
                 group_teams=["1177", "1556", "1924", "1786", "1184"])
    
    test_create(league_id = league_id, name=u'Группа Б',
                 group_teams=["1178", "1174", "1374", "1634", "1631"])
    '''
    
    
    group_browse(league_id = league_id, is_reload = True)
    
    
    #league_update(league_id = "1241")
    #league_update(league_id = "1243")
    
    
    end_time = time.time()

    # Count specifies the max number of RequestLogs shown at one time.
    # Use a boolean to initially turn off visiblity of the "Next" link.
    count = 5
    show_next = False
    last_offset = None
    offset = None

    # Iterate through all the RequestLog objects, displaying some fields and
    # iterate through all AppLogs beloging to each RequestLog count times.
    # In each iteration, save the offset to last_offset; the last one when
    # count is reached will be used for the link.
    i = 0
    
    '''
    for req_log in logservice.fetch(end_time=end_time, offset=offset,
                                    minimum_log_level=logservice.LOG_LEVEL_INFO,
                                    include_app_logs=True):

        logging.info(
            'IP: %s \t Method: %s \t  Resource: %s \t Cost: %s' %
            (req_log.ip, req_log.method, req_log.resource, req_log.cost))
    '''
              
    return True
    
    
@check_cache
def team_get(team_id = None,
                 is_reload=None, memcache_delete=None, key_name=""):

    team = models.Team.get_item(team_id)
    if not team:
        return None    
    
    item = models.Image.gql("WHERE team_id = :1 ORDER BY created DESC", team).get()    

    team.photo_small    = settings.GOOGLE_BUCKET + "images/anonymous_team.png"
    team.photo_big      = settings.GOOGLE_BUCKET + "images/anonymous_team.png"
    team.photo_original = settings.GOOGLE_BUCKET + "images/anonymous_team.png"


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
    rv = []
    
    if playerteams: 
        #rv = [x.player_id.key() for x in playerteams]
        
        for item in playerteams:
            try:
                rv.append(item.player_id.key())
            except:
                logging.warning("PlayerTeam not found: %s", item.key())
                pass    
        
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
                 
    results = models.Tournament.gql("where active = :1 ORDER BY created ASC", True).fetch(limit)
    
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
            
        






























