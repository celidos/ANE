import anehome_test.anehome.logic.snap.site_handler_interface as interface
import pandas as pd
from anehome_test.anehome.logic.ane_tools import get_html, penc
from bs4 import BeautifulSoup


class SiteHandlerGlobus(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://online.globus.ru'
        self.description = r'"Глобус"'
        self.site_id = 1
        self.pricelists = dict()
        self.site_code = 'globus'
        self.site_positions_per_page = 64

    def extract_products(self, html, page=1):
        soup = BeautifulSoup(html, 'lxml')
        products_div = soup.find('div', {'class': 'catalog-section'})

        if products_div is None:
            return False, []

        amount_div = soup.find('div', {'class': 'catalog-content'})
        total_amount = int('0'+amount_div.find('h1').find('sub').text.split(' ')[0])
        if page * self.site_positions_per_page >= total_amount:
            flag_nextpage = False
        else:
            flag_nextpage = True

        # print('TOTAL', total_amount)
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

        # print('  For product {} results has beed found'.format(len(res)), sep='')

        return flag_nextpage, res

    def process_single_url(self, url):
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = get_html(url + '&PAGEN_2=' + str(pagenum))
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1

        return price

    def product_handler(self, product):
        res = getattr(SiteHandlerGlobus, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)
