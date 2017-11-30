function validate_form_confirm_register(){
  return (email_is_valid("email"));
}

function validate_form_reset_password(){
  return (email_is_valid("email"));
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
	}

	var validator = new FormValidator();
	validator.texts = messages;
	validator.settings.alerts = true;
	result = validator.checkAll($('#form_change_password'));
	return true;//result.valid
}

function validate_form_login(){
  return (email_is_valid("email") && validate_password("password"));
}

function validate_form_register(){
  return (email_is_valid("email") && validate_password("password")) && compare_passwords("password","confirm_password");
}

function validate_password(senha){
  if (!is_empty(senha) && check_password_format(senha)){
    return true;
  }
  else{
    return error_notify("password","Senhas Insegura","Informe uma senha com ao menos 8 caracteres contendo letras e numeros.");
  }
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
	return email_is_valid("email")
}