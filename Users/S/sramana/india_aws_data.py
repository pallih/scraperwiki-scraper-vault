"""AWS Data collected from imdaws.com
"""

import sys
import scraperwiki
import lxml.html
import datetime

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['station_name', 'date', 'time_gmt_']


@utils.cache
def get_data(date):
    print "Processing", date
    # getting by hour because Scrperwiki is running out of memory.
    for i in range(24):
        url = 'http://www.imdaws.com/WeatherAwsData.aspx?FromDate=%s&ToDate=%s&Time=%02d' % (date, date, i)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        table = root.cssselect('table')[1]
        rows = table.cssselect('tr')
        headers = rows.pop(0)
        headers = [td.text_content() for td in headers.cssselect('td')]
        for row in rows:
            cells = [td.text_content() for td in row.cssselect('td')]
            rec = dict(zip(headers, cells))
            del rec['SR.NO.']
            utils.save(rec)


@utils.clear_cache
def main():
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    get_data(yesterday.strftime('%d/%m/%Y'))


main()
