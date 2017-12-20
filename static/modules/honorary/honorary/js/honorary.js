function init(){
	//verify_screen_paramters();
	angular.element(document.getElementById('controle_angular')).scope().load_objects();
	configurar_formulario_padrao()
}

function select_competence(){
	angular.element(document.getElementById('controle_angular')).scope().select_competence()
}

function post_screen_verified(){
	angular.element(document.getElementById('controle_angular')).scope().reajustar_tela();
}

function configurar_formulario_padrao(){
	//$("#competence").val('2')
	//$("#tipos_proventos").val('C')
	//$("#valor").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
}

function resetar_formulario(){
	configurar_formulario_padrao()
	$("#nome").val('')
	$("#valor").val('')
	$("#descricao").val('')
}

function validate_justify(){
	set_wrong_field('action_justify', 'Campo Obrigatório')
	if(document.getElementById('action_justify').value != ''){
		clean_wrong_field('action_justify')
		return true;
	}
	else{
		set_wrong_field('action_justify', 'Campo Obrigatório')
		return false;
	}
}

$('.modal').on('hidden.bs.modal', function () {
	var modal_id = $(this).attr('id');
	var form = $("#"+modal_id+" form").attr('id');
	reset_formulary(form)
})
