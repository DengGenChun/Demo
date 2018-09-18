$(function(){
	let logi_no = "";
	let logi_temp = "";
	let logi_sum = 0;

    getData();
    function getData(){

		var url = window.location.href;
		var paramsString = window.location.search;
		var re = RegExp(/(.+)?logi_no(.+)?/);
		var logi_d = '';
		if(re.test(paramsString)){
			paramsString  = paramsString.substring(1);//delete?
			paramsString  = paramsString.split("&");
			logi_no = paramsString[0];
			logi_no = logi_no.split("logi_no=");
			logi_no = logi_no[1];
			logi_d = document.getElementById("logi").innerHTML;
			logi_d = logi_d+logi_no;
			$("#logi").text(logi_d);
			loadOrder();
		}
		else{
			$("#content").prepend('<li class="first"><div class="aa"></div><img class="node-icon" src="images/red-icon.png"><span class="txt">等待商家发货</span></li>');
		}
	}

	function loadOrder() {

		$.ajax({
			url: '/api/sfquery',
			type: 'GET',
			dataType: 'json',
			async : true,//是否异步请求
			data: {
				"logi_no": logi_no
			},
			success: function(data) {
				if (data["code"] == 0) {

					logi_temp = data.msg;
					logi_sum = logi_temp.length;
					for (let i = 0; i<logi_sum; i++) {
						if(i!=(logi_sum-1)){
							
							$("#content").prepend('<li><img class="node-icon-grey" src="images/grey-icon.png"><span class="txt">'+logi_temp[i].remark+'</span><span class="time">'+logi_temp[i].accept_time+'</span></li>');
						}
						else{
							$("#content").prepend('<li class="first"><div class="aa"></div><img class="node-icon" src="images/red-icon.png"><span class="txt">'+logi_temp[i].remark+'</span><span class="time">'+logi_temp[i].accept_time+'</span></li>');
						}
					}
					

				}
				
				                   
			},
			error: function() {
				
			}
		});
	
	}

});
