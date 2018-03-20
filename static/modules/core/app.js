var app = angular.module('app', ['angularUtils.directives.dirPagination']);
app.controller('app.core.header_menu_controller', ['$scope', function($scope) {
	$scope.notifications = [];
	$scope.notifications_loaded = false;
	$scope.non_readed_notifications = 0;

	$scope.load_notifications = function () {
		$.ajax({
			type: 'GET',
			url: "/api/notifications/latest",

			success: function (data) {
				//alert("VEJA O RESULTADO: "+JSON.stringify(data))
				$scope.notifications = JSON.parse(data).object;
				$scope.$apply();
			},

			failure: function (data) {
				$scope.notifications = [];
				alert("Não foi possivel carregar a lista");
			},
		})
	}

	$scope.get_notifications_status = function () {
		$.ajax({
			type: 'GET',
			url: "/api/notifications/status",
			success: function (data) {
				//alert("VEJA O RESULTADO: "+JSON.stringify(data))
				$scope.notifications_status = JSON.parse(data).object;
				$scope.non_readed_notifications = $scope.notifications_status['non_readed_notifications'];
				$scope.$apply();
			},

			failure: function (data) {
				$scope.non_readed_notifications = 0;
				alert("Não foi possivel carregar a lista");
			},
		})
	}

	$scope.set_status_notification = function(registro){
		$scope.notifications[$scope.notifications.findIndex(x => x.id==registro.id)] = registro;
		$scope.$apply();
	}

	$scope.selecionar_linha = function(registro) {
		if(registro.module=='ENTITY'){
			window.open('/entidade/visualizar/'+registro.related_entity+'/#tab_servicos','_blank');
		}

		if(registro.module=='PROTOCOL'){
			window.open('/protocolo/visualizar/'+registro.related_object+'/','_blank');
			window.open('/protocolo/'+registro.related_object+'/','_blank');
		}
		$scope.confirm_notification(registro);
	}

	$scope.confirm_notification = function(registro){
		var user_id = $scope.ru;
		if (registro.related_users_readed == null || registro.related_users_readed.indexOf(user_id)==-1){
			var data_paramters = {};
			data_paramters['notification_id'] = registro.id;
			success_function = function(result,message,object,status){
				//success_notify("DEU CERTO",JSON.stringify(object))
				if(result == true){
					$scope.notifications[$scope.notifications.findIndex(x => x.id==registro.id)] = object;
				}

				var path_name = window.location.pathname;
				if(path_name.indexOf("/notifications")!=-1){
					angular.element(document.getElementById('controle_angular')).scope().confirm_notification(registro, user_id);
				}

				$scope.non_readed_notifications = $scope.non_readed_notifications - 1;
				$scope.$apply();
			}
			fail_function = function (result,message,data_object,status) {
				error_notify(null,'Falha na operação',message);
				//$scope.registro_selecionado = null;
				$scope.$apply();
			}
			validate_function = function () {return true;}
			request_api("/api/notification/confirm",data_paramters,validate_function,success_function,fail_function);
		}
	}
}]);

