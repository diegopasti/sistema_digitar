var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('MeuController', ['$scope', function($scope) {

	$scope.screen_height = null;  // screen.availHeight; - PEGA O TAMANHO DA TELA DO DISPOSITIVO
	$scope.screen_width  = null;  // PEGA O TAMANHO DA JANELA DO BROWSER

	$scope.sortType           = 'codigo'; // set the default sort type
	$scope.sortReverse        = false;    // set the default sort order
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","provento", "descricao"];
	$scope.search             = '';
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10];
	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.esta_adicionando     	= true;
	$scope.contratos = [];

	$scope.save_provent = function() {
		var data_paramters = create_data_paramters('form_adicionar_contrato');
		data_paramters['valor'] = data_paramters['valor'].replace(".","").replace(",",".");

		success_function = function(result,message,object,status){
			$scope.contratos.splice(0, 0, object);
			$scope.$apply();
			check_response_message_form('#form_adicionar_contrato', message);
			$("#modal_adicionar_contrato").modal('hide');
			reset_formulary('form_adicionar_contrato');
		}

		fail_function = function (result,message,data_object,status) {
			check_response_message_form('#form_adicionar_contrato', message);
		}

		validate_function = function () {
		 return check_required_fields('form_adicionar_contrato');//validate_form_regiter_person(); //validate_date($scope.birth_date_foundation);
		}
		//var base_controller = new BaseController();
		//base_controller.request("/api/provents/save",data_paramters,validate_function,success_function,fail_function);
		request_api("/api/provents/save",data_paramters,validate_function,success_function,fail_function);
	}

	$scope.update_provent = function() {
		var data_paramters = create_data_paramters('form_adicionar_contrato');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);
		data_paramters['valor'] = data_paramters['valor'].replace(".","").replace(",",".");

		success_function = function(result,message,object,status){
      if(result == true){
				$scope.contratos[$scope.contratos.findIndex(x => x.id==$scope.registro_selecionado.id)] = object;
				$scope.$apply();
				$scope.registro_selecionado = null;
				$scope.esta_adicionando = true;
				$scope.$apply();
				check_response_message_form('#form_adicionar_contrato', message);
				$("#modal_adicionar_contrato").modal('hide');
				reset_formulary('form_adicionar_contrato');
      }
		}

    fail_function = function (result,message,data_object,status) {
      check_response_message_form('#form_adicionar_contrato', message);
    }

    validade_function = function () {
     return  true;
    }
    request_api("/api/provents/update",data_paramters,validade_function,success_function,fail_function);
	}

	$scope.load_provents = function () {
    $.ajax({
      type: 'GET',
      url: "/api/provents",

      success: function (data) {
				data = data.replace("<html><head></head><body>{","{")
				data = data.replace("}</body></html>","}")
				$scope.contratos = JSON.parse(data).object;

        $("#loading_tbody").fadeOut();
        $scope.$apply();
        $scope.contratos_carregados = true;
        $scope.reajustar_tela();
        $scope.$apply();
      },

      failure: function (data) {
      	$scope.contratos = [];
        $scope.loaded_entities = true;
        alert("Não foi possivel carregar a lista");
      },
    })
	}

	$scope.disable = function(){
		var data_paramters = create_data_paramters('form_justify_action');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);

		success_function = function(result,message,object,status){
			var index = $scope.contratos.indexOf($scope.registro_selecionado);
  		$scope.contratos.splice(index, 1);
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
		request_api("/api/provents/disable",data_paramters,validate_function,success_function,fail_function);
		validate_justify
	}

	$scope.confirm_disable = function(){
		var object_name = $scope.registro_selecionado.nome;
		$('#action_type').val('Desativar')
		$('#action_object').val(object_name)
		$('#action_user').val('Operador')
	}

	$scope.open_object = function(){
		reset_formulary('form_adicionar_contrato');
		for (var key in $scope.registro_selecionado) {
			try{
				$("#"+key).val($scope.registro_selecionado[key]);
			}
			catch (err){
			}
		}
		$("#valor").maskMoney('mask', $scope.registro_selecionado.valor);
	}

	$scope.reajustar_tela = function (){
		$scope.screen_height = SCREEN_PARAMTERS['screen_height'];
		$scope.screen_width  = SCREEN_PARAMTERS['screen_width'];
		$scope.screen_model  = SCREEN_PARAMTERS['screen_model'];

		$scope.table_maximun_items_per_page = SCREEN_PARAMTERS['table_maximun_items_per_page'];
		$scope.table_minimun_items          = SCREEN_PARAMTERS['table_minimun_items'];
		$scope.table_maximun_body_heigth    = SCREEN_PARAMTERS['table_maximun_body_heigth'];
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