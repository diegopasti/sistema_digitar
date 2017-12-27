function working_qunit(){
  var request_page = window.location.href;
  request_page = request_page.slice(request_page.indexOf("/test"));
  $.ajax({
    type: "GET",
    url: "http://localhost:8000/api/working/register/",
    data: {
      request_page: request_page,
    },

    complete : function(data) {
      new PNotify({
				title: "WorkingAPI was updated",
				addclass: 'visible',
				width: '350px',
				text: '',
				hide: true,
				delay: 3000,
				mouse_reset: false,
				type: 'success',
				styling: 'fontawesome',
			});
    }
  });
}

function working(){
  var request_page = window.location.href;
  $.ajax({
    type: "GET",
    url: "/api/working/register/",
    data: {
      request_page: request_page,
    },

    complete : function(data) {
      var resultado = $.parseJSON(data['responseText'])['success'];
      var data = $.parseJSON(data['responseText'])['data']
      var texto = "<sub>"+data.date+": "+data.user_name+" working on <a class='' href='"+data.task_url+"'>task#"+data.task_number+".</a></sub>"
      if(resultado == true){
        new PNotify({
            title: "WorkingAPI was updated",
            width: '350px',
            text: texto,
            type: 'success',
            hide: true,
            delay: 3000,
            mouse_reset: false,
            styling: 'fontawesome',
        });
      }
      else{
        alert("Erro! WorkingApi failed to register job.")
      }
    }
  });
}

function register(working_key,request_page){
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8010/api/work/register",
    data: {
      key: working_key,
      request_page: request_page,
    },
    success: function (data) {
      $("#porcaria").html = data;
    },
    failure: function (data) {
      $("#porcaria").html = "Cade?";
      alert("Erro! WorkingApi does not have this key registered.")
    }

  });
}