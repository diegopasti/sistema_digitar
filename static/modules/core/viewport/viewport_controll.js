var SCREEN_PARAMTERS = {};
SCREEN_PARAMTERS['screen_width']  = '';
SCREEN_PARAMTERS['screen_height'] = '';
SCREEN_PARAMTERS['screen_model']  = '';
SCREEN_PARAMTERS['table_maximun_items_per_page'] = '';
SCREEN_PARAMTERS['table_maximun_body_height'] = '';
SCREEN_PARAMTERS['table_minimun_items'] = '';

var SESSION_PARAMTERS = {};
SESSION_PARAMTERS['init_load_page']      = '';
SESSION_PARAMTERS['load_page_duration']  = '';
SESSION_PARAMTERS['setup_page_duration'] = '';

SESSION_PARAMTERS['external_ip'] = null;
SESSION_PARAMTERS['internal_ipv4'] = null;
SESSION_PARAMTERS['internal_ipv6'] = null;
SESSION_PARAMTERS['country_code'] = '';
SESSION_PARAMTERS['country_name'] = '';
SESSION_PARAMTERS['region_name'] = '';
SESSION_PARAMTERS['city'] = '';
SESSION_PARAMTERS['zip_code'] = '';
SESSION_PARAMTERS['time_zone'] = '';
SESSION_PARAMTERS['latitude'] = '';
SESSION_PARAMTERS['longitude'] = '';

function get_session_paramters_freegeoip(){
	// MAX QUERIES 15000 PER HOUR
	get_session_paramters_internal_ip();
	var url = 'http://freegeoip.net/json/';
	$.ajax({
    type: 'get',
    url: url,
    success: function(data) {
    	//alert("FREEGEOIP: "+JSON.stringify(data))
    	SESSION_PARAMTERS['external_ip'] = data.ip;
			SESSION_PARAMTERS['country_code'] = data.country_code.toUpperCase();
			SESSION_PARAMTERS['country_name'] = data.country_name.toUpperCase();
			SESSION_PARAMTERS['region_name'] = data.region_name.toUpperCase();
			SESSION_PARAMTERS['region_code'] = data.region_code.toUpperCase();
			SESSION_PARAMTERS['city'] = data.city.toUpperCase();
			SESSION_PARAMTERS['zip_code'] = data.zip_code;
			SESSION_PARAMTERS['time_zone'] = data.time_zone.toUpperCase();
			SESSION_PARAMTERS['latitude'] = data.latitude;
			SESSION_PARAMTERS['longitude'] = data.longitude;
			//alert("VEJA COMO FICOU O FREEGEOIP: "+JSON.stringify(SESSION_PARAMTERS))
    },
    failure: function(data){

    }
  });
}

function get_session_paramters_ip_api(){
	// MAX QUERIES 9000 POR HOUR
	get_session_paramters_internal_ip();
	var url = 'http://ip-api.com/json'
	$.ajax({
    type: 'get',
    url: url,
    success: function(data) {
			//alert("IP-API: "+JSON.stringify(data))
    	SESSION_PARAMTERS['external_ip'] = data.query;
			SESSION_PARAMTERS['country_code'] = data.countryCode.toUpperCase();
			SESSION_PARAMTERS['country_name'] = data.country.toUpperCase();
			SESSION_PARAMTERS['region_name'] = data.regionName.toUpperCase();
			SESSION_PARAMTERS['region_code'] = data.region.toUpperCase();
			SESSION_PARAMTERS['city'] = data.city.toUpperCase();
			SESSION_PARAMTERS['zip_code'] = data.zip;
			SESSION_PARAMTERS['time_zone'] = data.timezone.toUpperCase();
			SESSION_PARAMTERS['latitude'] = data.lat;
			SESSION_PARAMTERS['longitude'] = data.lon;
			//alert("VEJA COMO FICOU O IP-API: "+JSON.stringify(SESSION_PARAMTERS))
    },
    failure: function(data){

    }
  });
}

function get_session_paramters_internal_ip(){
	window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;   //compatibility for firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
    pc.createDataChannel("");    //create a bogus data channel
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);    // create offer and set local description
    pc.onicecandidate = function(ice){  //listen for candidate events
        if(!ice || !ice.candidate || !ice.candidate.candidate)  return;
        var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];
        //console.log('my IP: ', myIP);
				if (myIP.indexOf(":") >= 0){
					alert("IPv6: "+myIP);
					if (SESSION_PARAMTERS['internal_ipv6'] == null){
						SESSION_PARAMTERS['internal_ipv6'] = myIP;
					}
				}
				else if (myIP.indexOf(".") >= 0){
					//alert("IPv4: "+myIP)
					if (SESSION_PARAMTERS['internal_ipv4'] == null){
						SESSION_PARAMTERS['internal_ipv4'] = myIP;
					}
				}

        pc.onicecandidate = noop;
        //return myIP;
    };
}

function verify_session_paramters(){
	try{
		get_session_paramters_freegeoip();
	}
	catch(erro){
		get_session_paramters_ip_api();
	}
}

function report_session_paramters(){
	var url = '/api/user/session/register';
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  SESSION_PARAMTERS['csrfmiddlewaretoken'] = csrftoken;

	$.ajax({
    type: 'POST',
    url: url,
    data: SESSION_PARAMTERS,
    success: function(data) {
    	//alert("olha o que veio: "+JSON.stringify(data));
    },
    failure: function(data){
			//alert("Erro na hora de salvar a sessao");
    }
  });
}

function verify_screen_paramters(){
	screen_width = window.innerWidth;
	screen_height = window.innerHeight;
	SCREEN_PARAMTERS['screen_width'] = screen_width;
	SCREEN_PARAMTERS['screen_height'] = screen_height;

	/*
	$scope.S9 = false;  // Giant Screen:   1921 or more
	$scope.S8 = false;  // Larger Screen:  1680 ~ 1920
	$scope.S7 = false;  // Giant Screen:   1367 ~ 1680
	$scope.S6 = false;  // Larger Screen:  1025 ~ 1366
	$scope.S5 = false;  // Giant Screen:    801 ~ 1024
	$scope.S4 = false;  // Larger Screen:   641 ~ 800
	$scope.S3 = false;  // Large Screen:    481 ~ 640
	$scope.S2 = false;  // Medium Screen:   321 ~ 480
	$scope.S1 = false;  // Small Screen:    241 ~ 320
	$scope.S0 = false;  // Smaller Screen:    0 ~ 240
	*/

	if (screen_width <= 240){ SCREEN_PARAMTERS['screen_model'] = 0; }
	else if (screen_width <= 320){ SCREEN_PARAMTERS['screen_model'] = 1; }
	else if (screen_width <= 480){ SCREEN_PARAMTERS['screen_model'] = 2;	}
	else if (screen_width <= 640){SCREEN_PARAMTERS['screen_model'] = 3; }
	else if (screen_width <= 800){ SCREEN_PARAMTERS['screen_model'] = 4; }
	else if (screen_width <= 1024){ SCREEN_PARAMTERS['screen_model'] = 5; }
	else if (screen_width <= 1366){ SCREEN_PARAMTERS['screen_model'] = 6; }
	else if (screen_width <= 1680){ SCREEN_PARAMTERS['screen_model'] = 7; }
	else if (screen_width <= 1920){ SCREEN_PARAMTERS['screen_model'] = 8; }
	else{ SCREEN_PARAMTERS['screen_model'] = 9; }

	pagination_itens_per_page = parseInt((screen_height/26)-12);
	if (pagination_itens_per_page < 2){
		pagination_itens_per_page = 2;
	}
	pagination_itens_per_page = pagination_itens_per_page + 1
	table_minimal_rows = Array.apply(null, Array(pagination_itens_per_page)).map(function (x, i) { return i; });
	total_rows_height = pagination_itens_per_page*26;
	SCREEN_PARAMTERS['table_maximun_items_per_page'] = pagination_itens_per_page;
	SCREEN_PARAMTERS['table_maximun_body_height'] = total_rows_height;
	SCREEN_PARAMTERS['table_minimun_items'] = table_minimal_rows;
	try{
		post_screen_verified();
	}
	catch(err){
	}
}

function configure_screen(){
	if(SCREEN_PARAMTERS['screen_width'] < 600){
		$("#profile_email_active").hide();
	}
	else{
		$("#profile_email_active").show();
	}
}

function register_action(start_request, status_request){
	var terminate_request = Date.now();
	var duration_request = terminate_request - start_request
	duration_request = duration_request/1000

	try{
		document.getElementById('session_action_info').innerHTML = 'Requisição processado em '+duration_request+'ms.';
		$("#footer_session_action").fadeIn(100);
		setTimeout(function(){$("#footer_session_action").fadeOut(5000);},5000)
	}
	catch(err) {
	}
}

function load_images(){
	var allimages= document.getElementsByTagName('img');
  for (var i=0; i<allimages.length; i++) {
    if (allimages[i].getAttribute('data-src')) {
      allimages[i].setAttribute('src', allimages[i].getAttribute('data-src'));
    }
  }
}

function measureCRP() {
  var time = window.performance.timing;
  var time_dom_loading = time.domLoading;
  var complete = time.domComplete - time_dom_loading;
  var load_event_end = time.loadEventEnd  - time_dom_loading;
  SESSION_PARAMTERS['load_page_duration'] = complete;
	SESSION_PARAMTERS['setup_page_duration'] = load_event_end;
	SESSION_PARAMTERS['status_message'] = 'Página carregada em '+SESSION_PARAMTERS['load_page_duration']+'ms e finalizada em '+SESSION_PARAMTERS['setup_page_duration']+"ms.";
  document.getElementById('session_action_info').innerHTML = SESSION_PARAMTERS['status_message'];
	$("#footer_session_action").fadeIn(100);
	setTimeout(function(){$("#footer_session_action").fadeOut(5000);},8000)
}

$(".alert").fadeOut(8000);

window.onresize = function(event) {
	verify_screen_paramters();
	try{
		post_screen_verified();
	}
	catch(err){
	}
};

window.addEventListener("load", function(){
 setTimeout(function(){measureCRP();}, 0);
});
//verify_screen_paramters();
