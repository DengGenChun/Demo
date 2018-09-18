$(function() {
	let order = [];

	load();


	function load() {
		loading();
		$.ajax({
			url: '/api/listOrder',
			type: 'GET',
			dataType: 'json',
			data: {
				"trade_state": "SUCCESS",
				"order_by_time": "desc",
			},
		})
		.done(function(data) {
			if (data["code"] == -1) {
				layer.alert(data["msg"]);
				return;
			}
			init(data["result"]);
			initEvent();
		})
		.fail(function() {
			layer.alert("网络连接异常，请稍后重试");
			showError();
		})
		.always(function() {
			cancelLoading();
		});
	}

	function init(result) {
		order = result;

		let content = $('.content');
		let html = '<div class="order"><div class="row header"><img class="icon"src="images/dianpu@2x.png"><div class="title gotoHome">康佳有品</div><div class="placeholder"></div><div class="subtitle"for="isSign">{$1}</div></div><div class="row productDesc"><img class="pic"src="{$2}"></img><div class="title"for="productTitle">{$3}</div></div><div class="row title"><div>共{$4}件商品</div><div>实付款:</div><div>￥{$5}</div></div><div class="line"></div><div class="row"><div class="purchase-btn">再次购买</div></div><div class="divide"></div></div>';

		for (let i = 0; i < result.length; i++) {
			let isSign = result[i].is_sign == "YES" ? true : false;
			let pic = result[i].p_icon;
			let productTitle = result[i].p_title;
			let productCount = result[i].p_count;
			let priceSum = result[i].price_sum;

			let h = html;
			h = h.replace('{$1}', isSign ? "已签收" : "未签收");
			h = h.replace('{$2}', pic);
			h = h.replace('{$3}', productTitle);
			h = h.replace('{$4}', productCount);
			h = h.replace('{$5}', priceSum);

			content.append(h);
		}
	}
	function initEvent() {
		// 再次购买
		let btnLists = $('.purchase-btn');
		btnLists.click(function(event) {
			let i = btnLists.index(this);
			let path = order[i]["promotion_path"];
			let order_no = order[i]["order_no"];
			window.location.href = path + "?order_no=" + order_no;
		});
		// 进入订单详情页
		let descLists = $('.productDesc');
		descLists.click(function(event) {
			let i = descLists.index(this);
			let order_no = order[i].order_no;
			window.location.href = "/order_detail.html?order_no=" + order_no;
		});
		// 进入官方商城页面
		$(".gotoHome").click(function() {
			window.location.href = "https://h5.youzan.com/v2/home/X8JlT7pnsA?reft=1536918283669&spm=f71487166&sf=wx_menu";
		});
	}


	function loading() {
		$('body').addClass("loading");
	}
	function cancelLoading() {
		$('body').removeClass("loading");
	}
	function showError() {
		$('.error-tip').css("display", "block");
	}
});