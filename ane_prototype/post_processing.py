import pandas as pd
import re
import standard_food_basket as SFB
from ane_tools import wspex, tofloat

"""
product features:

site_title
site_cost
site_unit
site_link

"""


class PostProcessor:

    def __init__(self):

        # may be 'write only' code

        self.f_patt1 = re.compile(r'[^\d]\d{1,4}(?:[,.]\d{,3})?\s*')
        self.i_patt1 = re.compile(r'[^\d]\d{1,4}')

        self.piece_patt1 = re.compile(r'\s+(\d{1,4})\s*(?:шт|Шт|ШТ|штук).?\s*$') # group 1
        # self.weight_patt1 = re.compile(r'\s+(\d{1,4}(?:[,.]\d{,3})?)\s*(?:[гГgG]|грамм|Грамм).?\s*$') # group 1

        self.weight_patt1 = re.compile(r'\s+(?P<amount>\d{1,4}(?:[,.]\d{,4})?)'+\
                                       r'\s*(?P<unit>[гГgG]|гр|грамм|Грамм|кг|Кг|КГ'+\
                                       r'|kg|Kg|KG|мл|Мл|МЛ|[лЛlL]|шт|Шт|штук|Штук)\.?\s*(?:упаковка|пак|пакет)?'+\
                                       r'(?:в ассортименте|ассорт|в ассорт)?$')  # group 1

        self.weight_patt2 = re.compile(r'(?P<first>\d{1,4}(?:[,.]\d{,3})?)\s*'+\
                                       r'(?P<unit1>[гГgG]|гр|грамм|Грамм|мл|Мл|МЛ|шт|штуки|пак|пакетиков)?\.?\s*(?:[xXхХ*×]|по)\s*'+\
                                       r'(?P<second>\d{1,4}(?:[,.]\d{,3})?)\s*'+\
                                       r'(?P<unit2>[гГgG]|гр|грамм|Грамм|мл|Мл|МЛ|шт|штуки|пак)?.?\s*$') # iks and kha

        self.weight_patt3 = re.compile(r'(?P<first>\d{1,4}(?:[,.]\d{,3})?)'+\
                                       r'\s*[xXхХ\*×]\s*'+\
                                       r'(?P<second>\d{1,4}(?:[,.]\d{,3})?)'+\
                                       r'\s*[xXхХ\*×]\s*' +\
                                       r'(?P<third>\d{1,4}(?:[,.]\d{,3})?)'+\
                                       r'(?P<unit>[гГgG]|гр|грамм|Грамм|мл|Мл|МЛ)\.?')

        self.kg_patt1 = re.compile(r'\s+(\d{1,4}(?:[,\.]\d{,3})?)\s*(?:(?:кг|Кг|КГ)|(?:kg|Kg|KG)).?\s*$') # group 1
        # self.ml_patt1 = re.compile(r'\s+(\d{1,4}(?:[,.]\d{,3})?)\s*(?:(?:мл|Мл|МЛ)|(?:ml|Ml|ML)).?\s*$')
        # self.litre_patt1 = re.compile(r'\s+\d{1,4}(?:[,.]\d{,3})?\s*[лЛlL].?\s*$')

        self.package_per_units = ['за1уп', 'за1уп.', '1уп', '1уп.']
        self.kg_per_units    = ['за1кг', 'за1кг.', '1кг', '1кг.', 'кг']
        self.piece_per_units = ['за1шт.', 'за1шт', '1шт.', '1шт']
        self.litre_per_units = ['за1л', 'за1л.', '1л', '1л.']

        self.kg_units = ['кг', 'kg', 'килограмм']
        self.gram_units = ['г', 'g', 'грамм', 'граммов', 'гр']
        self.litre_units = ['л', 'l', 'литр', 'литров', 'литра']
        self.ml_units = ['мл', 'ml', 'миллилитров', 'миллилитра']
        self.piece_units = ['шт', 'штук', 'штуки', 'штука', 'пак', 'пакетиков', 'пак']
        self.tenpiece_units = ['10 шт', '10 шт.', '10шт', '10шт.']
        pass

    def get_coeff_by_amount_and_unit(self, amount, unit):
        if unit in (self.gram_units + self.ml_units):
            return 1000 / amount
        elif unit in self.piece_units:
            return 10 / amount
        return 1. / amount

    def extract_cost_weight(self, row):
        s_title = row['site_title']
        s_unt = wspex(row['site_unit'])
        s_cst = row['site_cost']

        print('\n\nparsing for ', s_title)

        cur_cost = None
        if s_unt in (self.litre_per_units + self.kg_per_units):
            cur_cost = s_cst
        else:

            sr = self.weight_patt2.search(s_title)
            if sr is not None:
                extracted_first = tofloat(sr.group('first'))
                extracted_second = tofloat(sr.group('second'))
                if sr.group('unit1'):
                    extracted_unit1 = sr.group('unit1')
                else:
                    extracted_unit1 = None
                if sr.group('unit2'):
                    extracted_unit2 = sr.group('unit2')
                else:
                    extracted_unit2 = None

                if extracted_unit1 is not None:
                    if extracted_unit1 in self.piece_units:
                        extracted_unit = extracted_unit2
                    else:
                        extracted_unit = extracted_unit1
                else:
                    extracted_unit = extracted_unit2

                if extracted_unit is None:
                    return None

                coeff = self.get_coeff_by_amount_and_unit(extracted_first * extracted_second, extracted_unit)

                print(' (first =', extracted_first, ' second =', extracted_second,
                      ' unit =', extracted_unit, ' coeff = ', coeff)

                cur_cost = s_cst * coeff

            else:
                sr = self.weight_patt1.search(s_title)
                if sr is not None:
                    extracted_amount = tofloat(sr.group('amount'))
                    extracted_unit = sr.group('unit')
                    coeff = self.get_coeff_by_amount_and_unit(extracted_amount, extracted_unit)
                    cur_cost = s_cst * coeff
                else:
                    sr = self.weight_patt3.search(s_title)
                    if sr is not None:
                        extracted_first = tofloat(sr.group('first'))
                        extracted_second = tofloat(sr.group('second'))
                        extracted_third = tofloat(sr.group('third'))
                        extracted_unit = sr.group('unit')
                        coeff = self.get_coeff_by_amount_and_unit(extracted_first * extracted_second *\
                                                                  extracted_third, extracted_unit)
                        cur_cost = s_cst * coeff
                    else:
                        print('**WARNING**: unknown pattern:', s_title)

                        cur_cost = None
        if cur_cost is not None:
            cur_cost = round(cur_cost, 2)
        return cur_cost


    def extract_price_cost_weight(self, price):
        cost_column = []
        for index, row in price.iterrows():
            if 'unitcost' in price.columns:
                if pd.notna(row['unitcost']):
                    cost_column.append(row['unitcost'])
                    continue
            cur_cost = self.extract_cost_weight(row)
            cost_column.append(cur_cost)

        # if 'unitcost' not in price.columns:
        price['unitcost'] = cost_column

        return price

    def extract_cost_per_unit(self, price_dict):
        for product_id in price_dict.keys():
            prod_unit = SFB.STANDARD_FOOD_BASKET_INFO.loc[SFB.STANDARD_FOOD_BASKET_INFO['id'] ==
                                                                    product_id].iloc[0]['unit']
            print('processing product_id =', product_id)
            if prod_unit in (self.kg_units + self.gram_units + self.litre_units + self.ml_units + self.tenpiece_units):
                price_dict[product_id] = self.extract_price_cost_weight(price_dict[product_id])
            else:
                print('**WARNING**: unprocessed unit:', prod_unit)
                pass

    def transform_pricelist(self, price_dict):
        self.extract_cost_per_unit(price_dict)

    def transform(self, pricelists):
        for dct, handler in pricelists:
            if handler.site_id in [3]:
                self.transform_pricelist(dct)
