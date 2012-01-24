define([
  'underscore',
  'backbone'
], function(_, Backbone) {
  var Team = Backbone.Model.extend({
    
    url: function(){
        //return this.isNew() ? '/api/team/' : '/api/team/' + this.get('id') + "/";
        return '/api/team/' + this.get('item_id') + "/";
    },
    
    
    
    initialize: function(){
    }

  });
  return Team;

});
