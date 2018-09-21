from anehome_test.anehome.settings.settings import BASE_DIR
from anehome_test.anehome.logic.ane_tools import read_dict
from anehome_test.anehome.logic.standard_food_basket import sfb
from anehome_test.anehome.logic.avaiable_site_handlers import SITE_HANDLERS, SITE_CODE_TO_HANDLER

from anehome_test.anehome.logic.snap.post_processing import PostProcessor
import json
from anehome_test.anehome.logic.ane_tools import create_folder

# from pandas_model import PandasModel # deprecated Qt
from anehome_test.anehome.logic import standard_food_basket as sfb

from anehome_test.anehome.global_status import GlobalStatus


import re
import datetime
import os
import pandas as pd

ANE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
SNAPSHOTS_DIR = os.path.join(ANE_DIR, 'snapshots')


class Snapshot:
    def __init__(self, snap_folder_name=None):
        # self.something = None

        self.snap_date = None
        self.snap_folder_name = snap_folder_name
        self.snap_content_dir = None
        self.flag_full_load = False
        self.info = None  # should be dict

        self.basket = None                    # таблица корзины
        self.site_prices = {}                 # таблицы магазинов

        self.indexmap = []                    # ??
        self.pathprefix = r'./../../snapshots/'  # ??

        if snap_folder_name:
            self.load_from_folder(snap_folder_name)

    def is_valid(self):
        if self.info:
            if 'finished' in self.info:
                return self.info['finished']
        return False

    def load_from_folder(self, snap_folder_name, full_load=False):
        self.snap_folder_name = snap_folder_name

        sr = re.search(
            '\Asnap_(?P<year>\d+)_(?P<month>\d+)_(?P<day>\d+)__(?P<hour>\d+)_(?P<minute>\d+)_(?P<second>\d+)$',
            snap_folder_name)
        if sr:
            self.snap_date = datetime.datetime(year=int(sr.group('year')),
                                               month=int(sr.group('month')),
                                               day=int(sr.group('day')),
                                               hour=int(sr.group('hour')),
                                               minute=int(sr.group('minute')),
                                               second=int(sr.group('second')))

            self.snap_content_dir = os.path.join(SNAPSHOTS_DIR, snap_folder_name)

            self.info = read_dict(os.path.join(self.snap_content_dir,
                                               'info.txt'))

            if 'done' not in self.info:
                self.info['done'] = {}

            if 'type' not in self.info:
                self.info['type'] = 'broken'

            if self.info['type'] == 'gks':
                full_load = True

            if self.info['finished']:
                if 'basket' in self.info['done']:
                    self.basket = pd.read_csv(os.path.join(self.snap_content_dir,
                                                    'basket.csv'), sep='\t')
                if full_load:
                    for handler in SITE_HANDLERS:
                        site_price_file = os.path.join(self.snap_content_dir,
                                                    handler.site_code + '_acc.csv')
                        print('site_price_file', site_price_file)
                        if handler.site_code in self.info['done']:
                            if os.path.exists(site_price_file):
                                if os.path.isfile(site_price_file):
                                    self.site_prices[handler.site_code] = \
                                        pd.read_csv(site_price_file, sep='\t')

                    self.flag_full_load = True
        else:
            self.info = {'finished': False, 'type': 'broken'}

    def get_product_choose_form_options(self):
        if not self.flag_full_load:
            self.load_from_folder(self.snap_folder_name, full_load=True)

        if self.info['type'] == 'normal':
            return sfb.sfb.get_products()
        elif self.info['type'] == 'gks':
            return ('gks', 'Служба государственной статистики')

    def get_site_choose_form_options(self):
        if not self.flag_full_load:
            self.load_from_folder(self.snap_folder_name, full_load=True)

        options = []
        for handler in SITE_HANDLERS:
            if handler.site_code in self.site_prices.keys():
                options.append((handler.site_code, handler.description))

        return tuple(options)

    def get_by_site_and_product(self, site_name, product_id):
        if not self.flag_full_load:
            self.load_from_folder(self.snap_folder_name, full_load=True)

        if site_name == 'gks':
            response = self.site_prices['gks'].to_dict('records')
            return response

        # print(self.site_prices[site_name].keys())

        response = self.site_prices[site_name]\
            [self.site_prices[site_name]['product_id'] == int(product_id)].to_dict('records')
        return response

    def get_basket(self):
        data = self.basket.drop(self.basket[self.basket['id'] == 0].index)
        # data['']

    # --------------------------------------------------------

    def construct_snapname(self, date=None):
        if date is None:
            return datetime.datetime.now().strftime("snap_%Y_%m_%d__%H_%M_%S")
        else:
            return date.strftime("snap_%Y_%m_%d__%H_%M_%S")

    def calculate_basket(self, save_to_file=False, fullpath=''):
        df = []
        SFB = sfb.sfb.sfb_info

        for product_id in SFB['id']:
            prod = SFB.loc[SFB['id'] == product_id].iloc[0]
            prod_dict = {'id': product_id, 'title': prod['title']}
            if product_id != 0:
                for handler_code, data in self.site_prices.items():
                    print('getting up with basket and ', handler_code)
                    print(data)

                    # if product_id in data['product_id']:

                    data_slice = data[data['product_id'] == product_id]

                    print('calculating siteunit for product {} in the {}'.format(product_id,
                                                                                 handler_code))
                    if 'unitcost' in data_slice.columns:
                        siteunit = data_slice['unitcost'].min(skipna=True)
                    else:
                        siteunit = None

                    if siteunit is not None:
                        prod_dict[handler_code + '_unit'] = siteunit
                        prod_dict[handler_code + '_total'] = round(siteunit * prod['req_amount'], 2)
                    else:
                        prod_dict[handler_code + '_unit'] = None
                        prod_dict[handler_code + '_total'] = None
            df.append(prod_dict)

        df = pd.DataFrame(df)
        if save_to_file:
            df.to_csv(fullpath, sep='\t')

        self.info['done'].append('basket')
        return df

    def concat_to_single_df(self, dct):
        to_concat = [df for df in dct.values() if type(df) is not dict]
        for x in dct.values():
            print(type(x))
        return pd.concat(to_concat)

    def validate_completeness(self):
        if self.info['type'] == 'normal':
            for handler in SITE_HANDLERS:
                if handler.site_code != 'gks':
                    if handler.site_code not in self.site_prices.keys():
                        self.info['warnings'].append('Не обработан магазин {}'.format(handler.description))
                        continue

                    SFB = sfb.sfb.sfb_info

                    for product_id in SFB['id']:
                        if product_id not in self.site_prices[handler.site_code]['product_id'].values:
                            self.info['warnings'].append('Магазин {} - нет данных по товару "{}"'\
                                                         .format(handler.description,
                                                                 SFB[SFB['id'] == product_id]['title']))
                            continue

                        data_slice = self.site_prices[handler.site_code][self.site_prices[handler.site_code]['product_id'] == product_id]
                        slice_min = data_slice['site_cost'].min()
                        if pd.isna(slice_min):
                            self.info['warnings'].append('Магазин {}, товар "{}" - ошибочная цена ({})'\
                                                         .format(handler.description,
                                                                 SFB[SFB['id'] == product_id]['title'],
                                                                 slice_min))
                        elif slice_min < 2.0:
                            self.info['warnings'].append('Магазин {}, товар "{}" - ошибочная цена ({})'\
                                                         .format(handler.description,
                                                                 SFB[SFB['id'] == product_id]['title'],
                                                                 slice_min))


    def get_snapshot(self, save_to_file=False, type='normal', handlers=None):
        self.info = dict()
        self.info['finished'] = 0
        self.info['type'] = type
        self.info['done'] = []
        self.info['warnings'] = []
        self.snap_date = datetime.datetime.now()
        self.snap_date = self.snap_date.replace(microsecond=0)
        self.snap_folder_name = self.construct_snapname(self.snap_date) + r'/'
        full_snap_path = self.pathprefix + self.snap_folder_name
        if save_to_file:
            create_folder(full_snap_path)
            with open(full_snap_path + 'info.txt', 'w') as file:
                file.write(json.dumps(self.info))

        if type == 'normal':
            if handlers is None:
                handlers = SITE_HANDLERS
            it = 0
            for handler in handlers:
                GlobalStatus().setstatus('Готовим снапшот: обработка {} ({}/{})'.\
                                         format(handler.description, it, len(handlers) - 1))
                if handler.site_code != 'gks':
                    print('processing handler', handler.description)
                    newdata = handler.get_all_pricelists()
                    self.site_prices[handler.site_code] = newdata
                    self.info['done'].append(handler.site_code)
                it += 1
            print('---------- SITE HANDLERS done! ----------')
        elif type == 'gks':
            for handler in SITE_HANDLERS:
                if handler.site_code == 'gks':
                    print('processing handler', handler.description)
                    newdata = handler.get_all_pricelists()
                    self.site_prices[handler.site_code] = newdata
                    self.info['done'].append(handler.site_code)
            print('---------- SITE HANDLERS done! ----------')

        postprocessor = PostProcessor()
        for handler in SITE_HANDLERS:
            if handler.site_code in self.site_prices:
                postprocessor.transform(self.site_prices[handler.site_code], handler)

        for key in self.site_prices.keys():
            self.site_prices[key] = self.concat_to_single_df(self.site_prices[key])

        self.validate_completeness()

        self.info['finished'] = 1
        if save_to_file:
            for key, data in self.site_prices.items():  # todo
                all_goods = self.site_prices[key]
                all_goods.to_csv(full_snap_path + key + '_acc.csv', sep='\t')

            self.basket = self.calculate_basket(save_to_file=save_to_file,
                                                fullpath=full_snap_path + 'basket.csv')

            with open(full_snap_path + 'info.txt', 'w') as file:
                file.write(json.dumps(self.info))

        self.flag_full_load = True