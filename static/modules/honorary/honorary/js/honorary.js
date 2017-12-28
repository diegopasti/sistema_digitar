function init(){
	angular.element(document.getElementById('controle_angular')).scope().load_objects();
	configurar_formulario_padrao()
}

function select_competence(){
	angular.element(document.getElementById('controle_angular')).scope().select_competence();
}

function post_screen_verified(){
	angular.element(document.getElementById('controle_angular')).scope().reajustar_tela();
}

function configurar_formulario_padrao(){


	var month_names = {0:'JAN',1:'FEV',2:'MAR',3:'ABR',4:'MAI',5:'JUN',6:'JUL',7:'AGO',8:'SET',9:'OUT',10:'NOV',11:'DEZ'}
	var current_month = new Date().getMonth();
	var year = new Date().getFullYear();
	var array = [current_month+3,current_month+2,current_month+1,current_month,current_month-1,current_month-2,current_month-3,"TODOS"];
	var selected = "";
	var selectList = document.getElementById("competence");
	for (var i = 0; i < array.length; i++) {
			var option = document.createElement("option");
			var item = "";

			if(array[i] > 11){
				item = month_names[array[i] - 12]+"/"+(year+1).toString();
			}
			else if(array[i] < 0){
				item = month_names[array[i] + 12]+"/"+(year-1).toString();
			}
			else if(array[i] == "TODOS"){
				item = "TODOS"
			}
			else{
				item = month_names[array[i]]+"/"+year.toString();
			}

			option.value = item;
			option.text = item;
			if(array[i] == current_month){
				selected = item
			}

			selectList.appendChild(option);
	}
	$("#competence").val(selected)
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
