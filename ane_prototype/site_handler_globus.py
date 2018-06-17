import site_handler_interface as interface
import standard_food_basket as SFB
import pandas as pd
from ane_tools import get_html, penc
from bs4 import BeautifulSoup
import lxml

class SiteHandlerGlobus(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = 'https://online.globus.ru'

    def extract_products(self, html):
        soup = BeautifulSoup(html, 'lxml')
        products_div = soup.find('div', {'class': 'catalog-section'})
        price_list = products_div.find_all('div', {'class': 'catalog-section__item__body trans'})

        res = []

        for price_elem in price_list:
            price_dict = dict()
            price_dict['site_title'] = price_elem.find('span', {'class': 'catalog-section__item__title'}).text
            price_dict['site_cost'] = int(price_elem.find('span', {'class': 'item-price__rub'}).text.replace(" ", ""))+\
                0.01 * int(price_elem.find('span', {'class': 'item-price__kop'}).text)
            price_dict['site_unit'] = price_elem.find('span', {'class':
                'item-price__additional item-price__additional--solo'}).text.strip()
            price_dict['site_link'] = price_elem.find('a', {'class': 'catalog-section__item__link catalog-section__item__link--one-line notrans'}).get('href')\

            res.append(price_dict)

        print(res)

        return res

    def handle_id_1(self, product):
        url = 'https://online.globus.ru/search/?section_id=638&q=' + penc(u'говядина') +\
              '&s=' + penc(u'Найти') + '&count=100'
        html = get_html(url)
        self.extract_products(html)
        # print(html)

    def byurl(self, product):
        print('byurl method for ', product['title'])

        url = 'https://online.globus.ru/search/?q=' + penc(product['keyword']) +\
              '&s=' + penc(u'Найти') + '&count=100'
        html = get_html(url)
        return self.extract_products(html)

    def byurlcompl(self, product):
        pass

    def product_handler(self, product):
        res = getattr(SiteHandlerGlobus, product['globus_method'])(self, product)
        return pd.DataFrame(res)

    def get_all_pricelists(self):
        pricelists = []
        for index, product in SFB.STANDARD_FOOD_BASKET_INFO.iterrows():
            if pd.isna(product['mask_not_process']):
                print(product)
                if pd.notna(product['globus_method']):
                    url = product['globus_link']
                    print(url)
                    pricelists.append(self.product_handler(product))
                else:
                    pricelists.append(self.cannot_handle(product))
                    # get_html()
