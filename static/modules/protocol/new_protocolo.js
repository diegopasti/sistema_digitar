$(".desabilitado").click(function (e) {
    alert("opa.. tem que prevenir isso aqui..");
    e.preventDefault();
    return false;
});

function substituir_valor_nulo(valor){
    if (valor == null){ valor = ""; }
    return valor;
}

function reset_dados_modal(){
    $("#modal_documento").val("");
    $("#modal_complemento").val("");
    $("#modal_referencia").val("");
    $("#modal_vencimento").val("");
    $("#modal_valor").val("");
}

function fechar_modal(id){
    $("#"+id).modal('hide');
    $('.modal-backdrop').hide();
}

function abrir_modal(id){
    $("#"+id).modal('show');
    $('.modal-backdrop').show();
}

function verificar_campo_vazio(){ // Verifica se o campo documento esta vazio.
    var documento = $("#modal_documento").val();
    if (documento != ""){
        //$("#bt_adicionar_item").removeClass("desabilitado");
        return true;
    }

    else{
        //$("#bt_adicionar_item").addClass("desabilitado");
        return false;
    }
}

function validar_novo_documento(event){  // Verifica se os campos vencimentos e referencia estao em branco ou se são validos.
    if (validar_data_vencimento() && validar_referencia() && verificar_campo_vazio() && validar_complemento()){
        $("#bt_adicionar_item").removeClass("desabilitado");
        return true;
    }
    else{
        $("#bt_adicionar_item").addClass("desabilitado");
        return false;

    }
}

function validar_data_vencimento(){
    var valor = $("#modal_vencimento").val();

    if (valor == "" || valor=="__/__/____"){
        if (verificar_campo_vazio()){
            //$("#bt_adicionar_item").removeClass("desabilitado");
            return true;
        }
        else{
            //$("#bt_adicionar_item").addClass("desabilitado");
            return false;
        }

    }
    else{
        var patternValidaData = /^(((0[1-9]|[12][0-9]|3[01])([-.\/])(0[13578]|10|12)([-.\/])(\d{4}))|(([0][1-9]|[12][0-9]|30)([-.\/])(0[469]|11)([-.\/])(\d{4}))|((0[1-9]|1[0-9]|2[0-8])([-.\/])(02)([-.\/])(\d{4}))|((29)(\.|-|\/)(02)([-.\/])([02468][048]00))|((29)([-.\/])(02)([-.\/])([13579][26]00))|((29)([-.\/])(02)([-.\/])([0-9][0-9][0][48]))|((29)([-.\/])(02)([-.\/])([0-9][0-9][2468][048]))|((29)([-.\/])(02)([-.\/])([0-9][0-9][13579][26])))$/;
        if(!patternValidaData.test(valor)) {
            alert("Erro! Verifique se a data de vencimento foi digitada corretamente.");
            //$("#bt_adicionar_item").addClass("desabilitado");
            return false;
        }
        else{
            return true;
        }
    }
}

function validar_complemento() {
    var complemento = $("#modal_complemento").val();
    var documento = $("#modal_documento").val();
    var total = complemento.length + documento.length;

    if (total <= 65){
        return true;
    }
    else{
        alert("Atenção! Nome de documento e complemento devem possuir \njuntos no máximo 65 caractéres."+total+" caractéres informado.");
        return false;
    }

}

/* Valida se a data passada como parâmetro está dentro do período informado */
function validar_referencia() {
    var valor = $("#modal_referencia").val();

    if (valor == "" || valor=="__/____" || valor=="____/____"){
        return true
    }
    else{
        var mes_ano_atual = new Date();
        var arrayData = $('#modal_referencia').val().split('/');

        if (arrayData[0].length == 2){
            var mes = parseInt(arrayData[0]);
            if (mes > 0 && mes <= 12) {
                return true;
            }
            else {
                alert("Erro! Verifique se o Mês de Referencia foi digitado corretamente.");
                return false;
            }
        }

        else if (arrayData[0].length == 4){
            //alert("E um ano")
            return true;
        }

        else{
            alert("Erro! Verifique se o Mês de Referencia foi digitado corretamente.");
            return false;
        }

        //var dia = 1;
        //var mes = parseInt(arrayData[0]);
        //var ano = parseInt(arrayData[1]);

        /*if (mes > 0 && mes <= 12){
            return true;
            //alert("Mes valido"+mes);
            //*var dataUsuario = new Date();
            //dataUsuario.setDate(dia);
            //dataUsuario.setMonth(mes -1);
            //dataUsuario.setFullYear(ano);
            //if (dataUsuario.getTime() > mes_ano_atual.getTime()) {
            //    alert("Erro! Não é possivel adicionar documento referente à períodos futuros.");
                //$("#bt_adicionar_item").addClass("desabilitado");
            //    return false;
            //}
            //else{
            //    return true;
            //}
        }

        else {
            alert("Erro! Verifique se o Mês de Referencia foi digitado corretamente.");
            return false;
        }*/
    }
}


function conferir_destinatario(){
    var cliente = $("#select_destinatarios").val().split('-')[0];
    if (cliente != "" && cliente.indexOf("#") == -1){
        $('#modal_informacoes_complementares').modal('show');
        $("#bt_open_painel_informacoes_complementares").removeClass("desabilitado");

        var identificacao = angular.element(document.getElementById('controle_angular')).scope().complemento_identificacao;
        var contato = angular.element(document.getElementById('controle_angular')).scope().complemento_contato;
        var endereco = angular.element(document.getElementById('controle_angular')).scope().complemento_endereco;

        if (identificacao.length == 0 && contato.length == 0 && endereco.length == 0){
            angular.element(document.getElementById('controle_angular')).scope().limpar_informacoes_complementares();
        }
        else{
            var identificacao = angular.element(document.getElementById('controle_angular')).scope().complemento_identificacao;
            var contato = angular.element(document.getElementById('controle_angular')).scope().complemento_contato;
            var endereco = angular.element(document.getElementById('controle_angular')).scope().complemento_endereco;

            $("#complemento_contato").val(contato);
            $("#complemento_endereco").val(endereco);
            $("#complemento_identificacao").val(identificacao);
        }
    }
    else{
        if($("#select_destinatarios").val().length > 0){
            $("#bt_open_painel_informacoes_complementares").addClass("desabilitado");
        }

    }
}

function formatar_cpf_cnpj_simples(){
    var texto = $("#complemento_identificacao").val();
    if (texto.length != 0){
        if (texto.length == 11){
            if (valida_cpf(texto) == false){
                alert("Atenção! Verifique se CPF informado está correto.");
            }
        }

        else{
            if (valida_cnpj(texto) == false){
                alert("Atenção! Verifique se CNPJ informado está correto.");
            }
        }
    }
}

function filter_numbers(event) {
    var key_code = event.which || event.keyCode;
    //alert("olha se tem ponto:"+key_code);

    if (event.keyCode == 190){
        event.preventDefault();
    }

    if ($.inArray(event.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
         // Allow: Ctrl+A => (event.keyCode == 65 && e.ctrlKey === true) ||

         // Allow: Ctrl+C => (event.keyCode == 67 && e.ctrlKey === true) ||
         // Allow: Ctrl+X =>(event.keyCode == 88 && e.ctrlKey === true) ||
         // Allow: home, end, left, right
        (event.keyCode >= 35 && event.keyCode <= 39)) {
             // let it happen, don't do anything
             return;
    }
    // Ensure that it is a number and stop the keypress
    if ((event.shiftKey || (event.keyCode < 48 || event.keyCode > 57)) && (event.keyCode < 96 || event.keyCode > 105)) {
        event.preventDefault();
    }
}

function filter_cerquilha(event) {

    if (event.keyCode == 51 && event.shiftKey){
        event.preventDefault();
    }

    if (event.keyCode == 8 || event.keyCode == 32 || event.keyCode == 46){
        var cliente = $("#select_destinatarios").val();
        if (cliente.length <= 0){
            var identificacao = angular.element(document.getElementById('controle_angular')).scope().complemento_identificacao;
            var contato = angular.element(document.getElementById('controle_angular')).scope().complemento_contato;
            var endereco = angular.element(document.getElementById('controle_angular')).scope().complemento_endereco;

            if (identificacao.length != 0 || contato.length != 0 || endereco.length != 0){
                $("#bt_open_painel_informacoes_complementares").addClass("desabilitado");
                angular.element(document.getElementById('controle_angular')).scope().limpar_informacoes_complementares();
                alert("Atenção! Apagar o nome de destinatário irá apagar dados complementares, se houver.");
            }


        }

    }

    /*if ($.inArray(event.keyCode, [35]) !== -1 ||
         // Allow: Ctrl+A => (event.keyCode == 65 && e.ctrlKey === true) ||

         // Allow: Ctrl+C => (event.keyCode == 67 && e.ctrlKey === true) ||
         // Allow: Ctrl+X =>(event.keyCode == 88 && e.ctrlKey === true) ||
         // Allow: home, end, left, right
        (event.keyCode >= 35 && event.keyCode <= 39)) {
             // let it happen, don't do anything
             return;
    }
    // Ensure that it is a number and stop the keypress
    if ((event.shiftKey || (event.keyCode < 48 || event.keyCode > 57)) && (event.keyCode < 96 || event.keyCode > 105)) {
        event.preventDefault();
    }
    */
}

function verificar_dados_complementares() {
    abrir_modal("modal_informacoes_complementares");
    var identificacao = angular.element(document.getElementById('controle_angular')).scope().complemento_identificacao;
    var contato = angular.element(document.getElementById('controle_angular')).scope().complemento_contato;
    var endereco = angular.element(document.getElementById('controle_angular')).scope().complemento_endereco;

    $("#complemento_contato").val(contato);
    $("#complemento_endereco").val(endereco);
    $("#complemento_identificacao").val(identificacao);
}

function definir_tipo_referencia(){
    var opcao = $("#select_tipo_referencia").val();
    if(opcao == "mensal"){
        $("#modal_referencia").mask("99/9999");
    }
    else if (opcao == "anual"){
        $("#modal_referencia").mask("9999/9999");
    }

}