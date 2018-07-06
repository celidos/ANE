from PyQt5 import QtWidgets
from PyQt5.QtCore import qDebug
from post_processing import PostProcessor

from site_handler_globus      import SiteHandlerGlobus
from site_handler_perekrestok import SiteHandlerPerekrestok
from site_handler_okey        import SiteHandlerOkey
from site_handler_ashan       import SiteHandlerAshan
from site_handler_utkonos     import SiteHandlerUtkonos
from pandas_model import PandasModel
import standard_food_basket as SFB


class PriceManager:

    def __init__(self):
        self.handlers = []
        self.handlers.append(SiteHandlerGlobus())
        self.handlers.append(SiteHandlerPerekrestok())
        self.handlers.append(SiteHandlerOkey())
        self.handlers.append(SiteHandlerUtkonos())
        self.data = None
        self.indexmap = []
        pass

    def get_all_prices_from_all_sites(self):
        self.data = []
        for handler in self.handlers:
            print('processing handler', handler.description)
            newdata = handler.get_all_pricelists()
            self.data.append((newdata, handler))
        print('done!')

        postprocessor = PostProcessor()
        postprocessor.transform(self.data)

    def load_handlers_to_table(self, listWidget):
        listWidget.clear()
        for handler in self.handlers:
            listWidget.addItem(handler.description)

    def load_available_product_prices_to_table(self, index, listWidget):
        listWidget.clear()
        self.indexmap = []
        if self.data != None:
            if self.data[index] != None:

                lst = self.data[index][0]
                # print('_______________', lst)
                for product_id in lst.keys():
                    listWidget.addItem('[' + str(product_id) + '] ' +\
                                       SFB.STANDARD_FOOD_BASKET_INFO.loc[SFB.STANDARD_FOOD_BASKET_INFO['id'] ==
                                                                    product_id].iloc[0]['title'])
                    self.indexmap.append(product_id)

    def load_price_for_product_to_table(self, handler_index, product_listitem_id, tableWidget):
        # view = QtGui.QTableView()
        # print('trying load to table...')
        cur_data = self.data[handler_index][0][self.indexmap[product_listitem_id]]
        # print('cur_data :', self.data[handler_index][0])
        model = PandasModel(self.data[handler_index][0][self.indexmap[product_listitem_id]])
        tableWidget.setModel(model)
        tableWidget.show()
        # tableWidget.QHead#  .resizeRowsToContents()
