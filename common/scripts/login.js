{% load i18n %}


$("#login-form").dialog({
		autoOpen: false,
		height: 280,
		width: 360,
		modal: true
	});



$('#non-stylized-create-tournament').bind('click', function() {        

    {% if request.user %}
        window.location = "/create/";             
    {% else %}          
        $( "#login-form" ).dialog( "open" );         
    {% endif %}    
});                  

$('#login-button').bind('click', function() {        
  $( "#login-form" ).dialog( "open" );            
});    
         
                 
	
