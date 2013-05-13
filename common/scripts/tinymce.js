   $('textarea.tinymce').tinymce({
			// Location of TinyMCE script
			script_url : '/js/tinymce/tiny_mce.js',

			// General options
           
			theme : "advanced",			
    		mode: "textareas",
    		language : "en",

			theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,styleselect,formatselect,fontselect,fontsizeselect",
            theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
            theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
     		/*theme_advanced_resizing : true,*/
			theme_advanced_statusbar_location : "bottom"

    }); 
