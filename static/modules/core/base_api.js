function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function request_api(url,data_paramters,validator_functions,success_function,fail_function){
  var csrftoken = getCookie('csrftoken');//jQuery("[name=csrfmiddlewaretoken]").val();
  data_paramters['csrfmiddlewaretoken'] = csrftoken;
  NProgress.start();
  if (validator_functions()){
    alert("executo o ajax"+JSON.stringify(data_paramters));
    execute_ajax(url,'post',data_paramters,success_function,fail_function);
  }
  else{
      NProgress.done();
      return false;
  }
}

function execute_ajax(url,request_method,data_paramters,success_function,fail_function){
  $.ajax({
    type: request_method,
    url: url,
    data: data_paramters,
    success: function(data) {
    	var response = $.parseJSON(data);
      var message = response['message'];
      var resultado = response['result'];
      if (resultado == true) {
        var data_object = response['object'];
        //var moment_date = moment(data_object['fields']['joined_date']).format("DD/MM/YYYY - HH:mm:ss")
        if (success_function != null) {
          var redirect = success_function(data_object);
        }
      }

      else {
        if(typeof message === 'string' ) {
          notify('error',"Falha na operação",message)
          //alert("VEJA O ERRO: "+message)
        }
        else {
          fail_function(message);
        }
      }
      //register_action(start_request, status)
      NProgress.done();
      if (redirect){
      	window.location = redirect;
      }
      return true;
    },
    failure: function(data){
      NProgress.done();
      return notify('error','Falha na Operação',"Erro na requisição assincrona ao servidor.")
    }
  });
}
