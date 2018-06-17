import site_handler_interface as interface
import standard_food_basket as SFB
import pandas as pd
from ane_tools import get_html, penc
from bs4 import BeautifulSoup
import lxml

class SiteHandlerGlobus(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = 'https://online.globus.ru'
        self.description = '"Глобус"'

    def extract_products(self, html, page=1):
        soup = BeautifulSoup(html, 'lxml')
        products_div = soup.find('div', {'class': 'catalog-section'})

        amount_div = soup.find('div', {'class': 'catalog-content'})
        total_amount = int(amount_div.find('h1').find('sub').text.split(' ')[0])
        if page * 64 >= total_amount:
            flag_nextpage = False
        else:
            flag_nextpage = True

        print('TOTAL', total_amount)
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

        print('  For product {} results has beed found'.format(len(res)), sep='')

        return flag_nextpage, res

    def handle_id_1(self, product):
        url = 'https://online.globus.ru/search/?section_id=638&q=' + penc(u'говядина') +\
              '&s=' + penc(u'Найти') + '&count=64'
        html = get_html(url)
        self.extract_products(html)
        # print(html)

    def process_single_url(self, url):
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = get_html(url + '&PAGEN_2=' + str(pagenum))
        # html = get_html(url)
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1

        return price

    def byurls(self, product):
        print('byurl for', product['title'])

        urls = list(filter(None, product['globus_url'].split(' ')))

        # url = 'https://online.globus.ru/search/?q=' + penc(product['keyword']) +\
        #       '&s=' + penc(u'Найти') + '&count=100'

        price = []
        for url in urls:
            price.extend(self.process_single_url(url))
        return price

    def byurlcompl(self, product):
        pass

    def product_handler(self, product):
        res = getattr(SiteHandlerGlobus, product['globus_method'])(self, product)
        # print('RES HERE: \n\n', res)
        return pd.DataFrame(res)

    def get_all_pricelists(self):
        pricelists = dict()
        for index, product in SFB.STANDARD_FOOD_BASKET_INFO.iterrows():
            if pd.isna(product['mask_not_process']):
                # print(product)
                if pd.notna(product['globus_method']):
                    # url = product['globus_url']
                    # print(url)
                    pricelists[product['id']] = self.product_handler(product)
                else:
                    pricelists[product['id']] = self.cannot_handle(product)
                    # get_html()
        return pricelists
