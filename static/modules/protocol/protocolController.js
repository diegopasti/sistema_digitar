app.controller('protocolController', ['$scope', '$filter', function($scope,$filter) {
  $scope.registro_selecionado = null;
  $scope.registro_confirmado = false;

  $scope.selecionar_registro = function(linha, confirmado){
    $scope.registro_selecionado = linha;
    if(confirmado.indexOf('SIM')!=-1){
      $scope.registro_confirmado = true;
    }
    else{
      $scope.registro_confirmado = false;
    }
    $scope.$apply();
  }

  $scope.desmarcar_registro = function(){
    $scope.registro_selecionado = null;
    $scope.$apply();
  }
}]);