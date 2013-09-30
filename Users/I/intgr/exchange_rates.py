import scraperwiki
import lxml.html
import re

digit_re = re.compile(r'-?[,.0-9]+')
def clean_number(text):
    l = digit_re.findall(text)
    if not l:
        return None
    number = l[0].replace(',', '')
    return number

def fetch_table():
    html = scraperwiki.scrape('http://www.tradingeconomics.com/exchange-rates-list-by-country')
    root = lxml.html.fromstring(html)
    
    for row in root.cssselect('#ctl00_ContentPlaceHolder1_CurrencyMatrixChanges1_GridView1 tr'):
        cols = row.cssselect('td')
        if len(cols) >= 7:
            data = {
                'pair': cols[0].text_content().strip(),
                'description': cols[1].text_content().strip(),
                'current': clean_number(cols[2].text_content()),
                'weekly_chg': clean_number(cols[3].text_content()),
                'monthly_chg': clean_number(cols[4].text_content()),
                'yearly_chg': clean_number(cols[4].text_content()),
                'ytd_chg': clean_number(cols[4].text_content()),
            }

            print data['pair'], data
            scraperwiki.sqlite.save(["pair"], data)

fetch_table()

import scraperwiki
import lxml.html
import re

digit_re = re.compile(r'-?[,.0-9]+')
def clean_number(text):
    l = digit_re.findall(text)
    if not l:
        return None
    number = l[0].replace(',', '')
    return number

def fetch_table():
    html = scraperwiki.scrape('http://www.tradingeconomics.com/exchange-rates-list-by-country')
    root = lxml.html.fromstring(html)
    
    for row in root.cssselect('#ctl00_ContentPlaceHolder1_CurrencyMatrixChanges1_GridView1 tr'):
        cols = row.cssselect('td')
        if len(cols) >= 7:
            data = {
                'pair': cols[0].text_content().strip(),
                'description': cols[1].text_content().strip(),
                'current': clean_number(cols[2].text_content()),
                'weekly_chg': clean_number(cols[3].text_content()),
                'monthly_chg': clean_number(cols[4].text_content()),
                'yearly_chg': clean_number(cols[4].text_content()),
                'ytd_chg': clean_number(cols[4].text_content()),
            }

            print data['pair'], data
            scraperwiki.sqlite.save(["pair"], data)

fetch_table()

