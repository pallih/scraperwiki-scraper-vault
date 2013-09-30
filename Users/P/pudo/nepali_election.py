import requests
from lxml import html
from itertools import count
import scraperwiki

TABLE_URL = 'http://www.election.gov.np/reports/CAResults/FPTP/Districtwise/%s.php?'

for i in count(1):
    print i
    res = requests.get(TABLE_URL % i)
    doc = html.fromstring(res.content)
    header = doc.find('.//p').text
    print [header]
    rows = doc.findall('.//tr')
    cols = rows[2].findall('td')
    headers = map(lambda c: c.text, cols)
    for n, tr in enumerate(rows[3:]):
        cols = tr.findall('td')
        vals = map(lambda c: c.text, cols)
        if not len(vals) or vals[0] is None:
            continue
        data = dict(zip(headers, vals))
        data['header'] = header
        data['key'] = '%s-%s' % (i, n)
        scraperwiki.sqlite.save(unique_keys=['key'], data)