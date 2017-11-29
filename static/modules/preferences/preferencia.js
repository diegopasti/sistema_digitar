function validar_novo_salario(event){  // Verifica se os campos vencimentos e referencia estao em branco ou se são validos.
    if (validar_data_vencimento("inicio_vigencia") && validar_salario_vazio("salario_valor")){ // && validar_referencia() && verificar_campo_vazio() && validar_complemento()
        //$("#bt_adicionar_item").removeClass("desabilitado");
        return true;
    }
    else{
        //$("#bt_adicionar_item").addClass("desabilitado");
        //alert("viencia ou salario esta em branco")
        return false;
    }
}

function validar_salario_vazio(campo){
	var valor = $("#"+campo).val();
	if (valor == ""){
		alert("Erro! Valor do novo salário é um campo obrigatório.")
		$("#"+campo).focus();
		return false;
	}
	else{
		return true;
	}
}

function validar_data_vencimento(campo){
    var valor = $("#"+campo).val();
    if (valor == "" || valor=="__/__/____"){
		alert("Erro! Início da Vigência é um campo obrigatório.");
		$("#"+campo).focus();
		return false;
    }
    else{
        var patternValidaData = /^(((0[1-9]|[12][0-9]|3[01])([-.\/])(0[13578]|10|12)([-.\/])(\d{4}))|(([0][1-9]|[12][0-9]|30)([-.\/])(0[469]|11)([-.\/])(\d{4}))|((0[1-9]|1[0-9]|2[0-8])([-.\/])(02)([-.\/])(\d{4}))|((29)(\.|-|\/)(02)([-.\/])([02468][048]00))|((29)([-.\/])(02)([-.\/])([13579][26]00))|((29)([-.\/])(02)([-.\/])([0-9][0-9][0][48]))|((29)([-.\/])(02)([-.\/])([0-9][0-9][2468][048]))|((29)([-.\/])(02)([-.\/])([0-9][0-9][13579][26])))$/;
        if(!patternValidaData.test(valor)) {
            alert("Erro! Verifique se a data de vencimento foi digitada corretamente.");
            //$("#bt_adicionar_item").addClass("desabilitado");
			$("#"+campo).focus();
            return false;
        }
        else{
            return true;
        }
    }
}

function fechar_modal(id){
    $("#"+id).modal('hide');
    $('.modal-backdrop').hide();
}

function abrir_modal(id){
    $("#"+id).modal('show');
    $('.modal-backdrop').show();
}

function formatar_data(valor,padrao){
    if (padrao == "BR"){
        var data = valor.split("-");
        return data[2]+"/"+data[1]+"/"+data[0];
    }

    else {
        var data = valor.split("/");
        return data[2]+"-"+data[1]+"-"+data[0];
    }
}
