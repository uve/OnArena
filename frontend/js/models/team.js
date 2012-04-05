define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  var teamModel = Backbone.Model.extend({
    defaults: {
        
      },    
    url: function(){
        return this.isNew() ? '/api/team/' : '/api/team/' + this.get('id') + "/";
        //return '/api/team/1004/';
    },        
    
    initialize: function(){
    }

  });
  return teamModel;

});