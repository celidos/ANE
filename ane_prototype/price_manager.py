from PyQt5 import QtWidgets
from PyQt5.QtCore import qDebug
from post_processing import PostProcessor
import datetime
import json
import pandas as pd
from ane_tools import create_folder

from site_handler_globus      import SiteHandlerGlobus
from site_handler_perekrestok import SiteHandlerPerekrestok
from site_handler_okey        import SiteHandlerOkey
from site_handler_ashan       import SiteHandlerAshan
from site_handler_utkonos     import SiteHandlerUtkonos
from site_handler_gks         import SiteHandlerGks
from pandas_model import PandasModel
import standard_food_basket as SFB



class Snapshot:

    def __init__(self):
        self.handlers = []
        self.handlers.append(SiteHandlerGlobus())
        # self.handlers.append(SiteHandlerPerekrestok())
        # self.handlers.append(SiteHandlerOkey())
        # self.handlers.append(SiteHandlerUtkonos())

        self.handlers.append(SiteHandlerGks())
        self.data = None
        self.indexmap = []
        self.pathprefix = r'./../snapshots/'
        pass

    def construct_snapname(self):
        return datetime.datetime.now().strftime("snap_%y_%m_%d__%H_%M_%S")

    # def collapse_dict(self, data):
        #
        #
        # for tbl in data.values():
            # t

    def get_snapshot(self, save_to_file=False):

        info_dict = dict()
        if save_to_file:
            snap_path = self.pathprefix + self.construct_snapname() + r'/'
            create_folder(snap_path)
            info_dict['finished'] = 0
            with open(snap_path + 'info.txt', 'w') as file:
                file.write(json.dumps(info_dict))

        self.data = []
        for handler in self.handlers:
            print('processing handler', handler.description)
            newdata = handler.get_all_pricelists()
            self.data.append((newdata, handler))
        print('done!')

        postprocessor = PostProcessor()
        postprocessor.transform(self.data)

        if save_to_file:
            for data, handler in self.data:
                if handler.site_id not in [-1]:
                    all_goods = pd.concat(data.values())
                    all_goods.to_csv(snap_path + handler.site_code + '_acc.csv')
            info_dict['finished'] = 1
            with open(snap_path + 'info.txt', 'w') as file:
                file.write(json.dumps(info_dict))

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
