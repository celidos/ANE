import standard_food_basket as SFB
import pandas as pd

class SiteHandlerInterface:

    def __init__(self):
        self.site_prefix = r'https://example.com'
        self.site_id = -1
        self.site_code = ''
        self.pricelists = dict()
        pass

    def construct_full_link(self, url):
        return self.site_prefix + url

    def product_handler(self, product):
        # to do
        pass

    def cannot_handle(self, product):
        print('cannot handle', product['title'], '!')
        return pd.DataFrame()

    def process_single_url(self, url):
        # to do
        return []

    def process_single_url_product_page(self, prod_dict):
        return dict()

    def skip(self, product):
        pass
        return []

    def byurls(self, product):
        print('byurl for', product['title'], '...', end='')

        urls = list(filter(None, product[self.site_code + '_url'].split(' ')))

        price = []
        for url in urls:
            price.extend(self.process_single_url(url))
        print('total', len(price), 'results!')

        self.get_additional_info(price, product)

        return price

    def get_additional_info(self, price, product):
        pass

    def get_all_pricelists(self):
        self.pricelists = dict()
        for index, product in SFB.STANDARD_FOOD_BASKET_INFO.iterrows():
            if pd.isna(product['mask_not_process']):
                if pd.notna(product[self.site_code + '_method']):
                    self.pricelists[product['id']] = self.product_handler(product)
                else:
                    self.pricelists[product['id']] = self.cannot_handle(product)

        return self.pricelists

'''
product features:

site_title
site_cost
site_unit
site_link

'''