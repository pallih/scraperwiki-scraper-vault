import scraperwiki
import lxml.html
import dateutil.parser
import datetime

base_url = 'https://www.epexspot.com/en/market-data/intraday/intraday-table/'
url_tail = '/DE'

# date = dateutil.parser.parse('09/25/2006').date()
date = dateutil.parser.parse('03/09/2012').date()
today = datetime.date.today()

i = 1
while date <= today:
    datestr = str(date)
    html = scraperwiki.scrape(base_url+datestr+url_tail)
    root = lxml.html.fromstring(html)
    k = 1
    for tr in root.cssselect("tr"):
        if k >= 4 and k < 124:
            tds = tr.cssselect("td")
            data = {
                'id' : i,
                'date' : date,
                'time' : tds[1].text_content(),
                'low' : tds[2].text_content(),
                'high' : tds[3].text_content(),
                'last' : tds[4].text_content(),
                'wav' : tds[5].text_content(),
                'index' : tds[6].text_content(),
                'buyvol' : tds[7].text_content(),
                'sellvol' : tds[8].text_content(),
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
            i += 1
        k += 1
    print(date)
    date += datetime.timedelta(days=1)
