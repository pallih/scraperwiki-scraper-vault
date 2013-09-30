import scraperwiki
import requests
import lxml.html

html = requests.get('http://www.state.il.us/lcc/owners.asp?fn=271937028').text
dom = lxml.html.fromstring(html)

for tr in dom.cssselect('tr'):
    tds = tr.cssselect('td')
    if len(tds) == 3 and tds[0].text_content() != 'Owner Name':
        record = {
            'owner_name': tds[0].text,
            'title': tds[1].text,
            'pct_owned': float(tds[2].text)
        }
        scraperwiki.sqlite.save(['owner_name'], record)import scraperwiki
import requests
import lxml.html

html = requests.get('http://www.state.il.us/lcc/owners.asp?fn=271937028').text
dom = lxml.html.fromstring(html)

for tr in dom.cssselect('tr'):
    tds = tr.cssselect('td')
    if len(tds) == 3 and tds[0].text_content() != 'Owner Name':
        record = {
            'owner_name': tds[0].text,
            'title': tds[1].text,
            'pct_owned': float(tds[2].text)
        }
        scraperwiki.sqlite.save(['owner_name'], record)