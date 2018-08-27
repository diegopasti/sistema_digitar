function init(){
	init_datatable();
}

function post_screen_verified(){
	//angular.element(document.getElementById('controle_angular')).scope().reajustar_tela();
}

function init_datatable(){
$('#datatable').DataTable({
	"pagingType": "simple_numbers",
	"lengthMenu": [[20, 100, -1], [20, 100, "All"]],
	"dom": '<"top">rt"<"rightcolumn"><"clear">p',
	"bSort": true,
	"ordering": true,
	"bAutoWidth": false,
	"columns": [
		{"sWidth": "20px"},
		{"sWidth": "120px"},
		{"sWidth": null},
		{"sWidth": null},
		{"sWidth": "110px"},
		{"sWidth": "110px"},
		{"sWidth": "110px", "type": "date-eu"}
	],
});

$('#datatable'+' tbody').on('click', 'tr', function () {
	var table = $('#datatable').DataTable();
	if ($(this).hasClass('selected')) {
		var id_cliente = table.cell('.selected', 0).data();
		$(this).removeClass('selected');
		angular.element(document.getElementById('controle_angular')).scope().desmarcar_registro();
		desabilitar("bt_consultar_cliente");
		desabilitar("bt_desativar_cliente");
		desabilitar("bt_outras_acoes");
	}
	else {
		table.$('tr.selected').removeClass('selected');
		$(this).addClass('selected');
		var id_cliente = table.cell('.selected', 0).data();
		habilitar('bt_consultar_cliente');
		habilitar('bt_desativar_cliente');
		habilitar('bt_outras_acoes');
		//document.getElementById("bt_consultar_cliente").href = "/entidade/visualizar/"+id_cliente;
		angular.element(document.getElementById('controle_angular')).scope().selecionar_registro(id_cliente);
	}

	$('#bt_excluir').click( function () {
		$.ajax({
		url: '/protocolo/documento/excluir/'+table.cell('.selected', 0).data(),
		type: 'get',
		success: function(data) {
			table.row('.selected').remove().draw( false );
			$('#bt_excluir').addClass('link_desabilitado');
			$('#bt_alterar').addClass('link_desabilitado');
		},
		failure: function(data) {
			alert('Erro! Falha na exclusão do registro');
		}
		});
	});
});
}

$("#nascimento_fundacao").datepicker({
	dayNames: [ "Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado" ],
	monthNames: [ "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro" ],
	dayNamesMin: [ "D", "S", "T", "Q", "Q", "S", "S" ],
	dateFormat: 'dd/mm/yy'
});