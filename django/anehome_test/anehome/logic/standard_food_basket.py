"""
Needs a file ./стандартная_корзина.csv laying in the same folder.


"""

import pandas as pd
import os
from anehome_test.anehome.settings.settings import BASE_DIR


sfb = None


class StandardFoodBasket:
    def __init__(self):
        self.sfb_info = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 'стандартная_корзина.csv'), sep='\t')
        self.prods = self.sfb_info[self.sfb_info['id'] != 0][['id', 'title']]
        self.prods = tuple((str(x[0]), x[1]) for x in self.prods.values)


    def get_products(self):
        # print(self.prods)
        return self.prods

    def get_product_title(self, id):
        return self.sfb_info[self.sfb_info['id'] == id]['title'].iloc[0]

    # def get_all_pricelists(self):
    #     self.pricelists = dict()
    #     for index, product in self.sfb_info.iterrows():
    #         if pd.isna(product['mask_not_process']):
    #             if pd.notna(product[self.site_code + '_method']):
    #                 self.pricelists[product['id']] = self.product_handler(product)
    #             else:
    #                 self.pricelists[product['id']] = self.cannot_handle(product)
    #
    #     return self.pricelists


sfb = StandardFoodBasket()
