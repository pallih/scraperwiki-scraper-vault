import time
import urllib
from bs4 import BeautifulSoup as bs4
import scraperwiki

base_url = 'http://data.un.org/Handlers/DataHandler.ashx'

# load the page we reached last run
page = scraperwiki.sqlite.get_var('page', 1)

query_str = {
    'Service': 'page',
    'DataFilter': 'tableCode:240',
    'DataMartId': 'POP',
    'UserQuery': '',
    'c': '2,3,5,7,9,11,13,15,16,17',
    's': '_countryEnglishNameOrderBy:asc,refYear:desc,areaCode:asc',
    'RequestId': '428',
}

while True:
    # set the current page
    query_str['Page'] = page
    # create a URL
    page_url = '%s?%s' % (base_url, urllib.urlencode(query_str))
    # scrape!
    page_html = scraperwiki.scrape(page_url)
    # soupify!
    page_soup = bs4(page_html)
    try:
        headings
    except:
        # first time here, so fetch table headings
        headings = [x.text if x.text != u'\xa0' else u'Footnotes' for x in page_soup.table.findAll('th')]
        # convoluted way to generate the primary key
        data_key = {x: None for x in headings if x != 'Value'}.keys()

    data = None
    # fetch all table rows
    rows = page_soup.table.findAll('tr')
    # ignore the headings row
    for row in rows[1:]:
        # fetch the data
        data = dict(zip(headings, [x.text for x in row.findAll('td')]))
        # save it
        scraperwiki.sqlite.save(data_key, data)

    # we didn't find any data, so we're done
    if len(rows) <= 1:
        break

    # store the latest page reached
    scraperwiki.sqlite.save_var('page', page)

    # increment the page
    page += 1

    # rate limit
    time.sleep(1)

# reset the latest page stored
scraperwiki.sqlite.save_var('page', 0)
