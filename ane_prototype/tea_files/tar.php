if(typeof JSON!=="object"){JSON={}}(function(){"use strict";function f(e){return e<10?"0"+e:e}function quote(e){escapable.lastIndex=0;return escapable.test(e)?'"'+e.replace(escapable,function(e){var t=meta[e];return typeof t==="string"?t:"\\u"+("0000"+e.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+e+'"'}function str(e,t){var n,r,i,s,o=gap,u,a=t[e];if(a&&typeof a==="object"&&typeof a.toJSON==="function"){a=a.toJSON(e)}if(typeof rep==="function"){a=rep.call(t,e,a)}switch(typeof a){case"string":return quote(a);case"number":return isFinite(a)?String(a):"null";case"boolean":case"null":return String(a);case"object":if(!a){return"null"}gap+=indent;u=[];if(Object.prototype.toString.apply(a)==="[object Array]"){s=a.length;for(n=0;n<s;n+=1){u[n]=str(n,a)||"null"}i=u.length===0?"[]":gap?"[\n"+gap+u.join(",\n"+gap)+"\n"+o+"]":"["+u.join(",")+"]";gap=o;return i}if(rep&&typeof rep==="object"){s=rep.length;for(n=0;n<s;n+=1){if(typeof rep[n]==="string"){r=rep[n];i=str(r,a);if(i){u.push(quote(r)+(gap?": ":":")+i)}}}}else{for(r in a){if(Object.prototype.hasOwnProperty.call(a,r)){i=str(r,a);if(i){u.push(quote(r)+(gap?": ":":")+i)}}}}i=u.length===0?"{}":gap?"{\n"+gap+u.join(",\n"+gap)+"\n"+o+"}":"{"+u.join(",")+"}";gap=o;return i}}if(typeof Date.prototype.toJSON!=="function"){Date.prototype.toJSON=function(){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+f(this.getUTCMonth()+1)+"-"+f(this.getUTCDate())+"T"+f(this.getUTCHours())+":"+f(this.getUTCMinutes())+":"+f(this.getUTCSeconds())+"Z":null};String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(){return this.valueOf()}}var cx=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,escapable=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,gap,indent,meta={"\b":"\\b","	":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},rep;if(typeof JSON.stringify!=="function"){JSON.stringify=function(e,t,n){var r;gap="";indent="";if(typeof n==="number"){for(r=0;r<n;r+=1){indent+=" "}}else if(typeof n==="string"){indent=n}rep=t;if(t&&typeof t!=="function"&&(typeof t!=="object"||typeof t.length!=="number")){throw new Error("JSON.stringify")}return str("",{"":e})}}if(typeof JSON.parse!=="function"){JSON.parse=function(text,reviver){function walk(e,t){var n,r,i=e[t];if(i&&typeof i==="object"){for(n in i){if(Object.prototype.hasOwnProperty.call(i,n)){r=walk(i,n);if(r!==undefined){i[n]=r}else{delete i[n]}}}}return reviver.call(e,t,i)}var j;text=String(text);cx.lastIndex=0;if(cx.test(text)){text=text.replace(cx,function(e){return"\\u"+("0000"+e.charCodeAt(0).toString(16)).slice(-4)})}if(/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,""))){j=eval("("+text+")");return typeof reviver==="function"?walk({"":j},""):j}throw new SyntaxError("JSON.parse")}}})();
var rbnt_rt = {
	rbnt_host: '//rbnt.org',
	rbnt_rt_data: null,
	adv: 'pJ2',
	ru: '', 	ref_cookies: [
			],
	site_host: function(d) {
		var h = (d !== undefined) ? d : window.location.hostname;
		h = h.split('.');
		return h[h.length-2]+'_'+h[h.length-1];
	},
	addEl: function(r) {
		if (r) {
			var t, y, e;
			for (t in r) {
				if (r.hasOwnProperty(t)) {
					if (t == 'img' && r[t]) {
						for (y in r[t]) {
							if (r[t].hasOwnProperty(y)) {
								var e = new Image();
								e.src = r[t][y];
							}
						}
					} else if (t == 'iframe' && r[t]) {
						for (y in r[t]) {
							if (r[t].hasOwnProperty(y)) {
								e = document.createElement("iframe");
								e.style.width = '0';
								e.style.height = '0';
								e.style.border = '0';
								e.style.position = 'absolute';
								e.style.left = '-9999px';
								e.style.bottom = '0';
								e.style.visibility = 'hidden';
								e.src = r[t][y];
								document.body.appendChild(e);
							}
						}
					}
				}
			}
		}
	},
	isEmpty: function(obj) {
		for (var key in obj) {
			if(obj.hasOwnProperty(key)) return false;
		}
		return true;
	},
	showPC: function(pp, t) {
		
		var r = {}, ret = '', tg = 0;
		if (typeof t != 'undefined') {
			tg = t;
		}

		if (tg == '1') {
			r['iframe'] = [];
			r['iframe'].push('https:\/\/rbnt.org\/gtref.php?adv_id=pJ2&mode=hit&tg='+tg);

			if (pp == 1) {
				r['img'] = [];
				r['img'].push('https:\/\/rbnt.org\/rsc.php?ltc=1530104743&c_name=rd_pJ2_' + '&c_value=03');
			} else {
				ret = '&sclist[]=ltc%3D1530104743%26c_name%3Drd_pJ2_' + '%26c_value%3D03';
			}
		}

		this.addEl(r);
		return ret;
	},
	order: function(o) {
		if (typeof o != 'object') {
			o = [{oid: o}];
		}

		var r = {'img': [], 'iframe': []}, el, u, s = 'https:\/\/rbnt.org\/rsc.php?',
			p = 's=2&mode=pixel&id=pJ2&h='+this.site_host().replace('_', '.');

		for (var i = 0; i < o.length; i++) {
			u = p;
			for (n in o[i]) {
				if (o[i].hasOwnProperty(n)) {
					u += '&'+n+'='+encodeURIComponent(o[i][n]);
				}
			}

			if (i == 0) {
				r['iframe'].push('https:\/\/rbnt.org\/gtref.php?mode=content&adv_id=pJ2&page=complete');
			}

			u = s + u;

			r['img'].push(u);
		}

		this.addEl(r);
	},

    credit: function () {
        var r = {};
        r['img'] = [];
        r['img'].push('https:\/\/rbnt.org\/rsc.php?mode=credit&id=pJ2');

                    r['iframe'] = [];
            r['iframe'].push('https:\/\/rbnt.org\/gtref.php?mode=content&adv_id=pJ2&page=buttoncredit');
        	        this.addEl(r);
    },

	sendh: function() {},
	send: function() {
		var m = this;
		m.rbnt_rt_data = window.rbnt_rt_params || {};

		if (!m.isEmpty(m.rbnt_rt_data)) {
			m.rbnt_rt_data['adv'] = m.adv;
						m.rbnt_rt_data['vts'] = 0;

			var r = encodeURIComponent(JSON.stringify(m.rbnt_rt_data)),
				n = 'POST',
				o = m.rbnt_host + '/lw.php?t=rt';
			var x = window.XDomainRequest || window.XMLHttpRequest;
			if (typeof x != 'undefined') {
				x = new x();
				x.open(n, o, !0);
									x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
									x.onload = function() {
											var r = JSON.parse(x.responseText);
											if (r) {
						if (typeof r.pageType != 'undefined') {
							if (r.pageType == '6') {
																	m.order(r.orderId);
															} else if (r.pageType == '2' || r.pageType == '7') {
																									var isShopPC = true;
									for (var i = 0; i < m.ref_cookies.length; i++) {
										if ((m.ref_cookies[i].index == 'rd_pJ2_' + m.site_host()) || (m.ref_cookies[i].index == 'rd_pJ2_')) {
											if (m.ref_cookies[i].value.substr(0,2) == '03') {
												isShopPC = false;
											}
										}
									}
									if (isShopPC) {
										m.showPC(1, r.top);
									}
															}  else if (r.pageType == '1' || r.pageType == '4' || r.pageType == '5' || r.pageType == '10') {
                                							}
						}
					}
				};
				x.onerror = function() {
					m.sendh();
				};
				x.send('data=' + r);
			} else {
				m.sendh();
			}
		}
	}
};
	rbnt_rt.send();
	
var cur_loc = window.location,prev_loc = "";
if (typeof _rbnt_exist == 'undefined' || cur_loc != prev_loc) {
	var _rbnt_exist = 1;
	prev_loc = window.location;

	try {
		
		(function(w, d, o, ap) {
			function send() {
				var m = {};
				m["iframe"] = [];
				m["iframe"].push("https://rbnt.org/gtref.php?mode=ref&fr=" + (self != top ? 1 : 0) + "&adv_id=pJ2&l=" + encodeURIComponent(d.URL) + "&r=" + (r ? encodeURIComponent(r) : "null") + "&d=1530018338");
				o.addEl(m);
			}

			function sth(s) {
				var h = "";
				for (var i = 0; i < s.length; i++) {
					h += ""+s.charCodeAt(i).toString(16);
				}
				return h;
			}

			var l = o.site_host(), r = d.referrer;
			var a = d.createElement("a");
			o.ru = r

			if (r != "" && (a.href = r) && o.site_host(a.hostname) != l) {
				send();
			}
			else {
				
				var sr = false, i;
				a.href = d.URL;

				if (!sr) {
					var s = a.search.substring(1).split("&");
					for (i = 0; i < s.length; i++) {
						var v = s[i].split("=");
						if (ap.indexOf(v[0]) > -1 && v[1] !== undefined && v[1] != "") {
							sr = true;
							break;
						}
					}
				}

				if (!sr) {
					var p = a.pathname.substring(1).split("/");
					for (i = 0; i < p.length; i++) {
						if (ap.indexOf(p[i]) > -1) {
							sr = true;
							break;
						}
					}
				}

				if (!sr) {
					sr = sth(d.URL).indexOf("61646d696e") > -1 || (r != "" && sth(r).indexOf("61646d696e") > -1);
				}

				if (sr) {
					send();
				}
			}
		})(window, document, rbnt_rt, ["utm_source"]);

			} catch (e) {
		var newItemV = document.createElement("img");
		newItemV.src = 'https:\/\/rbnt.org\/lw.php?t=e&h=' + window.location + '&m=' + encodeURIComponent(e.message) + '---1---' + encodeURIComponent(document.referrer);
		newItemV.id = Math.random();
		newItemV.style.width = '0px';
		newItemV.style.height = '0px';
		newItemV.style.display = 'none';
		document.body.appendChild(newItemV);
	}

	setTimeout(function() {
		try {
			var tmp_val = '20180626', is_request_rbnt = true, is_preq_rbnt = true;
						for (var i = 0; i < rbnt_rt.ref_cookies.length; i++) {
				if ((rbnt_rt.ref_cookies[i].index == 'rdata_pJ2_' + rbnt_rt.site_host()) || (rbnt_rt.ref_cookies[i].index == 'rdata_pJ2_')) {
					if (rbnt_rt.ref_cookies[i].value == '20180626') {
						is_request_rbnt = false;
					}
				}
				if ((rbnt_rt.ref_cookies[i].index == 'rd_pJ2_' + rbnt_rt.site_host()) || (rbnt_rt.ref_cookies[i].index == 'rd_pJ2_')) {
					if (rbnt_rt.ref_cookies[i].value.substr(0,2) == '03') {
						is_preq_rbnt = false;
					}
				}
			}
							function loadScript(url, callback) {
					var head = document.getElementsByTagName('head')[0];
					var script = document.createElement('script');
					script.type = 'text/javascript';
					script.src = url;
										if(callback!='') {
						script.onreadystatechange = callback;
						script.onload = callback;
					}
										head.appendChild(script);
				}
				function loadCallbackRbnt() {
										if (typeof LS == 'undefined') {
						return 0;
					}

					var isCatalog = LS.isCatalog(),
												vt = null					;
					var ctecn = '';
					var ctecnwo = '';
											ctecnwo = 'https:\/\/rbnt.org\/gtref.php?mode=ppinst&adv_id=pJ2';
												if (ctecn || ctecnwo) {
							var r = {};
							r['iframe'] = [];
							if (ctecn) {
								r['iframe'].push(ctecn);
							}
							if (ctecnwo) {
								r['iframe'].push(ctecnwo);
							}

							rbnt_rt.addEl(r);
						}
						
															
					(function(l, r) {
						if (typeof l.getCoupon === "function") {
							var cc,
								fc = function(c, v) {
									if (c && cc != c) {
										cc = c;
										r.addEl({"img": [(window.location.protocol == "https:" ? "https:" : "http:")+'\/\/rbnt.org\/lw.php?t=sc&s=pJ2&v=' + encodeURIComponent(c) + '&iv=' + encodeURIComponent(v || 0)]});
										return true;
									}
									return false;
								},
								fi = function() {
									var gc = LS.getCoupon(), ac = gc['ac'], f = gc['f'], sf = gc['sf'];
									var ae = document.activeElement, u = undefined;

									if (sf !== u) {
										var ss = window.sessionStorage, k = '_coupon';
										if (f && ae == f) {
											var code = f.value;
											if (code) {
												ss.setItem(k, code);
											}
										}

										if (sf) {
											if (fc(ss.getItem(k), gc['v'])) {
												ss.removeItem(k);
											}
										}
									}
									else if (ac !== u) {
										fc(gc['ac'], gc['v']);
									}
									else if (f !== u) {
										if (f && ae != f) {
											fc(f.value, gc['v']);
										}
									}

									setTimeout(fi, 1e3);
								};
							fi();
						}
					})(LS, rbnt_rt);

					
					
					if (isCatalog && true) {
						
						var visited_today = JSON.parse(vt),
							url_param = '',
							vnct = 0
						;

						if (visited_today) {
							vnct = visited_today.length;
						}

												url_param += 'sclist[]='+encodeURIComponent('nc=1&ltc=1530018343&c_name=v_pJ2&c_value=' + encodeURIComponent('www.auchan.ru/pokupki/eda/kofe-chai-sahar/chay.html')+(rbnt_rt.ru !== ''?'&ru='+encodeURIComponent(rbnt_rt.ru):''));
						
						if (!visited_today || visited_today.indexOf('3a8450ad0a5799081e47367e33c21ed8') == -1) {
							var visited_today_new = [];
							if (visited_today) {
								visited_today_new = visited_today.slice(-7);
							}
							visited_today_new.push('3a8450ad0a5799081e47367e33c21ed8');
							if (url_param != '') {
								url_param += '&';
							}
															url_param += 'sclist[]='+encodeURIComponent('j=1&ltc=-1&c_name=vtpJ2&c_value=' + encodeURIComponent(visited_today_new.join(',')));
														vnct++;

							var vg = '';
							vg += '&vg[s]=pJ2';
							vg += '&vg[id]=' + encodeURIComponent(LS.getProductID());
							vg += '&vg[name]=' + encodeURIComponent(LS.getProductName());
							vg += '&vg[brand]=' + encodeURIComponent(LS.getProductBrand());
							vg += '&vg[category]=' + encodeURIComponent(LS.getProductCategory());
							vg += '&vg[price]=' + encodeURIComponent(LS.getProductPrice());
							vg += '&vg[price_old]=' + encodeURIComponent(LS.getProductOldPrice());
							vg += '&vg[currency_id]=' + encodeURIComponent(LS.getCurrencyId());
							vg += '&vg[is_available]=' + encodeURIComponent(LS.isProductAvailable());
							vg += '&vg[thumbnail]=' + encodeURIComponent(LS.getProductImage());
							vg += '&vg[description]=' + encodeURIComponent(LS.getProductDescription());
							vg += '&vg[product_url]=' + encodeURIComponent(LS.getProductClearUrl());

																												url_param = url_param + vg;
						}
						var allow_vc = (vnct >= 2);
												if (allow_vc) {
							if (url_param != '') {
								url_param = url_param + '&';
							}
							url_param = url_param + 'sclist[]=ltc%3D1535202343%26c_name%3Drdd_pJ2' + '%26c_value%3D20180626';
						}
						
						var allow_pc = is_preq_rbnt && allow_vc;
						if (url_param) {
															if (allow_pc) {
									url_param=url_param+rbnt_rt.showPC(0);
								}
								loadScript('https:\/\/rbnt.org\/rsc.php?scr=1&' + url_param,'');
						}
						return true;
					} else {
													if(rbnt_rt.ru!==''){
								loadScript('https:\/\/rbnt.org\/rsc.php?scr=1&'+'sclist[]='+encodeURIComponent('nc=0&ltc=1530018343&c_name=v_pJ2&c_value=' + encodeURIComponent('www.auchan.ru/pokupki/eda/kofe-chai-sahar/chay.html')+'&ru='+encodeURIComponent(rbnt_rt.ru)),'');
							}
											}
					

															if (LS.isOrder()) {
						rbnt_rt.order(LS.getOrderID());
						return true;
					}
					
					if (LS.isCart()) {
						if (LS.getTimer()) {
							var up = '';
							setInterval(function() {up = cart(LS, up);}, 2000);
						} else {
							cart(LS);
						}

						return true;
					}

					return false;
				}

				function cart(obj, up) {
					var c = obj.getCart();
					if (typeof c !== 'undefined' && c !== false) {
						var url_param = 'sclist[]='+encodeURIComponent('c_name=rb_pJ2&c_value=');

						if (c.length > 0) {
							var pid = [];
							for (var i = 0; i < c.length; i++) {
								pid.push(c[i]['ProductId']);
							}
							url_param += encodeURIComponent(pid.join(','));
						}

						if (up != url_param) {
							up = url_param;

							
							var newItemV = document.createElement("img");
							newItemV.src = 'https:\/\/rbnt.org\/rsc.php?' + url_param;
							newItemV.id = Math.random();
							newItemV.style.width = '0px';
							newItemV.style.height = '0px';
							newItemV.style.display = 'none';
							document.body.appendChild(newItemV);
						}

						return up;
					}
				}


									var LS = (function() {
	var isCatalog = null,
		dl_element = null,
		timer = false,
		creditUrl = null
	;

	var $q = function(selector, el) {
		if (!el) {el = document;}
		return el.querySelector(selector);
	};

	var $$q = function(selector, el) {
		if (!el) {el = document;}
		return el.querySelectorAll(selector);
	};

	var trim = function(str) {
		return str.replace(/^\s+|\s+$/g, '');
	};

	var innerTXT = function(str) {
		if (document.all) {
			return str.innerText;
		} else{
			return str.textContent;
		}
	};

	var murmurhash2_32_gc = function(str) {
		var
			l = str.length,
			h = l,
			i = 0,
			k;

		while (l >= 4) {
			k =
				((str.charCodeAt(i) & 0xff)) |
				((str.charCodeAt(++i) & 0xff) << 8) |
				((str.charCodeAt(++i) & 0xff) << 16) |
				((str.charCodeAt(++i) & 0xff) << 24);

			k = (((k & 0xffff) * 0x5bd1e995) + ((((k >>> 16) * 0x5bd1e995) & 0xffff) << 16));
			k ^= k >>> 24;
			k = (((k & 0xffff) * 0x5bd1e995) + ((((k >>> 16) * 0x5bd1e995) & 0xffff) << 16));

			h = (((h & 0xffff) * 0x5bd1e995) + ((((h >>> 16) * 0x5bd1e995) & 0xffff) << 16)) ^ k;

			l -= 4;
			++i;
		}

		switch (l) {
			case 3: h ^= (str.charCodeAt(i + 2) & 0xff) << 16;
			case 2: h ^= (str.charCodeAt(i + 1) & 0xff) << 8;
			case 1: h ^= (str.charCodeAt(i) & 0xff);
				h = (((h & 0xffff) * 0x5bd1e995) + ((((h >>> 16) * 0x5bd1e995) & 0xffff) << 16));
		}

		h ^= h >>> 13;
		h = (((h & 0xffff) * 0x5bd1e995) + ((((h >>> 16) * 0x5bd1e995) & 0xffff) << 16));
		h ^= h >>> 15;

		return h >>> 0;
	};

	return {

		getTimer: function() {
			return timer;
		},

		detectURL: function() {},

		detectCredit : function () {
			return false;
		},

		isCredit: function() {
			if (creditUrl == null) {
				this.detectCredit();
			}

			return creditUrl | false;
		},

		isMainPage: function() {
			var isMainPage = false;
			try {
				isMainPage = (window.location.pathname == '/');
			} catch (e) {}

			return isMainPage;
		},

		isCatalog: function() {
			if (isCatalog === null) {
				isCatalog = false;

				try {
					isCatalog = false;
					var dl = window['dataLayer'] || [], l = dl.length, i = 0;
					for (; i < l; i++) {
						var pt = dl[i]['event'] || '';
						if (pt == 'productDetail') {
							var e = dl[i]['ecommerce'] || {},
								d = e['detail'] || {},
								p = d['products'] || [];

							dl_element = p[0] || null;

							if (dl_element != null) {
								isCatalog = true;
							}
							break;
						}
					}
				} catch (e) {}
			}

			return isCatalog;
        },

		isCart: function() {
			var isCart = false;

			try {
				//var dl_element, isCart = false;
				if (document.URL.indexOf('/cart') > -1) {
					var dl = window['dataLayer'] || [], l = dl.length, i = 0;
					for (; i < l; i++) {
						var pt = dl[i]['event'] || '';
						if (pt == 'checkout') {
							var e = dl[i]['ecommerce'] || {},
								d = e['checkout'] || {};

							dl_element = d['products'] || null;

							if (dl_element != null) {
								isCart = true;
							}
							break;
						}
					}
				}
			} catch (e) {}

			return isCart;
		},

		isOrder: function() {
			/*var url = document.URL;
			return (url.indexOf('/pokupki/checkout/onepage/success/') > -1 && $q('.order-results') != null);*/

			var ret = false;
			try {
				/*var v1 = document.URL.indexOf('/pokupki/checkout/onepage/') > -1,
					v2 = (" " + $q('#checkoutSteps #opc-review').className + " ").replace(/[\n\t\r]/g, " ").indexOf(" active ") > -1;
				if (v1 && v2) {
					ret = true;
				}*/
				var dl = window['dataLayer'] || [], l = dl.length, i = 0;
				for (; i < l; i++) {
					var pt = dl[i]['event'] || '';
					if (pt == 'transaction') {
						var e = dl[i]['ecommerce'] || {};
						dl_element = e['purchase'] || {};
						ret = true;
						break;
					}
				}
			} catch (e) {}

			return ret;
		},

		getProductID: function() {
			if (!this.isCatalog()) {return '';}

			var id = '';
			try {
				id = dl_element['id'] || '';
			} catch (e) {}

			return id;
		},

		getProductName: function() {
			if (!this.isCatalog()) {return '';}

			var name = '';
			try {
				name = trim(dl_element['name'] || '');

			} catch (e) {}

			return name;
		},

		getProductBrand: function() {
			if (!this.isCatalog()) {return '';}

			var brand = '';
			try {
				brand = dl_element['brand'] || '';
				brand = (brand == 'not_set' ? '' : brand);
			} catch (e) {}

			return brand;
		},

		getProductCategory: function() {
			if (!this.isCatalog()) {return '';}

			var category = '';
			try {
				category = dl_element['category'] || '';
			} catch (e) {}

			return category;
		},

		getProductDescription: function() {
			if (!this.isCatalog()) {return '';}

			var description = '';
			try {
				description = trim(innerTXT($q('.product-box .title h2')).replace(/[\r\n\t]+/g, ' ').replace(/[\s]{2,}/g, ' ').substr(0,1000));
			} catch (e) {}

			return description;
		},

		getProductPrice: function() {
			if (!this.isCatalog()) {return 0;}

			var price = 0;
			try {
				if (this.getProductOldPrice() > 0) {
					price = trim(innerTXT($q('#product_view_block_container .prcard-current-price .price-val')).replace(/[^\d]+/g, ''));
				}
				else {
					price = dl_element['price'] || 0;
				}
			} catch (e) {}

			return price;
		},

		getProductOldPrice: function() {
			if (!this.isCatalog()) {return 0;}

			var old_price = 0;
			try {
				old_price = trim(innerTXT($q('#product_view_block_container .prcard-old-price .price-val')).replace(/[^\d]+/g, ''));
			} catch (e) {}

			return old_price;
		},

		getCurrencyId: function() {
			if (!this.isCatalog()) {return 0;}

			return 1;
		},

		isProductAvailable: function() {
			if (!this.isCatalog()) {return 0;}

			var available = 1,
				el = $q('#product_view_block_container .btn--subscribe-to-item');

			if (el != null && el.style.display != 'none') {
				available = 0;
			}

			return available;
		},

		getProductImage: function() {
			if (!this.isCatalog()) {return '';}

			var image = '';
			try {
				image = $q('#product_view_block_container .prcard__slider-img').src;
			} catch (e) {}

			return image;
		},

		getCart: function() {
			if (!this.isCart()) {return false;}

			var cartArr = [];
			try {
				for (var i = 0; i < dl_element.length; i++) {
					var id = dl_element[i]['id'] || '';
					if (id) {
						cartArr.push({
							'ProductId': id
						});
					}
				}
			} catch (e) {}

			return cartArr;
		},

		getOrderID: function() {
			var ret = [];

			try {
				if (this.isOrder()) {
					//var els = $$q('#checkout-review-load .bgGrey tr:not(.sep) td:not(.sep)'),
					//	dt = new Date(), dtf = dt.toISOString().slice(0,10).replace(/-/g, ''),
					//	sa = [dtf], s = '', oid, op = 0, og = [], ogi = [];
					//
					//var dl = window['dataLayer'] || [], l = dl.length, i = 0;
					//for (; i < l; i++) {
					//	var pt = dl[i]['event'] || '';
					//	if (pt == 'checkout') {
					//		var ec = dl[i]['ecommerce'] || {},
					//			d = ec['checkout'] || {},
					//			p = d['products'] || null;
					//
					//		if (p != null) {
					//			for (var di = 0; di < p.length; di++) {
					//				var id = p[di]['id'] || '',
					//					q = parseInt(p[di]['quantity']) || 0,
					//					m = parseFloat(p[di]['price']) || 0;
					//				op += q*m;
					//
					//				og.push([id, q, m]);
					//				ogi.push(id);
					//			}
					//		}
					//		break;
					//	}
					//}
					//
					//sa.push(ogi.join('/'));
					//for (var e = 0, el = els.length; e < el; e++) {
					//	sa.push(trim(innerTXT(els[e])));
					//}
					//s = sa.join('|');
					//oid = dtf+'_'+murmurhash2_32_gc(s);

					var af = dl_element['actionField'] || {}, oid = af['id'] || '';
					if (oid) {
						var op = parseFloat(af['revenue']) || 0, og = [],
							items = dl_element['products'] || [],
							il = items.length, ii, ip, iq;

						for (ii = 0; ii < il; ii++) {
							ip = parseFloat(items[ii]['price']) || 0;
							iq = parseInt(items[ii]['quantity']) || 0;
							og.push([items[ii]['id'] || '', iq, ip]);
						}

						ret.push({
							'oid': oid,
							'op': op,
							'og': JSON.stringify(og),
							'oc': 'RUB'
						});
					}
				}
			} catch (e) {}

			if (ret.length == 0 && this.isOrder()) {
				ret = '';
			}

			return ret;
		},

		getProductClearUrl: function() {
			if (!this.isCatalog()) {return '';}

			var cUrl = '';
			try {
				//if (isPopup) {
				//	cUrl = $q('.catalog_product .go_full_view').href.replace(/#.*$/g, '');
				//}
				//else {
					cUrl = window.location.protocol + '//' + window.location.host + window.location.pathname;
				//}

				var va = document.querySelectorAll('.catalog_product .props .values_block .values .active'), val = va.length, vai = 0, tpa = [];
				for (; vai < val; vai++) {
					tpa.push(va[vai].getAttribute('data-text'));
				}
				if (tpa.length > 0) {
					cUrl += '#' + tpa.join('***');
				}
			} catch (e) {}

			return cUrl;
		},

		getCustomer: function() {
			var r = {}, ae = document.activeElement;

			//region ===== E =====
			var efc = $q('.loginForm [name="email"]'),
				efl = $q('#login-form [name="login[username]"]'),
				efr = $q('#register-form [name="email"]') || $q('#co-register-form [name="billing[email]"]'),
				eflp = $q('#login-form [name="username"]'),
				eflp2 = $q('#popup-login-form [name="username"]');
			if (eflp && eflp.offsetWidth > 0 && eflp.offsetHeight > 0) {
				r['e'] = {f: eflp};
			}
			else if (eflp2 && eflp2.offsetWidth > 0 && eflp2.offsetHeight > 0) {
				r['e'] = {f: eflp2};
			}
			else if (efl && efr && efl != ae && efr != ae) {
				r['e'] = {va: [efl.value, efr.value]};
			}
			else if (efc) {
				r['e'] = {f: efc};
			}
			//endregion ===== E =====

			//region ===== M =====
			var mfc1 = $q('.loginForm .customer-homephone [name="homephone1"]'),
				mfc2 = $q('.loginForm .customer-homephone [name="homephone2"]'),
				mfc3 = $q('.loginForm .customer-homephone [name="homephone3"]'),
				mfc4 = $q('.loginForm .customer-homephone [name="homephone4"]'),
				mfo1 = $q('#shipping-new-address-form .customer-telephone [name="billing[telephone1]"]'),
				mfo2 = $q('#shipping-new-address-form .customer-telephone [name="billing[telephone2]"]'),
				mfo3 = $q('#shipping-new-address-form .customer-telephone [name="billing[telephone3]"]'),
				mfo4 = $q('#shipping-new-address-form .customer-telephone [name="billing[telephone4]"]');
			if (
				(mfc1 && mfc2 && mfc3 && mfc4)
				||
				(mfo1 && mfo2 && mfo3 && mfo4)
			) {
				var el1 = mfc1 || mfo1,
					el2 = mfc2 || mfo2,
					el3 = mfc3 || mfo3,
					el4 = mfc4 || mfo4;
				if (el1.value && el2.value && el3.value && el4.value) {
					r['m'] = {v: el1.value + el2.value + el3.value + el4.value};
				}
			}
			//endregion ===== M =====

			//region ===== N =====
			var nfr1 = $q('#register-form [name="lastname"]') || $q('#co-register-form [name="billing[lastname]"]'),
				nfr2 = $q('#register-form [name="firstname"]') || $q('#co-register-form [name="billing[firstname]"]'),
				nfc1 = $q('.loginForm .customer-name-middlename [name="lastname"]'),
				nfc2 = $q('.loginForm .customer-name-middlename [name="firstname"]'),
				nfc3 = $q('.loginForm .customer-name-middlename [name="middlename"]');
			if (nfr1 && nfr2 && nfr1 != ae && nfr2 != ae) {
				var nr = [
					nfr1.value,
					nfr2.value
				];
				var nsr = nr.join('|');
				if (nsr != '|') {
					r['n'] = {v: nsr};
				}
			}
			else if (nfc1 && nfc2 && nfc3 && nfc1 != ae && nfc2 != ae && nfc3 != ae) {
				var nc = [
					nfc1.value,
					nfc2.value,
					nfc3.value
				];
				var nsc = nc.join('|');
				if (nsc != '||') {
					r['n'] = {v: nsc};
				}
			}
			//endregion ===== N =====

			//region ===== B =====
			var bfcd = $q('.loginForm .customer-dob [name="day"]'),
				bfcm = $q('.loginForm .customer-dob [name="month"]'),
				bfcy = $q('.loginForm .customer-dob [name="year"]');
			if (bfcd && bfcm && bfcy) {
				var b = bfcy.value + '-' + bfcm.value + '-' + bfcd.value, reg = /^\d{4}-\d{1,2}-\d{1,2}$/;
				if (reg.test(b)) {
					r['b'] = {v: b};
				}
			}
			//endregion ===== B =====

			return r;
		}
	}

}());					loadCallbackRbnt();
								if (is_request_rbnt) {
				var url_param = 'sclist[]=ltc%3D1537794343%26c_name%3Drdata_pJ2_' + '%26c_value%3D' + tmp_val;
				if (typeof window.rbnt_rt_params == 'undefined') {
										url_param = url_param + '&sclist[]=ltc%3D1530104743%26c_name%3Drd_pJ2_' + '%26c_value%3D1';
				}
				var newItem = document.createElement("img");
				newItem.src = 'https:\/\/rbnt.org\/rsc.php?'+url_param;
				newItem.style.width = '0px';
				newItem.style.height = '0px';
				newItem.style.display = 'none';
				document.body.appendChild(newItem);
			}
					} catch (e) {
			var newItemV = document.createElement("img");
			newItemV.src = 'https:\/\/rbnt.org\/lw.php?t=e&h=' + window.location + '&m=' + encodeURIComponent(e.message) + '---1---' + encodeURIComponent(document.referrer);
			newItemV.id = Math.random();
			newItemV.style.width = '0px';
			newItemV.style.height = '0px';
			newItemV.style.display = 'none';
			document.body.appendChild(newItemV);
		}
	}, 0);
}
