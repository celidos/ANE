import anehome_test.anehome.logic.snap.site_handler_interface as interface
import pandas as pd
from anehome_test.anehome.logic.ane_tools import wspex_space, find_float_number, clever_sleep
from bs4 import BeautifulSoup
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
        cookie = \
            r'Utk_DvcGuid=DE1FA1B9A6F38D9FA84DEE2390FAE5EE;'+\
            r'Utk_SssTkn=4FCAFA40DB6F794DFE4A53A0C32E9185; '+\
            r'cto_lwid=00cefeb4-560d-4bac-bc42-caf8a8040422;'+\
            r' _ga=GA1.2.1618960211.1529598344;'+\
            r' SOURCE_ID=Brand; LAST_CLICK=google;'+\
            r' SOURCE_ID_client=1618960211.1529598344; '+\
            r'utm_source=google; '+\
            r'flocktory-uuid=6e4319e5-6bd6-4e92-8bfe-cb1a4a6fd146-2;'+\
            r' aprt_last_partner=google; '+\
            r'_ym_uid=15295983471010567068; '+\
            r'gr_reco=164232a8a7f-8ec9e48b37e6937d;'+\
            r' push_notify_hidden=1;'+\
            r'Utk_LncTime=2018-06-28+18%3A19%3A49%7C94FC29FB2860A68F65A1991C388C72F8;'+\
            r' SGM=82;'+\
            r' SOURCE_ID_time=Thu%2C%2028%20Jun%202018%2015%3A19%3A52%20GMT;'+\
            r' SOURCE_ID_utmz=1530199192641;'+\
            r'_gid=GA1.2.1518336458.1530199193;'+\
            r' _gac_UA-8149186-3=1.1530199194.EAIaIQobChMIqYat8NP22wIVD5SyCh1GxwX_EAAYASAAEgKFT_D_BwE;'+\
            r' _gac_UA-8149186-8=1.1530199194.EAIaIQobChMIqYat8NP22wIVD5SyCh1GxwX_EAAYASAAEgKFT_D_BwE;'+\
            r' _ym_d=1530199195;'+\
            r' _ym_isad=1;'+\
            r' _ym_visorc_942065=w;'+\
            r' CatId=14-1269-685161;'+\
            r' _gat=1;'+\
            r' _gat_googleOptimize=1;'+\
            r' _gat_UA-8149186-8=1'

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Cookie': cookie,
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


        price_list = products_div.find_all('div', {'class': 'goods_view_box-view goods_view goods_view-item'})

        if price_list == []:
            return False, []

        res = []

        for price_elem in price_list:

            price_dict = dict()

            # product_unavailable_div = price_elem.find('div', {'class': 'product-unavailable-text'})
        #     if product_unavailable_div is not None:
        #         continue # just skip
        #

            product_name_div = price_elem.find('div', {'class': 'goods_view_box-caption'})
            if product_name_div is not None:
                aref = product_name_div.find('a')
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
                price_dict['site_unit'] = str(product_price_div.get('data-weight'))[1:]

            # print(price_dict)

            res.append(price_dict)

        return flag_nextpage, res

    def process_single_url(self, url):
        # pass
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = self.get_html_custom_cookie(url + r'/page/' + str(pagenum))
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1

            # # NEED TO REMOVE!
            # return price
        #
        return price

    def product_handler(self, product):
        # print('handler')
        res = getattr(SiteHandlerUtkonos, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

