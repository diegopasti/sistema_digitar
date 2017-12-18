var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('Cadastro_usuario', ['$scope', function($scope) {
	$scope.screen_height = window.innerHeight;
	$scope.screen_width  = window.innerWidth;
	$scope.screen_model = null;

	$scope.sortType           = 'codigo';
	$scope.sortReverse        = false;
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","provento", "descricao"];
	$scope.search             = '';
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10];
	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.esta_adicionando     	= true;
	$scope.usuarios = [];

	$scope.save_usuario = function() {
		var data_paramters = create_data_paramters('form_adicionar_usuario');
		alert("Olha o data:\n"+JSON.stringify(data_paramters))
		success_function = function(result,message,object,status){
			$scope.usuarios.splice(0, 0, object);
			$scope.$apply();
			check_response_message_form('#form_adicionar_usuario', message);
			$("#modal_adicionar_usuario_adicionar_usuario").modal('hide');
			reset_formulary('form_adicionar_usuario');
		}

		fail_function = function (result,message,data_object,status) {
			check_response_message_form('#form_adicionar_usuario', message);
		}

		validate_function = function () {
		 return check_required_fields('form_adicionar_usuario');
		}
		//var base_controller = new BaseController();
		//base_controller.request("/api/provents/save",data_paramters,validate_function,success_function,fail_function);
		alert("Chegando")
		request_api("/api/user/save/register",data_paramters,validate_function,success_function,fail_function);
	}

	$scope.update_usuario = function() {
		var data_paramters = create_data_paramters('form_alterar_usuario');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);
		data_paramters['email'] = data_paramters['email'].toLowerCase()


		success_function = function(result,message,object,status){
			alert("Cheando e o result é:"+result)
      if(result){
				$scope.usuarios[$scope.usuarios.findIndex(x => x.id==$scope.registro_selecionado.id)] = object;
				$scope.$apply();
				$scope.registro_selecionado = null;
				$scope.esta_adicionando = true;
				check_response_message_form('#form_alterar_usuario', message);
				reset_formulary('form_alterar_usuario');
				$("#modal_alterar_usuario").modal('hide');
				$scope.$apply();
      }
		};

    fail_function = function (result,message,data_object,status) {
    	alert("deu caquita")
      check_response_message_form('#form_alterar_contrato', message);
    };

    validade_function = function () {
     return  true;
    };
    request_api("/api/user/update/",data_paramters,validade_function,success_function,fail_function);
	};
 
	$scope.reset_password = function () {
		var data_paramters = create_data_paramters('form_reset_password');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);

		success_function = function(result,message,object,status){
      if(result){
				$scope.usuarios[$scope.usuarios.findIndex(x => x.id==$scope.registro_selecionado.id)] = object;
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
      alert("Senhas informadas sçao diferentes")
    };

    validade_function = function () {
      return data_paramters['password'] == data_paramters['confirm_password']
    };
    request_api("/api/user/reset_password/",data_paramters,validade_function,success_function,fail_function);
	}
	
	$scope.load_users = function () {
    $.ajax({
      type: 'GET',
      url: "/api/filter",

      success: function (data) {
				data = data.replace("<html><head></head><body>{","{")
				data = data.replace("}</body></html>","}")
				$scope.usuarios = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.contratos_carregados = true;
        $scope.tdboy = $("#table_usuarios tbody").height();
        $scope.$apply();

      },

      failure: function (data) {
        alert("Não foi possivel carregar a lista");
      },
    })
	}

	$scope.disable = function(){
		var data_paramters = create_data_paramters('form_justify_action');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);

		success_function = function(result,message,object,status){
			//var index = $scope.usuarios.indexOf($scope.registro_selecionado);
  		//$scope.usuarios.splice(index, 1);
			//$scope.registro_selecionado.is_active = !($scope.registro_selecionado.is_active)
			$scope.usuarios[$scope.usuarios.findIndex(x => x.id==$scope.registro_selecionado.id)] = object;
			$scope.registro_selecionado = null;
			$scope.esta_adicionando = true;
			$scope.$apply();
			$("#modal_justify_action").modal('hide');
		}

		fail_function = function (result,message,data_object,status) {
			check_response_message_form('#form_justify_action', message);
		}

		validate_function = function () {
		 return validate_justify();
		}
		request_api("/api/user/chage_active/",data_paramters,validate_function,success_function,fail_function);
		validate_justify
	}

	$scope.confirm_disable = function(){
		var object_name = $scope.registro_selecionado.username;
		$('#action_type').val('Desativar')
		$('#action_object').val(object_name)
		$('#action_user').val('Operador')
	}

	$scope.confirm_active = function(){
		var object_name = $scope.registro_selecionado.username;
		$('#action_type').val('Reativar')
		$('#action_object').val(object_name)
		$('#action_user').val('Operador')
	}

	$scope.open_object = function(){
		reset_formulary('form_alterar_usuario');
		for (var key in $scope.registro_selecionado) {
			try{
				$('input[name='+key+']').val($scope.registro_selecionado[key])
				//$("#"+key).val($scope.registro_selecionado[key]);
			}
			catch (err){
			}
		}
		//$("#valor").maskMoney('mask', $scope.registro_selecionado.valor);
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
					case 'codigo':
							//alert("filtrar por codigo");
							return {id: $scope.search};
					default:
						return {nome: $scope.search};
			}
	}

	$scope.selecionar_linha = function(registro) {
			//alert("veja o index: "+registro.cliente_id+"-"+registro.cliente_nome);
			//alert("veja se tem plano: "+registro.plano)

			if ($scope.registro_selecionado != null){
					//alert("tinha uma linha selecionada, entao tem que desmarcar a anterior pra marcar a nova");
					if (registro.selecionado=='selected'){
							//alert("O cara clicou na linha que ja tava selecionada");
							$scope.desmarcar_linha_selecionada();
							//registro.selecionado = "";
							$scope.registro_selecionado = null;
							//$scope.opcao_desabilitada = "desabilitado";
							//alert("desmarquei entao deixa como se fosse adicionar")
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
}]);