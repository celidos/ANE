import pandas as pd
import re
import standard_food_basket as SFB


"""
product features:

site_title
site_cost
site_unit
site_link

"""


def wspex(x):
    return ''.join(x.split())


def tofloat(s):
    return float(wspex(s.replace(',', '.')))


class PostProcessor:

    def __init__(self):

        # may be 'write only' code

        self.f_patt1 = re.compile(r'[^\d]\d{1,4}(?:[,.]\d{,3})?\s*')
        self.i_patt1 = re.compile(r'[^\d]\d{1,4}')

        self.piece_patt1 = re.compile(r'\s+(\d{1,4})\s*(?:шт|Шт|ШТ|штук).?\s*$') # group 1
        # self.weight_patt1 = re.compile(r'\s+(\d{1,4}(?:[,.]\d{,3})?)\s*(?:[гГgG]|грамм|Грамм).?\s*$') # group 1

        self.weight_patt1 = re.compile(r'\s+(?P<amount>\d{1,4}(?:[,.]\d{,3})?)'+\
                                       r'\s*(?P<unit>[гГgG]|грамм|Грамм|кг|Кг|КГ'+\
                                       r'|kg|Kg|KG|мл|Мл|МЛ|[лЛlL]).?\s*$')  # group 1

        self.gram_patt2 = re.compile(r'(\d{1,4}(?:[,.]\d{,3})?)\s*[xXхХ\*×]\s*(\d{1,4}(?:[,.]\d{,3})?)') # iks and kha
        self.kg_patt1 = re.compile(r'\s+(\d{1,4}(?:[,.]\d{,3})?)\s*(?:(?:кг|Кг|КГ)|(?:kg|Kg|KG)).?\s*$') # group 1
        # self.ml_patt1 = re.compile(r'\s+(\d{1,4}(?:[,.]\d{,3})?)\s*(?:(?:мл|Мл|МЛ)|(?:ml|Ml|ML)).?\s*$')
        # self.litre_patt1 = re.compile(r'\s+\d{1,4}(?:[,.]\d{,3})?\s*[лЛlL].?\s*$')

        self.package_per_units = ['за1уп', 'за1уп.', '1уп', '1уп.']
        self.kg_per_units    = ['за1кг', 'за1кг.', '1кг', '1кг.']
        self.piece_per_units = ['за1шт.', 'за1шт', '1шт.', '1шт']
        self.litre_per_units = ['за1л', 'за1л.', '1л', '1л.']

        self.kg_units = ['кг', 'kg', 'килограмм']
        self.gram_units = ['г', 'g', 'грамм', 'граммов']
        self.litre_units = ['л', 'l', 'литр', 'литров', 'литра']
        self.ml_units = ['мл', 'ml', 'миллилитров', 'миллилитра']
        self.piece_units = ['шт', 'штук', 'штуки', 'штука']
        self.tenpiece_units = ['10 шт', '10 шт.', '10шт', '10шт.']
        pass

    def get_coeff_by_amount_and_unit(self, amount, unit):


    def extract_cost_pieces(self, row):
        s_title = row['site_title']
        s_unt = wspex(row['site_unit'])
        s_cst = row['site_cost']

        cur_cost = -6.6612345
        if s_unt in self.package_per_units:
            sr = self.piece_patt1.search(s_title)
            if sr is not None:
                pieces = tofloat(self.i_patt1.search(sr.group(0)).group(0))
                cur_cost = s_cst * 10 / pieces
            else:
                print('**WARNING**: unknown unit (pieces):', s_unt)

        cur_cost = round(cur_cost, 2)
        return cur_cost

    def extract_price_cost_pieces(self, price):
        cost_column = []
        for index, row in price.iterrows():
            cur_cost = self.extract_cost_pieces(row)
            cost_column.append(cur_cost)

        price['unitcost'] = cost_column
        return price

    def extract_cost_kg(self, row):
        s_title = row['site_title']
        s_unt = wspex(row['site_unit'])
        s_cst = row['site_cost']

        cur_cost = -1.2345
        if s_unt in self.kg_per_units:
            cur_cost = s_cst
        elif s_unt in (self.package_per_units + self.piece_per_units):
            sr = self.gram_patt1.search(s_title)
            if sr is not None:
                grams = tofloat(self.f_patt1.search(sr.group(0)).group(0))
                cur_cost = s_cst * 1000 / grams
            else:
                # кг case
                sr = self.kg_patt1.search(s_title)
                if sr is not None:
                    kilograms = tofloat(self.f_patt1.search(sr.group(0)).group(0))
                    cur_cost = s_cst / kilograms
        else:
            print('**WARNING**: unknown unit (kg)', s_unt)

        cur_cost = round(cur_cost, 2)
        return cur_cost

    def extract_price_cost_kg(self, price):
        cost_column = []
        print('type =', type(price))
        for index, row in price.iterrows():
            cur_cost = self.extract_cost_kg(row)
            cost_column.append(cur_cost)

        price['unitcost'] = cost_column
        return price

    def extract_cost_weight(self, row):
        s_title = row['site_title']
        s_unt = wspex(row['site_unit'])
        s_cst = row['site_cost']

        cur_cost = -1.2345
        if s_unt in self.litre_per_units:
            cur_cost = s_cst
        else:
            sr = self.ml_patt1.search(s_title)
            if sr is not None:
                millilitres = tofloat(self.f_patt1(sr.group(0)).group(0))
                cur_cost = s_cst * 1000 / millilitres
            else:
                # л case
                sr = self.litre_patt1.search(s_title)
                if sr is not None:
                    litres = tofloat(self.f_patt1(sr.group(0)).group(0))
                    cur_cost = s_cst / litres
                else:
                    cur_cost = self.extract_cost_kg(row)
        cur_cost = round(cur_cost, 2)
        return cur_cost

    def extract_price_cost_weight(self, price):
        cost_column = []
        for index, row in price.iterrows():
            cur_cost = self.extract_cost_litres(row)
            cost_column.append(cur_cost)

        price['unitcost'] = cost_column
        return price

    def extract_cost_per_unit(self, price_dict):
        for product_id in price_dict.keys():
            prod_unit = SFB.STANDARD_FOOD_BASKET_INFO.loc[SFB.STANDARD_FOOD_BASKET_INFO['id'] ==
                                                                    product_id].iloc[0]['unit']
            if prod_unit in (self.kg_units + self.gram_units + self.litre_units + self.ml_units):
                price_dict[product_id] = self.extract_price_cost_weight(price_dict[product_id])
            elif prod_unit in ['10 шт', '10 шт.', '10шт', '10шт.']:
                price_dict[product_id] = self.extract_price_cost_pieces(price_dict[product_id])
            else:
                print('**WARNING**: unprocessed unit:', prod_unit)
                pass

    def transform_pricelist(self, price_dict):
        self.extract_cost_per_unit(price_dict)

    def transform(self, pricelists):
        for dct, handler in pricelists:
            if handler.site_id in [1]:
                self.transform_pricelist(dct)
