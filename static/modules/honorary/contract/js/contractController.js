var app = angular.module('app', ['angularUtils.directives.dirPagination']);

app.controller('MeuController', ['$scope', '$filter', function($scope,$filter) {

	$scope.screen_height = window.innerHeight;
	$scope.screen_width  = window.innerWidth;

	$scope.screen4 = null;
	$scope.screen3 = null;
	$scope.screen2 = null;
	$scope.screen1 = null;

	$scope.sortType           = 'codigo';
	$scope.sortReverse        = false;
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","cliente", "plano"];
	$scope.search             = '';
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10]

	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.indicacao_selecionada 	= null;
	$scope.esta_adicionando     	= true;
	$scope.esta_indicando					= false;
	$scope.indicacoes_carregadas = false;
	$scope.servicos_carregados = false;
	$scope.dained_permission = false;
	$scope.dained_permission_indication = false;

	$scope.reajustar_tela = function (){
		$scope.screen_height = window.innerHeight
		$scope.screen_width  = window.innerWidth

		$scope.screen5 = false;  // Giant Screen:   1681 or more
		$scope.screen4 = false;  // Larger Screen:  1025 ~ 1680 + 656
		$scope.screen3 = false;  // Large Screen:    769 ~ 1024 + 304
		$scope.screen2 = false;  // Medium Screen:   321 ~ 720 + 240
		$scope.screen1 = false;  // Small Screen:    361 ~ 480 + 120
		$scope.screen0 = false;  // Smaller Screen:    0 ~ 360

		//if ($scope.col_cliente_size){
		//	$scope.col_cliente_size = $scope.col_cliente_size - 50; // PROBLEMA QUANDO 481,482,483,484px no 485 volta ao normal
		//}
		//else{
		//	$scope.col_cliente_size = 100;
		//}


		// QUANDO A TELA TA NO MENOR TAMANHO (304px) A COLUNA CLIENTE TEM 185px. SE EU QUERO UM OFFSET NO FINAL
		//alert("VEJA A COLUNA: "+$scope.col_cliente_size)

		//alert("TEM ALGUMA COISA AQui: "+$scope.col_cliente_size)
		// PROBLEMA QUANDO TO REFRESH NUMA TELA MAIOR DEPOIS DESCO PRA UMA MENOR
		//if(!$scope.col_cliente_size){
		//	$scope.col_cliente_size = $scope.screen_width - ($scope.screen_width*0,6788); // 120

			// 304 -> 185 = 0,6058
			// 360 -> 241 = 0,6694
			// 480 -> 360 = 0,7500
			// 720 -> 497 = 0,6902
			// MEDIA 0,6788
		//}

		//alert("VEJA O TAMANHO (NA RESOLUCAO BAIXA COMECA COM 185px: "+ $scope.col_cliente_size)
		//$scope.col_cliente_size = $('.col-cliente').width();

		if ($scope.screen_width <= 360){
			$scope.screen0 = true;
		}

		else if ($scope.screen_width <= 480){
			$scope.screen1 = true;
			//$scope.col_cliente_size = $scope.col_cliente_size - 120;
		}

		else if ($scope.screen_width <= 720){
			$scope.screen2 = true;
			//$scope.col_cliente_size = $scope.col_cliente_size - 10;
		}

		else if ($scope.screen_width <= 1024){
			$scope.screen3 = true;
		}
		else if ($scope.screen_width <= 1268){
			$scope.screen4 = true;
		}
		else{
			$scope.screen5 = true;
		}
		$scope.$apply();
	}

	$scope.carregar_clientes = function() {
		$.ajax({
			type: "GET",
				url: "/api/contract/lista_contratos",
				success: function (data) {
					try{
						$scope.contratos = JSON.parse(data).object;//Object.keys(data).map(function(_) { return data[_]; }) //_(data).toArray();
						$scope.contratos_carregados = true;
						$scope.$apply();
						$scope.reajustar_tela();
					}
					catch(err){
						if(data.indexOf('ERRO403')!= -1){
							error_notify(null,"Operação não autorizada","Nível de autonomia não permite o acesso à este recurso.");
							$scope.dained_permission = true;
							$scope.contratos_carregados = true;
							$scope.$apply();
						}
					}
				},
				failure: function (data) {
					$scope.contratos = [];
					$scope.desabilitar = 'link_desabilitado';
					alert('Erro! Não foi possivel carregar a lista de serviços');
				}
		});
	}

	$scope.atualizar_contrato = function(cliente) {
		var data = {cliente : cliente}

		function validate_function () {return true}

		success_function = function(result,message,object,status){
			$scope.registro_selecionado.contrato = object;
			$scope.$apply();
		}

		fail_function = function (result,message,data_object,status) {
			alert('Erro! Falha na atualização do contrato.')
		}
		request_api("/api/contract/atualizar_contrato/",data,validate_function,success_function,fail_function)
	}

	$scope.adicionar_contrato = function() {
		var data_paramters = $scope.get_data_from_form();
		if ($("#desconto_temporario").val() == ""){
			data_paramters['desconto_temporario'] = '0.0';
		}
		//alert("Olha o data>"+JSON.stringify(data_paramters))

		function validate_function(){
			return true
		}

		function success_function(result,message,data_object,status) {
			//alert("VEJA O RESULT: "+JSON.stringify(message))
			/*
			$scope.registro_selecionado.contrato.tipo_cliente = $('#tipo_cliente option:selected').text()
			$scope.registro_selecionado.plano = $('#select_plano option:selected').text()
			$scope.registro_selecionado.contrato.vigencia_inicio = data_paramters.vigencia_inicio
			$scope.registro_selecionado.contrato.vigencia_fim = data_paramters.vigencia_fim
			$scope.registro_selecionado.contrato.valor_honorario = message.fields.valor_honorario
			$scope.registro_selecionado.contrato.valor_total = message.fields.valor_total
			$scope.registro_selecionado.contrato.servicos_contratados = message.fields.servicos_contratados
			$scope.registro_selecionado.contrato.desconto_temporario = parseFloat(message.fields.desconto_temporario)

			if (message.fields.desconto_indicacoes!=0){
				$scope.registro_selecionado.contrato.desconto_indicacoes = message.fields.desconto_indicacoes//parseFloat(message.fields.desconto_indicacoes)
			}
			else{
				$scope.registro_selecionado.contrato.desconto_indicacoes = 0
			}

			$scope.registro_selecionado.contrato.desconto_temporario = message.fields.desconto_temporario
			*/
			//alert("deu True")
			$scope.registro_selecionado.contrato = data_object;
			$scope.registro_selecionado.plano = $('#select_plano option:selected').text();
			$scope.$apply()
			$('#modal_adicionar_contrato').modal('hide');
		}

		fail_function = function(result,message,data_object,status) {
			alert("deu false")
			$.each(message, function( index, value ) {
				//alert("ERRO: "+index + ": " + value );
				notificar('error','Falha na Operação',value);
				marcar_campo_errado(index);
				$("#"+index).focus();
			});
		}
		request_api("/api/contract/salvar_contrato",data_paramters,validate_function,success_function,fail_function)
	}

	$scope.alterar_contrato = function() {
		var data_paramters = $scope.get_data_from_form();
		data_paramters['id'] = $scope.registro_selecionado.contrato.id;
		if ($("#desconto_temporario").val() == ""){
			data_paramters['desconto_temporario'] = '0.0';
		}

		function validate_function(){
			if(data_paramters===null){return false}
			else{return true}
		}
		//alert("Olha o data:\n"+JSON.stringify(data_paramters));
		function success_function(result,message,data_object,status) {
			$scope.registro_selecionado.contrato = data_object;
			$scope.$apply();
			$('#modal_adicionar_contrato').modal('hide');
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

		if(data_paramters!=null){
			request_api("/api/contract/alterar_contrato",data_paramters,validate_function,success_function,fail_function)
		}
	}

	$scope.close_contract = function(){
		var data_paramters = {};
		data_paramters['id'] = $scope.registro_selecionado.contrato.id;

		function validate_function () {
			if($scope.registro_selecionado.contrato.ativo==false){
				warning_notify(null,"Atenção","Contrato do cliente "+$scope.registro_selecionado.cliente_nome+" já foi encerrado.");
				return false;
			}
			confirmation = confirm("Atenção! Deseja mesmo finalizar o contrato?");
			if(confirmation==true){
				return true;
			}
			else{
				return false;
			}
		}

		success_function = function(result,message,object,status){
			$scope.registro_selecionado.contrato = object;
			$scope.$apply();
			success_notify("Operação realizada com sucesso!","Contrato do cliente "+$scope.registro_selecionado.cliente_nome+" encerrado com sucesso!");
		};

		fail_function = function (result,message,data_object,status) {
			notify(null,'Falha na operação!',message)
		};
		request_api("/api/contract/close/",data_paramters,validate_function,success_function,fail_function)

	};

	$scope.get_data_from_form = function(){
		var tipo_cliente = $('#select_tipo_cliente option:selected').val();
		var plano = $('#select_plano option:selected').val();
		var honorario = $('#valor_honorario').val();
		var vigencia_inicio = $("#vigencia_inicio").val();
		var vigencia_fim = $("#vigencia_fim").val();
		var tipo_vencimento = $('#select_tipo_vencimento option:selected').val();
    var dia_vencimento = $('#select_dia_vencimento option:selected').val();
    var data_vencimento = $("#data_vencimento").val();
		var tipo_honorario = $('#select_tipo_honorario option:selected').val();
    var taxa_honorario = $("#taxa_honorario").val().replace('.','').replace(',','.');
    var valor_honorario = $('#valor_honorario').val().replace(".","").replace(",",".");
    var desconto_inicio = $('#desconto_inicio').val();
    var desconto_fim = $('#desconto_fim').val();
    var desconto_temporario = parseFloat($('#desconto_temporario').val().replace(".","").replace(",","."));
    var valor_total = $('#valor_total').val().replace("R$ ","").replace(".","").replace(",",".");

		tipo_cliente ? $('#select_tipo_cliente').removeClass('wrong') :  $('#select_tipo_cliente').addClass('wrong');
		plano ? $('#select_plano').removeClass('wrong') :  $('#select_plano').addClass('wrong');
		valor_honorario ? $('#valor_honorario').removeClass('wrong') :  $('#valor_honorario').addClass('wrong');

		var cliente = $scope.registro_selecionado.cliente_id
		if(tipo_cliente && plano && valor_honorario){
			var data = {
				cliente: cliente,
				tipo_cliente:tipo_cliente,
				plano:plano,
				valor_honorario:valor_honorario,

				vigencia_inicio:vigencia_inicio,
				vigencia_fim:vigencia_fim,

				tipo_vencimento:tipo_vencimento,
				dia_vencimento:dia_vencimento,
				data_vencimento:data_vencimento,

				tipo_honorario:tipo_honorario,
				taxa_honorario:taxa_honorario,
				valor_honorario:valor_honorario,

				desconto_inicio:desconto_inicio,
				desconto_fim:desconto_fim,
				desconto_temporario:desconto_temporario,
				valor_total:valor_total
				}
			return data
		}
		return null
	}

	$scope.select_filter_by = function (index) {
		$scope.filter_by_index = parseInt($scope.filter_by);
	}

	$scope.get_filter_column = function(){
			var filtrar_pesquisa_por = $scope.filter_by_options[$scope.filter_by_index];
			switch (filtrar_pesquisa_por) {
					case 'codigo':
							//alert("filtrar por codigo");
							return {cliente_id: $scope.search};
					case 'plano':
							//alert("filtrar pelo plano");
							return {plano: $scope.search};
					default:
							return {cliente_nome: $scope.search}
			}
	}

	$scope.verificar_contratos = function () {
			if ($scope.contratos == "" || $scope.contratos == []){
					$scope.desabilitar  = 'link_desabilitado';
			}
			else{
					$scope.desabilitar  = '';
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
	}

	$scope.desmarcar_linha_selecionada = function(){
			$scope.registro_selecionado.selecionado = "";
			$scope.registro_selecionado = null;
			$scope.opcao_desabilitada = "desabilitado";
	}

	$scope.excluir_servico = function () {
			var servico = $('#modal_servico').val().toUpperCase();
			var descricao = $('#modal_descricao').val().toUpperCase();

			if (confirm('Deseja mesmo excluir esse Serviço?')) {

					$.ajax({
							type: "POST",
							url: "/api/preferencias/excluir_servico/"+$scope.registro_selecionado.id+"/",
							data: {
									servico: servico,
									descricao: descricao,
									csrfmiddlewaretoken: '{{ csrf_token }}'
							},

							success: function (data) {

									var resultado = $.parseJSON(data);

									if (resultado['success'] == true){
											$scope.contratos.splice($scope.contratos.indexOf($scope.registro_selecionado), 1);
											$scope.registro_selecionado = null;
											$scope.opcao_desabilitada = "desabilitado";
											$scope.$apply();
											$scope.resetar_formulario_servico();
											//alert(resultado['message']);
									}

									else{
											alert(resultado["message"]);
									}
							},
							failure: function (data) {
									alert('Erro! Falha na execução do ajax');
							}
					});

					//return true;
			}
			else {
					e.preventDefault();

					//return false;
			}

			$scope.verificar_contratos();

	}

	$scope.get_salario_vigente = function(){
		$.ajax({
			url: '/api/preferencias/salario_vigente/',
			type: 'get', //this is the default though, you don't actually need to always mention it

			success: function(data) {
				$('#form-group-taxa-salario').tooltip({title:"Valor de Referência: "+data.salario_vigencia_atual});
				$scope.salario_vigente = data.salario_vigencia_atual;
				$('#salario_vigente').val(data.salario_vigencia_atual)
				$scope.$apply();
			},

			failure: function(data) {
				alert('Got an error dude');
			}
		});
	}

	$scope.open_contract = function(){
		if ($scope.registro_selecionado.contrato != null){
			$scope.esta_adicionando = false;
			var plano = $scope.registro_selecionado.contrato.plano;
			if(plano){
				$("#plano").val(plano).change();
				//$('#plano option[value=3]').prop('selected','selected');
				//$('#plano').find('option:selected').text(plano)
			}
			else{
				$('#plano option:first').prop('selected','selected');
			}

			//s$('#tipo_cliente').find('option:selected').val($scope.registro_selecionado.contato.tipo_cliente)
			$('#vigencia_inicio').val($filter('date')($scope.registro_selecionado.contrato.vigencia_inicio,'dd/MM/yyyy'));
			$('#vigencia_fim').val($filter('date')($scope.registro_selecionado.contrato.vigencia_fim,'dd/MM/yyyy'));
			$('#dia_vencimento option:selected').text($scope.registro_selecionado.contrato.dia_vencimento);
			$("#data_vencimento").val($filter('date')($scope.registro_selecionado.contrato.data_vencimento,'dd/MM/yyyy'));
			$('#tipo_honorario').find('option:selected').text($scope.registro_selecionado.contrato.tipo_honorario)
			$("#taxa_honorario").val($scope.registro_selecionado.contrato.taxa_honorario)
			$('#valor_honorario').val($scope.registro_selecionado.contrato.valor_honorario *100.0).trigger('mask.maskMoney');
			$('#desconto_inicio').val($filter('date')($scope.registro_selecionado.contrato.desconto_inicio,'dd/MM/yyyy'));
			$('#desconto_fim').val($filter('date')($scope.registro_selecionado.contrato.desconto_fim,'dd/MM/yyyy'));
			$('#desconto_temporario').val($scope.registro_selecionado.contrato.desconto_temporario).trigger('mask.maskMoney');
			//$("#desconto_temporario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
			//$('#valor_total').val($filter('currency')($scope.registro_selecionado.contrato.valor_total,"", 2)); //$scope.registro_selecionado.contrato.valor_total*100).trigger('mask.maskMoney');
			$scope.calcular_total();
		}
		else{
			$scope.esta_adicionando = true;
		}
	}

	$scope.calcular_total = function () {
		var honorario = $('#valor_honorario').val();
		var desconto = $('#desconto_temporario').val();
		if (!(honorario == '')){
			if(desconto != ""){
				if(verificar_vigencia_desconto()){
					honorario = Number(honorario.replace(/\./g,'').replace(',','.'));
					desconto = Number(desconto.replace(/\./g,'').replace(',','.'));
					var valor_total = honorario * (1 - (desconto/100))
					$('#valor_total').val($filter('currency')(valor_total,"R$ ", 2));
				}
				else{
					honorario = Number(honorario.replace(/\./g,'').replace(',','.'));
					//desconto = Number(desconto.replace(/\./g,'').replace(',','.'));
					var valor_total = honorario;
					$('#valor_total').val($filter('currency')(valor_total,"R$ ", 2));
				}
			}
			else{
				honorario = Number(honorario.replace(/\./g,'').replace(',','.'));
				var valor_total = honorario;
				$('#valor_total').val($filter('currency')(valor_total,"R$ ", 2));
			}
		}
	}

	$scope.load_clientes = function () {
		$.ajax({
			type: 'GET',
			url: "/api/contract/clientes/" + $scope.registro_selecionado.cliente_id,

			success: function (data) {
				$scope.registro_selecionado.clientes = JSON.parse(data);
				$scope.$apply();
			},
			failure: function (data) {
				$scope.clientes = [];
				$scope.desabilitar = 'link_desabilitado'
				alert("Não foi possivel carregar a lista de indicacoes")
			}
		});
	}

	$scope.calcular_total_desconto_fidelidade = function (){
		$scope.total_desconto_fidelidade = 0.0;
		$scope.total_credito_desconto_fidelidade = 0.0;
		$scope.registro_selecionado.indicacoes.forEach(function(item, index){
			if(item.indicacao_ativa==true){
				$scope.total_desconto_fidelidade = $scope.total_desconto_fidelidade + parseFloat(item.taxa_desconto);
			}
		});

		if($scope.total_desconto_fidelidade > 30){
			$scope.total_credito_desconto_fidelidade = $scope.total_desconto_fidelidade - 30.0;
			$scope.total_desconto_fidelidade =  30;
		}
	}

	$scope.incrementar_desconto_fidelidade = function(valor){
		$scope.total_desconto_fidelidade = $scope.total_desconto_fidelidade + parseFloat(valor);
	}

	$scope.decrementar_desconto_fidelidade = function(valor){
		$scope.total_desconto_fidelidade = $scope.total_desconto_fidelidade - parseFloat(valor);
	}

	$scope.carregar_servicos_contratados = function(){
		$scope.servicos_carregados = false;
		$.ajax({
			type: "GET",
				url: "/api/contract/carregar_servicos_contratados/"+$scope.registro_selecionado.cliente_id,
				success: function (data) {
					$scope.servicos_contratados = JSON.parse(data).object;
					$scope.servicos_carregados = true;
					$scope.$apply();
				},
				failure: function (data) {
					$scope.servicos_contratados = [];
					alert('Erro! Não foi possivel carregar os serviços do plano');
				}
		});
	}

	$scope.ativar_desativar_servico = function(registro){
		if(registro.ativo){
			if($scope.registro_selecionado.contrato.servicos_contratados.search(";"+registro.id.toString()+";") != -1){
				// Apagar o elemento que esta entre outros dois.
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados.replace(registro.id.toString()+';','');
			}
			else if($scope.registro_selecionado.contrato.servicos_contratados.search(";"+registro.id.toString()) != -1){
				// Apagar o elemento que esta por ultimo
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados.replace(";"+registro.id.toString(),'');
			}

			else if($scope.registro_selecionado.contrato.servicos_contratados.search(registro.id.toString()+";") != -1){
				// Apagar o primeiro elemento
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados.replace(registro.id.toString()+';','');
			}
			else{
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados.replace(registro.id.toString(),'');
			}
			registro.ativo = false

		}
		else{
			if($scope.registro_selecionado.contrato.servicos_contratados == ""){
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados+registro.id.toString();
			}
			else if($scope.registro_selecionado.contrato.servicos_contratados.search(";") != -1){
				//alert("Cara, axo que ja tem algum servico la, entao adicionar no final junto com um separador")
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados+";"+registro.id.toString();

			}
			else{
				//alert("Nao eh vazio, e nao tem separador, entao tem só um elemento")
				$scope.registro_selecionado.contrato.servicos_contratados = $scope.registro_selecionado.contrato.servicos_contratados+";"+registro.id.toString();
			}
			registro.ativo = true
		}

		var lista = $scope.registro_selecionado.contrato.servicos_contratados.split(';').sort()
		lista = lista.join(';')
		$scope.registro_selecionado.contrato.servicos_contratados = lista
		$scope.atualizar_servicos_contratados();
		//alert("VEJA OS SERVICOS: "+$scope.registro_selecionado.contrato.servicos_contratados+" - VALOR: ")
	}

	$scope.atualizar_servicos_contratados = function (){
		var servicos = $scope.registro_selecionado.contrato.servicos_contratados
		var cliente_id = $scope.registro_selecionado.cliente_id
		var data = {
			servicos : servicos,
			cliente_id : cliente_id
		}

		function validate_function () {
			return true
		}

		function success_function(message) {
			//alert("VEJA O RESULTADO "+JSON.stringify(message))
			//$('#modal_servicos').modal('hide');
			$scope.$apply()
		}

		function fail_function() {
			alert("Erro! Falha na alteração dos Serviços.")
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/contract/atualizar_servicos/",data,validate_function,success_function,fail_function)
	}

	$scope.carregar_indicacao = function () {
		$scope.total_desconto_fidelidade = 0;
		$scope.indicacoes_carregadas = false;
		$.ajax({
			type: 'GET',
			url: "/api/contract/lista_indicacao/" + $scope.registro_selecionado.cliente_id,

			success: function (data) {
				$scope.indicacoes_carregadas = true;
				try {
					$scope.registro_selecionado.indicacoes = JSON.parse(data).object;
					$scope.calcular_total_desconto_fidelidade();
					$scope.$apply();
				}catch (err){
					if (data.indexOf('ERRO403')!= -1){
							error_notify(null,"Operação não autorizada","Nível de autonomia não permite o acesso à este recurso.");
							$scope.dained_permission_indication = true;
							$scope.$apply();
					}
				}

			},
			failure: function (data) {
				$scope.indicacao = [];
				$scope.indicacoes_carregadas = true;
				$scope.$apply();
				alert("Não foi possivel carregar a lista de indicacoes")
			}
		});
	}

	$scope.adicionar_indicacao = function () {
		var empresa = $('#indicacao').val();
		var taxa_desconto = $('#taxa_desconto_indicacao').val();
		var cliente_id = $scope.registro_selecionado.cliente_id;

		var data = {
			empresa : empresa,
			taxa_desconto : taxa_desconto,
			cliente_id : cliente_id
		};

		function validate_function () {
			if(empresa === '' || taxa_desconto===''){
				alert('Preecha os campos');
				return false
			}
			return true
		}

		function success_function(result,message,data_object,status) {
			notify('success','Operação concluída','Indicação registrada com sucesso');
			$scope.registro_selecionado.indicacoes.push(data_object);
			$scope.$apply();
			if (data_object['change_contract']===true){
				$scope.calcular_total_desconto_fidelidade();
				$scope.atualizar_contrato(cliente_id);
			}
		};

		function fail_function(result,message,data_object,status) {
			alert('Empresa informada já foi indicada anteriormente')
		}
		request_api("/api/contract/salvar_indicacao/",data,validate_function,success_function,fail_function)
	};

	$scope.carregar_indicacao_selecionada = function(){
		var indica = $scope.indicacao_selecionada.indicacao;
		$('#taxa_desconto_indicacao').val($scope.indicacao_selecionada.taxa_desconto);
		$('#indicacao').val(indica)
	};

	$scope.alterar_indicacao = function () {
		var taxa_desconto = $('#taxa_desconto_indicacao').val().replace(".","").replace(',','.');
		if(parseFloat(taxa_desconto) <= 100.0){
			var empresa = $('#indicacao').val();
			var empresa_nome = $('#indicacao option:selected').text();
			var cliente_id = $scope.registro_selecionado.cliente_id;
			var data = {
				empresa : empresa,
				empresa_nome : empresa_nome,
				taxa_desconto : $('#taxa_desconto_indicacao').val(),
				cliente_id : cliente_id
			}

			function validate_function () {
				if(taxa_desconto==''){
					alert('Erro! Taxa de desconto precisa ser informado')
					return false
				}
				return true
			}

			function success_function(result,message,data_object,status) {
				var index = $scope.registro_selecionado.indicacoes.indexOf($scope.indicacao_selecionada);
				//data_object.taxa_desconto = $filter('currency')(data_object.taxa_desconto,"", 2)
				$scope.registro_selecionado.indicacoes[index] = data_object;
				if (data_object['change_contract']===true){
				$scope.atualizar_contrato(cliente_id);
				}
				$scope.calcular_total_desconto_fidelidade();
				$scope.desmarcar_linha_indicacao();
				$scope.$apply();
				$("#taxa_desconto_indicacao").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
			}

			function fail_function(result,message,data_object,status) {
				alert("Erro! Falha na alteração da indicação.")
			}
			request_api("/api/contract/alterar_indicacao/",data,validate_function,success_function,fail_function)
		}
		else{
			error_notify('taxa_desconto_indicacao',"Falha na operação","Taxa de desconto não pode ser maior que 100%.")
		}
	}

	$scope.ativar_desativar_indicacao = function (indicacao_selecionada, $event) {
		if(indicacao_selecionada!=null){
			var cliente_id = $scope.registro_selecionado.cliente_id;
			var status = indicacao_selecionada.indicacao_ativa;
			var indicated_company = indicacao_selecionada.indicacao;

			var data = {
				cliente: cliente_id,
				indicated_company : indicated_company,
				indicacao_ativa : status
			}

			function validate_function () {
				var operacao = "";
				if(status==true){
					operacao = "desativar"
				}
				else{
					operacao = "ativar"
				}
				var confirm_action = confirm("Deseja mesmo "+operacao+" indicação?");
				if (confirm_action == true) {
					return true;
				}
				else{
					$event.stopPropagation();
					return false;
				}
			}

			function success_function(result,message,data_object,status) {
				if(result==true){
					var index = $scope.registro_selecionado.indicacoes.indexOf(indicacao_selecionada);
					$scope.registro_selecionado.indicacoes[index] = data_object;
					$scope.calcular_total_desconto_fidelidade();
					$scope.$apply();
					if (data_object['change_contract']===true){
						$scope.atualizar_contrato(cliente_id);
					}
				}
				else{
				}
				$scope.desmarcar_linha_indicacao();
			}

			function fail_function(result,message,data_object,status) {
				alert("Erro! Falha na alteração do estado da indicação.")
			}
			request_api("/api/contract/alterar_boolean_indicacao/",data,validate_function,success_function,fail_function)
		}

	}

	$scope.deletar_indicacao = function (indicacao_selecionada, $event) {
		var r = confirm("Deseja mesmo excluir essa indicação?");
		if (r == true) {
			var indicated_company = indicacao_selecionada.indicacao;
			var cliente_id = $scope.registro_selecionado.cliente_id;

			var data = {
				indicated_company : indicated_company,
				cliente_id : cliente_id
			};

			function validate_function () {
				if($('#indicacao').val()==''){
					return false
				}
				else{
					return true
				}
			}

			function success_function(result,message,data_object,status) {
				success_notify(message,'');

				var index = $scope.registro_selecionado.indicacoes.indexOf(indicacao_selecionada);
				$scope.desmarcar_linha_indicacao();
				$scope.registro_selecionado.indicacoes.splice($scope.registro_selecionado.indicacoes.indexOf(indicacao_selecionada), 1);
				$scope.calcular_total_desconto_fidelidade();
				if (data_object['change_contract']===true){
					$scope.atualizar_contrato(cliente_id);
				}
				$scope.$apply()
			}

			function fail_function(result,message,data_object,status) {
				alert("Não foi possivel deletar neste momento")
			}
			request_api("/api/contract/deletar_indicacao/",data,validate_function,success_function,fail_function)
		} else {

		}
	};

	$scope.desmarcar_linha_indicacao = function () {
		$('#taxa_desconto_indicacao').val('')
		$('#indicacao').val('')
		$scope.indicacao_selecionada.selected = "";
		$scope.indicacao_selecionada = null;
		$scope.esta_indicando = false
	}

	$scope.selecionar_linha_indicacao = function(indicacao){
		if ($scope.indicacao_selecionada !==  null){
			if($scope.indicacao_selecionada == indicacao){
				$scope.desmarcar_linha_indicacao();
			}
			else{
				$scope.desmarcar_linha_indicacao();
				indicacao.selected = 'selected';
				$scope.indicacao_selecionada = indicacao;
				$scope.esta_indicando = true
				$scope.carregar_indicacao_selecionada();
			}
		}
		else{
			indicacao.selected = 'selected';
			$scope.indicacao_selecionada = indicacao;
			$scope.esta_indicando = true;
			$scope.carregar_indicacao_selecionada();
		}
	}

}]);