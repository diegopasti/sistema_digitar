/*
    Campos desabilitados devem ter seu evento de clicd
*/
$(".disabled").click(function (e) {
	e.preventDefault();
	return false;
});

/*
    Desabilita/Habilita componente.
*/
function desabilitar(campo){
  $("#"+campo+ ' input').attr('disabled', true);
  $("#"+campo).addClass('desabilitado noselect');
}

function habilitar(campo){
  $("#"+campo+ ' input').attr('disabled', false);
  $("#"+campo).removeClass('desabilitado noselect');
}
/*
    Desabilita/Habilita fieldset container.
*/
function desabilitar_fieldset(campo){
    desabilitar_botao("#"+campo);
    //$("#lb_"+campo).addClass('label_desabilitado');
}

function habilitar_fieldset(campo){
    habilitar_botao("#"+campo);
    //$("#lb_"+campo).removeClass('label_desabilitado');
}

/*
    Desabilita/Habilita o input e o label de um determinado
    campo do formulario. O label so e desabilitado
    caso seu id seja o mesmo id do input acrescido
    de um prefixo "lb_".
*/
function desabilitar_campo(campo){
    desabilitar_botao("#"+campo);
    $("#lb_"+campo).addClass('label_desabilitado');
}

function habilitar_campo(campo){
    habilitar_botao("#"+campo);
    $("#lb_"+campo).removeClass('label_desabilitado');
}

/*
    Desabilita/Habilita um componente nav-tabs ou nav-pills
    sendo necessario informar o id da aba e o link para
    qual ela aponta, fazendo com que possamos desabilitar
    tambem o link do conteudo referenciado.
*/

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

/*
    Configurar mascara e componente calendario
    aos campos para digitação de datas.
*/
function configurar_campo_data(campo){
	$("#"+campo).datepicker({
		dayNames: [ "Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado" ],
		monthNames: [ "Janeiro", "Fevereiro", "março", "Abril", "Maio", "Junho", "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro" ],
		dayNamesMin: [ "D", "S", "T", "Q", "Q", "S", "S" ],
		dateFormat: 'dd/mm/yy'
	}).on('change', function() {
			$(this).valid();  // triggers the validation test
			// '$(this)' refers to '$("#datepicker")'
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

/*
    Configurar valor pre definido para um determinado campo.
    Quando o campo recebe o foco, o conteudo e limpado permitindo
    que o campo esteja pronto para a digitacao de outros valores.
    Ao perder o foco, se o conteudo digitado for diferente de vazio
    o conteudo e mantido, se nao o valor padrao e recolocado.
*/
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
  document.getElementById(id).focus();
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
