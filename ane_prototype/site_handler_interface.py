from PyQt5 import QtWidgets
from PyQt5.QtCore import qDebug
import standard_food_basket as SFB

class SiteHandlerInterface:

    def __init__(self):
        self.site_prefix = r'https://example.com'
        self.site_id = 0
        pass

    def product_handler(self, product):
        pass

    def cannot_handle(self, product):
        print('cannot handle', product['title'], '!')
        return pd.DataFrame()
        pass

    def get_all_pricelists(self):
        pass

    def get_table(self):
        pass

'''
product features:

site_title
site_cost
site_unit
site_link

'''