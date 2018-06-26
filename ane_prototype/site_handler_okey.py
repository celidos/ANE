import site_handler_interface as interface
import standard_food_basket as SFB
import pandas as pd
from ane_tools import get_html, get_html_headers, penc, wspex, tofloat
from bs4 import BeautifulSoup
import yaml
import re


class SiteHandlerOkey(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'https://www.okeydostavka.ru/'
        self.description = r'"Окей"'
        self.site_id = 4
        self.pricelists = dict()
        self.site_code = 'okey'
        self.site_positions_per_page = 72


    def extract_products(self, html, page=1):
        pass
        soup = BeautifulSoup(html, 'lxml')

        print('noooo!')

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

        for price_elem in price_list:
            print(price_elem, '\n\n')
            price_dict = dict()

            product_name_div = price_elem.find('div', {'class': 'product_name'})
            if product_name_div is not None:
                aref = price_elem.find('a')

                price_dict['site_title'] = aref.text.strip()
                price_dict['site_link'] = aref.get('href')
            else:
                price_dict['site_title'], price_dict['site_link'] = '', ''

            product_price_script = price_elem.find('script', {'id': 'productData_'})
            if product_price_script is not None:
                print(product_price_script)
                script_text = product_price_script.text

                print(re.search('(?<=var product = ).+$', script_text).group(0))
                return False, []
                # txt = product_price_script.find(lambda tag: tag.name == 'span' and
                #                                           tag.get('class').startswith('price label')).\
                    # get('value').split('руб.')[0]
                # price_dict['site_cost'] = tofloat(txt)
            # else:
                # price_dict['site_cost'] = -6666.66

            price_dict['site_unit'] = price_elem.find('div', {'class': 'product_weight'}).text

        #         find('a', {'class': 'xf-product-title__link js-product__title'})
        #     price_dict['site_title'] = aref.text.strip()
        #     cost_div = price_elem.find('div', {'class': 'xf-product__cost xf-product-cost'})
        #
        #     if cost_div is None:
        #         print('skipped position:', price_dict['site_title'])
        #         continue
        #
        #     price_dict['site_cost'] = int(cost_div.find('span', {'class': 'xf-price__rouble'}).text)
        #
        #     pennies_ans_unit = cost_div.find('span', {'class': 'xf-price__penny'}).text.strip().replace(',','.')
        #     pennies_ans_unit = pennies_ans_unit.split(r'/')
        #
        #
        #     # print('pennies', pennies_ans_unit)
        #     price_dict['site_cost'] += tofloat(pennies_ans_unit[0])
        #     price_dict['site_unit'] = wspex(pennies_ans_unit[1])
        #     price_dict['site_link'] = aref.get('href')
        #
            print(price_dict)

        #     res.append(price_dict)
        #
        return True, res

    def process_single_url(self, url):
        # pass
        price = []
        pagenum = 1
        nextpage = True
        while nextpage:
            html = get_html(url + '&productBeginIndex:' + str((pagenum - 1)*self.site_positions_per_page))
            nextpage, newblock = self.extract_products(html, page=pagenum)
            price.extend(newblock)
            pagenum += 1

        return price

    def product_handler(self, product):
        res = getattr(SiteHandlerOkey, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)

