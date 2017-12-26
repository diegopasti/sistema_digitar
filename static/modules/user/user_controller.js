/**
 * Created by diego on 05/05/2017.
 */
var application = angular.module('modules.user', []);

application.controller('reset_password_controller', function($scope) {


});

application.controller('change_password_controller', function($scope) {

  $scope.save_password = function () {
    var data_paramters = {
      old_password: $('#old_password').val(),
      password:  $('#password').val(),
      confirm_password: $('#confirm_password').val()
    };

    success_function = function(result,message,data_object,status){
    	alert("Operação realizada com Sucesso!"+"Senha de acesso redefinida.")
      $("#old_password").val("");
      $("#password").val("");
      $("#confirm_password").val("");
      return "/"
    };

    fail_function = function (result,message,data_object,status) {
      notify_response_message(message);
    };

  	alert("Ja chegando aqui amore:"+JSON.stringify(data_paramters))
    request_api("/api/user/change_password/",data_paramters,validate_form_change_password,success_function,fail_function)
  }


  $scope.save_email = function () {

  	var data_paramters = create_data_paramters('form_change_personal_info');

  	success_function = function(result,message,data_object,status){
			alert("Operação realizada com Sucesso")
			$scope.$apply()
  	}

  	fail_function = function() {
			alert('Não foi possível realizar operação')
  	}

		validate_function = function (){
  		if ( email_is_valid('email') && data_paramters['first_name'].length > 3 && data_paramters['last_name'].length > 3){
  			return true
			}else{
  			alert("Formulario com erros, não foi possiel realizar alteração")
			}
  	}


		request_api('/api/user/change_personal_info/',data_paramters,validate_function,success_function,fail_function)
  }
});

application.controller('register_controller', function($scope) {
	$scope.email = "";
	$scope.password = "";
	$scope.confirm_password = "";

	$scope.save_first_user = function () {
		alert("venho?")
		var data_paramters = create_data_paramters('form_register');
		alert("Olha o data:\n"+JSON.stringify(data_paramters))

		success_function = function(result,message,object,status){
			alert("olha no q deu:"+JSON.stringify(message))
			alert("resultado:"+result)
		}

		fail_function = function (result,message,data_object,status) {
			alert('n deu'+JSON.stringify(message)+"\n"+data_object)
		}

		validate_function = function () {
		 return true
		}
		//var base_controller = new BaseController();
		//base_controller.request("/api/provents/save",data_paramters,validate_function,success_function,fail_function);
		alert("Chegando")
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

    var data_paramters = {};
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
      notify_response_message(message);
    }
    request_api("/api/user/login/autentication",data_paramters,validate_form_login,success_function,fail_function)
  }

  $scope.reset_password = function () {
  	alert('eh aqui')
  	var data_paramters = {email: $("#email").val()}

  	var success_function = function success_function(result,message,data_object,status){
			success_notify("Operação realizada com Sucesso!","Verifique seu email, você receberá um email em instantes.")
			$("#email").val("")
			$('a[href="#login"]').tab('show');
    }

    var fail_function = function (result,message,data_object,status) {
      notify_response_message(message);
    }

    validate_function = function(){
			return email_is_valid("email");
		}
    request_api("/api/user/reset_password/",data_paramters,validate_function,success_function,fail_function)
  }
});

application.controller('users_controller', function($scope) {
	$scope.list_users = [];
	$scope.min_row_table = [1,1,1,1,1,1,1,1,1,1];
	$scope.loaded_users = false
	$scope.user_selected = null;

	/*Menus do Sistema com Label e ID*/
	$scope.list_menu_Cadastros = [
		{label: 'Entidades',id:'entidade'},
		{label:'Permissões',id:'permissoes'},
		{label:'Grupos Mercadológicos',id:'grupos_mercadologicos'},
		{label:'Produtos', id:'produtos'},
		{label:'Vinculos de Produtos',id:'vinculos_de_produtos'},
		{label:'Agenda Telefônica',id:'agenda_telefonica'},
		{label:'Tabelas Auxíliares',id:'tabelas_auxiliares'}
		];

	$scope.list_menu_Compras = [
		{label:'Pedido e Fornecedoras', id:'pedido_e_fornecedores'},
		{label:'Lista para Reposição',id:'lista_reposicao'},
		{label: 'Pedidos para Cotação', id:'pedidos_cotacao'},
		{label: 'Entrada de Mercadorias', id:'entrada_mercadorias'},
		{label: 'Aquisição de Serviços', id:'aquisicao_servicos'},
		{label: 'Corrigir Entrada', id:'corrigir_entrada'},
		{label: 'Devolução e Fornecedores', id:'devolucao_fornecedores'},
		{label: 'Manifesto e Recusa NF-e', id:'manifesto_recusa'},
		{label: 'Histórico de Compras', id:'historico_compras'}];

	$scope.list_menu_Vendas = [
		{label:'Manuntenção de Preços',id:'manuntencao_precos'},
		{label:'Terminal Caixa',id:'terminal_caixa'},
		{label:'Venda Balcão',id:'venda_balcao'},
		{label:'Tele-Vendas',id:'tele_vendas'},
		{label:'Carteira de Pedidos',id:'carteira_pedidos'},
		{label:'Faturamento',id:'faturamento'},
		{label:'Devolução de Vendas',id:'devolucao_vendas'},
		{label:'Histórioco de Vendas',id:'historico_vendas'}
		];

	$scope.list_menu_Servicos = [
		{label:'Grupo de Serviços',id:'grupo_servicos'},
		{label:'Cadastro de Serviço',id:'cadastro_servico'},
		{label:'Chamados Técnicos',id:'chamados_tecnicos'},
		{label:'Serviços de Locação',id:'servicos_locacao'},
		{label:'Serviços de Logística',id:'servicos_logistica'},
		{label:'Representação Comercial',id:'representacao_comercial'}
		];

	$scope.list_menu_Outras_operacoes = [
			{label:'Tranferências',id:'transferencias'},
	{label:'Ordem de Abastecimento',id:'ordem_abastecimento'},
	{label:'Desmembrametos',id:'desmembramentos'},
	{label:'Produção',id:'producao'},
	{label:'Digitação de Balanço',id:'digitacao_balanco'},
	{label:'Notas de Simples Remessa',id:'notas_simples_remessa'},
	{label:'Emissão de Notas Avulsas',id:'emissao_notas_avulsas'},
	{label:'Controle de Frota',id:'controle_frota'}];

	$scope.list_menu_Financas = [{label:'Programação Financeira',id:'programacao_financeira'},
		{label:'Lançamento de Guias',id:'lancamentos_guias'},
		{label:'Liberar Comissões',id:'liberar_comissoes'},
		{label:'Tesouraria',id:'tesouraria'},
		{label:'Vale para Funcionários',id:'vale_funcionarios'},
		{label:'Empréstimos e Vales',id:'emprestimo_vales'}
		];

	$scope.list_menu_Supervisao_vendas = [{label:'Locais Atendidos',id:'locais_atentidos'},
		{label:'Segmentos Atendidos',id:'segmentos_atendidos'},
		{label:'Carteiras de Venda',id:'carteiras_vendas'},
		{label:'Rota de Entrega',id:'rota_entrega'},
		{label:'Motivos de Devolução',id:'motivos_devolucao'},
		/*Duplicidade de Menu*/
		{label:'Liberar Comissões',id:'liberar_comissoes_2'},
		{label:'Análise de Vendas',id:'analise_vendas'}
		];

	$scope.list_menu_Gerencia = [
		{label:'Empresas do Grupo',id:'empresas_grupo'},
		{label:'Funcionários/Usuários',id:'funcinarios_usuarios'},
		{label:'Cadastros Gerências',id:'cadastro_gerencias'},
		{label:'Formas de Recebimento',id:'formas_recebimento'},
		{label:'Plano de Contas',id:'plano_contas'},
		{label:'Contratos',id:'contratos'},
		{label:'Análises Gerenciais',id:'analise_gerencial'},
		{label:'Histórico de Produtos',id:'hitorico_produtos'},
		{label:'Altrações Manuais',id:'alteracoes_manuais'}];

	$scope.list_menu_Contabil = [{label:'Configurações Fiscais',id:'configuracoes_fiscais'},
		{label:'Modelo de Documento',id:'modelo_documento'},
		{label:'Tributação Produtos',id:'tributacao_produtos'},
		{label:'Gerar Arquivos Governo',id:'gerar_arq_governo'},
		{label:'Ánalise Tributária',id:'analise_tributaria'},
		{label:'Planilha Sub. Tributária',id:'planilha_sub_tributaria'}];

	/*Lista com todos Menus*/
	$scope.lista_all_menus = {
		registration : $scope.list_menu_Cadastros ,
		purchases : $scope.list_menu_Compras,
		sales : $scope.list_menu_Vendas,
		services : $scope.list_menu_Servicos,
		finances : $scope.list_menu_Financas,
		supervision : $scope.list_menu_Supervisao_vendas,
		management : $scope.list_menu_Gerencia,
		contabil : $scope.list_menu_Contabil,
		others : $scope.list_menu_Outras_operacoes
	};


  $scope.filter_users = function(){
  	$.ajax({
      type: 'GET',
      url: "/api/user/users/filter",

      success: function (data) {
				data = JSON.parse(data);
				$scope.list_users = data['object'];
        $("#loading_tbody").fadeOut();
        $scope.loaded_users = true
        $scope.$apply();
      },

      failure: function (data) {
      	$scope.loaded_users = true
        alert("Não foi possivel carregar a lista")
      }
    })
	};

	$scope.select_user = function(user){
    if ($scope.user_selected !==  null){
      if($scope.user_selected == user){
        $scope.unselect_row();
      }
      else{
        $scope.unselect_row();
        $scope.select_row(user);
      }
    }
    else{
      $scope.select_row(user);
    }
    $scope.$apply();
  };

  $scope.select_row = function (user) {
  	$scope.user_selected = user;
		$scope.user_selected.selected = 'selected';
		$scope.load_permissions();
  };

  $scope.unselect_row = function () {
		$scope.user_selected.selected = '';
		$scope.user_selected.permissions = null;
    $scope.user_selected = null;
  };

  $scope.load_permissions = function () {
  	$.ajax({
				type: 'GET',
				url: "/api/user/load/permissions/" + $scope.user_selected.id + "/",
			success: function (data) {
					var dict = JSON.parse(data);
					var list_respost = JSON.parse(dict["data-object"]);
					list_respost =list_respost[0]['fields'];
					$scope.user_selected.permissions = list_respost;
					$scope.complete_menus(list_respost);
					$scope.$apply()
				},

				failure: function () {
					alert("Não foi possivel carregar a lista")
				}
			})

	};

  $scope.complete_menus = function (list_respost) {
		for (var i in list_respost){
			var aux = list_respost[i].split(';');
			for (var j = 0; j <$scope.lista_all_menus[i].length;j++){
				select_rating($scope.lista_all_menus[i][j].id,parseInt(aux[j]))
			}
		}
	};

	$scope.save_permission = function () {
		$scope.user_selected = angular.element(document.getElementById('administration_users_controller')).scope().user_selected;
		var menus = {};

		/*Cria dicionario de menus com as strings*/
		for (var i in $scope.lista_all_menus) {
			var monta_str = '';
			for (var k in $scope.lista_all_menus[i]) {
				monta_str += get_value($scope.lista_all_menus[i][k].id) + ";"
			}
			monta_str = monta_str.substr(0, monta_str.length - 1); //remove o ultimo ';'
			menus[i] = monta_str
		}

		//menus.registration = '4;5;5;3;4;5;0;1'
		if (!(JSON.stringify(menus) === (JSON.stringify($scope.user_selected.permissions)))) {
			alert("OLHA+"+$scope.user_selected.id);
			var data_paramters = {
				id_user: $scope.user_selected.id,
				registration: menus.registration,
				sales: menus.sales,
				purchases: menus.purchases,
				services: menus.services,
				finances: menus.finances,
				supervision: menus.supervision,
				management: menus.management,
				contabil: menus.contabil,
				others: menus.others
			};
			success_function = function () {
				notify('success','Operação concluida','Autonomias salvas com sucesso')
				$scope.lista_buscada = menus
			};
			fail_function = function () {
				notify("error","Erro ao tentar forçar entradas","Favor preencher o formulario com selecionando as estrelas")
			};
			validate_function = function () {
				return validate_permission(menus)
			};
			alert("INDO TENTAR:"+JSON.stringify(data_paramters));
			request_api("/api/user/save/permissions/", data_paramters, validate_function, success_function, fail_function)
		}
		else{
			notify("error","Sem alterações","No momento a ação não pode ser concluida.\nFavor tentar mais tarde ")
		}
		$scope.user_selected.permissions = menus;
	};


});