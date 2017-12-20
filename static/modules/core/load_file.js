function load_file(file_path, file_type){
		if (file_type=='js'){
			var scriptElement = document.createElement('script');
			scriptElement.type = 'text/javascript';
			scriptElement.src = file_path;
			document.head.appendChild(scriptElement);
			return true;
		}
		else if(file_type=='css'){
		  var styleElement = document.createElement('link');
			styleElement.rel = 'stylesheet';
			styleElement.href = file_path;
			document.head.appendChild(styleElement);
		}
		else{
		}
	}

//load_file("{% static 'bower_components/bootstrap/dist/js/bootstrap.min.js' %}","js");
//load_file("{% static 'custom/adminlte/js/app.min.js' %}","js");
//load_file("{% static 'bower_components/pnotify/dist/pnotify.js' %}","js");
//load_file("{% static 'modules/core/working/working.min.js' %}","js");
//load_file("{% static 'modules/core/base.min.css' %}","css");
//load_file("{% static 'bower_components/pnotify/dist/pnotify.css' %}","css");