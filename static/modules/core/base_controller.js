function request_api(url,data_paramters,validator_functions,success_function,fail_function){
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  data_paramters['csrfmiddlewaretoken'] = csrftoken;
  NProgress.start();

  if (validator_functions()){
    execute_ajax(url,'post',data_paramters,success_function,fail_function);
  }
  else{
		NProgress.done();
		return false;
  }
}

function execute_ajax(url,request_method,data_paramters,success_function,fail_function){
	var start_request = Date.now();
  $.ajax({
    type: request_method,
    url: url,
    data: data_paramters,
    success: function(data) {
			var response = $.parseJSON(data);
      var message = response['message']
      var result = response['result']
      var data_object = response['object'];//$.parseJSON()
      var status = response['status']

      if (result == true) {
        //var moment_date = moment(data_object['fields']['joined_date']).format("DD/MM/YYYY - HH:mm:ss")
        if (success_function != null) {
        	var redirect = success_function(result,message,data_object,status);
        }
      }

      else {
        if( typeof message === 'string' ) {
          notify('error',"Falha na operação",message)
        }
        else {
        	if(fail_function != null){
        		fail_function(result,message,data_object,status);
        	}
        }
      }

     	register_action(start_request, status)
      NProgress.done();
      if (redirect){
      	window.location = redirect;
      }
      return true;
    },
    failure: function(data){
    	alert('Erro: '+JSON.stringify(data))
    	NProgress.done();
      register_action(start_request,status.request_path, status.request_size, status.server_processing_time_duration, status.cliente_processing_time_duration)
    }
  });
}

function check_response_message_form(form_id, response_message){
  $(form_id +" input, textarea").each(function () {
    var id = $(this).attr("id");
    var erro = response_message[id];
    if (erro){
      set_wrong_field(id, erro);
    }
    else{
      clean_wrong_field(id);
    }
  });
}

function notify_response_message(response_message){
	for (var key in response_message) {
    notify('error',"Falha na operação",response_message[key])
	}
}

function check_required_fields(form_id){
	var form_is_valid = true;
	$.each($('#form_adicionar_contrato').serializeArray(), function(i, field) {
		//alert("VEJA O ELEMENTO: "+i+" - "+field.name+": "+field.value)
		try{
			var required = document.getElementById(field.name).required
			if(required){
				if(field.value){
					clean_wrong_field(field.name)
				}
				else{
					//alert("NAO TEM NADA "+field.value)
					form_is_valid = false;
					set_wrong_field(field.name, 'Campo Obrigatório')
				}
			}
			else{
				//alert("NAO EH OBRIGATORIO")
			}
		}
		catch (err){
			//alert("NAO DEU")
		}
	});
	return form_is_valid
}


function set_wrong_field(id, erro_value){
  $("#field_"+id).addClass('bad')
  var myDivs = $("#field_"+id).children('div.alert');
	if(myDivs.length === 0){
			myDivs = $('<div class="alert"></div>')
					.appendTo("#field_"+id);
					//.css('opacity', 0);
	}
	$("#field_"+id+" .alert").html(erro_value);
	$("#"+id).addClass('wrong_field')
}

function clean_wrong_field(id){
  $("#field_"+id).removeClass('bad')
  $("#field_"+id+" .alert").html("");
  $("#"+id).removeClass('wrong_field')
}

function reset_formulary(formulary_id){
	document.getElementById(formulary_id).reset();
}