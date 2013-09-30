import scraperwiki
import lxml.html
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')

def raagatop10(lang):
    html = scraperwiki.scrape('http://www.raaga.com/channels/' + lang + '/top10.asp')
    root = lxml.html.fromstring(html)
    titles = [x.text for x in root.cssselect('a') if x.get('onclick') and x.get('onclick').find('setList1') >= 0]
    albums = [x.text for x in root.cssselect('td td td a') if x.get('href').find('/channels/' + lang + '/moviedetail.asp') >= 0]
    for i in xrange(0,len(titles)):
        data = {'date':today, 'lang': lang, 'rank': i+1, 'title': titles[i], 'album': albums[i] }
        scraperwiki.datastore.save(unique_keys=['date', 'lang', 'rank'], data=data)

raagatop10('hindi')
raagatop10('tamil')
import scraperwiki
import lxml.html
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')

def raagatop10(lang):
    html = scraperwiki.scrape('http://www.raaga.com/channels/' + lang + '/top10.asp')
    root = lxml.html.fromstring(html)
    titles = [x.text for x in root.cssselect('a') if x.get('onclick') and x.get('onclick').find('setList1') >= 0]
    albums = [x.text for x in root.cssselect('td td td a') if x.get('href').find('/channels/' + lang + '/moviedetail.asp') >= 0]
    for i in xrange(0,len(titles)):
        data = {'date':today, 'lang': lang, 'rank': i+1, 'title': titles[i], 'album': albums[i] }
        scraperwiki.datastore.save(unique_keys=['date', 'lang', 'rank'], data=data)

raagatop10('hindi')
raagatop10('tamil')
