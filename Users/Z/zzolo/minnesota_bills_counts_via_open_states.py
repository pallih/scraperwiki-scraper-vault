import scraperwiki
import demjson
import datetime
import dateutil.parser
import lxml.html  

# Please don't steal this key
os_key = "49c5c72c157d4b37892ddb52c63d06be"
os_query = "http://openstates.org/api/v1/bills/?state=MN&search_window=session:2013-2014&apikey=%s" % os_key

# Get data
raw = scraperwiki.scrape(os_query)
json = demjson.decode(raw)

# Total number of bills
data = {
    'stat': 'total-bills',
    'value': len(json)
}
scraperwiki.sqlite.save(unique_keys = ['stat'], data = data)

# Get number of bills updated or created in the
# past two weeks
def count_date_type(stype):
    count = {}
    
    for b in json:
        dt = dateutil.parser.parse(b['%s_at' % stype])
        dt_key = '%s-%04d-%02d-%02d' % (stype, dt.year, dt.month, dt.day)
        dt_sort = '%04d%02d%02d' % (dt.year, dt.month, dt.day)
    
        if dt_key in count:
            count[dt_key]['count'] = count[dt_key]['count'] + 1
        else:
            count[dt_key] = {
                'count': 1,
                'sort': int(dt_sort)
            }
    
    for k, v in count.items():
        data = {
            'stat': k,
            'value': v['count'],
            'int': v['sort']
        }
        scraperwiki.sqlite.save(unique_keys = ['stat'], data = data)

count_date_type('updated')
count_date_type('created')


# Get cound of bills (search with revisor)
def search_count(url, key):
    html = scraperwiki.scrape(url)         
    root = lxml.html.fromstring(html)
    h2s = root.cssselect('div#leg_PageContent h2')
    parts = h2s[0].text_content().split()
    
    data = {
        'stat': key,
        'value': int(parts[0])
    }
    scraperwiki.sqlite.save(unique_keys = ['stat'], data = data)

passed_url = 'https://www.revisor.mn.gov/bills/status_result.php?body=House&search=basic&session=0882013&location=House&bill=&bill_type=bill&rev_number=&keyword_type=all&keyword=&keyword_field_text=1&action%5B%5D=1413&submit_action=GO&titleword'
signed_url = 'https://www.revisor.mn.gov/bills/status_result.php?body=House&search=basic&session=0882013&location=House&bill=&bill_type=bill&rev_number=&keyword_type=all&keyword=&keyword_field_text=1&action%5B%5D=1338&submit_action=GO&titleword='

search_count(passed_url, 'total-bills-passed')
search_count(signed_url, 'total-bills-signed')

