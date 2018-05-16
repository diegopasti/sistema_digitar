/**
 * Created by diego on 05/05/2017.
 */
var application = angular.module('modules.user', []);

application.controller('register_controller', function($scope) {
	$scope.email = "";
	$scope.password = "";
	$scope.confirm_password = "";

	$scope.save_first_user = function () {
		var data_paramters = create_data_paramters('form_register');
		success_function = function(result,message,object,status){

			notify('success','Operação concluida','Administrador criado com sucesso')
			return "/"
		}

		fail_function = function (result,message,data_object,status) {
			notify('error','Erro! Operação não concluída','Usuario ainda não cadastrado')
		}

		validate_function = function () {
		 return true
		}
		//var base_controller = new BaseController();
		//base_controller.request("/api/provents/save",data_paramters,validate_function,success_function,fail_function);
		request_api("/api/user/save/first/register/",data_paramters,validate_function,success_function,fail_function);
	}

	$scope.save_user = function () {
		$scope.email = "";
		$scope.password = "";
		$scope.confirm_password = "";
		var data_paramters = {};
		$.each($('#form_register').serializeArray(), function(i, field) {
				data_paramters[field.name] = field.value;
				//alert("VEJA: "+field.name+" - "+field.value)
		});

		success_function = function(data_object){
				var redirect = "/"
    	return redirect
			};

		fail_function = function () {
				notify('error','Usuario não cadastrado','Formulário com campos inválidos')
		}
		request_api("/api/user/save/register",data_paramters,validate_form_register,success_function,fail_function)

	};

  $scope.resend_activation_code = function () {
  	var data_paramters = {email: $scope.email}

    var success_function = function success_function(result,message,data_object,status){
			success_notify("Operação realizada com Sucesso!","Verifique seu email, você receberá um email em instantes. <br><a href='/login'>Clique aqui para acessar sistema.</a>")
    };

    var fail_function = function (result,message,data_object,status) {
    	notify_response_message(message);
    };

    validate_function = function(){
    	return true;
		};
		alert("OLHA o meu DP:"+JSON.stringify(data_paramters))
		request_api("/api/user/reactivate",data_paramters,validate_function,success_function,fail_function)
  }
});

application.controller('login_controller', function($scope) {
  $scope.login_autentication = function () {
  	SESSION_PARAMTERS['username'] = $scope.username;
  	SESSION_PARAMTERS['password'] = $scope.password;

    var data_paramters = SESSION_PARAMTERS//{};
		$.each($('#form_login').serializeArray(), function(i, field) {
				data_paramters[field.name] = field.value;
		});
    function success_function(result,message,data_object,status){
    	//alert('success'+'Login realizado'+'Usuário apto para entrar no Sistema')
			notify_success_message(message);
			var url = window.location.href;
			var index = url.indexOf("?next=");
			if(index != -1){
				var redirect = url.slice(index+6)
			}
			else{
				var redirect = "/"
			}
    	return redirect
    }

    fail_function = function (result,message,data_object,status) {
    	//alert("FALHA: "+result+" - "+message+" - "+data_object+" - "+status)
      notify_response_message(['Operação Não concluida']);
    }
    request_api("/api/user/login/autentication",data_paramters,validate_form_login,success_function,fail_function)
  }

  $scope.reset_password = function () {
  	var data_paramters = {email: $("#email").val()}

  	var success_function = function success_function(result,message,data_object,status){
			success_notify("Operação realizada com Sucesso!","Verifique seu email, você receberá um email em instantes.")
			$("#email").val("")
			$('a[href="#login"]').tab('show');
    }

    var fail_function = function (result,message,data_object,status) {
      notify_response_message(['Operação Não concluida']);
    }

    validate_function = function(){
			return email_is_valid("email");
		}
    request_api("/api/user/reset_password/",data_paramters,validate_function,success_function,fail_function)
  }
});