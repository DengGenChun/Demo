

$(function() {
    let contactPhone = 17712341234;
    let minCount = 1;
    let maxCount = 10;
    let currCount = 1;
    let firstImageSrc = "";
	let detailImageSrc = [];
	let selectedIndex = 0;
	let flags = [];
	let items = [];

	adjustScreen();
	load();

	function load() {
		$.getJSON("data.json", function(data) {
			contactPhone = data.contactPhone;
			minCount = data.minCount;
			maxCount = data.maxCount;
			currCount = data.currCount;
			firstImageSrc = data.firstImageSrc;
			detailImageSrc = data.detailImageSrc;
			selectedIndex = data.selectedIndex;
			flags = data.flags;
			items = data.items;
		}).fail(function() {
			console.log("fail load config");
		}).always(function() {
			init();
            initEvent();
		});
	}

	function init() {
		$('.first-image').attr("src", firstImageSrc);
		let detailHtml = '<img class="detail-image" src="{$1}"></img>';
		for (let i = 0; i < detailImageSrc.length; i++) {
			let html = detailHtml.replace("{$1}", detailImageSrc[i]);
			$('.detail-container').append(html);
		}
		let titleHtml = '<li class=""><span class="radio-icon"></span>{$1}</li>';
		for (let i = 0; i < items.length; i++) {
			let html = titleHtml.replace("{$1}", items[i].title);
			$('.radio-group.product-type').append(html);
		}
		let descHtml ='<div class="product-desc hide"><p class="desc">{$1}</p></div>';
		for (let i = 0; i < items.length; i++) {
			let html = descHtml.replace("{$1}", items[i].desc);
			$('.product-desc-container').append(html);
		}

		let contactTelElement = $('#contact-tel');
        contactTelElement.text(contactPhone);
        contactTelElement.attr("href", "tel:" + contactPhone);
		$('#contact-no').attr("href", "tel:" + contactPhone);
		updateCountButton();
		updatePrice();
		flags[selectedIndex] = true;
		$($(".radio-group.product-type > li").get(selectedIndex)).addClass("radio-active");
		$($(".product-desc-container .product-desc").get(selectedIndex)).removeClass("hide");
	}

	function initEvent() {
        $(".radio-group.product-type > li").click(function() {
            let radioGroup = $(".radio-group.product-type > li");
            let index = radioGroup.index(this);
            if (flags[index]) {
                return;
            }
            // Inactive off previous item
            let prevItemIndex = selectedIndex;
            $(radioGroup.get(prevItemIndex)).removeClass("radio-active");
            $($(".product-desc").get(prevItemIndex)).addClass("hide");
            flags[prevItemIndex] = false;

            // Active the selected item
            selectedIndex = index;
            $(this).addClass("radio-active");
            $($(".product-desc").get(selectedIndex)).removeClass("hide");
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
        $('#name').blur(function() {
            let msg = validateName($(this).val());
            $("div[for*='name']").text(msg);
        });
        $('#phone').blur(function() {
            let msg = validatePhone($(this).val());
            $("div[for*='phone']").text(msg);
        });
        $("#dist-select > select").change(function() {
            let msg = validateArea();
            $("div[for*='dist-select']").text(msg);
        });
        $('#address').blur(function() {
            let msg = '';
            if ($(this).val() === '') {
                msg = "请输入详细地址";
            }
            $("div[for*='address']").text(msg);
        });
        // Purchase button event
        $('#purchase-btn, .index-buying').click(function() {
            $('html, body').animate({
                scrollTop: $('.order-header').offset().top
            }, 500);
        });
        $(window).scroll(function() {
            let windowBottom = $(window).scrollTop() + $(window).height();
            if (windowBottom > $('.order-header').offset().top) {
                $('#btn-list').fadeOut(300);
            } else {
                $('#btn-list').fadeIn(300);
            }
        });
        // Order submit
        $('.order-submit-button').click(function() {
            submitOrder();
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
        let price = currCount * items[selectedIndex].price;
        $("#price-sum").text("￥" + price);
        $(".index-price").text("￥" + items[selectedIndex].price);
    }

    function validateName(name) {
        let msg = '';
        if (name === '') {
            msg = "请输入姓名";
        } else if (!isChinese(name)) {
            msg = "姓名只能输入中文";
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

        console.log("count: " + count);
        console.log("name: " + name);
        console.log("phone: " + phone);
        console.log("area: " + area);
        console.log("address: " + address);
        console.log("comment: " + comment);

        $('body').addClass("loading");
        $.get("/api/createOrder", {
            "p_id": items[selectedIndex].itemId,
            "p_count": currCount,
            "username": name,
            "phone": phone,
            "address": address,
            "comment": comment
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
                // if (res.err_msg == "get_brand_wcpay_request:ok") {
                //     window.location.href = "/order/orderSuccess?order_no=" + order_no
                // }
                window.location.href = "/order_detail?order_no=" + order_no;
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

    function adjustScreen() {
        var browser={
            versions:function(){
               var u = navigator.userAgent, app = navigator.appVersion;
               return {//移动终端浏览器版本信息
                    trident: u.indexOf('Trident') > -1, //IE内核
                    presto: u.indexOf('Presto') > -1, //opera内核
                    webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
                    gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核
                    mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
                    ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
                    android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器
                    iPhone: u.indexOf('iPhone') > -1 , //是否为iPhone或者QQHD浏览器
                    iPad: u.indexOf('iPad') > -1, //是否iPad
                    webApp: u.indexOf('Safari') == -1, //是否web应该程序，没有头部与底部
                    weixin: u.indexOf('MicroMessenger') > -1, //是否微信
                    qq: u.match(/\sQQ/i) == " qq" //是否QQ
                };
             }(),
             language:(navigator.browserLanguage || navigator.language).toLowerCase()
        }

        if(!(browser.versions.mobile || browser.versions.ios || browser.versions.android ||
            browser.versions.iPhone || browser.versions.iPad)){
            $('.main').addClass('pc');
            $('#btn-list').css('width', 640);
        }
    }
});