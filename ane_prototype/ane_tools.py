import urllib


def get_html(url):
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    html = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    return html


def penc(url):
    return urllib.parse.quote(url.encode('utf8'))