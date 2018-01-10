function configurar_formulario_padrao(){
	$("#tipo_cliente").val('PJ');
	$("#plano").val(1);
	$("#tipo_honorario").val('FIXO');
	$("#tipo_vencimento").val('MENSAL');
	$("#dia_vencimento").val('5');
	configurar_campo_data('vigencia_inicio');
	configurar_campo_data('vigencia_fim');
	configurar_campo_data('data_vencimento');
	configurar_campo_data('desconto_inicio');
	configurar_campo_data('desconto_fim');
	$("#taxa_desconto_indicacao").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#desconto_temporario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#valor_honorario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#valor_total").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	desabilitar('field_data_venvimento');
	desabilitar('field_valor_honorario');
	desabilitar('field_valor_total');
}

$('#modal_adicionar_contrato').on('hidden.bs.modal', function () {
  reset_formulary('form_adicionar_contrato');
	configurar_formulario_padrao();
});

function verificar_tipo_vencimento () {
	var tipo_vencimento = $('#select_tipo_vencimento option:selected').val();
	if (tipo_vencimento == 'ANUAL'){
		$("#dia_vencimento").val('');
		desabilitar('field_dia_vencimento');
		habilitar('field_data_venvimento');
	}else{
		$("#dia_vencimento").val('5');
		$("#data_vencimento").val('');
		desabilitar('field_data_venvimento');
		habilitar('field_dia_vencimento');
	}
}

function verificar_tipo_honorario () {
	var tipo_vencimento = $('#select_tipo_honorario option:selected').val();
	if (tipo_vencimento == 'VARIAVEL'){
		$('#valor_honorario').val('');
		$('#taxa_honorario').val('1')
		habilitar('field_valor_honorario');
		$("#valor_total").val('');
	}
	else{
		$('#taxa_honorario').val('')
		desabilitar('field_valor_honorario')
		$("#valor_total").val('')
	}

}

function calcular_honorario() {
	var salario_vigente = angular.element(document.getElementById('controle_angular')).scope().salario_vigente;
	salario_vigente = Number(salario_vigente.replace('R$ ','').replace('.','').replace(',','.')); //975.3
	var multiplicador = $('#taxa_honorario').val().replace(',','.')
	if (multiplicador != ''){
		var valor_total = salario_vigente * (Number(multiplicador))
		valor_total = Math.round(valor_total*10000)/100.0;
		$('#valor_honorario').val(valor_total).trigger('mask.maskMoney')
	}
}

function verificar_data_vigencia() {
	var data_inicio = $('#vigencia_inicio').val();
	var data_fim = $('#vigencia_fim').val();
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
