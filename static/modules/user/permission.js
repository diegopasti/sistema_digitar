/**
 * Created by lucas on 17/11/2017.
 */
function validate_permission (dict){
	for (var string_menu in dict){
		var list_permissions = dict[string_menu].replace(/;/g,'');
		if (!(menus_is_numeric_limits(list_permissions))){
			return error_notify(string_menu,"Campo com conteudo imprópio","Preencha os campos selecionando as estrelas")
		}
	}
	alert("vou retornar true")
	return true
}

function menus_is_numeric_limits(list) {
	for (var item in list){
		var aux = parseInt(list[item]);
		if ((aux < 0) || (aux > 5)){
			return false
		}
	}
	return true
}