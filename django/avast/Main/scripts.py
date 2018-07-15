import numpy as np
from settings.settings import BASE_DIR


color_scheme = {0: '#7CB342', 1: '#FFA000', 2: '#7B1FA2'}

class ImgText:
    def __init__(self, **kwargs):
        self.img = ""
        self.text = ""
        self.title = ""
        self.table_title = ""
        self.table = ""

        if 'title' in kwargs.keys():
            self.title = kwargs['title']
        if 'img' in kwargs.keys():
            self.img = kwargs['img']
        if 'text' in kwargs.keys():
            self.text = kwargs['text']
        if 'table' in kwargs.keys():
            self.table_title = kwargs['table_title']
            self.table = kwargs['table']

# !TODO draw head of data here

# OTHER FUNCTIONS HERE -----------------------------


def call_all_funcs(data, name):
    images = []

    images.append(ImgText(**{'title': title, 'img': img, 'table_title': table_title, 'table': table}))

    return images
