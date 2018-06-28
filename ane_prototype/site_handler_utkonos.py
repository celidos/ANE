import site_handler_interface as interface
import pandas as pd
from ane_tools import wspex_space, find_float_number, clever_sleep
from post_processing import PostProcessor
from bs4 import BeautifulSoup
import re
import codecs
import demjson
import time
import datetime
import requests


class SiteHandlerUtkonos(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://www.utkonos.ru/'
        self.description = r'"Утконос"'
        self.site_id = 5
        self.pricelists = dict()
        self.site_code = 'utkonos'
        self.site_positions_per_page = 90
        self.time_cooldown = 0 # s
        self.last_time_access = datetime.datetime.now()

    def get_html_custom_cookie(self, url):
        cookie = ''

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            # 'Cookie': cookie,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Cache-Control': 'max-age=0'
        }

        print('loading url', url)

        r = requests.get(url, headers=headers) # CRITICAL

        self.last_time_access = clever_sleep(self.last_time_access, self.time_cooldown)

        # f = codecs.open("okey_smetana.html", 'r')
        # html = f.read()
        return r.text

        # return html

    def representsInt(self, s):
        try:
            intnumber = int(s)
            return intnumber
        except ValueError:
            return None

    def extract_products(self, html, page=1):
        pass
        soup = BeautifulSoup(html, 'lxml')

        products_div = soup.find('div', {'class': 'goods_view_box'})

        if products_div is None:
            return False, []

        pages_controller_div = soup.find('div', {'class': 'el_paginate'})
        if pages_controller_div is None:
            flag_nextpage = False
        else:
            pages_refs = pages_controller_div.find_all('a', {'class': 'hoverover'})

            max_page_index = 1
            for ref in pages_refs:
                page_index = self.representsInt(ref.text.strip())
                if page_index is not None:
                    if page_index > max_page_index:
                        max_page_index = page_index
            if max_page_index > page:
                flag_nextpage = True
            else:
                flag_nextpage = False

        # # if page * self.site_positions_per_page >= total_amount:
        # #     flag_nextpage = False
        # # else:
        # #     flag_nextpage = True

        price_list = products_div.find_all('div', {'class': 'goods_view_box-view goods_view goods_view-item'})

        if price_list == []:
            return False, []

        res = []

        # pproc = PostProcessor()
        #
        for price_elem in price_list:

            price_dict = dict()

            # product_unavailable_div = price_elem.find('div', {'class': 'product-unavailable-text'})
        #     if product_unavailable_div is not None:
        #         continue # just skip
        #

            product_name_div = price_elem.find('div', {'class': 'goods_view_box-caption'})
            if product_name_div is not None:
                aref = price_elem.find('a')
                if aref is not None:
                    price_dict['site_title'] = wspex_space(aref.text)
                    price_dict['site_link'] = aref.get('href')
                else:
                    price_dict['site_title'], price_dict['site_link'] = '', ''
            else:
                price_dict['site_title'], price_dict['site_link'] = '', ''

            product_price_div = price_elem.find('div', {'class': 'goods_price-item current'})
            if product_price_div is not None:
                price_dict['site_cost'] = find_float_number(product_price_div.text)
                price_dict['site_unit'] = product_price_div.get('data-weight')

        #     product_price_script = price_elem.find('script', {'id': 'productData_'})
        #     if product_price_script is not None:
        #         # print(product_price_script)
        #         script_text = product_price_script.text
        #
        #         sr = re.search('var\s+product\s*=\s*(?P<dct>.+\});\s*$\s*', script_text, re.MULTILINE)
        #         if sr is not None:
        #             dct_str = sr.group('dct')
        #             dct = demjson.decode(dct_str) # yaml and json fails here
        #             price_dict['site_price'] = dct['price']
        #
        #     weight_div = price_elem.find('div', {'class': 'product_weight'})
        #     if weight_div is None:
        #         print('[okey] For product', price_dict['site_title'], ' weight not found!')
        #         continue
        #
        #     price_dict['site_unit'] = wspex_space(weight_div.text)
        #
        #     if not price_dict['site_unit'].startswith('Цена за'):
        #
        #         sunt = price_dict['site_unit'].split()
        #         amount, unit = tofloat(sunt[0]), sunt[1]
        #
        #         price_dict['unitcost'] = price_dict['site_price'] * pproc.get_coeff_by_amount_and_unit(amount, unit)
        #     else:
        #         price_dict['unitcost'] = None
        #
            print(price_dict)
        #
            res.append(price_dict)
        #
        return flag_nextpage, res

    def process_single_url(self, url):
        pass
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = self.get_html_custom_cookie(url + r'/page/' + str(pagenum))
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1

            # NEED TO REMOVE!
            return price
        #
        return price

    def product_handler(self, product):
        res = getattr(SiteHandlerUtkonos, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

