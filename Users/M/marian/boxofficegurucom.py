import scraperwiki
import lxml.html
import sys
import datetime

HOME_URL = 'http://www.boxofficeguru.com/'
SUB_PAGES = ['num', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz']

SUBSUB_PAGES = ['', '2', '3', '4']

def data_form_page(html):
    root = lxml.html.fromstring(html)
    rowcount = 0
    for tr in root.cssselect('tr'):
        if rowcount > 3:
            tds = tr.cssselect('td')
            content = []
            for td in tds:
                content.append(clean_text(td.text_content()))
            if content[0] is None:
                continue
            #print rowcount, content
            dataset = {
                'title': content[0],
                'opening': to_date(content[1]),
                'closing': to_date(content[2]),
                'weekend_info': opening_weekend(content[3]),
                'gross_total': clean_figure(content[4]),
                'gross_opening': clean_figure(content[5]),
                'theaters_opening': to_int(content[6]),
                'theaters_widest': to_int(content[7]),
                'first_week_percentage': to_float(content[8]),
                'per_theatre': to_float(clean_figure(content[9])),
                'distributor': content[10]
            }
            scraperwiki.sqlite.save(unique_keys=['title'], data=dataset)
        rowcount += 1
        

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    if text == '':
        text = None
    return text


def clean_figure(fig):
    if fig is None:
        return None
    fig = fig.replace(',', '')
    return fig


def to_float(string):
    #print [string]
    if string == '' or string is None:
        return None
    try:
        fl = float(string)
        return fl
    except ValueError:
        return None


def to_int(string):
    if string is None:
        return None
    return int(string)


def to_date(string):
    if string == '' or string is None:
        return None
    return datetime.datetime.strptime(string, '%m-%d-%y').strftime('%Y-%m-%d')


def opening_weekend(string):
    if string is None:
        return '3_DAY_OPENING_WEEKEND'
    if string == '*':
        return '4_DAY_OPENING_WEEKEND'
    if string == '^':
        return '5_DAY_OPENING_WEEKEND'
    if string == '#':
        return '2_DAY_OPENING_WEEKEND'


for page in SUB_PAGES:
    url = HOME_URL + page + '.htm'
    print url
    html = scraperwiki.scrape(url)
    rows = data_form_page(html)
    for ssp in SUBSUB_PAGES:
        url = HOME_URL + page + ssp + '.htm'
        try:
            html = scraperwiki.scrape(url)
            print url
            rows = data_form_page(html)
        except:
            continue
    #sys.exit()
import scraperwiki
import lxml.html
import sys
import datetime

HOME_URL = 'http://www.boxofficeguru.com/'
SUB_PAGES = ['num', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz']

SUBSUB_PAGES = ['', '2', '3', '4']

def data_form_page(html):
    root = lxml.html.fromstring(html)
    rowcount = 0
    for tr in root.cssselect('tr'):
        if rowcount > 3:
            tds = tr.cssselect('td')
            content = []
            for td in tds:
                content.append(clean_text(td.text_content()))
            if content[0] is None:
                continue
            #print rowcount, content
            dataset = {
                'title': content[0],
                'opening': to_date(content[1]),
                'closing': to_date(content[2]),
                'weekend_info': opening_weekend(content[3]),
                'gross_total': clean_figure(content[4]),
                'gross_opening': clean_figure(content[5]),
                'theaters_opening': to_int(content[6]),
                'theaters_widest': to_int(content[7]),
                'first_week_percentage': to_float(content[8]),
                'per_theatre': to_float(clean_figure(content[9])),
                'distributor': content[10]
            }
            scraperwiki.sqlite.save(unique_keys=['title'], data=dataset)
        rowcount += 1
        

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    if text == '':
        text = None
    return text


def clean_figure(fig):
    if fig is None:
        return None
    fig = fig.replace(',', '')
    return fig


def to_float(string):
    #print [string]
    if string == '' or string is None:
        return None
    try:
        fl = float(string)
        return fl
    except ValueError:
        return None


def to_int(string):
    if string is None:
        return None
    return int(string)


def to_date(string):
    if string == '' or string is None:
        return None
    return datetime.datetime.strptime(string, '%m-%d-%y').strftime('%Y-%m-%d')


def opening_weekend(string):
    if string is None:
        return '3_DAY_OPENING_WEEKEND'
    if string == '*':
        return '4_DAY_OPENING_WEEKEND'
    if string == '^':
        return '5_DAY_OPENING_WEEKEND'
    if string == '#':
        return '2_DAY_OPENING_WEEKEND'


for page in SUB_PAGES:
    url = HOME_URL + page + '.htm'
    print url
    html = scraperwiki.scrape(url)
    rows = data_form_page(html)
    for ssp in SUBSUB_PAGES:
        url = HOME_URL + page + ssp + '.htm'
        try:
            html = scraperwiki.scrape(url)
            print url
            rows = data_form_page(html)
        except:
            continue
    #sys.exit()
import scraperwiki
import lxml.html
import sys
import datetime

HOME_URL = 'http://www.boxofficeguru.com/'
SUB_PAGES = ['num', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'xyz']

SUBSUB_PAGES = ['', '2', '3', '4']

def data_form_page(html):
    root = lxml.html.fromstring(html)
    rowcount = 0
    for tr in root.cssselect('tr'):
        if rowcount > 3:
            tds = tr.cssselect('td')
            content = []
            for td in tds:
                content.append(clean_text(td.text_content()))
            if content[0] is None:
                continue
            #print rowcount, content
            dataset = {
                'title': content[0],
                'opening': to_date(content[1]),
                'closing': to_date(content[2]),
                'weekend_info': opening_weekend(content[3]),
                'gross_total': clean_figure(content[4]),
                'gross_opening': clean_figure(content[5]),
                'theaters_opening': to_int(content[6]),
                'theaters_widest': to_int(content[7]),
                'first_week_percentage': to_float(content[8]),
                'per_theatre': to_float(clean_figure(content[9])),
                'distributor': content[10]
            }
            scraperwiki.sqlite.save(unique_keys=['title'], data=dataset)
        rowcount += 1
        

def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    text = text.strip()
    if text == '':
        text = None
    return text


def clean_figure(fig):
    if fig is None:
        return None
    fig = fig.replace(',', '')
    return fig


def to_float(string):
    #print [string]
    if string == '' or string is None:
        return None
    try:
        fl = float(string)
        return fl
    except ValueError:
        return None


def to_int(string):
    if string is None:
        return None
    return int(string)


def to_date(string):
    if string == '' or string is None:
        return None
    return datetime.datetime.strptime(string, '%m-%d-%y').strftime('%Y-%m-%d')


def opening_weekend(string):
    if string is None:
        return '3_DAY_OPENING_WEEKEND'
    if string == '*':
        return '4_DAY_OPENING_WEEKEND'
    if string == '^':
        return '5_DAY_OPENING_WEEKEND'
    if string == '#':
        return '2_DAY_OPENING_WEEKEND'


for page in SUB_PAGES:
    url = HOME_URL + page + '.htm'
    print url
    html = scraperwiki.scrape(url)
    rows = data_form_page(html)
    for ssp in SUBSUB_PAGES:
        url = HOME_URL + page + ssp + '.htm'
        try:
            html = scraperwiki.scrape(url)
            print url
            rows = data_form_page(html)
        except:
            continue
    #sys.exit()
