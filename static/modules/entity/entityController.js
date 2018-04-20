app.controller('entityController', ['$scope', '$filter', function($scope,$filter) {
  $scope.registro_selecionado = null;
  $scope.registro_selecionado_id = null;

  $scope.selecionar_registro = function(id){
    $scope.registro_selecionado = true;
    $scope.registro_selecionado_id = id;
    $scope.$apply();
  }

  $scope.desmarcar_registro = function(){
    $scope.registro_selecionado = null;
    $scope.registro_selecionado_id = null;
    $scope.$apply();
  }

  $scope.consultar_cliente = function(){
		if($scope.registro_selecionado!=null){
			window.open('/entidade/visualizar/'+$scope.registro_selecionado_id+'/', '_blank');
		}
	}

	$scope.adicionar_cliente = function(){
    window.open('/entidade/adicionar', '_blank');
	}
}]);