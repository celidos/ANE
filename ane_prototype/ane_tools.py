import urllib
import re
import requests


def penc(url):
    return urllib.parse.quote(url.encode('utf8'))


def get_html_headers(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    return r.text.encode('utf-8')

def get_html(url):
    # url = url.encode('utf8')
    # print('URL:', url[54:])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    html = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    return html


def wspex(x):
    return re.sub(u'\u200a', '', ''.join(x.split()))


def tofloat(s):
    return float(wspex(s.replace(',', '.')))

def save_html_to_file(html, filename):
    f = open(filename, 'w')
    f.write(html)
    f.close()