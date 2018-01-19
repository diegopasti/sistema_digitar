var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('Cadastro_usuario', ['$scope', function($scope) {
	$scope.screen_height = window.innerHeight;
	$scope.screen_width  = window.innerWidth;
	$scope.screen_model = null;

	$scope.sortType           = 'codigo';
	$scope.sortReverse        = false;
	$scope.filter_by          = '0';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ['codigo','nome_completo','email','username'];
	$scope.search             = '';
	$scope.table_minimun_items = [1,2,3,4,5,6,7,8,9,10];
	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.esta_adicionando     	= true;
	$scope.usuarios = [];

	$scope.save_usuario = function() {
		var data_paramters = create_data_paramters('form_adicionar_usuario');
		data_paramters['first_name'] = data_paramters['first_name'].toUpperCase();
		data_paramters['last_name'] = data_paramters['last_name'].toUpperCase();
		data_paramters['email'] = data_paramters['email'].toLowerCase();
		data_paramters['username'] = data_paramters['username'].toLowerCase();

		success_function = function(result,message,object,status){
			notify_success_message(['Novo Usuário adicionado com Sucesso']);
			$scope.usuarios.splice(0,0,{});
			$scope.usuarios[0] = object;
			$scope.usuarios[0]['get_full_name'] = object['first_name']+ ' ' + object['last_name'];
			$scope.usuarios[0]['groups'] =  [object['group_id']];
			$scope.$apply();
			check_response_message_form('#form_adicionar_usuario', message);
			$("#modal_adicionar_usuario").modal('hide');
			reset_formulary('form_adicionar_usuario');
			$scope.$apply();

		}

		fail_function = function (result,message,data_object,status) {
			notify_error(null,'Falha na operação',message);
			check_response_message_form('#form_adicionar_usuario', message);
		}

		validate_function = function () {
		 return check_required_fields('form_adicionar_usuario');
		}
		//var base_controller = new BaseController();
		//base_controller.request("/api/provents/save",data_paramters,validate_function,success_function,fail_function);
		request_api("/api/user/save/register",data_paramters,validate_function,success_function,fail_function);
	}

	$scope.update_usuario = function() {
		var data_paramters = create_data_paramters('form_alterar_usuario');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);
		data_paramters['email'] = data_paramters['email'].toLowerCase()


		success_function = function(result,message,object,status){
      if(result){
				var posicao = $scope.usuarios.findIndex(x => x.id==$scope.registro_selecionado.id)
				notify_success_message(["Usuário atualizado com sucesso"])
				$scope.usuarios[posicao] = object;
				$scope.usuarios[posicao]['get_full_name'] = object['first_name']+ ' ' + object['last_name'];
				$scope.registro_selecionado = null;
				$scope.esta_adicionando = true;
				check_response_message_form('#form_alterar_usuario', message);
				reset_formulary('form_alterar_usuario');
				$("#modal_alterar_usuario").modal('hide');
				$scope.$apply();
      }
		};

    fail_function = function (result,message,data_object,status) {
      notify_response_message(['Atualizações não foram salvas']);
    };

    validade_function = function () {

    	return (email_is_valid('email') && validade_variable_size(data_paramters['username'],6)
					&& validade_variable_size(data_paramters['first_name'],3) && validade_variable_size(data_paramters['last_name'],3))

    };
    request_api("/api/user/update/",data_paramters,validade_function,success_function,fail_function);
	};
 
	$scope.reset_password = function () {
		var data_paramters = create_data_paramters('form_reset_password');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);

		success_function = function(result,message,object,status){
      if(result){
      	$scope.$apply();
				$scope.registro_selecionado = null;
				$scope.esta_adicionando = true;
				check_response_message_form('#form_reset_password', message);
				reset_formulary('form_reset_password');
				$("#modal_reset_password").modal('hide');
				$scope.$apply();
      }
		};

    fail_function = function (result,message,data_object,status) {
      notify_response_message(["Senhas informadas sçao diferentes"])
    };

    validade_function = function () {
      return data_paramters['password'] == data_paramters['confirm_password']
    };
    request_api("/api/user/reset_password/",data_paramters,validade_function,success_function,fail_function);
	}

	$scope.load_users = function (){
    $.ajax({
      type: 'GET',
      url: "/api/user/filter",

      success: function (data) {
      	try
				{
					data = data.replace("<html><head></head><body>{", "{")
					data = data.replace("}</body></html>", "}")
					$scope.usuarios = JSON.parse(data).object;
					$("#loading_tbody").fadeOut();
					$scope.usuarios_carregados = true;
					$scope.tdboy = $("#table_usuarios tbody").height();
					$scope.$apply();
				}
				catch(err)
				{
					if(data.indexOf('ERRO403')!= -1){
						error_notify(null,"Operação não autorizada","Nível de autonomia não permite o acesso à este recurso.");
					}
				}
      },

      failure: function (data) {
        notify_error(["Não foi possivel carregar a lista"]);
      },
    })
	}

	$scope.disable = function(operador){
		var data_paramters = create_data_paramters('form_justify_action');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);
		data_paramters['action_object'] = $('#action_object').val()
		success_function = function(result,message,object,status){
			var posicao = $scope.usuarios.findIndex(x => x.id==$scope.registro_selecionado.id)
			$scope.registro_selecionado = null;
			notify_success_message(["Usuário atualizado com sucesso"])
			$scope.usuarios[posicao]['is_active'] = object['is_active'];
			$scope.usuarios[posicao]['selecionado'] = '';
			$scope.esta_adicionando = true;
			$scope.$apply();
			$("#modal_justify_action").modal('hide');
		};

		fail_function = function (result,message,data_object,status) {
			notify_response_message(['Não foi possivel realizar a operação no momento'])
			check_response_message_form('#form_justify_action', message);
		};

		validate_function = function () {
		 return validate_justify();
		};
		alert("Olha o q eu pego:"+JSON.stringify(data_paramters))
		request_api("/api/user/chage_active/",data_paramters,validate_function,success_function,fail_function);
	};

	$scope.confirm_disable = function(){
		var object_name = $scope.registro_selecionado.first_name + ' ' + $scope.registro_selecionado.last_name;
		$('#action_type').val('Desativar')
		$('#action_object').val(object_name)
		$('#action_user').val('Operador')
	}

	$scope.confirm_active = function(){
		var object_name = $scope.registro_selecionado.first_name + ' ' + $scope.registro_selecionado.last_name;
		$('#action_type').val('Reativar')
		$('#action_object').val(object_name)
		$('#action_user').val('Operador')
	}

	$scope.open_modal_add = function () {
		$('input[name=username] ').prop('readonly', false).val('');
		$('input[name=email] ').val('');
		$('input[name=first_name] ').val('');
		$('input[name=last_name] ').val('');
	};

	$scope.open_object = function(){
		reset_formulary('form_adicionar_usuario')
		reset_formulary('form_alterar_usuario')
		for (var key in $scope.registro_selecionado) {
			try{
				$('input[name='+key+']').val($scope.registro_selecionado[key])
				//$("#"+key).val($scope.registro_selecionado[key]);
			}
			catch (err){
			}
		}
		$('input[name=username] ').prop('readonly', true);
		$('#field_group_update > [name=groups]').val($scope.registro_selecionado.groups[0])
	}

	$scope.reajustar_tela = function (){
		$scope.screen_height = SCREEN_PARAMTERS['screen_height'];
		$scope.screen_width  = SCREEN_PARAMTERS['screen_width'];
		$scope.screen_model  = SCREEN_PARAMTERS['screen_model'];

		$scope.table_maximun_items_per_page = SCREEN_PARAMTERS['table_maximun_items_per_page'];
		$scope.table_minimun_items          = SCREEN_PARAMTERS['table_minimun_items'];

		var extra_height = 0;
		if(SCREEN_PARAMTERS['table_maximun_items_per_page'] <= 5){
			extra_height = SCREEN_PARAMTERS['table_maximun_items_per_page']
		}
		else if(SCREEN_PARAMTERS['table_maximun_items_per_page'] <= 9){
			extra_height = 6;
		}
		else{
			extra_height = 7;
		}

		$scope.table_maximun_body_heigth = SCREEN_PARAMTERS['table_maximun_body_height']+extra_height;
		$scope.$apply();
	}

	$scope.select_filter_by = function (index) {
			$scope.filter_by_index = parseInt($scope.filter_by);
			$scope.apply();
	}

	$scope.get_filter_column = function(){
			var filtrar_pesquisa_por = $scope.filter_by_options[$scope.filter_by_index];
			switch (filtrar_pesquisa_por) {
				case 'username':
							return {username: $scope.search};
				case 'codigo':
						return {id: $scope.search};
				case 'email':
						return {email: $scope.search};
				default:
					return {get_full_name : $scope.search}
			}
	}


	$scope.selecionar_linha = function(registro) {
			if ($scope.registro_selecionado != null){
					if (registro.selecionado=='selected'){
							$scope.desmarcar_linha_selecionada();
							//registro.selecionado = "";
							$scope.registro_selecionado = null;
							$scope.esta_adicionando = true;
					}

					else{
							$scope.desmarcar_linha_selecionada();
							registro.selecionado = "selected";
							$scope.registro_selecionado = registro;
							$scope.opcao_desabilitada = "";

							if(registro.plano == null){
								$scope.esta_adicionando = true;
							}
							else{
								$scope.esta_adicionando = false;
							}
					}
			}

			else{
					registro.selecionado = 'selected';
					$scope.registro_selecionado = registro;
					$scope.opcao_desabilitada = "";

					if($scope.registro_selecionado.plano){
						$scope.esta_adicionando = false;
					}
					else{
						$scope.esta_adicionando = true;
					}
			}
			//$scope.$apply();
	}

	$scope.desmarcar_linha_selecionada = function(){
			$scope.registro_selecionado.selecionado = "";
			$scope.registro_selecionado = null;
			$scope.opcao_desabilitada = "desabilitado";
			//$scope.apply();
	}
}])