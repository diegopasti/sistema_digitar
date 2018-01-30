/**
 * Created by diego on 14/11/2017 - 14:42.
 */
var application = angular.module('modules.configurations', ['angularUtils.directives.dirPagination','filters']);
application.controller('configurations_controller', function ($scope) {
  	$scope.screen_height = window.innerHeight;
	$scope.screen_width  = window.innerWidth;
	$scope.screen_model = null;

	$scope.sortType           = 'codigo';
	$scope.sortReverse        = false;

	$scope.backups = null;
	$scope.loaded_backups = false;
	$scope.creating_backup = false;

	$scope.filter_by          = '0';
	$scope.filter_by_index    = parseInt($scope.filter_by);
	$scope.filter_by_options  = ['id','username','register'];
	$scope.search             = '';
	$scope.table_minimun_items = [1,2,3,4,5,6,7,8,9,10];

	$scope.load = function () {
    $.ajax({
      type: 'GET',
      //url: "/api/core/configurations/backup/backups",
      url: "/api/core/configurations/backup",

      success: function (data) {
        $scope.backups = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.loaded_backups = true;
        $scope.$apply();
        if ($scope.creating_backup==true){
          $.unblockUI();
          success_notify('Operação realizada com Sucesso','Backup gerado com sucesso.');
          $scope.creating_backup = false;
          $scope.$apply();
        }

      },

      failure: function () {
        $scope.loaded_backups = true;
        alert("Não foi possivel carregar a lista")
      }
    })
	};

	$scope.create_backup = function () {
    if (confirm('Este processo pode ser demorado, deseja prosseguir?')) {
      $.blockUI({ message: "<h1>Remote call in progress...</h1>" });
      $.blockUI({
        message: '<h1>Por favor aguarde...</h1><img src="http://127.0.0.1:8000/static/imagens/ajax-loader.gif" />',
        css: {
          border: 'none',
          padding: '15px',
          backgroundColor: '#000',
          '-webkit-border-radius': '10px',
          '-moz-border-radius': '10px',
          opacity: .5,
          color: '#fff'}
      });

      NProgress.start();
      var start_request = Date.now();
      $.ajax({
        type: 'GET',
        url: "/api/core/configurations/backup/create",

        success: function (data) {
          $scope.creating_backup = true;
          var response = JSON.parse(data);
          var item = response.object;
          if(response.result){
            //$scope.backups.splice(0, 0, item);
            $scope.$apply();
          }
          register_action(start_request, status);
          $scope.load_backups_informations()
          $scope.load()
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
    else{
      return false;
    }
	}

  $scope.create_backup_local = function () {
      if (confirm('Este processo pode ser demorado, deseja prosseguir?')) {
        $.blockUI({ message: "<h1>Remote call in progress...</h1>" });
        $.blockUI({
          message: '<h1>Por favor aguarde...</h1><img src="http://127.0.0.1:8000/static/imagens/ajax-loader.gif" />',
          css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'}
        });

        NProgress.start();
        var start_request = Date.now();
        $.ajax({
          type: 'GET',
          url: "/api/core/configurations/backup/local",

          success: function (data) {
            $scope.creating_backup = true;
            var response = JSON.parse(data);
            var item = response.object;
            if(response.result){
              //$scope.backups.splice(0, 0, item);
              $scope.$apply();
            }
            register_action(start_request, status);
            //$scope.load_backups_informations()
            $scope.load_system_informations()
            $scope.load()
            $.unblockUI();
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
      else{
        return false;
      }
  }


  $scope.load_system_informations = function(){
      $.ajax({
        type: 'GET',
        url: "/api/core/configurations/backup/system_info",

        success: function (data) {
          $scope.system_informations = JSON.parse(data).object;
          $("#loading_tbody").fadeOut();
          $scope.$apply();
        },

        failure: function () {
          alert("Não foi possivel carregar a lista")
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

	$scope.restore_backups = function(){
      $.blockUI({
        message: '<h1>Por favor aguarde...</h1><img src="http://127.0.0.1:8000/static/imagens/ajax-loader.gif" />',
        css: {
          border: 'none',
          padding: '15px',
          backgroundColor: '#000',
          '-webkit-border-radius': '10px',
          '-moz-border-radius': '10px',
          opacity: .5,
          color: '#fff'}
      });
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/backup/restore",

      success: function (data) {
        $scope.restore_backups_informations = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.load_backups_informations()
        $scope.load()
        $.unblockUI();
        success_notify('Operação realizada com Sucesso','Restauração concluída com sucesso.');
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
        $scope.shared_informations = JSON.parse(data).object;
        $("#loading_tbody").fadeOut();
        $scope.$apply();

      },

      failure: function () {
        alert("Não foi possivel carregar a lista")
      }
    })
	}

	$scope.manager_dropbox = function(){
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/backup/manager",

      success: function (data) {
        $scope.manager_informations = JSON.parse(data).object;
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
    $.blockUI({
        message: '<h1>Por favor aguarde...</h1><img src="http://127.0.0.1:8000/static/imagens/ajax-loader.gif" />',
        css: {
          border: 'none',
          padding: '15px',
          backgroundColor: '#000',
          '-webkit-border-radius': '10px',
          '-moz-border-radius': '10px',
          opacity: .5,
          color: '#fff'}
      });
    $.ajax({
      type: 'GET',
      url: "/api/core/configurations/version/update",

      success: function (data) {
        var response = JSON.parse(data)
        if(response.result == true){
          $.unblockUI();
          window.location = '/logout';
        }
        else{
          $.unblockUI();
          error_notify(null, 'Falha na operação', response.message)
        }
      },

      failure: function () {
        $.unblockUI();
          error_notify(null, 'Falha na operação', 'Atualização não pode ser concluída')
      }
    })
  }

  /* |<===============================================>| */
  /*             Contralor do operations
                   *  */

  $scope.loaded_operations = null;
  $scope.operations = null;

  $scope.load_operations = function() {

    $.ajax({
      type: 'GET',
      url: '/api/core/configurations/operations',

      success : function (data) {
        $scope.operations = JSON.parse(data).object;
        $scope.loaded_operations = true
        $scope.$apply()
			},

      failure: function () {
        notify('error','Erro!','Não foi possivel carregar operações')
			}
    });
  }

  $scope.reajustar_tela = function (){
		$scope.screen_height = SCREEN_PARAMTERS['screen_height'];
		$scope.screen_width  = SCREEN_PARAMTERS['screen_width'];
		$scope.screen_model  = SCREEN_PARAMTERS['screen_model'];

		$scope.table_maximun_items_per_page = SCREEN_PARAMTERS['table_maximun_items_per_page'];
		$scope.table_minimun_items          = SCREEN_PARAMTERS['table_minimun_items'];

		var extra_height = 0;
		if(SCREEN_PARAMTERS['table_maximun_items_per_page'] <= 5){
			extra_height = SCREEN_PARAMTERS['table_maximun_items_per_page']
		}
		else if(SCREEN_PARAMTERS['table_maximun_items_per_page'] <= 9){
			extra_height = 6;
		}
		else{
			extra_height = 7;
		}

		$scope.table_maximun_body_heigth = SCREEN_PARAMTERS['table_maximun_body_height']+extra_height;
		$scope.$apply();
	};

	$scope.select_filter_by = function (index) {
			$scope.filter_by_index = parseInt($scope.filter_by);
			$scope.apply();
	};

	$scope.get_filter_column = function(){
			var filtrar_pesquisa_por = $scope.filter_by_options[$scope.filter_by_index];
			switch (filtrar_pesquisa_por) {
				case 'username':
						return {username: $scope.search};
				case 'register':
						return {object_name: $scope.search};
				default:
					return {id : $scope.search}
			}
	};
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
