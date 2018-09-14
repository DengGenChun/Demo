$(function() {
	let args = {};
	let minCount = 1;
	let maxCount = 10;
	let currCount = 1;
	let firstImageSrc = "";
	let detailImageSrc = [];
	let selectedIndex = -1;
	let flags = [];
	let items = [];
	let isRecordAddress = true;
	let order = {};

	preLoad();
	load();

	function load() {
		loading();
		$.when(loadData(), loadOrder())
			.done(function() {
				initEvent();
				initOrderData();
			})
			.fail(function(msg) {
				if (msg && msg !== "") {
					layer.alert(msg);
				}
			})
			.always(function() {
				cancelLoading();
			});
	}

	function loadData() {
		let url = location.pathname + ".json"
		let $d = $.Deferred();
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			success: function(data) {
				if (data["code"] == -1) {
					$d.reject(data["msg"]);
					return;
				}
				initData(data["result"]);
				$d.resolve();
			},
			error: function() {
				$d.reject("网络连接失败，请重试");
			}
		});
		return $d.promise();
	}

	function loadOrder() {
		let $d = $.Deferred();
		let order_no = getArgs("order_no");
		if (!order_no || order_no == "") {
			$d.resolve();
		} else {
			$.ajax({
				url: '/api/listOrder',
				type: 'GET',
				dataType: 'json',
				data: {
					"order_no": order_no
				},
				success: function(data) {
					if (data["code"] == -1) {
						$d.reject(data["msg"]);
						return;
					}
					order = data["result"];
					setTimeout(function() {
						$d.resolve("订单信息获取成功");
					}, 200);
				},
				error: function() {
					$d.reject("");
				}
			});

		}
		return $d.promise();
	}

	function preLoad() {
		$(window).scroll(function() {
			let windowBottom = $(window).scrollTop() + $(window).height();
			if (windowBottom > $('.order-header').offset().top) {
				$('#btn-list').fadeOut(300);
			} else {
				$('#btn-list').fadeIn(300);
			}
		});
		$("#gotoHome").click(function() {
			window.location.href = "https://h5.youzan.com/v2/home/X8JlT7pnsA?reft=1536918283669&spm=f71487166&sf=wx_menu";
		});
	}

	function initData(result) {
		firstImageSrc = result["first_image"];
		detailImageSrc = result["detail_image"];
		items = result["products"];


		$('.first-image').attr("src", firstImageSrc);
		let detailHtml = '<img class="detail-image" src="{$1}"></img>';
		for (let i = 0; i < detailImageSrc.length; i++) {
			let html = detailHtml.replace("{$1}", detailImageSrc[i]);
			$('.detail-container').append(html);
		}
		let buttonHtml = '<div class="color-button">{$1}</div>';
		for (let i = 0; i < items.length; i++) {
			let html = buttonHtml.replace("{$1}", items[i].color);
			$('#color-button-container').append(html);
		}

		updateCountButton();
		updatePrice();

		let saleCount = 0;
		for (let i = 0; i < items.length; i++) {
			saleCount += items[i].sale_count;
		}
		$(".saleCount").text("销量：" + saleCount);
	}

	function initOrderData() {
		if (!order || Object.keys(order).length === 0) {
			return;
		}

		$('#name').val(order.username);
		$('#phone').val(order.phone);
		$('#comment').val(order.comment);
		$('#postcode').val(order.postcode);

		let ary = order.raw_address.split("{/}")
		let province = ary[0];
		let city = ary[1];
		let district = ary[2];
		let address = ary[3];
		$('#dist-select').distpicker('destory');
		$('#dist-select').distpicker({
			province: province,
			city: city,
			district: district
		});
		$('#address').val(address);
		isRecordAddress = order.record_address == "YES" ? true : false;
		if (!isRecordAddress) {
			$('.record-address .circle').addClass('inactive');
		}

		for (let i = 0; i < items.length; i++) {
			if (items[i].product_id == order.p_id) {
				selectedIndex = i;
				break;
			}
		}
		currCount = order.p_count;
		$($(".color-button")[selectedIndex]).addClass('active');
		updateCountButton();
		updatePrice();
		$('html, body').animate({
			scrollTop: $('.order-header').offset().top
		}, 500);
	}

	function initEvent() {
		$(".color-button").click(function() {
			let buttons = $(".color-button");
			let index = buttons.index(this);
			if (flags[index]) {
				return;
			}
			// Inactive off previous item
			let prevItemIndex = selectedIndex;
			$(buttons.get(prevItemIndex)).removeClass("active");
			flags[prevItemIndex] = false;

			// Active the selected item
			selectedIndex = index;
			$(this).addClass("active");
			flags[selectedIndex] = true;
			updatePrice();
		});
		$("#count-spinner .left").click(function() {
			if (currCount > minCount) {
				currCount--;
			}
			if (currCount <= minCount) {
				currCount = minCount;
			}
			updateCountButton();
			updatePrice();
		});
		$("#count-spinner .right").click(function() {
			if (currCount < maxCount) {
				currCount++;
			}
			if (currCount >= maxCount) {
				currCount = maxCount;
			}
			updateCountButton();
			updatePrice();
		});
		$('#purchase-btn').click(function() {
			$('html, body').animate({
				scrollTop: $('.order-header').offset().top
			}, 500);
		});
		$('.record-address').click(function() {
			if (isRecordAddress) {
				$('.record-address .circle').addClass("inactive");
			} else {
				$('.record-address .circle').removeClass("inactive");
			}
			isRecordAddress = !isRecordAddress;
		});
		let debounceSubmit = debounce(submitOrder, 100, true);
		$('.order-submit-button').click(function() {
			debounceSubmit();
		});
		$('#dist-select').distpicker('reset', true);
	}

	function updateCountButton() {
		if (currCount === minCount) {
			$("#count-spinner .left").addClass("disabled");
		} else {
			$("#count-spinner .left").removeClass("disabled");
		}

		if (currCount === maxCount) {
			$("#count-spinner .right").addClass("disabled");
		} else {
			$("#count-spinner .right").removeClass("disabled");
		}
		$("#product-count").text(currCount);
	}
	function updatePrice() {
		if (selectedIndex == -1) {
			$(".price").text("￥" + items[0].price);
			$(".productTitle").text(items[0].title);
			$("#price-sum").text("￥" + items[0].price);
		} else {
			let price = currCount * items[selectedIndex].price
			$(".price").text("￥" + items[selectedIndex].price);
			$(".productTitle").text(items[selectedIndex].title);
			$("#price-sum").text("￥" + price);
		}
	}

	function validateName(name) {
		let msg = '';
		if (name === '') {
			msg = "请输入姓名";
		}
		return msg;
	}
	function isChinese(text) {
		let regex = /[^\u4e00-\u9fa5]/;
		if (regex.test(text)) {
			return false;
		}
		return true;
	}

	function validatePhone(phone) {
		let msg = '';
		if (phone === '') {
			msg = "请输入手机号码";
		} else if (!isPhoneCorrect(phone)) {
			msg = "手机号码格式错误";
		}
		return msg;
	}
	function isPhoneCorrect(phone) {
		let regex = /^1[3|4|5|8][0-9]\d{4,8}$/;
		if (!regex.test(phone)) {
			return false;
		}
		return true;
	}

	function validateArea() {
		let msg = '';
		let areaElement = $("#dist-select option:selected");
		if ($(areaElement[0]).val() === '') {
			msg = "请选择省份";
		} else if ($(areaElement[1]).val() === '') {
			msg = "请选择城市";
		} else if ($(areaElement[2]).val() === '') {
			msg = "请选择地区";

			// 特殊情况, 地区可能不存在
			let areaAll = $("#dist-select option");
			let len = areaAll.length;
			if ($(areaAll[len-1]).val() === '') {
				msg = '';
			}
		}
		return msg;
	}


	function submitOrder() {
		if (selectedIndex == -1) {
			layer.alert("请选择商品");
			return;
		}
		let nameElement = $('#name');
		let msg = validateName(nameElement.val());
		if (msg !== '') {
			layer.alert(msg);
			return;
		}
		let phoneElement = $('#phone');
		msg = validatePhone(phoneElement.val());
		if (msg !== '') {
			layer.alert(msg);
			return;
		}
		msg = validateArea();
		if (msg !== '') {
			layer.alert(msg);
			return;
		}
		let addressElement = $('#address');
		if (addressElement.val() === '') {
			layer.alert("请输入详细地址");
			return
		}

		let count = currCount;
		let name = nameElement.val();
		let phone = phoneElement.val();
		let address = addressElement.val();
		let comment = $('#comment').val();
		let areaElement = $("#dist-select option:selected");
		let area = $(areaElement[0]).val() + $(areaElement[1]).val() + $(areaElement[2]).val();
		let rawAddress = $(areaElement[0]).val() + "{/}" + $(areaElement[1]).val() + "{/}" + $(areaElement[2]).val() + "{/}" + address;
		let postcode = $("#postcode").val();

		console.log("count: " + count);
		console.log("name: " + name);
		console.log("phone: " + phone);
		console.log("area: " + area);
		console.log("address: " + address);
		console.log("comment: " + comment);
		console.log("rawAddress: " + rawAddress);
	 	console.log("postcode: " + postcode);

		$('body').addClass("loading");
		$.get("/api/createOrder", {
			"p_id": items[selectedIndex].product_id,
			"p_count": currCount,
			"username": name,
			"phone": phone,
			"address": address,
			"comment": comment,
			"raw_address": rawAddress,
			"postcode": postcode,
			"record_address": isRecordAddress ? "YES" : "NO",
			"promotion_path": location.pathname
		}, function(data, status) {
			if (status === "success") {
				if (data["code"] === -1) {
					layer.alert(data["msg"]);
				} else {
					WXPayRequest(data.result);
				}
			} else {
				layer.alert(status);
			}
		}, "json").fail(function () {
			layer.alert("无法连接网络，请稍后再试");
		}).always(function() {
			$('body').removeClass("loading")
		});
	}

	function WXPayRequest(result) {
		let order_no = result.order_no;

		function onBridgeReady() {
			WeixinJSBridge.invoke('getBrandWCPayRequest', result.data, function(res) {
				window.location.href = "/trade_result.html?order_no=" + order_no;
			});
		}

		if (typeof WeixinJSBridge == "undefined") {
			if (document.addEventListener) {
				document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
			} else if (document.attachEvent) {
				document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
				document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
			}
		} else {
			onBridgeReady();
		}
	}

	function loading() {
		$('body').addClass("loading");
	}

	function cancelLoading() {
		$('body').removeClass("loading");
	}


	function getArgs(key) {
		if (args[key]) {
			return args[key];
		}
		let url = window.location.search.substring(1);
		let kvs = url.split("&");
		for (let i = 0; i < kvs.length; i++) {
			let kv = kvs[i].split("=");
			args[kv[0]] = kv[1];
		}
		return args[key];
	}

	function debounce(func, delay, immediate) {
		let tid;
		return function() {
			let context = this, args = arguments;
			let later = function() {
				tid = null;
				if (!immediate) {
					func.apply(context, args);
				}
			}
			let callImmediate = immediate && !tid;
			clearTimeout(tid)
			tid = setTimeout(later, delay);
			if (callImmediate) {
				func.apply(context, args);
			}
		}
	}
});