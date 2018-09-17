$(function() {
	let params = {};
	let signTitle = "等待商家发货";
	let signTime = "";
	let username = "";
	let phone = "";
	let address = "";
	let isSign = false;
	let icon = "";
	let productTitle = "";
	let orderCount = 1;
	let productColor = "";
	let priceSum = 0.0;
	let comment = "";
	let orderNo = "";
	let orderTime = 0;
	let payTime = 0;
	let result = {};

	preLoad();
	load();


	function preLoad() {
		$("#gotoHome").click(function() {
			window.location.href = "https://h5.youzan.com/v2/home/X8JlT7pnsA?reft=1536918283669&spm=f71487166&sf=wx_menu";
		});
		orderNo = getQueryParameter("order_no");
	}
	function load() {
		loading();
		$.when(loadOrder())
			.done(function() {
				initEvent();
			})
			.fail(function(msg) {
				layer.alert(msg + ", 请重试");
			})
			.always(function() {
				cancelLoading();
			});
	}


	function getQueryParameter(key) {
		if (params[key]) {
			return params[key];
		}
		let url = window.location.search.substring(1);
		let kvs = url.split("&");
		for (let i = 0; i < kvs.length; i++) {
			let kv = kvs[i].split("=");
			params[kv[0]] = kv[1];
		}
		return params[key];
	}
	function loadOrder() {
		let $d = $.Deferred();
		$.ajax({
			url: '/api/listOrder',
			type: 'GET',
			dataType: 'json',
			data: {
				"order_no": orderNo,
			},
			success: function(data) {
				if (data["code"] == -1) {
					$d.reject(data["msg"]);
					return;
				}
				result = data["result"];
				loadOrderSuccess(data["result"]);
				loadWuliuSuccess(data["result"])
				$d.resolve("订单信息获取成功");
			},
			error: function() {
				$d.reject("订单信息获取失败");
			}
		});
		return $d.promise();
	}
	function loadOrderSuccess(res) {
		username = res["username"];
		phone = res["phone"];
		address = res["address"];
		icon = res["p_icon"];
		productTitle = res["p_title"];
		orderCount = res["p_count"];
		productColor = res["p_color"];
		priceSum = res["price_sum"];
		comment = res["comment"];
		orderNo = res["order_no"];
		orderTime = res["order_time"];
		payTime = res["pay_time"];

		$("div[for='username']").text(username);
		$("div[for='phone']").text(phone.substring(0, 3) + "****" + phone.substring(7, 11));
		$("div[for='address']").text(address);
		$("img[for='icon']").attr("src", icon);
		$("div[for='productTitle']").text(productTitle);
		$("div[for='orderCount']").text(orderCount);
		$("div[for='productColor']").text(productColor);
		$("div[for='priceSum']").text("￥" + priceSum);
		$("div[for='comment']").text(comment);
		$("div[for='orderNo']").text(orderNo);
		if (orderTime > 0) {
			$("div[for='orderTime']").text(formatDate(new Date(orderTime), "%Y-%M-%d %H:%m:%s"));
		}
		if (payTime > 0) {
			$("div[for='payTime']").text(formatDate(new Date(payTime), "%Y-%M-%d %H:%m:%s"));
		}
	}
	function loadWuliuSuccess(res) {
		signTitle = res["track_state"];
		signTime = res["sign_time"];
		isSign = res["is_sign"] == "YES" ? true : false;

		$("div[for='signTitle']").text(signTitle);
		if (signTime > 0) {
			$("div[for='signTime']").text(formatDate(new Date(signTime), "%Y-%M-%d %H:%m:%s"));
		} else {
			$("div[for='signTime']").css("padding-top", "0");
		}
		$("div[for='isSign']").text(isSign ? "已签收" : "未签收");
	}


	function formatDate(date, fmt) {
		function pad(value) {
			return (value.toString().length < 2) ? '0' + value : value;
		}
		return fmt.replace(/%([a-zA-Z])/g, function(_, fmtCode) {
			switch (fmtCode) {
				case 'Y':
					return date.getFullYear();
				case 'M':
					return pad(date.getMonth() + 1);
				case 'd':
					return pad(date.getDate());
				case 'H':
					return pad(date.getHours());
				case 'm':
					return pad(date.getMinutes());
				case 's':
					return pad(date.getSeconds());
				default:
					throw new Error('Unsupported format code: ' + fmtCode);
			}
		});
	}


	function initEvent() {
		$(".first .row:nth-child(1)").click(function(event) {
			console.log("进入物流信息页面");
			console.log("进入物流信息页面-----TODO");
			console.log("进入物流信息页面-----TODO");
			console.log("进入物流信息页面-----TODO");
			console.log("进入物流信息页面-----TODO");
			console.log("进入物流信息页面-----TODO");
		});
		$("#reorder-button").click(function(event) {
			console.log("再来一单");

			let path = result["promotion_path"];
			let order_no = result["order_no"];
			window.location.href = path + "?order_no=" + order_no;
		});
	}


	function loading() {
		$('body').addClass("loading");
	}
	function cancelLoading() {
		$('body').removeClass("loading");
	}
});