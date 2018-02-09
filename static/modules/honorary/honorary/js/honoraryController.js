var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('MeuController', ['$scope','$filter', function($scope,$filter) {
	$scope.screen_height = window.innerHeight;
	$scope.screen_width  = window.innerWidth;
	$scope.screen_model = null;

	$scope.sortType           = 'codigo';
	$scope.sortReverse        = false;
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","cliente", "competence"];
	$scope.search             = '';
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10];
	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.esta_adicionando     	= true;
	$scope.registros = [];
	$scope.provents_options = [];
	$scope.max_honorary_itens = 0;
	$scope.screen_model = null;

	$scope.save_provent = function() {
		var data_paramters = create_data_paramters('form_adicionar_contrato');
		data_paramters['valor'] = data_paramters['valor'].replace(".","").replace(",",".");
		success_function = function(result,message,object,status){
			$scope.registros.splice(0, 0, object);
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
				$scope.registros[$scope.registros.findIndex(x => x.id==$scope.registro_selecionado.id)] = object;
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

	$scope.load_objects = function () {
    $.ajax({
      type: 'GET',
      url: "/api/honorary",

      success: function (data) {
				data = data.replace("<html><head></head><body>{","{")
				data = data.replace("}</body></html>","}")
				$scope.registros = JSON.parse(data).object;
				$scope.$apply();
        $scope.registros_carregados = true;
        $scope.$apply();
      },

      failure: function (data) {
      	$scope.registros = [];
        $scope.loaded_entities = true;
        alert("Não foi possivel carregar a lista");
      },
    })
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

	$scope.load_competences = function(){
		NProgress.start();
		$.ajax({
      type: 'GET',
      url: "/api/honorary/competences",

      success: function (data) {
				data = data.replace("<html><head></head><body>{","{")
				data = data.replace("}</body></html>","}")
				$scope.registros = JSON.parse(data).object;
        $scope.registros_carregados = true;
        $scope.$apply();
        success_notify('Operação realizada com Sucesso','Honorários atualizados com sucesso.')
        //notify('success','Operação realizada com Sucesso','Controle de honorário atualizado com sucesso.')
        NProgress.done();
      },

      failure: function (data) {
      	$scope.registros = [];
        $scope.loaded_entities = true;
        alert("Não foi possivel carregar a lista");
        NProgress.done();
      },
    })
	}

	$scope.close_current_competences = function(){
		NProgress.start();
		$.ajax({
      type: 'GET',
      url: "/api/honorary/competences/current/close",

      success: function (data) {
				data = data.replace("<html><head></head><body>{","{")
				data = data.replace("}</body></html>","}")
        if(JSON.parse(data).result){
        	success_notify('Operação realizada com Sucesso',JSON.parse(data).message)
					NProgress.done();
					$scope.load_objects();
        }
        else{
        	NProgress.done();
        	warning_notify(null,'Atenção',JSON.parse(data).message)
        }
      },

      failure: function (data) {
        error_notify('Falha na Operação',JSON.parse(data).message)
        NProgress.done();
      },
    })
	}

	$scope.select_competence = function(){
		$scope.get_filter_column();
		$scope.$apply();
	}

	$scope.disable = function(){
		var data_paramters = create_data_paramters('form_justify_action');
		data_paramters['id'] = parseInt($scope.registro_selecionado.id);

		success_function = function(result,message,object,status){
			var index = $scope.registros.indexOf($scope.registro_selecionado);
  		$scope.registros.splice(index, 1);
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
		var competence = $("#competence").val();
		var filtrar_pesquisa_por = $scope.filter_by_options[$scope.filter_by_index];
		$('#competence').prop('disabled', false);
		if(competence=='TODOS'){
			switch (filtrar_pesquisa_por) {
				case 'codigo':
					return {id: $scope.search};
				case 'competence':
					$("#competence").val('TODOS');
					$('#competence').prop('disabled', true);
					return {competence: $scope.search};
				default:
					return {entity_name: $scope.search};
			}
		}
		else{
			switch (filtrar_pesquisa_por){
				case 'codigo':
					return {id: $scope.search, competence:competence};
				case 'competence':
					$("#competence").val('TODOS');
					$('#competence').prop('disabled', true);
					return {competence: $scope.search};
				default:
					return {entity_name: $scope.search, competence:competence};
			}
		}
		$scope.$apply();
	}

	$scope.selecionar_linha = function(registro) {
		if ($scope.registro_selecionado != null){
			if (registro.selecionado=='selected'){
				$scope.desmarcar_linha_selecionada();
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
	}

	$scope.carregar_vencimento = function(){
		var month_names = ['01', '02', '03','04', '05', '06', '07','08', '09', '10', '11', '12'];
		if($scope.registro_selecionado != null){

			//if($scope.registro_selecionado.contract__data_vencimento!=null){
			//	$('#data_vencimento').val($scope.registro_selecionado.contract__data_vencimento.toString());
			//}

			if($scope.registro_selecionado.contract__dia_vencimento!=null){

				date = new Date();
				var new_date = month_names[date.getMonth()]+"/"+date.getFullYear();
				if($scope.registro_selecionado.contract__dia_vencimento.length==1){
					$('#data_vencimento').val('0'+$scope.registro_selecionado.contract__dia_vencimento.toString()+"/"+new_date);
				}
			}
			else{
				var currentDate = new Date();
				var day = currentDate.getDate();
				var month =  month_names[currentDate.getMonth()];
				var year = currentDate.getFullYear();

				if(day.toString().length==1){
					day = "0"+day;
				}
				$('#data_vencimento').val(day+"/"+month+"/"+year);
			}
		}
		else{
			error_notify(null,'Falha na Operação','Selecione um honorário para gerar o documento.');
		}
	}

	$scope.generate_honorary = function(){
		var vencimento = $('#data_vencimento').val();
		if($scope.registro_selecionado != null && vencimento!=""){
			vencimento = vencimento.replace("/","").replace("/","")
			window.open('/honorary/'+$scope.registro_selecionado.id+"/"+vencimento);
		}
		else{
			error_notify('data_vencimento','Falha na Operação','Vencimento do honorário precisa ser informado.');
		}
	}

	$scope.get_honorary = function(honorary_id){
		var data_paramters = {};
		data_paramters['id'] = honorary_id;

		validate_function = function () {return true;}

		success_function = function(result,message,object,status){


			var itens = '';
			var index = $scope.registros.indexOf($scope.registro_selecionado);
			var backup_itens = $scope.registro_selecionado.honorary_itens;
  		$scope.registros[index] = object;
  		$scope.registros[index].honorary_itens = backup_itens;
  		$scope.$apply();
  		$scope.registro_selecionado = $scope.registros[index];
  		$scope.$apply();
			//success_notify("Operação realizada com sucesso!",JSON.stringify(object));
		}
		fail_function = function (result,message,data_object,status) {
			for (var key in message) {
				if (message.hasOwnProperty(key)) {
					if(typeof(message[key]) == Array){
						message[key].forEach(function(item, index){
							set_wrong_field(key, item);
						});
					}
					else{
						error_notify(null,'Falha na Operação',message[key]);
					}
					return false;
				}
			}
		}
		request_api("/api/honorary/object",data_paramters,validate_function,success_function,fail_function);
	}

	$scope.get_honorary_item = function(){
		var data_paramters = {};
		data_paramters['id'] = $scope.registro_selecionado.id;

		validate_function = function () {return true;}

		success_function = function(result,message,object,status){
			$scope.max_honorary_itens = 0;
			if($scope.registro_selecionado.contract != null){
				$scope.max_honorary_itens = $scope.max_honorary_itens + 1;
			}

			if($scope.registro_selecionado.temporary_discount > 0){
				$scope.max_honorary_itens = $scope.max_honorary_itens + 1;
			}

			if($scope.registro_selecionado.fidelity_discount > 0){
				$scope.max_honorary_itens = $scope.max_honorary_itens + 1;
			}
			$scope.registro_selecionado.honorary_itens = object;

			$scope.$apply();
		}
		fail_function = function (result,message,data_object,status) {
			for (var key in message) {
				if (message.hasOwnProperty(key)) {
					if(typeof(message[key]) == Array){
						message[key].forEach(function(item, index){
							set_wrong_field(key, item);
						});
					}
					else{
						error_notify(null,'Falha na Operação',message[key]);
					}
					return false;
				}
			}
		}
		request_api("/api/honorary/item",data_paramters,validate_function,success_function,fail_function);

	}

	$scope.save_honorary_item = function(){
		if($scope.registro_selecionado.is_closed==false){
			$scope.max_honorary_itens = 0;
			if($scope.registro_selecionado.contract != null){
				$scope.max_honorary_itens = $scope.max_honorary_itens + 1;
			}

			if($scope.registro_selecionado.temporary_discount > 0){
				$scope.max_honorary_itens = $scope.max_honorary_itens + 1;
			}

			if($scope.registro_selecionado.fidelity_discount > 0){
				$scope.max_honorary_itens = $scope.max_honorary_itens + 1;
			}

			if($scope.registro_selecionado.honorary_itens == null || $scope.registro_selecionado.honorary_itens == ''){
				$scope.registro_selecionado.honorary_itens = [];
			}

			if($scope.registro_selecionado.honorary_itens.length < 10-$scope.max_honorary_itens){
				if($scope.selected_option_provent!=null){
					var data_paramters = {}
					data_paramters['honorary_id'] = parseInt($scope.registro_selecionado.id);
					data_paramters['type_item'] = $('#type_item').val();
					data_paramters['type_value'] = $scope.selected_option_provent.tipo_valor;
					data_paramters['item_id'] = $scope.selected_option_provent.id;
					data_paramters['unit_value'] = $('#unit_value').val().replace(".","").replace(",",".");
					data_paramters['quantity'] =  $('#quantity').val().replace(".","").replace(",",".");
					data_paramters['total_value'] = $('#total_value').val().replace(".","").replace(",",".");
					data_paramters['complement'] = $("#complement").val().toUpperCase();
					//setTimeout(function(){$("#item_id").val($scope.selected_option_provent.id.toString()).trigger('change');},5);

					success_function = function(result,message,object,status){
						if(result){
							if ($scope.registro_selecionado.honorary_itens==''){
								$scope.registro_selecionado.honorary_itens = [];
							}
							$scope.registro_selecionado.honorary_itens.push(object);
							$scope.get_honorary($scope.registro_selecionado.id);
							$("#quantity").val('');
							$("#unit_value").val('');
							$("#total_value").val('');
							$("#complement").val('');
							$scope.selected_option_provent = null;
						}
						else{
							error_notify(null,"Falha na Operação",message);
						}
					}

					fail_function = function (result,message,data_object,status) {
						for (var key in message) {
							if (message.hasOwnProperty(key)) {
								if(typeof(message[key]) == Array){
									message[key].forEach(function(item, index){
										set_wrong_field(key, item);
									});
								}
								else{
									error_notify(null,'Falha na Operação',message[key]);
								}
								return false;
							}
						}
					}

					validate_function = function () {
						var length_text = $scope.selected_option_provent.nome.length + data_paramters['complement'].length + 3;
						if(length_text <= 60){
							return true;
						}
						else{
							error_notify('complement','Falha na Operação','Nome do item e complemento não podem exceder 65 caracteres ('+length_text+' informado).');
							return false;
						}
					}
					request_api("/api/honorary/item/save",data_paramters,validate_function,success_function,fail_function);
				}
				else{
					//set_wrong_field("item", "Campo Obrigatório");
					error_notify(null,'Falha na operação','Item precisa ser informado.')
				}
			}
			else{
				error_notify(null,'Falha na operação','Cada honorário deve conter no máximo dez itens.')
			}
		}
		else{
			error_notify(null,'Falha na operação','Erro! Não é permitido a alteração de honorários encerrados.')
		}
	}

	$scope.update_honorary_item = function(){
		if($scope.selected_item!=null){
			if($scope.registro_selecionado.is_closed==false){
				var data_paramters = {}

				if($scope.edited_item_option){
					setTimeout(function(){$("#item_id").val($scope.edited_item_option.toString()).trigger('change');},5);
					data_paramters['item_id'] = $scope.edited_item_option;
				}
				else{
					setTimeout(function(){$("#item_id").val($scope.selected_item.item.toString()).trigger('change');},5);
					data_paramters['item_id'] = $scope.selected_item.item;
				}
				data_paramters['id'] = parseInt($scope.selected_item.id);
				data_paramters['honorary_id'] = parseInt($scope.registro_selecionado.id);
				data_paramters['type_item'] = $('#type_item').val();

				data_paramters['type_value'] = $scope.selected_item.type_value;
				if($scope.selected_option_provent!=null){
					if($scope.selected_option_provent.tipo_valor != $scope.selected_item.type_value){
						data_paramters['type_value'] = $scope.selected_option_provent.tipo_valor;
					}
				}

				data_paramters['unit_value'] = $('#unit_value').val().replace(".","").replace(",",".");
				data_paramters['quantity'] =  $('#quantity').val().replace(".","").replace(",",".");
				data_paramters['total_value'] = $('#total_value').val().replace(".","").replace(",",".");
				//setTimeout(function(){$("#item_id").val($scope.selected_option_provent.id.toString()).trigger('change');},5);

				success_function = function(result,message,object,status){
					if(result){
						if ($scope.registro_selecionado.honorary_itens==''){
							$scope.registro_selecionado.honorary_itens = [];
						}

						var index = $scope.registro_selecionado.honorary_itens.indexOf($scope.selected_item);
						//var backup_itens = $scope.registro_selecionado.honorary_itens;
						$scope.registro_selecionado.honorary_itens[index] = object;
						$scope.$apply();

						//$scope.registro_selecionado.honorary_itens.push(object);
						$scope.get_honorary($scope.registro_selecionado.id);
						$("#quantity").val('');
						$("#unit_value").val('');
						$("#total_value").val('');
						$scope.selected_option_provent = null;
						$scope.desmarcar_item();
					}
					else{
						for (var key in message) {
						if (message.hasOwnProperty(key)) {
							if(typeof(message[key]) == Array){
								message[key].forEach(function(item, index){
									set_wrong_field(key, item);
								});
							}
							else{
								error_notify(null,'Falha na Operação',message[key]);
							}
							return false;
						}
					}
					}
				}

				fail_function = function (result,message,data_object,status) {
					for (var key in message) {
						if (message.hasOwnProperty(key)) {
							if(typeof(message[key]) == Array){
								message[key].forEach(function(item, index){
									set_wrong_field(key, item);
								});
							}
							else{
								error_notify(null,'Falha na Operação',message[key]);
							}
							return false;
						}
					}
				}

				validate_function = function () {return true;}

				request_api("/api/honorary/item/update",data_paramters,validate_function,success_function,fail_function);
			}
			else{
				error_notify(null,'Falha na Operação','Erro! Não é permitido a alteração de honorários encerrados.');
			}
		}
		else{
			set_wrong_field("item", "Campo Obrigatório");
		}
	}

	$scope.delete_honorary_item = function(){
		if($scope.registro_selecionado.is_closed==false){
			if(confirm("Deseja mesmo excluir o item selecionado desse honorário?")){
				var data_paramters = {'id':$scope.selected_item.id}

				success_function = function(result,message,object,status){
					if(result==true){
						var index = $scope.registro_selecionado.honorary_itens.indexOf($scope.selected_item);
						$scope.registro_selecionado.honorary_itens.splice(index, 1);
						var temp = $scope.registro_selecionado.honorary_itens;
						object.selected = 'selected';

						var index = $scope.registros.indexOf($scope.registro_selecionado);
						$scope.registros[index] = object;
						$scope.$apply();
						$scope.registro_selecionado = $scope.registros[index];
						$scope.registro_selecionado.honorary_itens = temp;
						$scope.$apply();
						$("#quantity").val('');
						$("#unit_value").val("");
						$("#total_value").val("");
					}
					else{
						for (var key in message) {
							if (message.hasOwnProperty(key)) {
								if(typeof(message[key]) == Array){
									message[key].forEach(function(item, index){
										set_wrong_field(key, item);
									});
								}
								else{
									error_notify(null,'Falha na Operação',message[key]);
								}
								return false;
							}
						}
					}
				}

				fail_function = function (result,message,data_object,status) {
					for (var key in message) {
						if (message.hasOwnProperty(key)) {
							if(typeof(message[key]) == Array){
								message[key].forEach(function(item, index){
									set_wrong_field(key, item);
								});
							}
							else{
								error_notify(null,'Falha na Operação',message[key]);
							}
							return false;
						}
					}
				}

				validade_function = function () {return  true;}

				request_api("/api/honorary/item/delete",data_paramters,validate_function,success_function,fail_function);

			}
			else{
				return false;
			}
		}
		else{
			error_notify(null,'Falha na Operação','Erro! Não é permitido a alteração de honorários encerrados.');
			return false;
		}

	}

	$scope.load_provents = function(){
		var data_paramters = {}

		success_function = function(result,message,object,status){
      if(result == true){
				$scope.provents_options = object;
				$scope.$apply();
      }
      else{
      	error_notify(null,'Falha na Operação',message);
      }
		}

    fail_function = function (result,message,data_object,status) {
    	error_notify(null,"Falha na Operação",message);
    }

    validade_function = function () {
     return  true;
    }
    request_api("/api/honorary/provents/options",data_paramters,validade_function,success_function,fail_function);
	}

	$scope.selecionar_item = function(registro){
		if ($scope.selected_item != null){
			if (registro.selected=='selected'){
				$scope.desmarcar_item();
				$scope.selected_item = null;
			}

			else{
				$scope.desmarcar_item();
				registro.selected = "selected";
				$scope.selected_item = registro;
				$scope.load_item_selected();
			}
		}

		else{
			registro.selected = 'selected';
			$scope.selected_item = registro;
			$scope.load_item_selected();
		}
	}

	$scope.desmarcar_item = function(registro){
		$scope.selected_item.selected = "";
		$scope.selected_item = null;
		$("#type_item").val("P");
		$("#item_id").val("").change();
		$("#unit_value").val("");
		$("#quantity").val("");
		$("#total_value").val("");
	}

	$scope.load_item_selected = function(){
		$("#type_item").val($scope.selected_item.type_item);
		setTimeout(function(){$("#item_id").val($scope.selected_item.item.toString()).trigger('change');},10);
		$("#unit_value").val($filter('currency')($scope.selected_item.unit_value,"", 2));
		$("#total_value").val($filter('currency')($scope.selected_item.total_value,"", 2));
		$("#quantity").val($filter('currency')($scope.selected_item.quantity,"", 2));
	}

	$scope.view_provents_per_type = function(provent){
		$scope.selected_type = $("#type_item").val();
		var item_provent_selected = $("#item_id").val();
		$("#item_id").val("");
		if(provent.tipo==$scope.selected_type){
			return true;
		}
		else{
			return false;
		}
	}

	$scope.change_provents_type = function(){
		$scope.selected_type = $("#type_item").val();
		$("#quantity").val('');
		$("#unit_value").val("");
		$("#total_value").val("");
	}

	$scope.select_provent_option = function(option){
		$scope.selected_option_provent = option;
		setTimeout(function(){$("#item_id").val(option.id.toString()).trigger('change');},10);
		if($scope.selected_item!=null){$scope.edited_item_option = option.id;}
		if($scope.selected_option_provent.tipo_valor=='R'){
			$("#lb_unit_value").text("Valor unitário");
			$("#lb_quantity").text("Quantidade");
			$("#quantity").val('1');
			$("#unit_value").val($filter('currency')(option.valor,"", 2));
			$("#total_value").val($filter('currency')(option.valor*1,"", 2));
		}
		else{
			if($scope.registro_selecionado.initial_value_contract != null){
				$("#lb_unit_value").text("Valor Base");
				$("#unit_value").val($filter('currency')($scope.registro_selecionado.initial_value_contract,"", 2));
				$("#lb_quantity").text("Taxa (%)");
				if(option.valor!=''){
					$("#quantity").val($filter('currency')(option.valor,"", 2));
					$("#total_value").val($filter('currency')(option.valor*$scope.registro_selecionado.initial_value_contract,"", 2));
				}
				else{
					$("#quantity").val('');
					$("#unit_value").val('');
					$("#total_value").val('');
				}
			}
			else{
				$("#quantity").val('');
				$("#unit_value").val('');
				$("#total_value").val('');
			}
		}

		return true;
	}

	$scope.calculate_provent_value = function(){
		var quantity = parseFloat($("#quantity").val().replace(".","").replace(",","."));
		var unit_value = parseFloat($("#unit_value").val().replace(".","").replace(",","."));

		if($scope.selected_item==null){
			setTimeout(function(){$("#item_id").val($scope.selected_option_provent.id.toString()).trigger('change');},5);
			if($scope.selected_option_provent.tipo_valor == 'R'){
				var total_value = unit_value*quantity;
			}
			else{
				var total_value = unit_value*(quantity/100);
			}
			$("#total_value").val($filter('currency')(total_value,"", 2));
		}
		else{
			if($scope.edited_item_option){
				setTimeout(function(){$("#item_id").val($scope.edited_item_option.toString()).trigger('change');},10);
			}
			else{
				setTimeout(function(){$("#item_id").val($scope.selected_item.item.toString()).trigger('change');},5);
			}

			var quantity = parseFloat($("#quantity").val().replace(".","").replace(",","."));
			var unit_value = parseFloat($("#unit_value").val().replace(".","").replace(",","."));

			if($scope.selected_option_provent.tipo_valor == 'R'){
				var total_value = unit_value*quantity;
			}
			else{
				var total_value = unit_value*(quantity/100);
			}


			$("#total_value").val($filter('currency')(total_value,"", 2));
		}
	}
}]);