import scraperwiki
import lxml.html
import scraperwiki
import re
import urlparse
from BeautifulSoup import BeautifulSoup


def scrape_table(html_arg):
    html = scraperwiki.scrape(html_arg)

    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table[class='registry-search-results sticky-enabled'] tr[class='odd']"):
        tds = tr.cssselect("td")
        scrape_page("http://www.reaa.govt.nz" + tds[0].cssselect('a')[0].get('href'))

    for tr in root.cssselect("table[class='registry-search-results sticky-enabled'] tr[class='even']"):
        tds = tr.cssselect("td")
        scrape_page("http://www.reaa.govt.nz" + tds[0].cssselect('a')[0].get('href'))

    if root.cssselect("a[title='Go to next page']")[0].get('href'):
        scrape_table("http://www.reaa.govt.nz" + root.cssselect("a[title='Go to next page']")[0].get('href'))


def scrape_page(html_arg):
    html = scraperwiki.scrape(html_arg)
    root = lxml.html.fromstring(html)

    record = {}  
    record['first name'] = ''
    record['last name'] = ''
    record['preferred name'] = ''
    record['email address'] = ''
    record['phone number'] = ''
    record['company address'] = ''

    for tr in root.cssselect("div[class='first-name']"):
        data_string = tr.text_content()
        data_string = re.sub('First name:', '', data_string)
        data_string = re.sub('\\n ', '', data_string)
        data_string = re.sub(' ', '', data_string)
        record['first name'] = data_string

    for tr in root.cssselect("div[class='last-name']"):
        data_string = tr.text_content()
        data_string = re.sub('Last name:', '', data_string)
        data_string = re.sub('\\n ', '', data_string)
        data_string = re.sub(' ', '', data_string)
        record['last name'] = data_string

    for tr in root.cssselect("div[class='other-names']"):
        data_string = tr.text_content()
        data_string = re.sub('Preferred name\(s\):', '', data_string)
        data_string = re.sub('\\n ', '', data_string)
        data_string = re.sub(' ', '', data_string)
        record['preferred name'] = data_string

    for tr in root.cssselect("div[class='address']"):
        data_string = tr.text_content()
        if data_string.count('Email:') > 0:
            data_string = re.sub('Email:', '', data_string)
            data_string = re.sub('\\n ', '', data_string)
            data_string = re.sub(' ', '', data_string)
            record['email address'] = data_string
        elif data_string.count('Phone:') > 0:
            data_string = re.sub('Phone:', '', data_string)
            data_string = re.sub('\\n ', '', data_string)
            data_string = re.sub(' ', '', data_string)
            record['phone number'] = data_string
        else:
            data_string = re.sub('Address Information:', '', data_string)
            data_string = re.sub('\\n ', '', data_string)
            record['company address'] = data_string.strip()
    
    scraperwiki.sqlite.save(['first name', 'last name'], data=record, table_name='REAA Scrape')




scrape_table('http://www.reaa.govt.nz/registry/search/licensees?page=549&licence_number=1&type=licensees&h=c659df0cbd6ae4f7a59ebf303f68a2ee')