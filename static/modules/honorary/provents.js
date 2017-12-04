function init(){
	angular.element(document.getElementById('controle_angular')).scope().load_provents();
	configurar_formulario_padrao()
	window.onresize = function(event){
		angular.element(document.getElementById('controle_angular')).scope().reajustar_tela();
	};
}

function configurar_formulario_padrao(){
	$("#tipos_proventos").val('C')
	$("#valor").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
}

function resetar_formulario(){
	configurar_formulario_padrao()
	$("#nome").val('')
	$("#valor").val('')
	$("#descricao").val('')
}

