app.controller('change_password_controller', function($scope) {

  $scope.save_password = function () {
    var data_paramters = {
      old_password: $('#old_password').val(),
      password:  $('#password').val(),
      confirm_password: $('#confirm_password').val()
    };

    success_function = function(result,message,data_object,status){
    	//alert("Operação realizada com Sucesso!"+"Senha de acesso redefinida.")
      $("#old_password").val("");
      $("#password").val("");
      $("#confirm_password").val("");
      success_notify("Operação Realizada com sucesso","");
      return "/"
    };

    fail_function = function (result,message,data_object) {
    	error_notify(null,message['password'])
			$('#form_change_password').find("input[type=password]").val("");
    };

    validate_function = function(){
     return	validate_form_change_password(data_paramters['old_password'],data_paramters['password'],data_paramters['confirm_password'])
		}
    request_api("/api/user/change_password/",data_paramters,validate_function,success_function,fail_function)
  }

  $scope.save_email = function () {
  	var data_paramters = create_data_paramters('form_change_personal_info');

  	success_function = function(result,message,data_object,status){
  		success_notify("Operação Realizada com sucesso","");
			$scope.$apply();
  	}

  	fail_function = function() {
			error_notify(null,"Falha na operação","Não foi possível salvar alterações.")
  	}

		validate_function = function (){
  		if(email_is_valid('email')==false){
  			error_notify(null,"Falha na operação","Email inválido.")
  			return false;
  		}

  		if(data_paramters['first_name'].length == 0 || data_paramters['last_name'].length == 0){
  			error_notify(null,"Falha na operação","Nome e sobrenome precisam ser informados.");
  			return false;
  		}
  		return true;
  	}

		request_api('/api/user/change_personal_info/',data_paramters,validate_function,success_function,fail_function)
  }
});