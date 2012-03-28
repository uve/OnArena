$(function () {


var cache = new CacheProvider;

var Group = Backbone.Model.extend({
    //subalbum: function() { return 'c' + gallery._currentsub; }

});


var GroupCollection = Backbone.Collection.extend({
    model: Group,
    url: function(){
        return "/api/?name=group_browse_league_id_"+this.league_id;
    },      
    comparator: function(item) {
        return item.get('id');
    }
});


var GroupView = Backbone.View.extend({
    el: "#group-browse",
    indexTemplate: $("#template-group-browse").template(),

    render: function() {
              
        removeFallbacks();
        var sg = this;                    
        
        $(sg.el).fadeOut(0, function() {
            $(sg.el).empty();        
            
            var values = sg.model.toJSON();
            
            $.each(values, function(index, value) { 
               value.index = index + 1 ;
            });  
            
            
            $.tmpl(sg.indexTemplate, values).appendTo($(sg.el));                          
            
            var $tabs1 = $( "#tabs1" ).tabs();
            $tabs1.tabs('select', 0); 
            
            var $tabs2 = $( "#tabs2" ).tabs();
            $tabs2.tabs('select', 0); 
            
            var $tabs3 = $( "#tabs3" ).tabs();
            $tabs3.tabs('select', 0); 
            
            $(sg.el).fadeIn(0);            
        });
        
        return this;
    }

});



var Match = Backbone.Model.extend({
    //subalbum: function() { return 'c' + gallery._currentsub; }

});


var MatchCollection = Backbone.Collection.extend({
    model: Match,
    url: function(){
        return "/api/?name=match_browse_league_id_"+this.league_id;
    }      
});


var MatchView = Backbone.View.extend({
    el: "#match-browse",
    indexTemplate: $("#template-match-browse").template(),

    render: function() {  
                
        removeFallbacks();
        var sg = this;                    

        $(sg.el).empty();        
        $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
   
        return this;
    }

});

var MatchListCollection = Backbone.Collection.extend({
    model: Match,
    url: function(){
        return "/api/?name=match_browse_tournament_id_"+this.tournament_id;
    }      
});

var MatchListView = Backbone.View.extend({
    el: "#list-match",
    indexTemplate: $("#template-list-match").template(),

    render: function() {
              
        removeFallbacks();
        var sg = this;                    

        $(sg.el).empty();        
        $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
        
        return this;
    }

});


var Team = Backbone.Model.extend({
    url: function(){
        return "/api/?name=team_get_team_id_"+this.get('item_id');
    },  

});


var TeamItemView = Backbone.View.extend({
    el: "#main-content",
    indexTemplate: $("#template-team-item").template(),

    render: function() {
              
        removeFallbacks();
        var sg = this;                            
        
       $(sg.el).empty();        
       $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
        
       $("#main-content").css({ opacity: 1 });
  
        return this;
    }

});



var League = Backbone.Model.extend({
    url: function(){
        return "/api/?name=league_get_league_id_"+this.get('item_id');
    },  

});


var LeagueCollection = Backbone.Collection.extend({
    model: League,
    url: function(){
        return "/api/?name=league_browse_tournament_id_"+this.tournament_id;
    },        
    comparator: function(item) {
        return item.get('id');
    }
});


var LeagueView = Backbone.View.extend({
    el: "#list-league",
    indexTemplate: $("#template-list-league").template(),

    render: function() {
              
        removeFallbacks();
        var sg = this;                    

        
        $(sg.el).fadeOut(0, function() {
            $(sg.el).empty();        
            $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
            $(sg.el).fadeIn(0);
        });
   
        return this;
    }

});



var LeagueItemView = Backbone.View.extend({
    el: "#main-content",
    indexTemplate: $("#template-league-item").template(),

    render: function() {
              
        removeFallbacks();
        var sg = this;                    

        
            $(sg.el).empty();        
            $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
                                   
            
           sg._group_browse = new GroupCollection();
           sg._group_browse.league_id = sg.model.id;
           sg._group_browse.fetch( {  success: function() {                    
           
                           sg._group_view = new GroupView({model: sg._group_browse}); 
                           sg._group_view.render();                            
                           }}); 
                                                                                             

           sg._match_browse = new MatchCollection();
           sg._match_browse.league_id = sg.model.id;
           sg._match_browse.fetch( {  success: function() {                    
           
                           sg._match_view = new MatchView({model: sg._match_browse}); 
                           sg._match_view.render();                            
                           }});      
                           
           $("#main-content").css({ opacity: 1 });
               
   
        return this;
    }

});




/**
 * IndexView: The default view seen when opening up the application for the first time. This 
 * contains the first level of images in the JSON store (the level-one albums). Prior to rendering 
 * our jQuery templates here we remove any messages or elements displayed in the version where 
 * JavaScript is disabled.
 * @type Backbone.View
 */
var IndexView = Backbone.View.extend({
    el: $('#tournament-browse'),
    indexTemplate: $("#template-tournament-browse").template(),

    render: function() {
        removeFallbacks();
        var sg = this;
        
        this.el.fadeOut(0, function() {
        sg.el.empty();        
        $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo(sg.el);        
        sg.el.fadeIn(0);
        });
        
        return this;
    }

});


var Referee = Backbone.Model.extend({
    url: function(){
        return "/api/?name=referee_get_referee_id_"+this.get('item_id');
    },   

});

var RefereeCollection = Backbone.Collection.extend({
    model: Referee,    
    url: function(){
        return "/api/?name=referees_browse_tournament_id_"+this.tournament_id;
    }, 
    comparator: function(item) {
        return item.get('id');
    }

});

var RefereeBrowseView = Backbone.View.extend({
    el: "#main-content",
    indexTemplate: $("#template-referee-browse").template(),
    
    
    render: function() {
              
        removeFallbacks();
        var sg = this;    
        
        $(sg.el).empty();        
        $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
        
        $("#main-content").css({ opacity: 1 });  
          
        return this;
    }

});

var News = Backbone.Model.extend({
    url: function(){
        return "/api/?name=news_get_news_id_"+this.get('item_id');
    },   

});



var NewsItemView = Backbone.View.extend({
    el: "#main-content",
    indexTemplate: $("#template-news-item").template(),

    render: function() {
              
        removeFallbacks();
        var sg = this;                    
        
        $(sg.el).empty();                   
        $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
        $(sg.el).fadeIn(0);
        
        $("#main-content").css({ opacity: 1 });
   
        return this;
    }

});

var NewsView = Backbone.View.extend({
    el: "#list-news",
    indexTemplate: $("#template-news-browse").template(),
    
    
    render: function() {
              
        removeFallbacks();
        var sg = this;    
        
        $(sg.el).fadeOut(0, function() {
            $(sg.el).empty();        
            $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo($(sg.el));        
            $(sg.el).fadeIn(0);
        });
        
     
   
        return this;
    }

});


var NewsCollection = Backbone.Collection.extend({
    model: News,    
    url: function(){
        return "/api/?name=news_browse_tournament_id_"+this.tournament_id;
    }, 
    comparator: function(item) {
        return item.get('id');
    }

});



var Tournament = Backbone.Model.extend({   
    url: function(){
        return "/api/?name=tournament_get_tournament_id_"+this.get('tournament_id');
    },    
    
});



var TournamentCollection = Backbone.Collection.extend({
    model: Tournament,
    url: "/api/?name=tournament_browse_limit_1000",        
    comparator: function(item) {
        return item.get('id');
    }
});

/**
 * SubalbumView: The view reached when clicking on a level-one album or browsing to a subalbum bookmark. 
 * This contains the images found in the 'subalbum' section of an album entry. Clicking on any of the 
 * images shown in a subalbum takes you to the PhotoView of that specific image
 * @type Backbone.View
 */
var TournamentView = Backbone.View.extend({
    el: $('#container'),    
    indexTemplate: $("#template-tournament-container").template(),

    initialize: function(options){
        var ws = this;
       
      
    },
    
    render: function() {
        var sg = this;
        removeFallbacks();

        sg.el.empty();            
        $.tmpl(sg.indexTemplate, sg.model.toJSON()).appendTo(sg.el);                                   
               


       sg._league_browse = new LeagueCollection();
       sg._league_browse.tournament_id = sg.model.id;
       sg._league_browse.fetch( {  success: function() {                    
       
                       sg._league_view = new LeagueView({model: sg._league_browse}); 
                       sg._league_view.render();                             
                       }});
        
        
       sg._news_browse = new NewsCollection();
       sg._news_browse.tournament_id = sg.model.id;
       sg._news_browse.fetch( {  success: function() {                    
       
                       sg._news_view = new NewsView({model: sg._news_browse}); 
                       sg._news_view.render();                            
                       }});
                      
                       
       sg._match_list = new MatchListCollection();
       sg._match_list.tournament_id = sg.model.id;
       sg._match_list.fetch( {  success: function() {                    
       
                       sg._match_list = new MatchListView({model: sg._match_list}); 
                       sg._match_list.render();                            
                       }});                           

            
        

       return this;
    }

});

/**
 * Gallery: The controller that defines our main application 'gallery'. Here we handle how 
 * routes should be interpreted, the basic initialization of the application with data through 
 * an $.ajax call to fetch our JSON store and the creation of collections and views based on the 
 * models defined previously.
 * @type Backbone.Controller
 */
var Gallery = Backbone.Router.extend({
    _index: null,
    _tournaments: null,    
    _tournament: null,
    _photos: null,
    _album :null,
	_subalbums:null,
	_subphotos:null,
	_data:null,
	_photosview:null,
	_currentsub:null,


    routes: {
        "": "index",
        "!/tournament/:id/": "tournament",

        "!/league/:id/": "league",        
        "!/team/:id/": "team",                
        "!/news/:id/": "news",        
                
        "!/tournament/:id/referees/": "referee_browse",                
                
        "subalbum/:id": "hashsub",
        "subalbum/:id/" : "directphoto",                
        "subalbum/:id/:num" : "hashphoto"
        
    },

    initialize: function(options) {
                               
                            
                            

    },


    /**
	 * Handle rendering the initial view for the application
	 * @type function
	*/
	
    index: function() {

        var sg = this;
        
        sg._tournament_browse = new TournamentCollection();
        sg._tournament_browse.fetch( {  success: function() {   
   
                           sg._index = new IndexView({model: sg._tournament_browse}); 
                           sg._index.render();   
                           
                           }});  
      
    },
	
	
	tournament:function(id){
		
	   var properindex = id.replace('c','');		   
       var sg = this;
         	    
       sg._tournament = new Tournament({tournament_id: properindex});	    
       sg._tournament.fetch( {  success: function() {   
   
                          sg._tournament_view = new TournamentView({model: sg._tournament}); 
                           sg._tournament_view.render();   
                           
                           }});                           

	},	
	
	league:function(id){
		
	   var properindex = id.replace('c','');		   
       var sg = this;
         	    
         	       
         	    
       sg._league = new League({item_id: properindex});	    
       sg._league.fetch( { 
                           beforeSend: function( xhr ) {
                                                              
                            $("#main-content").css({ opacity: 0.2 });
                            var $loader = $( "<div class='ui-loader'><span class='ui-icon-loading'></span><h1>Loading...</h1></div>" ); 

					$loader.appendTo( "#container");
					
					
                            $("#container").addClass( "ui-loading" );
                           },
                          
                           success: function() {   
   
                           sg._league_view = new LeagueItemView({model: sg._league}); 
                           sg._league_view.render();   
                           
                           $( ".ui-loader").remove();
                           
                           
                            $("#container").removeClass( "ui-loading" );

                           }});     
	    
       
http://www.last.fm/music/ATB
	},	
	
	team:function(id){
		
	   var properindex = id.replace('c','');		   
       var sg = this;
         	    
       sg._team = new Team({item_id: properindex});	    
       sg._team.fetch( { beforeSend: function( xhr ) {
                            $("#main-content").css({ opacity: 0.5 });
                          },
   
                         success: function() {   
   
                           sg._team_view = new TeamItemView({model: sg._team}); 
                           sg._team_view.render();   
 
                           }});     
	    
       

	},		
		
	
	news:function(id){
		
	   var properindex = id.replace('c','');		   
       var sg = this;
         	    
       sg._news = new News({item_id: properindex});	    
       sg._news.fetch( {  success: function() {   
   
                           sg._news_view = new NewsItemView({model: sg._news}); 
                           sg._news_view.render();   
                           
                           }});  
	   
       	      	
	},		
	
	referee_browse: function(id) {
  	    var properindex = id.replace('c','');
        var sg = this;
        
        sg._referee_browse = new RefereeCollection();
        sg._referee_browse.tournament_id = properindex;        
        sg._referee_browse.fetch( {  success: function() {   
   
                           sg._referee_browse_view = new RefereeBrowseView({model: sg._referee_browse}); 
                           sg._referee_browse_view.render();   
                           
                           }});  
      
    },

	/**
	 * Gallery -> hashsub: Handle URL routing for subalbums. As subalbums aren't traversed 
	 * in the default initialization of the app, here we create a new PhotoCollection for a 
	 * particular subalbum based on indices passed through the UI. We then create a new SubalbumView 
	 * instance, render the subalbums and set the current subphotos array to contain our subalbum Photo 
	 * items. All of this is cached using the CacheProvider we defined earlier
	 * @type function
	 * @param {String} id An ID specific to a particular subalbum based on CIDs
	 */
	 
	hashsub:function(id){
		
	   var properindex = id.replace('c','');	
	   this._currentsub = properindex;
	   this._subphotos = cache.get('pc' + properindex) || cache.set('pc' + properindex, new PhotoCollection(this._data[properindex].subalbum));
	   this._subalbums = cache.get('sv' + properindex) || cache.set('sv' + properindex, new SubalbumView({model: this._subphotos}));
	   this._subalbums.render();

		
	},
	
	directphoto: function(id){

	},

	/**
	 * Gallery -> hashphoto: Handle routing for access to specific images within subalbums. This method 
	 * checks to see if an existing subphotos object exists (ie. if we've already visited the 
	 * subalbum before). If it doesn't, we generate a new PhotoCollection and finally create 
	 * a new PhotoView to display the image that was being queried for. As per hashsub, variable/data 
	 * caching is employed here too
	 * @type function
	 * @param {String} num An ID specific to a particular image being accessed
	 * @param {Integer} id An ID specific to a particular subalbum being accessed
	 */
	  hashphoto: function(num, id){
	    this._currentsub = num;
	    
	    num = num.replace('c','');
	    
		if(this._subphotos == undefined){
		   this._subphotos = cache.get('pc' + num) || cache.set('pc' + num, new PhotoCollection(this._data[num].subalbum));
		 }	
	    this._subphotos.at(id)._view = new PhotoView({model: this._subphotos.at(id)});
	    this._subphotos.at(id)._view.render();
	    
	  }
});


function removeFallbacks(){
  var query = $('.jstest,.gallery');
        if(query.length){
          query.remove();
        }
}


gallery = new Gallery();
Backbone.history.start();



  }); 

