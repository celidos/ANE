import site_handler_interface as interface
import standard_food_basket as SFB
import pandas as pd
from ane_tools import get_html, penc, wspex, tofloat
from bs4 import BeautifulSoup



class SiteHandlerPerekrestok(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://www.perekrestok.ru/catalog'
        self.description = r'"Перекресток"'
        self.site_id = 2
        self.pricelists = dict()
        self.site_code = 'perekrestok'
        self.site_positions_per_page = 24

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

    def product_handler(self, product):
        res = getattr(SiteHandlerPerekrestok, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

