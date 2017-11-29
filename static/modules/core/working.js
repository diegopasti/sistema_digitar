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
      //alert("Olha a data: "+JSON.stringify(data))
      new PNotify({
            title: "WorkingAPI was updated",
            addclass: 'visible',
            text: '',
            hide: true,
            delay: 2000,
            mouse_reset: false,
            type: 'success',
            styling: 'bootstrap3'
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
            text: texto,
            type: 'success',
            hide: true,
            delay: 2000,
            mouse_reset: false,
            styling: 'bootstrap3'
        });
      }
      else{
        alert("Erro! WorkingApi failed to register job.")
      }
    }

    /*success: function (data){
      $("#porcaria").html(data)
      alert(data)
      //var resultado = data;//$.parseJSON(data);

    },
    failure: function (data) {
      alert('Erro! Falha na execução do ajax');
    }*/
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

  /*$.ajax({
    type: "GET",
    url: "/api/working/register",
    data: {
      request_page: request_page,
    },
    success: function (data) {
      $("#porcaria").html = data;
    },
    failure: function (data) {
      alert("Erro! Configuration for WorkingApi not avaible.");
    }
  });
  */
}
