$(".disabled").click(function (e) {
	e.preventDefault();
	return false;
});

function desabilitar(campo){
  $("#"+campo+ ' input').attr('disabled', true);
  $("#"+campo).addClass('desabilitado noselect');
}

function habilitar(campo){
  $("#"+campo+ ' input').attr('disabled', false);
  $("#"+campo).removeClass('desabilitado noselect');
}

function desabilitar_fieldset(campo){
	desabilitar_botao("#"+campo);
}

function habilitar_fieldset(campo){
  habilitar_botao("#"+campo);
}

function desabilitar_campo(campo){
    desabilitar_botao("#"+campo);
    $("#lb_"+campo).addClass('label_desabilitado');
}

function habilitar_campo(campo){
    habilitar_botao("#"+campo);
    $("#lb_"+campo).removeClass('label_desabilitado');
}

function habilitar_nav_page(tab,page){
    $(tab).removeClass('disabled')
    $(tab).find('a').attr('data-toggle','tab');
    $(tab).find('a').attr('href',page);
}

function desabilitar_nav_page(tab){
    $(tab).addClass('disabled')
    $(tab).find('a').removeAttr('data-toggle');
    $(tab).find('a').removeAttr('href');
}

function desabilitar_botao(botao_id){
	$(botao_id).prop("disabled", true);
}

function habilitar_botao(botao_id){
	$(botao_id).prop("disabled", false);
}

function configurar_campo_data(campo){
	$("#"+campo).datepicker({
		dayNames: [ "Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado" ],
		monthNames: [ "Janeiro", "Fevereiro", "março", "Abril", "Maio", "Junho", "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro" ],
		dayNamesMin: [ "D", "S", "T", "Q", "Q", "S", "S" ],
		dateFormat: 'dd/mm/yy'
		}).on('change', function() {
			$(this).valid();
	});
	$("#"+campo).mask("99/99/9999");
}

$('.decimal').keydown(function(e){
  // Allow: backspace, delete, tab, escape, enter and .
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
       // Allow: Ctrl/cmd+A
      (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
       // Allow: Ctrl/cmd+C
      (e.keyCode == 67 && (e.ctrlKey === true || e.metaKey === true)) ||
       // Allow: Ctrl/cmd+X
      (e.keyCode == 88 && (e.ctrlKey === true || e.metaKey === true)) ||
       // Allow: home, end, left, right
      (e.keyCode >= 35 && e.keyCode <= 39)) {
           // let it happen, don't do anything
           return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});

function configurar_valor_padrao(campo,valor) {
	if($('#' + campo).val() == ""){
		$('#' + campo).val(valor);
	}

	$('#' + campo).blur(function () {
		if ($('#' + campo).val() == "") {
			$('#' + campo).val(valor);
		}
	});

	$('#' + campo).focus(function () {
		if ($('#' + campo).val() == valor) {
			$('#' + campo).val("");
		}
	});
}


function notify(type,title,description){
	var width = ""
	if(type == "success"){
		width = '400px'
	}
	else if(type == "confirm"){
		width = '400px'
	}
	else{
		width = '400px'
	}

  new PNotify({
    title: title,
    text: description,
    width: width,
    hide: type=='confirm' ? false : true,
    delay: type=='error' ? 7000 : 7000,
    mouse_reset: false,
    type: type=='confirm' ? 'success' : type,
    styling: 'fontawesome',//'bootstrap3' // bootstrap3 ,
  });
  return (type=='error' ? false : true);
}

function confirm_notify(title,description){
  return notify("confirm",title,description);
}

function info_notify(title,description){
  return notify("info",title,description);
}

function success_notify(title,description){
  return notify("success",title,description);
}

function error_notify(id,title,description){
  if(id!=null){document.getElementById(id).focus();}
  return notify("error",title,description);
}

function warning_notify(id,titulo,descricao){
	if(id!=null){document.getElementById(id).focus();}
  return notify("warning",titulo,descricao);
}

function notificar(type,title,text){
	new PNotify({
		title: title,
		addclass: 'visible',
		text: text,
		hide: true,
		delay: 7000,
		mouse_reset: false,
		type: type,
		styling: 'bootstrap3'
	});
}

function marcar_campo_errado(campo){
	$("#"+campo).addClass('wrong_field')
}

function desmarcar_campo_errado(){
	$("#"+campo+" input").removeClass('wrong_field')
}