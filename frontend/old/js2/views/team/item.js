// Filename: views/team/item
define([
  'jquery',
  //'underscore',
  'backbone',
  //'tmpl',
  'models/team',
  'text!views/team/item.html'
], function($, _, Backbone, Team, TeamItemTemplate){

  var TeamItemView = Backbone.View.extend({
    el: $("#main-content"),
    
    initialize: function(){
    
                                
     
    },
    render: function(){
      //this.el.html("<b>Hello 444</b>");
      console.log("team render"); 
    
      var sg = this;   
      
      
      sg.item = new Team({ item_id: this.item_id });	   
            
      sg.item.fetch( { 
                         beforeSend: function( xhr ) {                        
                           
                           },
   
                         success: function() {                                                           
                            var compiledTemplate = _.template( TeamItemTemplate, sg.item.toJSON() );
                            sg.el.html( compiledTemplate );                            
                           },
                         error: function(errorThrown) {

                             console.log(errorThrown);
                         }
                          
                        });  
      

    }
  });
  return new TeamItemView;
});
