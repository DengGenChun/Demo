$(function() {
	let signTitle = "【签收】已签收，感谢使用顺丰，期待再次为您服务";
	let signTime = "2018-08-31 11:47:08";
	let username = "曾敏";
	let phone = "188****7489";
	let address = "广东省深圳市南山区南山区华侨城汕头街8号康家苑康家园";
	let isSign = true;
	let icon = "";
	let productTitle = "康佳手机康佳手机康佳手机康佳手机康佳手机康佳手机康佳手机康佳手机";
	let orderCount = 1;
	let productColor = "曜石黑";
	let priceSum = "999.00";
	let comment = "广东省深圳市南山区南山区华侨城汕头街8号康佳苑";
	let orderNo = "071511687310";
	let orderTime = 0;
	let payTime = 0;


	load();

	function load() {
		loading();
		$.when(loadOrder(), loadWuliu())
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

	function loadOrder() {
		let $d = $.Deferred();
		$.ajax({
			url: '/api/listOrder',
			type: 'GET',
			dataType: 'json',
			data: {
				"order_no": "829153577711003113",
				"openid": "obU8M1Gxj7GmyS2IQTQOr6Iz3ZEs",
			},
			success: function(data) {
				if (data["code"] == -1) {
					$d.reject(data["msg"]);
					return;
				}
				fillOrderData(data["result"]);
				$d.resolve("订单信息获取成功");
			},
			error: function() {
				$d.reject("订单信息获取失败");
			}
		});
		return $d.promise();
	}

	function loadWuliu() {
		let $d = $.Deferred();
		// $.ajax({
		// 	url: '',
		// 	type: 'GET',
		// 	dataType: 'json',
		// 	data: {},
		// 	success: function(data) {
		// 		if (data["code"] == -1) {
		// 			$d.reject(data["msg"]);
		// 			return;
		// 		}
		// 		fillWuliuData(data["result"]);
		// 		$d.resolve("物流信息获取成功");
		// 	},
		// 	error: function() {
		// 		$d.reject("物流信息获取失败");
		// 	}
		// });
		setTimeout(function() {
			$d.reject("获取物流失败");
		}, 1000);
		return $d.promise();
	}

	function fillOrderData(res) {
		username = res["username"];
		phone = res["phone"];
		address = res["address"];
		icon = res["icon"];
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

	function fillWuliuData(res) {
		// $("div[for='signTitle']").text(signTitle);
		// $("div[for='signTime']").text(signTime);
		// $("div[for='isSign']").text(isSign ? "已签收" : "未签收");
	}

	function formatDate(date, fmt) {
		function pad(value) {
			return (value.toString().length < 2) ? '0' + value : value;
		}
		return fmt.replace(/%([a-zA-Z])/g, function(_, fmtCode) {
			switch (fmtCode) {
				case 'Y':
					return date.getUTCFullYear();
				case 'M':
					return pad(date.getUTCMonth() + 1);
				case 'd':
					return pad(date.getUTCDate());
				case 'H':
					return pad(date.getUTCHours());
				case 'm':
					return pad(date.getUTCMinutes());
				case 's':
					return pad(date.getUTCSeconds());
				default:
					throw new Error('Unsupported format code: ' + fmtCode);
			}
		});
	}


	function initEvent() {
		$(".first .row:nth-child(1)").click(function(event) {
			console.log("进入物流信息页面");
		});
		$("#reorder-button").click(function(event) {
			console.log("再来一单");
			window.location.href = "/VwqXrMRgdzjBpP69cSt6LhLHYAwCwyF";
		});
	}

	function loading() {
		$('body').addClass("loading");
	}

	function cancelLoading() {
		$('body').removeClass("loading");
	}
});