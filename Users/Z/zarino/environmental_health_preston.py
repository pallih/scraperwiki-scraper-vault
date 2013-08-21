import scraperwiki
import requests
import lxml.html
import re

for i in range(1,61):

    print 'scraping page #%s' % i
    url = 'http://www.environmentalhealthpreston.co.uk/display.asp?LA=Preston&PS=%s' % i
    html = requests.get(url)
    dom = lxml.html.fromstring(html.text)
    eateries = []

    for tr in dom.cssselect('table tr'):
        if tr.cssselect('td'):
            rating_source = tr.cssselect('td')[0].text_content()
            temp = {
                'name': tr.cssselect('td')[1].text,
                'address': tr.cssselect('td')[2].text,
                'url': "http://www.environmentalhealthpreston.co.uk/"+tr.cssselect('td')[3].cssselect('a')[0].get('href'),
                'rating': int(re.search("rObj = '([^']+)'", rating_source).group(1))
            }
            print '-- ' + temp['name']
            eateries.append(temp)
    
    scraperwiki.sqlite.save(['url'], eateries, 'eateries')