import anehome_test.anehome.logic.snap.site_handler_interface as interface
import pandas as pd
import urllib
import requests
from anehome_test.anehome.logic.ane_tools import tofloat, wspex_space
from bs4 import BeautifulSoup


class SiteHandlerGks(interface.SiteHandlerInterface):

    def __init__(self):
        self.site_prefix = r'http://www.gks.ru/dbscripts/cbsd/DBInet.cgi'
        self.description = r'Федеральная служба государственной статистики'
        self.site_id = 0
        self.pricelists = dict()
        self.site_code = 'gks'

    def extract_products(self, html):
        soup = BeautifulSoup(html, 'lxml')
        products_table = soup.find('table', {'class': 'OutTbl'})
        price_list_divs = products_table.find_all('tr')

        res = []
        if not price_list_divs:
            return []

        for price_elem in price_list_divs:
            tds = price_elem.find_all('td')
            if tds[0].get('class') != 'TblShap' and wspex_space(tds[0].text):
                price_dict = dict()
                price_dict['site_title'] = tds[0].text
                price_dict['unitcost'] = tofloat(tds[1].text)

                res.append(price_dict)

        return res

    def process_table(self, product):
        url = 'http://www.gks.ru/dbscripts/cbsd/DBInet.cgi'
        values = {
            'rdLayoutType': 'Au',
            '_Pokazateli': 'on',
            '_sengoroda': 'on',
            '_grtov': 'on',
            '_god': 'on',
            '_period': 'on',
            'a_Pokazateli': '1',
            'a_sengoroda': '2',
            'a_period': '3',
            'Qry': 'Pokazateli:1921003;sengoroda:45000000;grtov:111,113,116,114,411,501,701,801,1001,1111,1102,1106,1201,1501,1601,1701,1711,1903,2002,2004,2101,2201,2203,2301,2303,2306,2401,2501,2601,2603,2605,2621,2701;god:2018;period:5;',
            'QryGm': 'Pokazateli_z:1;sengoroda_z:2;period_z:3;god_s:1;grtov_b:1;',
            'QryFootNotes': ';',
            'YearsList': '2013;2014;2015;2016;2017;2018;'
        }
        data = urllib.parse.urlencode(values)
        r = requests.post(url, data=data)
        r.encoding = 'cp1251'
        html = r.text
        return self.extract_products(html)

    def product_handler(self, product):
        res = getattr(SiteHandlerGks, product[self.site_code + '_method'])(self, product)
        return pd.DataFrame(res)
