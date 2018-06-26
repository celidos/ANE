import site_handler_interface as interface
import pandas as pd
from ane_tools import wspex_space, tofloat, clever_sleep
from post_processing import PostProcessor
from bs4 import BeautifulSoup
import re
import codecs
import demjson
import time
import datetime
import requests


class SiteHandlerOkey(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://www.okeydostavka.ru/'
        self.description = r'"Окей"'
        self.site_id = 4
        self.pricelists = dict()
        self.site_code = 'okey'
        self.site_positions_per_page = 72
        self.time_cooldown = 30 # s
        self.last_time_access = datetime.datetime.now()

    def get_html_custom_cookie(self, url):
        cookie = \
r"_ga=GA1.2.1743913103.1529597174; _ym_uid=1529597174997115265; _gac_UA-58508147-1=1.1529607077.EAIaIQobChMItoj"+\
r"f2rLl2wIVjIeyCh2stAAuEAAYASAAEgLCdvD_BwE; _gid=GA1.2.654182099.1529924428; _ym_d=1529924428; _ym_isad=1; _ym_"+\
r"visorc_27891822=w; storeGroup=msk1; ffcId=13151; WC_SESSION"+\
r"_ESTABLISHED=true; WC_PERSISTENT=3EJGXVtLqH2nPYh%2FBwXZCgqDdro%3D%0A%3B2018-06-26+21%3A22%3A20.903_1530037336"+\
r"387-297473_10151; WC_AUTHENTICATION_-1002=-1002%2CshqcDFo2KYvSQjMlws143PZaUdk%3D; WC_ACTIVEPOINTER=-20%2C10151;"+\
r"WC_GENERIC_ACTIVITYDATA=[876474606%3Atrue%3Afalse%3A0%3ACLFoHnycXg06Qmg4qmgtx7v6u%2Bc%3D][com.ibm.commerce"+ \
r".context.audit.AuditContext|1530037336387-297473][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext"+\
r"|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.Globalization"+\
r"Context|-20%26RUB%26-20%26RUB][com.ibm.commerce.catalog.businesscontext.CatalogContext|12051%26null%26false%26false"+\
r"%26false][com.ibm.commerce.context.ExternalCartContext|null][com.ibm.commerce.context.base.BaseContext|10151%26-"+\
r"1002%26-1002%26-1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement"+\
r".EntitlementContext|4000000000000000003%264000000000000000003%26null%26-2000%26null%26null%26null][com.ibm."+\
r"commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; isNative=1; searchTermHistory=%7C%D1%81%D0%"+\
r"BC%D0%B5%D1%82%D0%B0%D0%BD%D0%B0; gtmListKey=GTM_LIST_SEARCH; tmr_detect=1%7C1530037350771"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Cookie': cookie,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Cache-Control': 'max-age=0'
        }
        # r = requests.get(url, headers=headers) # CRITICAL

        self.last_time_access = clever_sleep(self.last_time_access, self.time_cooldown)

        f = codecs.open("okey_smetana.html", 'r')
        html = f.read()
        # return r.text

        return html

    def extract_products(self, html, page=1):
        pass
        soup = BeautifulSoup(html, 'lxml')

        products_div = soup.find('div', {'class': 'product_listing_container'})

        # total_amount = int(soup.find('span', {'class': 'js-list-total__total-count'}).text)
        # print('Total amount', total_amount)


        # if page * self.site_positions_per_page >= total_amount:
        #     flag_nextpage = False
        # else:
        #     flag_nextpage = True
        #
        price_list = products_div.find_all('div', {'class': 'product ok-theme'})

        res = []

        if price_list == []:
            return False, []

        pproc = PostProcessor()

        for price_elem in price_list:

            price_dict = dict()

            product_unavailable_div = price_elem.find('div', {'class': 'product-unavailable-text'})
            if product_unavailable_div is not None:
                continue # just skip

            product_name_div = price_elem.find('div', {'class': 'product_name'})
            if product_name_div is not None:
                aref = price_elem.find('a')

                price_dict['site_title'] = aref.text.strip()
                price_dict['site_link'] = aref.get('href')
            else:
                price_dict['site_title'], price_dict['site_link'] = '', ''

            product_price_script = price_elem.find('script', {'id': 'productData_'})
            if product_price_script is not None:
                # print(product_price_script)
                script_text = product_price_script.text

                sr = re.search('var\s+product\s*=\s*(?P<dct>.+\});\s*$\s*', script_text, re.MULTILINE)
                if sr is not None:
                    dct_str = sr.group('dct')
                    dct = demjson.decode(dct_str) # yaml and json fails here
                    price_dict['site_price'] = dct['price']

            price_dict['site_unit'] = wspex_space(price_elem.find('div', {'class': 'product_weight'}).text)

            sunt = price_dict['site_unit'].split()
            amount, unit = tofloat(sunt[0]), sunt[1]

            price_dict['unitcost'] = price_dict['site_price'] * pproc.get_coeff_by_amount_and_unit(amount, unit)

            # print(price_dict)

            res.append(price_dict)

        return True, res

    def process_single_url(self, url):
        # pass
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = self.get_html_custom_cookie(url + '&productBeginIndex:' + str((pagenum - 1)*self.site_positions_per_page))
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1

            # NEED TO REMOVE!
            return price

        return price

    def product_handler(self, product):
        res = getattr(SiteHandlerOkey, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

