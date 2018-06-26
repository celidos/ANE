import site_handler_interface as interface
import standard_food_basket as SFB
import pandas as pd
from ane_tools import get_html, get_html_headers, penc, wspex, tofloat
from bs4 import BeautifulSoup
import requests
import re
import json
import yaml


class SiteHandlerAshan(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://www.auchan.ru'
        self.description = r'"Ашан"'
        self.site_id = 3
        self.pricelists = dict()
        self.site_code = 'ashan'
        self.site_positions_per_page = 96

    def get_html_custom_cookie(self, url):
        cookie = \
r"rrpvid=329389679545328; rcuid=5aca01941fd5d500019edd5b; rrlpuid=; _ga=GA1.2.1339962274.1529155045;"+\
r"cto_lwid=223ded34-6060-4d69-a5d2-89f7ea4d70a3; _ym_uid=1529155045368704387; PHPSESSID=3t7pr3ukr2g0"+\
r"r8233ftgrta7sh; _cid=WQ0oumgKljG0vdJv; user_shop_id=1; user_shop_id_render=1; user_shop_name=%25D0"+\
r"%259C%25D0%25BE%25D1%2581%25D0%25BA%25D0%25B2%25D0%25B0; find_city_question=1; scs=%7B%22t%22%3A1%"+\
r"7D; gdeslon.ru.user_id=462bdb5f-8dc7-4d63-a191-8984490a615f; spUID=15291550518513c1e415807.aaca32d"+\
r"9; selected_shop=1338; selected_shop_name=%D0%90%D0%B2%D0%B8%D0%B0%D0%BF%D0%B0%D1%80%D0%BA; select"+\
r"ed_shop_url=%2Fru%2Faviapark; _gid=GA1.2.1234119899.1529930359; _ym_d=1529930360; shownCampCount=%"+\
r"7B%22camps%22%3A%5B%221661%22%5D%7D; current-currency=RUB; rrsmf=3; rrlevt=1529930454766; _ems_vis"+\
r"itor=1305482314.875033461; X-AUHP=nw5; _ym_visorc_24584168=w; _ym_isad=1; ins-gaSSId=b93a894c-e734"+\
r"-1ac9-4d5d-6bef6773c737_1530012779; _gac_UA-49770337-2=1.1530009553.EAIaIQobChMIl9u8p5Dx2wIVFeAZCh"+\
r"3OKwypEAAYASAAEgJ5e_D_BwE; _ems_session=1305482314.695254406; cartGenericId=CART5802bc77327372dd7b"+\
r"57572c05af715a%7C1530010457; tmr_detect=1%7C1530010721790; _gat_UA-49770337-2=1; insdrSV=69"+\
r"; __srqat=17"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Cookie': cookie,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Cache-Control': 'max-age=0'
        }
        r = requests.get(url, headers=headers)
        return r.text

    def extract_products(self, html):
        soup = BeautifulSoup(html, 'lxml')

        script_divs = soup.find_all('script')
        price_script = ''
        for script in script_divs:
            script = str(script)
            if script.find('var productListBlockJson') > -1:
                price_script = script
                fr = re.search(r'var productListBlockJson\s*=\s*(?P<dct>.+\});\s*$\s*', script, flags=re.MULTILINE)
                dct_str = fr.group('dct')

                dct = json.loads(dct_str)

                res = []
                for product in dct['products']:
                    price_dict = dict()
                    price_dict['site_title'] = product['name']
                    price_dict['site_cost'] = product['price']
                    price_dict['site_link'] = product['url']
                    price_dict['site_unit'] = 'unknown'

                    print(price_dict)

                    res.append(price_dict)
                return res
        return []

    def extract_pages(self, html):
        soup = BeautifulSoup(html, 'lxml')

        script_divs = soup.find_all('script')
        for script in script_divs:
            script = str(script)
            if script.find('var productListBlockJson') > -1:
                fr = re.search(r'var productListBlockJson\s*=\s*(?P<dct>.+\});\s*$\s*', script, flags=re.MULTILINE)
                dct_str = fr.group('dct')

                dct = json.loads(dct_str)

                pages = dct['toolbarInitData']['pagerInitData']['pages']
                pages_list = [x['url'] for x in pages]
                return pages_list
        return []

    def process_single_url(self, url):
        pages_list = self.extract_pages(self.get_html_custom_cookie(url))

        price = []
        for url_paged in pages_list:
            html = self.get_html_custom_cookie(url_paged)
            newblock = self.extract_products(html)
            price.extend(newblock)

        return price

    def product_handler(self, product):
        res = getattr(SiteHandlerAshan, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

