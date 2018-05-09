//var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('MeuController', ['$scope','$filter', function($scope,$filter) {
	$scope.screen_height = window.innerHeight;
	$scope.screen_width  = window.innerWidth;
	$scope.screen_model = null;

	$scope.sortType           = 'entity_name';
	$scope.sortReverse        = false;
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","cliente", "competence"];

	$scope.filter_contract_by = 'todos';
	$scope.filter_conferred = 'T';

	$scope.search             = '';
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10];
	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.esta_adicionando     	= true;
	$scope.registros = [];
	$scope.provents_options = [];
	$scope.opened_competences = [];
	$scope.max_honorary_itens = 0;
	$scope.screen_model = null;

	$scope.item_provent_editing = null;

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
				data = data.replace("<html><head></head><body>{","{");
				data = data.replace("}</body></html>","}");
				//alert("VEJA OS DADOS: "+JSON.stringify(data));
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

	$scope.load_opened_competences = function(){
		NProgress.start();
		$.ajax({
      type: 'GET',
      url: "/api/honorary/competences/open",

      success: function (data) {
				data = data.replace("<html><head></head><body>{","{")
				data = data.replace("}</body></html>","}")
				$scope.opened_competences = JSON.parse(data).object;
        $scope.$apply();
        NProgress.done();
      },

      failure: function (data) {
      	$scope.opened_competences = [];
        alert("Não foi possivel carregar a lista");
        NProgress.done();
      },
    })
	}

	$scope.close_competence = function(item){
		if(confirm('Deseja mesmo encerrar os honorário de '+item.competence+'?')){
			NProgress.start();
			$.ajax({
				type: 'GET',
				url: "/api/honorary/competence/close",
				data: {'competence':item.competence},

				success: function (data) {
					data = data.replace("<html><head></head><body>{","{")
					data = data.replace("}</body></html>","}")
					if(JSON.parse(data).result){
						success_notify('Operação realizada com Sucesso',JSON.parse(data).message);
						$scope.opened_competences.splice(item, 1);
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
	}

	$scope.change_honorary_status = function(registro){
		var data_paramters = {};
		if ($scope.registro_selecionado != null){
			$scope.desmarcar_linha_selecionada();
		}

		registro;
		if(registro.status!='E'){
			data_paramters['honorary_id'] = parseInt(registro.id);
			if(registro.status=='A'){
				if(confirm("Deseja mesmo marcar esse honorário como Conferido?")){
					success_function = function(result,message,object,status){
						//success_notify("DEU CERTO",JSON.stringify(object))
						if(result == true){
							$scope.registros[$scope.registros.findIndex(x => x.id==registro.id)] = object;
						}
						$scope.$apply();
					}
					fail_function = function (result,message,data_object,status) {
						error_notify(null,'Falha na operação',message);
						$scope.registro_selecionado = null;
						$scope.$apply();
					}
					validate_function = function () {return true;}
					request_api("/api/honorary/item/confirm",data_paramters,validade_function,success_function,fail_function);
				}
			}
			else{
				if(confirm("Deseja mesmo finalizar esse honorário?")){
					success_function = function(result,message,object,status){
						//success_notify("DEU CERTO",JSON.stringify(object))
						if(result == true){
							$scope.registros[$scope.registros.findIndex(x => x.id==registro.id)] = object;
						}
						$scope.$apply();
					}

					fail_function = function (result,message,data_object,status) {
						error_notify(null,'Falha na operação',message);
						$scope.$apply();
					}
					validate_function = function () {return true;}
					request_api("/api/honorary/item/close",data_paramters,validade_function,success_function,fail_function);
				}
			}
		}
		else{
			return error_notify(null,"Falha na operação","Honorário já foi finalizado!");
		}
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
		//$scope.apply();
	}

	$scope.get_filter_column = function(){
		var competence = $("#competence").val();
		var filtrar_pesquisa_por = $scope.filter_by_options[$scope.filter_by_index];
		$('#competence').prop('disabled', false);
		if(competence=='TODOS'){
			switch ($scope.filter_contract_by){
				case 'com_contrato':
					switch (filtrar_pesquisa_por) {
						case 'codigo':
							if($scope.filter_conferred == 'T'){
								return {id: $scope.search, have_contract: true};
							}
							else{
								return {id: $scope.search, have_contract: true, status:$scope.filter_conferred};
							}

						case 'competence':
							$("#competence").val('TODOS');
							$('#competence').prop('disabled', true);
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search, have_contract: true};
							}
							else{
								return {competence: $scope.search, have_contract: true, status:$scope.filter_conferred};
							}

						default:
							if($scope.filter_conferred == 'T'){
								return {entity_name: $scope.search, have_contract: true};
							}
							else{
								return {entity_name: $scope.search, have_contract: true, status:$scope.filter_conferred};
							}
					}
				case 'sem_contrato':
					switch (filtrar_pesquisa_por) {
						case 'codigo':
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search, have_contract: false};
							}
							else{
								return {competence: $scope.search, have_contract: false, status:$scope.filter_conferred};
							}
						case 'competence':
							$("#competence").val('TODOS');
							$('#competence').prop('disabled', true);
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search, have_contract: false};
							}
							else{
								return {competence: $scope.search, have_contract: false, status:$scope.filter_conferred};
							}
						default:
							if($scope.filter_conferred == 'T'){
								return {entity_name: $scope.search, have_contract: false};
							}
							else{
								return {entity_name: $scope.search, have_contract: false, status:$scope.filter_conferred};
							}
					}
				default:
					switch (filtrar_pesquisa_por) {
						case 'codigo':
							if($scope.filter_conferred == 'T'){
								return {id: $scope.search};
							}
							else{
								return {id: $scope.search, status:$scope.filter_conferred};
							}

						case 'competence':
							$("#competence").val('TODOS');
							$('#competence').prop('disabled', true);
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search};
							}
							else{
								return {competence: $scope.search, status:$scope.filter_conferred};
							}
						default:
							if($scope.filter_conferred == 'T'){
								return {entity_name: $scope.search};
							}
							else{
								return {entity_name: $scope.search, status:$scope.filter_conferred};
							}
					}
			}
		}

		else{
			switch ($scope.filter_contract_by){
				case 'com_contrato':
					switch (filtrar_pesquisa_por){
						case 'codigo':
							if($scope.filter_conferred == 'T'){
								return {id: $scope.search, competence:competence, have_contract: true};
							}
							else{
								return {id: $scope.search, competence:competence, have_contract: true, status:$scope.filter_conferred};
							}

						case 'competence':
							$("#competence").val('TODOS');
							$('#competence').prop('disabled', true);
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search, have_contract: true };
							}
							else{
								return {competence: $scope.search, have_contract: true, status:$scope.filter_conferred };
							}
						default:
							if($scope.filter_conferred == 'T'){
								return {entity_name: $scope.search, competence: competence, have_contract: true};
							}
							else{
								return {entity_name: $scope.search, competence: competence, have_contract: true, status:$scope.filter_conferred };
							}
					}

				case 'sem_contrato':
					switch (filtrar_pesquisa_por){
						case 'codigo':
							if($scope.filter_conferred == 'T'){
								return {id: $scope.search, competence:competence, have_contract: false};
							}
							else{
								return {id: $scope.search, competence:competence, have_contract: false, status:$scope.filter_conferred};
							}
						case 'competence':
							$("#competence").val('TODOS');
							$('#competence').prop('disabled', true);
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search, have_contract: false};
							}
							else{
								return {competence: $scope.search, have_contract: false, status:$scope.filter_conferred};
							}
						default:
							if($scope.filter_conferred == 'T'){
								return {entity_name: $scope.search, competence:competence, have_contract: false};
							}
							else{
								return {entity_name: $scope.search, competence:competence, have_contract: false, status:$scope.filter_conferred};
							}
					}

				default:
					switch (filtrar_pesquisa_por){
						case 'codigo':
							if($scope.filter_conferred == 'T'){
								return {id: $scope.search, competence:competence};
							}
							else{
								return {id: $scope.search, competence:competence, status:$scope.filter_conferred};
							}

						case 'competence':
							$("#competence").val('TODOS');
							$('#competence').prop('disabled', true);
							if($scope.filter_conferred == 'T'){
								return {competence: $scope.search};
							}
							else{
								return {competence: $scope.search, status:$scope.filter_conferred};
							}

						default:
							if($scope.filter_conferred == 'T'){
								return {entity_name: $scope.search, competence:competence};
							}
							else{
								return {entity_name: $scope.search, competence:competence, status:$scope.filter_conferred};
							}
					}
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
			if($scope.registro_selecionado.contract__dia_vencimento!=null){
				date = new Date();
				var day = '';

				if($scope.registro_selecionado.contract__dia_vencimento.length==1){
					day = '0'+$scope.registro_selecionado.contract__dia_vencimento.toString();
				}
				else{
					day = $scope.registro_selecionado.contract__dia_vencimento.toString();
				}

				var new_date = month_names[date.getMonth()+1]+"/"+date.getFullYear();
				var iso_date = date.getFullYear()+"-"+month_names[date.getMonth()+1]+"-"+day;
				var label_day = "";
				switch(new Date(iso_date).getDay()){
					case 0: label_day = "SEGUNDA"; break;
					case 1: label_day = "TERÇA"; break;
					case 2: label_day = "QUARTA"; break;
					case 3: label_day = "QUINTA"; break;
					case 4: label_day = "SEXTA"; break;
					case 5:label_day = "SEXTA";day = parseInt(day)-1;break;
					case 6: label_day = "SEGUNDA"; day = parseInt(day)+1;break;
					default: break;
				}

				day = day.toString();
				if(day.length==1){
					day = '0'+day;
				}
				new_date = day+"/"+new_date+" - "+label_day;
				$('#data_vencimento').val(new_date);
			}
			else{
				//var currentDate = new Date();
				//var day = currentDate.getDate();
				//var month =  month_names[currentDate.getMonth()];
				//var year = currentDate.getFullYear();

				//if(day.toString().length==1){
				//	day = "0"+day;
				//}
				$('#data_vencimento').val('');
			}
		}
		else{
			error_notify(null,'Falha na Operação','Selecione um honorário para gerar o documento.');
		}
	}

	$scope.generate_honorary = function(){
		var vencimento = '';
		if($('#data_vencimento').val().indexOf(" - ") !== -1){
			vencimento = $('#data_vencimento').val().split(' - ')[0];
		}
		else{
			vencimento = $('#data_vencimento').val();
		}

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
		if($scope.registro_selecionado.status!='E'){
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

			if($scope.registro_selecionado.honorary_itens.length < 9-$scope.max_honorary_itens){
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
				error_notify(null,'Falha na operação','Cada honorário deve conter no máximo dez itens sendo que o ultimo é reservado pelo sistema para arredondamentos.')
			}
		}
		else{
			error_notify(null,'Falha na operação','Erro! Não é permitido a alteração de honorários encerrados.')
		}
	}

	$scope.update_honorary_item = function(){
		if($scope.selected_item!=null){
			if($scope.registro_selecionado.status!='E'){
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
		if($scope.registro_selecionado.status!='E'){
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
			//alert("VEJA O REGISTRO qUE TEM QUE CARREGAR: "+JSON.stringify(registro));
			$scope.selected_item = registro;
			$scope.provents_options.forEach(function(item, index){
				//alert("VEJA AS OPÇÔES: "+index+" - "+item.id);
				if(item.id==registro.item){
					//$("#item_id").val(item.id);
					setTimeout(function(){$("#item_id").val(item.id).trigger('change');},10);
				}
			});
			$scope.load_item_selected();
		}
	}

	$scope.desmarcar_item = function(registro){
		if($scope.item_provent_editing!=null){
			$scope.item_provent_editing.attr('selected',false);
			$scope.item_provent_editing = null;
			$scope.selected_item.selected = "";
			$scope.selected_item = null;
			document.getElementById('item_id').disabled = false;
			document.getElementById('type_item').disabled = false;
		}


		$("#type_item").val("P");
		//$("#item_id").val("") //.change();
		$("#unit_value").val("");
		$("#complement").val("");
		$("#quantity").val("");
		$("#total_value").val("");

	}

	$scope.load_item_selected = function(){
		if($scope.item_provent_editing!=null){
			//alert("JA TINHA UM SELECIONADO")
			$scope.item_provent_editing.attr('selected',false);
			$scope.selected_item.selected = "";
			$scope.item_provent_editing = null;
		}

		$("#type_item").val($scope.selected_item.type_item);
		$("#complement").val($scope.selected_item.complement);
		$("#unit_value").val($filter('currency')($scope.selected_item.unit_value,"", 2));
		$("#total_value").val($filter('currency')($scope.selected_item.total_value,"", 2));
		$("#quantity").val($filter('currency')($scope.selected_item.quantity,"", 2));

		$("#unit_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
		$("#total_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
		$("#quantity").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});

		$("#item_id option").each(function () {
			//alert("VEJA: "+$(this).html());
			if ($(this).html().indexOf($scope.selected_item.item__nome)!=-1) {
				//alert("encontrei "+$(this).attr("id"));
				//setTimeout(function(){$("#item_id").val($(this).attr("id")).trigger('change');},10);
				//setTimeout(function(){$(this).attr("selected", "selected").trigger('change');},10);
				$scope.item_provent_editing = $(this);
				setTimeout(function(){
					//alert("VEJA QUEM TA: "+$scope.item_provent_editing);
					$scope.item_provent_editing.attr("selected", "selected");
					//alert("TROQUEI: "+$scope.item_provent_editing);
					//$("#item_id").trigger('change');
					document.getElementById('item_id').disabled = true;
					document.getElementById('type_item').disabled = true;
					//$scope.$apply();
				},100);
				return;
			}
		});
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

	$scope.select_provent_option = function(){
	  var index = $("#item_id").val();
	  if(index != null && index != ""){
      $scope.selected_option_provent = $scope.provents_options[index];
      //alert("VEJA O OBJETO: "+ JSON.stringify($scope.selected_option_provent))
      //setTimeout(function(){$("#item_id").val(option).trigger('change');},10);

      if($scope.selected_option_provent.tipo_valor=='R'){
        $("#lb_unit_value").text("Valor unitário");
        $("#lb_quantity").text("Quantidade");
        $("#quantity").val('1,00');
        $("#unit_value").val($filter('currency')($scope.selected_option_provent.valor,"", 2));
        $("#total_value").val($filter('currency')(parseInt($scope.selected_option_provent.valor)*1,"", 2));
      }
      else{
        if($scope.registro_selecionado.initial_value_contract != null){
          $("#lb_unit_value").text("Valor Base");
          $("#lb_quantity").text("Taxa (%)");
          $("#unit_value").val($filter('currency')($scope.registro_selecionado.initial_value_contract,"", 2));
          $("#quantity").val($filter('currency')($scope.selected_option_provent.valor,"", 2));
          $("#total_value").val($filter('currency')(($scope.selected_option_provent.valor/100)*$scope.registro_selecionado.initial_value_contract,"", 2));

          /*if(option!=''){
            $("#quantity").val($filter('currency')(option,"", 2));
            $("#total_value").val($filter('currency')(parseInt(option)*$scope.registro_selecionado.initial_value_contract,"", 2));
          }
          else{
            $("#quantity").val('');
            $("#unit_value").val('');
            $("#total_value").val('');
          }
          */
        }
        else{
          $("#quantity").val('');
          $("#unit_value").val('');
          $("#total_value").val('');
        }
      }
		}
		$("#unit_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
		$("#total_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
		$("#quantity").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
		setTimeout(function(){$("#item_id").val(index).trigger('change');},1);
	}

	$scope.calculate_provent_value = function(){
		var quantity = parseFloat($("#quantity").val().replace(".","").replace(",","."));
		var unit_value = parseFloat($("#unit_value").val().replace(".","").replace(",","."));

		if($scope.selected_option_provent!=null && $scope.selected_item == null){
			// Adicionando item
			var index = $("#item_id").val();
			if($scope.selected_option_provent.tipo_valor=='R'){
				var total_value = unit_value*quantity;
			}
			else{
				var total_value = unit_value*(quantity/100);
			}
			$("#total_value").val($filter('currency')(total_value,"", 2));
			$("#unit_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
			$("#quantity").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
			$("#total_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
			setTimeout(function(){$("#item_id").val(index).trigger('change');},1);
		}
		else{

			if($scope.selected_item != null){
				//alert("VAMOS calcular com os valores carregados: "+JSON.stringify($scope.selected_item))
				if($scope.selected_item.type_value=='R'){
					var total_value = unit_value*quantity;
				}
				else{
					var total_value = unit_value*(quantity/100);
				}

				$("#total_value").val($filter('currency')(total_value,"", 2));
				setTimeout(function(){$("#item_id").val(index).trigger('change');},1);
				//$("#total_value").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
				//$("#item_id").val(1).trigger('change');
			}
			else{
				//alert("Nao calcula nada nao..")
			}
		}
	}





		/*var index = $("#item_id").val();
		var quantity = parseFloat($("#quantity").val().replace(".","").replace(",","."));
		var unit_value = parseFloat($("#unit_value").val().replace(".","").replace(",","."));

		alert("VEJA QUEM EH selected_option_provent: "+JSON.stringify($scope.selected_option_provent));
		alert("VEJA QUEM EH selected_item: "+JSON.stringify($scope.selected_item));

		if($scope.selected_option_provent==null){
			alert("NAO TEM ITEM SELECIONADO?");
			//setTimeout(function(){$("#item_id").val($scope.selected_option_provent.id.toString()).trigger('change');},5);
			if($scope.selected_option_provent.tipo_valor=='R'){
				var total_value = unit_value*quantity;
			}
			else{
				var total_value = unit_value*(quantity/100);
			}
			$("#total_value").val($filter('currency')(total_value,"", 2));
		}
		else{
			alert("TEM ITEM SELECIONADO");
			if($scope.edited_item_option){
				alert("TEM EDITED_ITEM_OPTION");
				setTimeout(function(){$("#item_id").val($scope.edited_item_option.toString()).trigger('change');},10);
			}
			else{
				alert("NAO TEM EDITED_ITEM_OPTION");
				setTimeout(function(){$("#item_id").val($scope.selected_item.item.toString()).trigger('change');},5);
			}

			alert("PASSEI");
			var quantity = parseFloat($("#quantity").val().replace(".","").replace(",","."));
			alert("PASSEI");
			var unit_value = parseFloat($("#unit_value").val().replace(".","").replace(",","."));
			alert("PASSEI");

			if($scope.selected_option_provent.tipo_valor=='R'){
				alert("TIPO SELECIONADO R");
				var total_value = unit_value*quantity;
				//alert(total_value)
			}
			else{
			alert("TIPO SELECIONADO P");
				var total_value = unit_value*(quantity/100);
				//alert(total_value)
			}
			alert("HORA DE APRESENTAR O VALOR TOTAL");
			$("#total_value").val($filter('currency')(total_value,"", 2));
			alert("APRESENTEI");
		}
		alert("VEJA QUEM EH selected_option_provent: "+JSON.stringify($scope.selected_option_provent));
		alert("VEJA QUEM EH selected_item: "+JSON.stringify($scope.selected_item));
		alert("INDO EMBORA");
		//setTimeout(function(){$("#item_id").val(index).trigger('change');},1);
	}	*/
}]);