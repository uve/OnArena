'''
import pipeline
from common import models




class MatchBrowse(pipeline.Pipeline):
    def run(self, tournament_id, league_id):        
        api.match_browse(league_id = league_id, is_reload = True)        
        api.match_browse(tournament_id = tournament_id, is_reload = True) 
        api.match_browse(tournament_id = tournament_id, league_id = league_id, is_reload = True)         
        

class GroupBrowse(pipeline.Pipeline):
    def run(self, league_id):
        api.group_browse(league_id = league_id, is_reload = True)
        


class PlayoffBrowse(pipeline.Pipeline):
    def run(self, league_id):
        api.playoff_browse(league_id = league_id, is_reload = True)


class Statistics(pipeline.Pipeline):
    def run(self, league_id):
        
        api.statistics(league_id = league_id, is_reload = True)
        api.stat_league(league_id = league_id, is_reload = True)            
        api.statistics(league_id = league_id, limit = 1000, is_reload = True)        
        

class TeamRating(pipeline.Pipeline):
    def run(self, tournament_id):
        
        api.team_browse_rating(tournament_id = tournament_id, is_reload = True)   
        
        
class RefereeBrowse(pipeline.Pipeline):
    def run(self, tournament_id):
        
        api.referees_browse(tournament_id = tournament_id, stat = True, is_reload = True)
                
                
                

class LeagueUpdate(pipeline.Pipeline):
    def run(self, league_id):
        
        league = models.League.get_item(league_id)
        tournament = league.tournament_id   
        tournament_id = tournament.id       
        
        yield GroupBrowse(league_id)
        yield PlayoffBrowse(league_id)
        yield MatchBrowse(tournament_id = tournament_id, league_id = league_id)                
        yield Statistics(league_id)
        
        yield RefereeBrowse(tournament_id)        
'''