function configurar_formulario_padrao(){
	$("#tipo_cliente").val('PJ');
	$("#plano").val(1);
	$("#tipo_honorario").val('FIXO');
	$("#tipo_vencimento").val('MENSAL');
	$("#dia_vencimento").val('5');
	$("#tipo_honorario").val('VARIAVEL');
	configurar_campo_data('vigencia_inicio');
	configurar_campo_data('vigencia_fim');
	configurar_campo_data('data_vencimento');
	configurar_campo_data('desconto_inicio');
	configurar_campo_data('desconto_fim');
	$("#taxa_desconto_indicacao").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#desconto_temporario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
	$("#taxa_honorario").maskMoney({showSymbol:false, symbol:"R$", decimal:",", thousands:"."});
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
	if (tipo_vencimento == 'FIXO'){
		$('#valor_honorario').val('');
		$('#taxa_honorario').val('')
		habilitar('field_valor_honorario');
		desabilitar('field_taxa_honorario')
		$("#valor_total").val('');
	}
	else{
		$('#taxa_honorario').val('');
		$('#valor_honorario').val('');
		habilitar('field_taxa_honorario');
		desabilitar('field_valor_honorario')
		$("#valor_total").val('');
		calcular_honorario();
	}
}

function calcular_honorario(){
	var salario_vigente = angular.element(document.getElementById('controle_angular')).scope().salario_vigente;
	salario_vigente = Number(salario_vigente.replace('R$ ','').replace('.','').replace(',','.')); //975.3
	var multiplicador = $('#taxa_honorario').val().replace(',','.')
	if (multiplicador != ''){
		var valor_total = salario_vigente*(Number(multiplicador))
		valor_total = Math.round(valor_total*10000)/100.0;
		$('#valor_honorario').val(valor_total).trigger('mask.maskMoney');
	}
	else{
		//$('#taxa_honorario').val('1');
		$('#valor_honorario').val(salario_vigente*100).trigger('mask.maskMoney');
	}
}

function verificar_data_vigencia(){
	var data_fim = $('#vigencia_inicio').val();
	var data_fim = $('#vigencia_fim').val();
	var contract_is_active = false;

	if($('#vigencia_inicio').val()!="" && $('#vigencia_inicio').val()!="__/__/____"){
		var vigencia_inicio = new Date($('#vigencia_inicio').val());
		contract_is_active = true;
		clean_wrong_field('vigencia_inicio');
	}
	else{
		set_wrong_field('vigencia_inicio','Campo obrigatório.');
	}

	if($('#vigencia_fim').val()!="" && $('#vigencia_fim').val()!="__/__/____"){
		var vigencia_fim = new Date($('#vigencia_fim').val());
		if(vigencia_fim > vigencia_inicio){
			clean_wrong_field('vigencia_fim');
			contract_is_active = true;
		}
		else{
			set_wrong_field('vigencia_fim','Data de encerramento precisa ser posterior à data de inicio.');
			contract_is_active = false;
		}
	}
	else {
		clean_wrong_field('vigencia_fim');
	}
	return contract_is_active;
}


function initial_temporary_is_valid(){

}

function get_date_contract(field){
	if($('#'+field).val()!="" && $('#'+field).val()!="__/__/____"){
		var numbers = $('#'+field).val().split('/')
		var date = new Date(numbers[2], numbers[1]-1, numbers[0])
		return date;
	}
	else{
		return null;
	}
}

function verificar_vigencia_desconto(){
	var discount_have_initial_date = false;
	var discount_have_terminate_date = false;
	var can_apply_discount = true;
	var current_date = new Date();

	var data_inicio = get_date_contract('desconto_inicio');
	var data_fim = get_date_contract('desconto_fim');
	clean_wrong_field('desconto_inicio');
	clean_wrong_field('desconto_fim');
	if(data_inicio!=null){
		if(data_fim!=null){
			//alert("INI: "+data_inicio+" ---> FIM: "+data_fim);
			if(data_inicio!=data_fim){
				if(data_inicio<data_fim){
					if(current_date=>data_inicio){
						if(current_date<=data_fim){
							can_apply_discount = true;
						}
						else{
							can_apply_discount = false;
						}
					}
					else{
						//alert("INICIO EXISTE, TA ANTES DO FIM, NAO CHEGOU NA VIGENCIA");
						can_apply_discount = false;
					}
				}
				else{
					//alert("INICIO EXISTE, FIM TBM, MAS TA ERRADO O FIM ANTES DO INICIO");
					set_wrong_field('desconto_fim','Encerramento do desconto não pode ser igual ou antes da data início.')
					can_apply_discount = false;
				}
			}
			else{
				//alert("INICIO EXISTE, FIM TBM, MAS TA ERRADO SAO IGUAIS");
				set_wrong_field('desconto_fim','Data de encerramento e início não podem ser iguais.')
				can_apply_discount = false;
			}
		}
		else{
			if(current_date>data_inicio){
				//alert("INICIO EXISTE E NAO TEM FIM E ESTA DENTRO DA VIGENCIA")
				can_apply_discount = true;
			}
			else{
				//alert("INICIO EXISTE E NAO TEM FIM MAS NAO CHEGOU NA VIGENCIA");
				can_apply_discount = false;
			}
		}
	}
	else{
		if(data_fim!=null){
			if(current_date<=data_fim){
				//alert("NAO EXISTE INICIO MAS TEM FIM E ESTA DENTRO DA VIGENCIA")
				can_apply_discount = true;
			}
			else{
				//alert("NAO EXISTE INICIO, TEM FIM MAS JA PASSOU");
				can_apply_discount = false;
			}
		}
		else{
			//alert("NAO EXISTE INICIO NE FIM ENTAO PODE APLICAR")
			can_apply_discount = true;
		}
	}
	return can_apply_discount;
}