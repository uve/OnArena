define([
  'jquery',
 
  'underscore',
  'backbone',
  'vm',
  'models/team',
  'text!templates/team/edit.html'
], function($, _, Backbone, Vm, Team, teamPageTemplate, teamEditTemplate){
	

  var TeamPage = Backbone.View.extend({
    el: '.page',
 
    
    render: function () {

      var sg = this;               
      sg.item = new Team({ id: this.id });	 
      
      
      var compiledTemplate = _.template( teamEditTemplate, sg.item.toJSON() );
      sg.$el.html( compiledTemplate );	
        
      /*console.log(sg.$el);*/
      
      require(["jquery", "jqueryui"], function($) {
   	    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
   	    $(function() {
   	    	$("#task_form_tpl").dialog({
       			autoOpen: true,
       			height: 460,
       			width: 350,
       			title:"Tasks",
       			modal: true
       		})
   	    });
   	});
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
		initialize : function(){
			_.bindAll(this,"render")
		/*	this.template = _.template($("#task_form_tpl").html());
			this.render().el;
			*/
		},		
		edit: function () {
			
		
             var sg = this;         
			
             /*
     	 	var compiledTemplate = _.template( teamEditTemplate, sg.item.toJSON() );
            sg.$el.html( compiledTemplate );	             
            */

             /*
         	require(["jqueryui"], function(someModule) {
         	    //...
         	 });
         	 
         	 */
             
           var compiledTemplate = _.template( teamEditTemplate, sg.item.toJSON() );
           sg.$el.html( compiledTemplate );	
             
           /*console.log(sg.$el);*/
           
           require(["jquery", "jqueryui"], function($) {
        	    //the jquery.alpha.js and jquery.beta.js plugins have been loaded.
        	    $(function() {
        	    	$("#task_form_tpl").dialog({
            			autoOpen: true,
            			height: 460,
            			width: 350,
            			title:"Tasks",
            			modal: true
            		})
        	    });
        	});
        
    	
       
         	
    		/*this.el = $(".dialogForm");
    		this.delegateEvents(this.events)
    		return this;
    		*/
    		
            
			  /*
 
 		  	 sg.item.attributes['name'] = 'Затулинка';
		
			  
		      		      
			  var res = sg.item.save({att1 : "value"},
					  				 {
				  						success: function(model, response) {
				  							console.log('saved');
				  						},
				  						error: function(model, response) {
				  							console.log('error save team');
				  						}
					  				 });
			  
			  */
		      
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
