import scraperwiki
import lxml.html
from datetime import datetime

# Scrape River Thames flow conditions from Maidenhead Rowing Club observations

data_uri = 'http://www.mwronline.net/mrc/default.aspx'
table_id = 'table1'
table_skip_rows = 2
date_format = "%d/%m/%Y"
data_items = []
unique_keys = ['date']
table_name = 'observations'
data_verbose = 1

def main():
    html = scraperwiki.scrape(data_uri)
    item_els = lxml.html.fromstring(html).cssselect("#%s tr" % (table_id))
    print len(item_els)
    if len(item_els) > table_skip_rows:
        for item in item_els[table_skip_rows-1:]:
            scrape_item(item)
        scraperwiki.sqlite.save(unique_keys=unique_keys, data=data_items, table_name=table_name, verbose=data_verbose)

def scrape_item(el):
    td_els = el.findall('td')
    if (len(td_els) >= 5):
        date_str = td_els[0].text_content().strip()
        time = td_els[1].text_content().strip()
        flow = td_els[2].text_content().strip()
        temp = td_els[3].text_content().strip()
        wind_fog = td_els[4].text_content().strip()
        if (len(date_str) > 0 and len(time) > 0 and len(flow) > 0):
            date = datetime.strptime(date_str, date_format)
            if date is None:
                raise Exception('Could not parse date ' + date_str)
            data_items.append({ 'date': date.isoformat(), 'time': time.replace('.', ':'), 'flow': float(flow), 'temp': float(temp), 'wind_fog': wind_fog })

main()