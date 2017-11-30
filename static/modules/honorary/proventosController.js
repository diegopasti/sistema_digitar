var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('MeuController', ['$scope', function($scope) {

	$scope.screen_height = window.innerHeight // screen.availHeight; - PEGA O TAMANHO DA TELA DO DISPOSITIVO
	$scope.screen_width  = window.innerWidth  // PEGA O TAMANHO DA JANELA DO BROWSER

	$scope.screen4 = null;
	$scope.screen3 = null;
	$scope.screen2 = null;
	$scope.screen1 = null;

	$scope.sortType           = 'codigo';    // set the default sort type
	$scope.sortReverse        = false;  // set the default sort order
	$scope.filter_by          = '1';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ["codigo","provento", "descricao"];
	$scope.search             = '';     // set the default search/filter term
	$scope.minimal_quantity_rows = [1,2,3,4,5,6,7,8,9,10]

	$scope.opcao_desabilitada = "desabilitado";
	$scope.registro_selecionado 	= null;
	$scope.indicacao_selecionada 	= null;
	$scope.esta_adicionando     	= true;
	$scope.esta_indicando					= false;
	$scope.indicacoes_carregadas = false;
	$scope.servicos_carregados = false;

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
			//if($scope.screen_width <= $scope.col_cliente_size){
			//	alert("COLUNA SERIA MAIOR QUE A A TELA.. AI VOU ACERTAR.."+$scope.col_cliente_size)
			//	$scope.col_cliente_size = $scope.screen_width - 120;
			//}

			//else{
			//	alert("OLHA AS PROPORÇOES.."+$scope.screen_width+" - "+$scope.col_cliente_size)
			//}
			//$scope.col_cliente_size = $scope.screen_width - 120;
			//$scope.col_cliente_size = $scope.col_cliente_size - 10;
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

	$scope.adicionar_provento = function() {
		var data_paramters = {};
		$.each($('#form_adicionar_contrato').serializeArray(), function(i, field) {
			data_paramters[field.name] = field.value.toUpperCase();
		});

		data_paramters['valor'] = data_paramters['valor'].replace(".","").replace(",",".")

    success_function = function(result,message,object,status){
			$scope.contratos.splice(0, 0, object);
			$scope.$apply();
			check_response_message_form('#form_adicionar_contrato', message);
			$("#modal_adicionar_contrato").modal('hide');
			reset_formulary(form_adicionar_contrato);
		}

    fail_function = function (result,message,data_object,status) {
      check_response_message_form('#form_adicionar_contrato', message);
    }

    validate_function = function () {
     return check_required_fields('form_adicionar_contrato');//validate_form_regiter_person(); //validate_date($scope.birth_date_foundation);
    }


		request_api("/api/proventos/adicionar",data_paramters,validate_function,success_function,fail_function)
	}

	$scope.update = function() {
		var data_paramters = {};
		data_paramters['id'] = $scope.entity_selected.id;

		$.each($('#form-save-entity').serializeArray(), function(i, field) {
			data_paramters[field.name] = field.value.toUpperCase();
		});

    success_function = function(result,message,object,status){
      if(result == true){
				//alert("QUERO MECHER NO ELEMENTO:"+$scope.list_entities.findIndex(x => x.id==$scope.entity_selected.id))
				$scope.list_entities[$scope.list_entities.findIndex(x => x.id==$scope.entity_selected.id)] = object;
				$scope.entity_selected = null;
				$scope.$apply();
				document.getElementById("form-save-entity").reset();
				check_response_message_form('#form-save-entity', message);
				$("#modal_identification").modal('hide');
      }
		}

    fail_function = function (result,message,data_object,status) {
      check_response_message_form('#form-save-entity', message);
    }

    validade_function = function () {
     return  true;//validate_form_regiter_person(); //validate_date($scope.birth_date_foundation);
    }

    request_api("/api/entity/update",data_paramters,validade_function,success_function,fail_function)
	}

	/*
	var data_paramters = $scope.get_data_from_form();
	function validate_function(){
		if(data_paramters){
			if(data_paramters['tipo'] && data_paramters['nome'] && data_paramters['valor'])
				return true
		}
		alert("Preencha os campos obrigatórios!")
		return false;
	}

	function success_function(message) {
		var registro = message.fields
		registro.id = message.pk
		$scope.contratos.splice(0,0, registro)
		$scope.$apply()
		resetar_formulario()
		$('#modal_adicionar_contrato').modal('hide');
	}

	function fail_function(message) {
		$.each(message, function( index, value ) {
			alert("ERRO: "+index + ": " + value );
			notificar('error','Falha na Operação',value);
			marcar_campo_errado(index)
			$("#"+index).focus();
		});
	}*/


	$scope.carregar_clientes = function () {
    $.ajax({
      type: 'GET',
      url: "/api/proventos",

      success: function (data) {
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
        alert("Não foi possivel carregar a lista")
      },
    })
	}


	$scope.adicionar_indicacao = function () {
		var empresa = $('#indicacao').val()
		var taxa_desconto = $('#taxa_desconto_indicacao').val()
		var cliente_id = $scope.registro_selecionado.cliente_id

		var data = {
			empresa : empresa,
			taxa_desconto : taxa_desconto,
			cliente_id : cliente_id
		}

		function validate_function () {
			if(empresa == '' || taxa_desconto==''){
				alert('Preecha os campos')
				return false
			}
			return true
		}

		function success_function(message) {
			var date = message['fields']["data_cadastro"]
			nova_indicaco = {
				cliente_id: cliente_id,
				indicacao: {
					nome_razao : $('#indicacao option:selected').text(),
					taxa_desconto : taxa_desconto,
					indicacao_ativa : true,
					data_cadastro : date
				}
			}
			$scope.registro_selecionado.indicacoes.push(nova_indicaco)
			$scope.atualizar_contrato(cliente_id)
			$scope.$apply()
		}

		function fail_function() {
			alert('Empresa informada já foi indicada anteriormente')
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/honorario/salvar_indicacao/",data,validate_function,success_function,fail_function)
	}

	$scope.atualizar_contrato = function(cliente) {
		var data = {
			cliente : cliente,
		}

		function validate_function () {
			return true
		}

		function success_function(message) {
			$scope.registro_selecionado.contrato = message.fields
			//alert('veja o que veio: '+$scope.registro_selecionado.contrato.desconto_indicacoes)
			$scope.$apply()
			resetar_formulario()
			//$('#modal_indicacoes').modal('hide');
		}

		function fail_function(message) {
			alert('Erro! Falha na atualização do contrato.')
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/honorario/atualizar_contrato/",data,validate_function,success_function,fail_function)
	}



	$scope.alterar_contrato = function() {
		var data_paramters = $scope.get_data_from_form();
		//alert("veja os parametros: "+JSON.stringify(data_paramters))

		function validate_function(){
			if(data_paramters){
				if(data_paramters['tipo'] && data_paramters['nome'] && data_paramters['valor'])
					return true
			}
			alert("Preencha os campos obrigatórios!")
			return false;
		}

		function success_function(message) {
			$scope.registro_selecionado.contrato = message.fields
			$scope.registro_selecionado.plano = $('#plano option[value=' + message.fields.plano + ']').text();
			$scope.$apply()
			resetar_formulario()
		}
		function fail_function(message) {
			return notify('error','Falha na Operação',message);
		}

		request_api("/api/honorario/alterar_contrato",data_paramters,validate_function,success_function,fail_function)
	}

	$scope.get_data_from_form = function(){
		var tipo = $('#tipo option:selected').val().toUpperCase()
		var nome = $('#nome').val().toUpperCase()
		var descricao = $('#descricao').val().toUpperCase()
		var valor = $('#valor').val()
		valor = valor.replace("R$ ","").replace(".","").replace(",",".")
		valor = parseFloat(valor)

		var data = {
			tipo: tipo,
			nome:nome,
			valor:valor,
			descricao:descricao
		}
		return data
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
			$scope.apply();
	}

	$scope.desmarcar_linha_selecionada = function(){
			$scope.registro_selecionado.selecionado = "";
			$scope.registro_selecionado = null;
			$scope.opcao_desabilitada = "desabilitado";
			//$scope.apply();
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

	$scope.load_fields = function(){
		var plano = $scope.registro_selecionado.plano_id
		//var tipo_cliente = $scope.registro_selecionado.contrato.tipo_cliente
		//alert("plano:		"+plano);
		//alert("plano:		"+JSON.stringify($scope.registro_selecionado));
		//$scope.registro_selecionado;
		//$scope.esta_adicionando = true;

		if(plano){
			$("#plano").val(plano).change();
			//$('#plano option[value=3]').prop('selected','selected');
			//$('#plano').find('option:selected').text(plano)
		}
		else{
			$('#plano option:first').prop('selected','selected');
		}
	}

	$scope.load_clientes = function () {
		//alert("vindo aqui")
		$.ajax({
			type: 'GET',
			url: "/api/honorario/clientes/" + $scope.registro_selecionado.cliente_id,

			success: function (data) {
				//alert("VEJA A RESPOSTA: "+JSON.stringify(data))
				$scope.registro_selecionado.clientes = JSON.parse(data);
				$scope.$apply();
				//alert("VEJA O QUE TEMOS NAS INDICACOES: "+$scope.registro_selecionado.indicacoes[0].cliente_id)
			},
			failure: function (data) {
				$scope.clientes = [];
				$scope.desabilitar = 'link_desabilitado'
				alert("Não foi possivel carregar a lista de indicacoes")
			}
		});
	}

	$scope.selecionar_linha_indicacao = function(indicacao){
		if ($scope.indicacao_selecionada !==  null){
			if($scope.indicacao_selecionada == indicacao){
				$scope.desmarcar_linha_indicacao();
			}
			else{
				$scope.desmarcar_linha_indicacao();
				indicacao.selecionado = 'selected';
				$scope.indicacao_selecionada = indicacao;
				$scope.esta_indicando = true
				$scope.carregar_indicacao_selecionada();
			}
		}
		else{
			indicacao.selecionado = 'selected';
			$scope.indicacao_selecionada = indicacao;
			$scope.esta_indicando = true;
			$scope.carregar_indicacao_selecionada();
		}
		//alert(JSON.stringify($scope.indicacao_selecionada))
		$scope.apply();
	}

	$scope.desmarcar_linha_indicacao = function () {
		$('#taxa_desconto_indicacao').val('')
		$('#indicacao').val('')
		$scope.indicacao_selecionada.selecionado = "";
		$scope.indicacao_selecionada = null;
		$scope.esta_indicando = false
	}

	$scope.incrementar_desconto_fidelidade = function(valor){
		$scope.total_desconto_fidelidade = $scope.total_desconto_fidelidade + parseFloat(valor)
		$scope.$apply();
	}

	$scope.decrementar_desconto_fidelidade = function(valor){
		$scope.total_desconto_fidelidade = $scope.total_desconto_fidelidade - parseFloat(valor)
		$scope.$apply();
	}

	$scope.carregar_indicacao_selecionada = function(){
		var indica = $scope.indicacao_selecionada.indicacao_id
		$('#taxa_desconto_indicacao').val($scope.indicacao_selecionada.taxa_desconto)
		$('#indicacao').val(indica)
	}

	$scope.carregar_servicos_contratados = function(){
		$scope.servicos_carregados = false;
		$.ajax({
			type: "GET",
				url: "/api/honorario/carregar_servicos_contratados/"+$scope.registro_selecionado.cliente_id+"/"+$scope.registro_selecionado.plano_id,

				success: function (data) {
					$scope.servicos_contratados = JSON.parse(data);//Object.keys(data).map(function(_) { return data[_]; }) //_(data).toArray();
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
		//alert("VEJA SO: "+JSON.stringify(registro))
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
			//alert("VAMOS ATIVAR O SUJEITO "+registro.id)
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
		$scope.atualizar_servicos_contratados()
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
		request_api("/api/honorario/atualizar_servicos/",data,validate_function,success_function,fail_function)
	}

	$scope.alterar_indicacao = function () {
		var empresa = $('#indicacao').val()
		var empresa_nome = $('#indicacao option:selected').text()
		var taxa_desconto = $('#taxa_desconto_indicacao').val()
		var cliente_id = $scope.registro_selecionado.cliente_id

		var data = {
			empresa : empresa,
			empresa_nome : empresa_nome,
			taxa_desconto : taxa_desconto,
			cliente_id : cliente_id
		}

		function validate_function () {
			if(taxa_desconto==''){
				alert('Erro! Taxa de desconto precisa ser informado')
				return false
			}
			return true
		}

		function success_function(message) {
			$scope.decrementar_desconto_fidelidade($scope.indicacao_selecionada.taxa_desconto)
			$scope.incrementar_desconto_fidelidade(taxa_desconto)
			$scope.indicacao_selecionada.taxa_desconto = taxa_desconto
			$scope.atualizar_contrato(cliente_id)
			$scope.$apply()
		}

		function fail_function() {
			alert("Erro! Falha na alteração da indicação.")
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/honorario/alterar_indicacao/",data,validate_function,success_function,fail_function)

	}

	$scope.ativar_desativar_indicacao = function () {

		var empresa = $('#indicacao').val()
		var cliente_id = $scope.registro_selecionado.cliente_id
		var status = $('#indicacao_ativa').val()

		var data = {
			empresa : empresa,
			indicacao_ativa : status
		}

		function validate_function () {
			return true
		}

		function success_function(message) {
			$scope.atualizar_contrato(cliente_id)
			alert("Veja o status: "+$scope.registro.indicacao.indicacao_ativa)
			//$scope.decrementar_desconto_fidelidade($scope.indicacao_selecionada.taxa_desconto)
			//$scope.incrementar_desconto_fidelidade(taxa_desconto)
			$scope.$apply()
		}

		function fail_function() {
			alert("Erro! Falha na alteração do estado da indicação.")
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/honorario/alterar_boolean_indicacao/",data,validate_function,success_function,fail_function)
	}

	$scope.deletar_indicacao = function () {
		var empresa = $('#indicacao').val()
		var cliente_id = $scope.registro_selecionado.cliente_id

		var data = {
			empresa : empresa,
			cliente_id : cliente_id
		}

		function validate_function () {
			return true
		}

		function success_function(message) {
			alert("Deletado o registro")
			$scope.carregar_indicacao()
			$scope.indicacao_selecionada = null
			$scope.$apply()
		}

		function fail_function() {
			alert("Não foi possivel deletar neste momento")
		}
		//request_api(url,data_paramters,validator_functions,success_function,fail_function){
		request_api("/api/honorario/deletar_indicacao/",data,validate_function,success_function,fail_function)

	}

}]);