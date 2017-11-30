/**
 * Created by diego on 05/05/2017.
 */
var application = angular.module('modules.user', []);

application.controller('reset_password_controller', function($scope) {

  $scope.reset_password = function () {
  	var data_paramters = {email: $scope.email}

  	var success_function = function success_function(result,message,data_object,status){
			success_notify("Operação realizada com Sucesso!","Verifique seu email, você receberá um email em instantes.")
    }

    var fail_function = function (result,message,data_object,status) {
      notify_response_message(message);
    }

    validate_function = function(){
			return email_is_valid("email")
		}
    request_api("/api/user/reset_password",data_paramters,validate_function,success_function,fail_function)
  }

  $scope.resend_activation_code = function () {
    var data_paramters = {email: $scope.email}

    var success_function = function success_function(result,message,data_object,status){
			success_notify("Operação realizada com Sucesso!","Verifique seu email, você receberá um email em instantes.")
    }

    var fail_function = function (result,message,data_object,status) {
    	notify_response_message(message);
    }

    validate_function = function(){
			return email_is_valid("email")
		}
    request_api("/api/user/reactivate",data_paramters,validate_function,success_function,fail_function)
  }
});

application.controller('change_password_controller', function($scope) {

  $scope.save_password = function () {
    var data_paramters = {
      old_password: $scope.old_password,
      password:  $scope.password,
      confirm_password:  $scope.confirm_password
    }

    success_function = function(result,message,data_object,status){
    	success_notify("Operação realizada com Sucesso!","Senha de acesso redefinida.")
      $("#old_password").val("")
      $("#password").val("")
      $("#confirm_password").val("")
      $scope.old_password = "";
      $scope.password = "";
      $scope.confirm_password = "";
    }

    fail_function = function (result,message,data_object,status) {
      notify_response_message(message);
    }

    request_api("/api/user/change_password",data_paramters,validate_form_change_password,success_function,fail_function)
  }
});

application.controller('register_controller', function($scope) {

  $scope.email = "";
  $scope.password = "";
  $scope.confirm_password = "";

  $scope.save_user = function () {

		var data_paramters = {};
  	$.each($('#form_register').serializeArray(), function(i, field) {
			data_paramters[field.name] = field.value;
		});

    success_function = function(result,message,data_object,status){
    	var redirect = "/register/confirm/"+$scope.email;
    	return redirect
    }

    fail_function = function (result,message,data_object,status) {
      notify_response_message(message);
    }
    request_api("/api/user/register/save",data_paramters,validate_form_register,success_function,fail_function)
  }

  $scope.resend_activation_code = function () {
  	var data_paramters = {email: $scope.email}

    var success_function = function success_function(result,message,data_object,status){
			success_notify("Operação realizada com Sucesso!","Verifique seu email, você receberá um email em instantes. <br><a href='/login'>Clique aqui para acessar sistema.</a>")
    }

    var fail_function = function (result,message,data_object,status) {
    	notify_response_message(message);
    }

    validate_function = function(){
    	return true;
		}

		alert("veja eh isso")
    request_api("/api/user/reactivate",data_paramters,validate_function,success_function,fail_function)
  }
});

application.controller('login_controller', function($scope) {

  $scope.login_autentication = function () {

  	SESSION_PARAMTERS['email'] = $scope.email
  	SESSION_PARAMTERS['password'] = $scope.password

    var data_paramters = SESSION_PARAMTERS//{email: $scope.email, password: $scope.password}

    function success_function(result,message,data_object,status){
    	//alert("VEJA O QUE VEIO: "+result+" - "+message+" - "+data_object+" - "+status.request_path)

    	var redirect = "/"
    	return redirect
    }

    fail_function = function (result,message,data_object,status) {
    	//alert("FALHA: "+result+" - "+message+" - "+data_object+" - "+status)
      notify_response_message(message);
    }

    request_api("/api/user/login/autentication",data_paramters,validate_form_login,success_function,fail_function)
  }
});

application.controller('users_controller', function($scope) {
	$scope.list_users = [];
	$scope.table_minimun_items_u = [1,1,1,1,1,1,1];
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

	$scope.save_new_user = function () {
		$('#password').val('1q2w3e4r')
		$('#confirm_password').val('1q2w3e4r')
		var data_paramters = {};
  	$.each($('#form-save-user').serializeArray(), function(i, field) {
  		alert("OLHA O VALOR:"+field.value)
			data_paramters[field.name] = field.value;
		});

		success_function = function(result,message,data_object,status){
    	notify('success','Email enviado','Conseguindo mandar esse email')
    }

    fail_function = function (result,message,data_object,status) {
      notify_response_message(message);
    }
    alert("Vou usar a API")
    request_api("/api/user/register/save",data_paramters,validade_new_user,success_function,fail_function)
  }

});
