// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/team/item'
], function($, _, Backbone, TeamItemView ){

    var Router = Backbone.Router.extend({

        routes: {
          "!/tournament/:id/": "tournament",
          "!/team/:id/": "team"
        },        
    
        tournament:function(id){
		
            var properindex = id.replace('c','');		   
            console.log(properindex); 
        },  
    
        team:function(id){
		
            var properindex = id.replace('c','');		   
            console.log("team " + properindex); 
            
            TeamItemView.item_id = properindex;            
            TeamItemView.render();
        }

    });

    return {

        initialize: function() {
            new Router();
            Backbone.history.start();
            
            Backbone.old_sync = Backbone.sync;
            Backbone.sync = function(method, model, options) {
                var new_options =  _.extend({
                    beforeSend: function(xhr) {
                        var token = $('input[name="csrfmiddlewaretoken"]').attr('value');
                        if (token) xhr.setRequestHeader('X-CSRF-Token', token);
                    }
                }, options)
                Backbone.old_sync(method, model, new_options);
            };

        }

    };
});
