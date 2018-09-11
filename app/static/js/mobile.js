(function() {
	let viewport = document.querySelector("meta[name='viewport']");
	let docElement = document.documentElement;

	function adjust() {
		let screenW = screenWidth();
		let dpr = window.devicePixelRatio || 1;
		let scale = 1 / dpr;
		let rem = screenW * dpr / 10;

		scale = 1;
		rem = screenW / 10;
		viewport.setAttribute('content', 'width=device-width' + ',initial-scale=' + scale + ',minimum-scale=' + scale + ',maximum-scale=' + scale + ',user-scalable=no')
		docElement.setAttribute('data-dpr', dpr);
		docElement.style.fontSize = rem + 'px';

		if (document.readyState === 'complete') {
			runAtReady();
		}
	}

	function runAtReady() {
		let dpr = (window.devicePixelRatio || 1);

		dpr = 1;
		document.body.style.fontSize = 14 * dpr + 'px';
		document.body.style.width = screenWidth() * dpr + 'px';
		adjustScreen();
	}

	function adjustScreen() {
		var browser = {
			versions: function() {
				var u = navigator.userAgent;
				return {
					mobile: !!u.match(/AppleWebKit.*Mobile.*/),
					ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/),
					android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1,
					iPhone: u.indexOf('iPhone') > -1,
					iPad: u.indexOf('iPad') > -1,
				};
			}()
		}

		if (!(browser.versions.mobile || browser.versions.ios || browser.versions.android ||
				browser.versions.iPhone || browser.versions.iPad)) {
			document.body.style.width = "640px";
			document.body.style.backgroundColor = "#FFF";
			document.body.style.margin = "0 auto";
		}
	}

	function screenWidth() {
		let screenW = window.screen.width;
		if (screenW < 320) {
			screenW = 320;
		}
		if (screenW > 540) {
			screenW = 540;
		}
		return screenW;
	}

	function debounce(func, delay) {
		let tid;
		return function() {
			let context = this, args = arguments;
			let later = function() {
				tid = null;
				func.apply(context, args);
			}
			clearTimeout(tid)
			tid = setTimeout(later, delay);
		}
	}



	if (window.addEventListener) {
		window.addEventListener('resize', debounce(adjust, 100), false);
	} else if (window.attachEvent) {
		window.attachEvent('onresize', debounce(adjust, 100));
	}
	adjust();
	if (document.readyState === 'complete') {
		runAtReady();
	} else {
		document.addEventListener("DOMContentLoaded", runAtReady, false);
		window.addEventListener("load", runAtReady);
	}
}());