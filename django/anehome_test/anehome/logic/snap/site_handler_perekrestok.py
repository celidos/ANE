import anehome_test.anehome.logic.snap.site_handler_interface as interface
import pandas as pd
from anehome_test.anehome.logic.ane_tools import get_html, wspex, wspex_space, tofloat, strsim
from bs4 import BeautifulSoup


class SiteHandlerPerekrestok(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://www.perekrestok.ru/catalog'
        self.description = r'"Перекресток"'
        self.site_id = 2
        self.pricelists = dict()
        self.site_code = 'perekrestok'
        self.site_positions_per_page = 24
        self.additional_load_products = [10, 15, 31]

    def extract_products(self, html, page=1):
        soup = BeautifulSoup(html, 'lxml')
        products_div = soup.find('div', {'class': 'catalog__items-wrap js-catalog-wrap'})
        total_amount = int(soup.find('span', {'class': 'js-list-total__total-count'}).text)
        # print('Total amount', total_amount)
        if page * self.site_positions_per_page >= total_amount:
            flag_nextpage = False
        else:
            flag_nextpage = True

        price_list = products_div.find_all('div', {'class': 'xf-product js-product '})

        res = []

        for price_elem in price_list:
            # print(price_elem, '\n\n')
            price_dict = dict()
            aref = price_elem.find('div', {'class': 'xf-product__title xf-product-title'}).\
                find('a', {'class': 'xf-product-title__link js-product__title'})
            price_dict['site_title'] = aref.text.strip()
            cost_div = price_elem.find('div', {'class': 'xf-product__cost xf-product-cost'})

            if cost_div is None:
                print('skipped position:', price_dict['site_title'])
                continue

            price_dict['site_cost'] = int(cost_div.find('span', {'class': 'xf-price__rouble'}).text)

            pennies_ans_unit = cost_div.find('span', {'class': 'xf-price__penny'}).text.strip().replace(',','.')
            pennies_ans_unit = pennies_ans_unit.split(r'/')


            # print('pennies', pennies_ans_unit)
            price_dict['site_cost'] += tofloat(pennies_ans_unit[0])
            price_dict['site_unit'] = wspex(pennies_ans_unit[1])
            price_dict['site_link'] = aref.get('href')

            # print(price_dict)

            res.append(price_dict)

        return flag_nextpage, res

    def process_single_url(self, url):
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = get_html(url + '&page=' + str(pagenum))
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1
        #
        return price

    def process_single_url_product_page(self, pos):
        print('Product page ({})'.format(self.construct_full_link(pos['site_link'])))
        html = get_html(self.construct_full_link(pos['site_link']))
        soup = BeautifulSoup(html, 'lxml')

        general_info_table = soup.find('table', {'class': 'xf-product-info__table xf-product-table'})
        table_elements_divs = general_info_table.find_all('tr', {'class': 'xf-product-table__row'})

        for row in table_elements_divs:

            th = row.find('th', {'class': 'xf-product-table__col-header'})
            td = row.find('td', {'class': 'xf-product-table__col'})

            if th and td:
                th_text = wspex_space(th.text).lower()
                if th_text.startswith('способ обработки') or th_text.startswith('вид сахара'):
                    # print('found "{}" = {}'.format('способ обработки', wspex_space(td.text)))
                    pos['site_title'] = wspex_space(td.text) + ' ' + pos['site_title']
                elif th_text =='вес':
                    pos['site_title'] = pos['site_title'] + ' весом ' + wspex_space(td.text)

        return {}

    def get_additional_info(self, price, product):
        if product['id'] in self.additional_load_products:
            for pos in price:
                # full_link = self.construct_full_link(product['site_link'])
                extracted_values = self.process_single_url_product_page(pos)

                pos.update(extracted_values)

        # guaranteed by link in the table, be careful!
        elif product['id'] == 19:
            for pos in price:
                pos['site_title'] = 'Шлифованный ' + pos['site_title']

    def product_handler(self, product):
        res = getattr(SiteHandlerPerekrestok, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

