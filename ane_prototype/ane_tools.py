import urllib
import re
import requests
import datetime
import time
from random import uniform


def penc(url):
    return urllib.parse.quote(url.encode('utf8'))


def get_html_headers(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    return r.text.encode('utf-8')

def get_html(url):
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    html = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    return html


def wspex(x):
    """
    White SPace EXclude
    :param x: string
    :return: string x without any whitespaces
    """
    return re.sub(u'\u200a', '', ''.join(x.split()))

def wspex_space(x):
    return re.sub(u'\u200a', '', ' '.join(str(x).split()))

def strsim(a, b):
    return wspex_space(a).lower() == wspex_space(b).lower()

def tofloat(s):
    return float(wspex(s.replace(',', '.')))

def save_html_to_file(html, filename):
    f = open(filename, 'w')
    f.write(html)
    f.close()

def clever_sleep(last_access, cooldown):
    d = datetime.datetime.now() - last_access
    d_sec = d.days * 86400 + d.seconds + d.microseconds / 1000000.0

    if d_sec > cooldown:
        pass
    else:
        delay = cooldown + uniform(0, 0.35) * cooldown - d_sec
        print('sleeping delay for {:.2f} s...'.format(delay))
        time.sleep(delay)

    return datetime.datetime.now()

def find_float_number(str):
    sr = re.findall(r"[-+]?\d*[.,]\d+|\d+", str)
    if sr:
        return float(sr[0].replace(',','.'))
    else:
        return None