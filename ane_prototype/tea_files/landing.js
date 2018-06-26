var gs_landing_params = {"mode":"main","offers":[],"cat_id":null,"order_id":null,"mid":74323,"user_id":"462bdb5f-8dc7-4d63-a191-8984490a615f","url":"https:\u002F\u002Fwww.auchan.ru\u002Fpokupki\u002Feda\u002Fkofe-chai-sahar\u002Fchay.html","query":{"mid":"74323","mode":"main"}};

;(function () {

    try {

      function parseKeyValueList(str, pairsSeparator, keyValueSeparator) {
        var result = {},
          pairs,
          pair,
          key, value, i, l;

        if (!keyValueSeparator) {
          keyValueSeparator = '=';
        }

        if (!str) {
          return result;
        }

        pairs = str.split(pairsSeparator);
        for (i = 0, l = pairs.length; i < l; i++) {
          pair = pairs[i]
            .replace(/^\s+|\s+$/g, '')
            .split(keyValueSeparator);
          try {
            key = decodeURIComponent(pair[0]);
            value = decodeURIComponent(pair[1]);
            result[key] = value;
          } catch (e) {}
        }

        return result;
      }

      var location = document.location;
      var queryParams = parseKeyValueList(location.search.slice(1), '&');
      var href = location.href;
      var referrer = document.referrer;

      var domain = (function (){
        var domain = location.hostname || location.host.split(':')[0];
        var domainParts = domain.split('.');
        var l = domainParts.length;

        if (l > 1) {
          domain = domainParts[l - 2] + '.' + domainParts[l - 1];
        }
        return domain;
      }());

      var cookies = parseKeyValueList(document.cookie, ';');
      var cookieTtl = parseInt(queryParams._gs_cttl, 10);
      if (!cookieTtl || isNaN(cookieTtl)) {
        cookieTtl = 180;
      }

      function writeCookie(name, value) {
        if (!(name && value)) {
          return;
        }

        value = encodeURIComponent(value);

        var date = new Date();
        date.setTime(date.getTime() + cookieTtl * 24 * 60 * 60 * 1000);
        var expires = "; expires=" + date.toGMTString();
        var domainParam = 'domain=' + domain + '; ';

        document.cookie = name + "=" + value + expires + "; " + domainParam + "path=/";
      }

      function writeCookieIfEmpty(name, value) {
        if (cookies[name]) {
          return;
        }
        writeCookie(name, value);
      }

      
        writeCookie('gdeslon.ru.user_id', '462bdb5f-8dc7-4d63-a191-8984490a615f');
      

    } catch (e) {}

  

  

  

    setTimeout(function () {
    


      
        ;(function(){
          try {

            // adlabs

            (function(){function c(){if(!g){g=!0;var d=a.createElement(e);d.type="text/java"+e;var b;b="?rnd="+(100*((new Date).getTime()%1E7)+h.round(99*h.random()));
  b+=a.referrer?"&r="+encodeURIComponent(a.referrer):"";b+="&t="+(new Date).getTime();
  "undefined"!==typeof __lx__target&&(b+="&trg="+encodeURIComponent(__lx__target));
  d.src= ("https:" == document.location.protocol ? "https://ssl." : "http://") +"luxup.ru/rt/trd/1446/"+b;
  "undefined"!=typeof d&&a.getElementsByTagName(e)[0].parentNode.appendChild(d)}}var g=!1,a=document,i=a.documentElement,h=Math,f=window,e="script";c()})();

          } catch (e) {}
        }());
      
        ;(function(){
          try {

            // rbnt

            (function(){var s=document.createElement('script');s.type='text/javascript';
s.async=!0;s.src=(document.location.protocol=="https:"?"https:":"http:")+'//rbnt.org/tar.php?k=pJ2';
var x=document.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);})();

          } catch (e) {}
        }());
      
        ;(function(){
          try {

            // clickfrog_80393

            

          } catch (e) {}
        }());
      
        ;(function(){
          try {

            // smi2_81568

            

          } catch (e) {}
        }());
      
        ;(function(){
          try {

            // relap_82542

            

          } catch (e) {}
        }());
      
        ;(function(){
          try {

            // media_ruexpo_82458

            

          } catch (e) {}
        }());
      

    }, 1000);

  
}());
