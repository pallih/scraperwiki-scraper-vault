import urllib2
import scraperwiki
import lxml.html           

url = 'http://www.london2012.com/archery/event/men-individual/phase=arm070900/index.html'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
headers = {
    'User-Agent': user_agent,
    'Accept': '*/*',
}
request = urllib2.Request(url, headers=headers)
html = urllib2.urlopen(request).read()

root = lxml.html.fromstring(html)
for n, tr in enumerate(root.cssselect("table.or-tbl tr")):
    try:
        data = {
            'back_no': tr.cssselect("td")[1].text_content(),
            'name': tr.cssselect("td")[2].text_content(),
            'country': tr.cssselect("td img.or-fgs")[0].attrib['alt'],
        }
        print n, data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
    except:
        pass

