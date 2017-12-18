/**
 * Created by diego on 14/11/2017 - 14:42.
 */
var application = angular.module('modules.configurations', ['angularUtils.directives.dirPagination','filters']);
application.controller('configurations_controller', function ($scope) {

	$scope.backups = null;
	$scope.loaded_backups = false;
	$scope.load = function () {
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/backup",

      success: function (data) {
        $scope.backups = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.loaded_backups = true;
        $scope.$apply();

      },

      failure: function () {
        $scope.loaded_backups = true;
        alert("Não foi possivel carregar a lista")
      }
    })
	};

	$scope.create_backup = function () {
		NProgress.start();
		var start_request = Date.now();
		$.ajax({
      type: 'GET',
      url: "/api/core/configurations/backup/create",

      success: function (data) {
      	var response = JSON.parse(data);
      	var item = response.object;
      	if(response.result){
      		$scope.backups.splice(0, 0, item);
					$scope.$apply();
      	}
      	register_action(start_request, status);
      	$scope.load_backups_informations()

      	NProgress.done();
      },

      failure: function () {
      	alert("Não foi possivel carregar a lista");
        $scope.loaded_backups = true;
        register_action(start_request, status);
      	NProgress.done();
      }
    })
	}

	$scope.load_backups_informations = function(){
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/backup/info",

      success: function (data) {
        $scope.backups_informations = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.$apply();
      },

      failure: function () {
        alert("Não foi possivel carregar a lista")
      }
    })
	}

	$scope.shared_folder = function(){
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/backup/share",

      success: function (data) {
        $scope.shared = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.$apply();
      },

      failure: function () {
        alert("Não foi possivel carregar a lista")
      }
    })
	}

  $scope.load_version_informations = function(){
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/version/info",

      success: function (data) {
        $scope.version_informations = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.$apply();
      },

      failure: function () {
        alert("Não foi possivel carregar a lista")
      }
    })
  }

  $scope.update = function(){
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/version/update",

      success: function (data) {
        alert('FAÇO O UPDATE???')
        $scope.update = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.$apply();
      },

      failure: function () {
        alert("Não foi possivel carregar a lista")
      }
    })
  }
});

angular.module('filters', [])
	.filter('Filesize', function () {
		return function (size) {
			if (isNaN(size))
				size = 0;

			if (size < 1024)
				return size + ' Bytes';

			size /= 1024;

			if (size < 1024)
				return size.toFixed(2) + ' Kb';

			size /= 1024;

			if (size < 1024)
				return size.toFixed(2) + ' Mb';

			size /= 1024;

			if (size < 1024)
				return size.toFixed(2) + ' Gb';

			size /= 1024;

			return size.toFixed(2) + ' Tb';
		};
	});
