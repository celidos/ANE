from PyQt5 import QtWidgets
from PyQt5.QtCore import qDebug

from site_handler_globus import SiteHandlerGlobus
from pandas_model import PandasModel
from standard_food_basket import STANDARD_FOOD_BASKET_INFO


class PriceManager:

    def __init__(self):
        self.handlers = []
        self.handlers.append(SiteHandlerGlobus())
        self.data = None
        self.indexmap = []
        pass

    def get_all_prices_from_all_sites(self):
        self.data = []
        for handler in self.handlers:
            print('processing handler', handler.description)
            newdata = handler.get_all_pricelists()
            self.data.append(newdata)
        print('done!')

    def load_handlers_to_table(self, listWidget):
        listWidget.clear()
        for handler in self.handlers:
            listWidget.addItem(handler.description)

    def load_avaiable_product_prices_to_table(self, index, listWidget):
        global STANDARD_FOOD_BASKET_INFO
        listWidget.clear()
        self.indexmap = []
        # print('hui konya')
        if self.data != None:
            if self.data[index] != None:

                lst = self.data[index]
                # print('_______________', lst)
                for product_id in lst.keys():
                    listWidget.addItem('[' + str(product_id) + '] ' +\
                                       STANDARD_FOOD_BASKET_INFO.loc[STANDARD_FOOD_BASKET_INFO['id'] ==
                                                                    product_id].iloc[0]['title'])
                    self.indexmap.append(product_id)

    def load_price_for_product_to_table(self, handler_index, product_listitem_id, tableWidget):
        # view = QtGui.QTableView()
        print('trying load to table...')
        cur_data = self.data[handler_index][self.indexmap[product_listitem_id]]
        print('cur_data :', self.data[handler_index])
        model = PandasModel(self.data[handler_index][self.indexmap[product_listitem_id]])
        tableWidget.setModel(model)
        tableWidget.show()
