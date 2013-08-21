import scraperwiki
import mechanize
import lxml.html
from datetime import datetime

def scrape_table(root, date):
    headers = []
    for header in root.find_class('headerdatatable')[0]:
        headers.append(''.join(s for s in header.text_content() if s.isalnum()))
    results = []
    for row in root.find_class('dataresults'):
        d = {'DataAsOf':date}
        for i, col in enumerate(row):
            try:
                d[headers[i]] = str(col.text_content())
            except UnicodeEncodeError:
                pass
        results.append(d)
    scraperwiki.sqlite.save(unique_keys = ['Ticker', 'DataAsOf'], data=results,
            table_name='etf_data')

def main():
    br = mechanize.Browser()
    br.open('http://www.indexuniverse.com/data/data.html')
    query_root = lxml.html.fromstring(br.response().read())
    etfs = query_root.cssselect('div[id="divEtfOnly"]')[0] 
    etf_attributes = [d.attrib['value'] for d in etfs.cssselect('input[id="cbDataPoints"]')]
    br.select_form(name='DataQuery')
    br['dataPoints[]'] = etf_attributes
    html = br.submit().read()
    root = lxml.html.fromstring(html)
    n = int(root.find_class('pageLinks')[0].text_content().split(' ')[-1])
    date_string = root.find_class('dateData2')[0].text_content()[-10:]
    date = datetime.strptime(date_string, '%m/%d/%Y')
    scrape_table(root, date)
    for i in range(50, n, 50):
        url = 'http://www.indexuniverse.com/data/data.html?task=showResults&start={}&direction=ASC'.format(i)
        html = br.open(url).read()
        root = lxml.html.fromstring(html)
        scrape_table(root, date)

main()
