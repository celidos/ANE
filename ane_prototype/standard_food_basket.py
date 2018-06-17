import pandas as pd

STANDARD_FOOD_BASKET_INFO = None


def read_standard_food_basket_params():
    global STANDARD_FOOD_BASKET_INFO
    STANDARD_FOOD_BASKET_INFO = pd.read_csv('./стандартная_корзина.csv', sep='\t')


read_standard_food_basket_params()
