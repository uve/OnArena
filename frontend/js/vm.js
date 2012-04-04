// Use this as a quick template for future modules
define([
  'jquery',
  'underscore',
  'backbone',
  //'events'
], function($, _, Backbone, Events){
	var create = function (context, name, View, id, options) {
		// View clean up isn't actually implemented yet but will simply call .clean, .remove and .unbind
		var view = new View(options);
		
		view.id = id;   // Defined Id
		
		if(typeof context.children === 'undefined'){
		  context.children = {};
		  context.children[name] = view;
		} else {
		  context.children[name] = view;
		}
		//Events.trigger('viewCreated');
		return view;
	}
	
	
  return {
  	create: create
  };
});
