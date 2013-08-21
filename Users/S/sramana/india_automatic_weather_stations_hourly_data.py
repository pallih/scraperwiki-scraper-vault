"""Hourly Weather Observation Data collected from http://www.imd.gov.in/section/nhac/aws/aws.htm
"""

import scraperwiki
import lxml.html
import dateutil.parser

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['observed_date', 'station_name', 'state']

scraperwiki.sqlite.execute("create index if not exists idx1 on swdata (observed_date, station_name, state)")


def get_hourly_data(i):
    url = 'http://www.imd.gov.in/section/nhac/aws/aws%02d.htm' % i
    html = scraperwiki.scrape(url)
    html = html.replace('&nbsp', '') # Lot of strings like this
    root = lxml.html.fromstring(html)
    date = root.cssselect('p')[0].text_content().split('/')[-1]
    observed_date = dateutil.parser.parse(date + ' %02d:00' % i)
    table = root.cssselect('table')[0]
    rows = table.cssselect('tr')
    headers = rows.pop(0)
    headers = [td.text_content() for td in headers.cssselect('td')]
    for row in rows:
        cells = [td.text_content() for td in row.cssselect('td')]
        rec = dict(zip(headers, cells))
        rec['observed_date'] = observed_date
        rec['station_name'] = rec['Name']
        del rec['Name']
        del rec['S.No']
        utils.save(rec)


def main():
    for i in range(24):
        get_hourly_data(i)


main()
