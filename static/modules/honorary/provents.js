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

