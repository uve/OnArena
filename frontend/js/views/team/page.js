define([
  'jquery',
  //'jsrender',
  'underscore',
  'backbone',
  'vm',
  'models/team',
  'text!templates/team/page.html'
], function($, _, Backbone, Vm, Team, teamPageTemplate){
	

  var TeamPage = Backbone.View.extend({
    el: '.page',
 
    
    render: function () {

      var sg = this;         
      
      sg.item = new Team({ id: this.id });	   
           
      sg.item.fetch( { 
                         beforeSend: function( xhr ) {                        
                           
                           },
   
                         success: function() {

                        	 	var compiledTemplate = _.template( teamPageTemplate, sg.item.toJSON() );
                             
	                             sg.$el.html( compiledTemplate );
	                             
	                             //sg.item.attributes['name'] = 'Затулинка';
	                             
	                             //console.log(sg.item);
	                             	                             	                            	                             	   
	                             
	                             /*
	                             sg.item.destroy({
	                            	 success: function(model, response) {
	                            		 console.log('s2');
	                            	 },
	                            	 error: function(model, response) {
	                            		 
	                            		 console.log('e2');
	                            		 console.log(model);
	                            		 console.log(response);
	                            	 },	                            	 
	                            	 complete: function(model, response) {
	                            		 console.log(model.responseText);
	                            	 }
	                             });
	                             */
	                                                                                           
                           },
                         error: function( request, error) {

                        	 sg.$el.html( 'Error ' + error.status  );                        	 
                        	
                         }
                          
                        });             
      
      //console.log('end');
      //this.$el.html(teamPageTemplate);
    },
		events: {
		  'click .add-view': 'addView',
		  
		  'click #edit': 'edit',
		  'click #remove': 'remove'
		},
		counter: 1,
		addView: function () {
			var RandomView = Backbone.View.extend({})
			var randomView = Vm.create(this, 'RandomView ' + this.counter, RandomView);
			this.counter++;
			return false;
		},
		edit: function () {
			
		
			  var sg = this;         
			  
			  //sg.item.attributes['name'] = 'Затулинка';
		      		      
			  var res = sg.item.save({att1 : "value"},
					  				 {
				  						success: function(model, response) {
				  							console.log('saved');
				  						},
				  						error: function(model, response) {
				  							console.log('error save team');
				  						}
					  				 });
			  
			  
		      
			return true;
		},
		remove: function () {						
			  var sg = this;         		      		      
			  sg.item.destroy();
			  return true;
		}		
  });
  return TeamPage;
});
