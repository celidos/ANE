import urllib
import re


def penc(url):
    return urllib.parse.quote(url.encode('utf8'))


def get_html(url):
    # url = url.encode('utf8')
    # print('URL:', url[54:])
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    html = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    return html


def wspex(x):
    return re.sub(u'\u200a', '', ''.join(x.split()))


def tofloat(s):
    return float(wspex(s.replace(',', '.')))