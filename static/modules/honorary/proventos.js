function configurar_formulario_padrao(){
	$("#tipos_proventos").val('C')
	$("#valor").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	//$("#total").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});

	desabilitar('group_data_venvimento')
	desabilitar('group_taxa_honorario')
	desabilitar('group_total')



	//$("#group_data_venvimento").addClass('desabilitado')
}

function resetar_formulario(){
	configurar_formulario_padrao()
	$("#nome").val('')
	$("#valor").val('')
	$("#descricao").val('')
}

/*	Funções de eventos	*/
function verificar_tipo_vencimento () {
	var tipo_vencimento = $('#select_tipo_vencimento option:selected').val();
	if (tipo_vencimento == 'ANUAL'){
		$("#dia_vencimento").val('')
		desabilitar('group_dia_vencimento');
		habilitar('group_data_venvimento');
	}else{
		$("#dia_vencimento").val('5')
		$("#data_vencimento").val('')
		desabilitar('group_data_venvimento');
		habilitar('group_dia_vencimento')
	}
}

function calcular_honorario() {
	var salario_vigente = angular.element(document.getElementById('controle_angular')).scope().salario_vigente;
	salario_vigente = Number(salario_vigente.replace('R$ ','').replace('.','').replace(',','.')); //975.3
	var multiplicador = $('#taxa_honorario').val().replace(',','.')
	if (multiplicador != ''){
		var total = salario_vigente * (Number(multiplicador))
		total = Math.round(total*10000)/100.0;
		$('#valor_honorario').val(total).trigger('mask.maskMoney')
	}
}

function calcular_total (){
	var honorario = $('#valor_honorario').val();
	var desconto = $('#desconto_temporario').val();
	if (!(honorario == '')) {
		honorario = Number(honorario.replace(/\./g,'').replace(',','.'));
		desconto = Number(desconto.replace(',','.'));
		var total =honorario * (1 - (desconto/100))
		//total = Math.round(total *10000) / 100.0
		//total *= 100;
		$('#total').val(total)//.trigger('mask.maskMoney');
	}
}


/*	Funções de validar no final	*/
function verificar_data_vigencia(inicio, fim) {
	//alert('venho aqui?')
	var data_inicio = $('#' + inicio).val();
	var data_fim = $('#' + fim).val();
	var retorno = false
	if (!((data_inicio && data_fim) == ('__/__/____' || '') )) {
		var Compara01 = parseInt(data_inicio.split("/")[2].toString() + data_inicio.split("/")[1].toString() + data_inicio.split("/")[0].toString());
		var Compara02 = parseInt(data_fim.split("/")[2].toString() + data_fim.split("/")[1].toString() + data_fim.split("/")[0].toString());
		if (Compara01 < Compara02 || Compara01 == Compara02) {
			retorno = true;
		}
	}
	return retorno;
}


