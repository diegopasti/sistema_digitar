function validate_form_confirm_register(){
  return (email_is_valid("email"));
}

function validate_form_reset_password(){
  return (email_is_valid("email"));
}

function post_screen_verified(){
	angular.element(document.getElementById('controle_angular_cadastro_user')).scope().reajustar_tela();
}

function validate_form_change_password(){
  var messages = {
		invalid         : 'Informe numeros e letras!',
		short           : 'Informe pelo menos 8 caracteres!',
		long            : 'Informe no máximo x caracteres!',
		checked         : 'must be checked',
		empty           : 'Campo obrigatório!',
		select          : 'Please select an option',
		number_min      : 'too low',
		number_max      : 'too high',
		url             : 'invalid URL',
		number          : 'not a number',
		email           : 'email address is invalid',
		email_repeat    : 'emails do not match',
		date            : 'invalid date',
		time            : 'invalid time',
		password_repeat : 'Senhas não conferem!',
		no_match        : 'no match',
		complete        : 'input is not complete'
	};

	var validator = new FormValidator();
	validator.texts = messages;
	validator.settings.alerts = true;
	result = validator.checkAll($('#form_change_password'));
	return true;//result.valid
}

function validate_form_login(){
  	return ( validate_size("password",6));

}

function validate_form_register(){
	var retorno = (validate_size("username",6) & validate_size("password",6) & validate_size("confirm_password",6) &
		confirm_pass_valid("password","confirm_password") & validate_size("primeiro_nome",3)  & validate_size("sobrenome", 3)  & validate_email("")) ;
	return retorno
}

function validate_size (campo,tamanho_minimo){
	var retorno = ($('#'+campo+'').val().length >= tamanho_minimo)
	if (!retorno){
		alert('Dados inválidos no campo:'+campo)
	}
	return retorno
}

function validate_email(){
	var retorno = false;
	var email = $('#email').val()
	if (email.length > 0 && email != null){
		retorno =  email_is_valid('email')
	}
	return retorno;
}

function email_is_valid(id) {
  var filter = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
  if(!is_empty(id)){
    if(filter.test(document.getElementById(id).value)){
      return true;
    }
    else{
			alert("error"+" Email Inválido"+" Verifique se o email foi digitado corretamente.")
			return false
    }
  }
  else{
    return true;
  }
}

function is_empty(id){
  return (document.getElementById(id).value.length == 0 ? true : false)
}

function confirm_pass_valid(password, confirm_password){
	var pass = $('#'+password+'').val()
	var conf_pass =  $('#'+confirm_password+'').val()
	return (pass == conf_pass)
}

function check_password_format(senha){
  return ((contains_alpha(senha) && contains_numeric(senha) && contains_minimal_size(senha,8)) ? true : false);
}

function compare_passwords(id_senha, id_confirma_senha){
  var senha = document.getElementById(id_senha).value;
  var confirma_senha = document.getElementById(id_confirma_senha).value;
  return (senha === confirma_senha ? true : error_notify("confirm_password","Senhas não conferem","Verifique as senhas informadas."));
}

function validade_new_user(){
	return true
	//return email_is_valid("email")
}