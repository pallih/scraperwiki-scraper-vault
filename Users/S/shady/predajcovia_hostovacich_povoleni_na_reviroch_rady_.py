import scraperwiki
import urllib, lxml.html

url = 'http://www.srzrada.sk/index.php?n=Povolenia.Predajcovia'

f = urllib.urlopen(url)
html = f.read()
f.close()

root = lxml.html.fromstring(html)
tabulka = root.cssselect('table')

trs = tabulka[0].cssselect('tr')

for tr in trs:
    th = tr.cssselect('th')
    if ( len(th) != 0 ):
        location = th[0].text_content().rstrip()

    tds = tr.cssselect('td')
    if ( len(tds) != 0 ):
        name = tds[0].text_content().rstrip()
        if (len(name) != 0):
            data = {
                'location' : location,
                'name' : name,
                'address' : tds[1].text_content().rstrip(),
                'tel1' :  tds[2].text_content().rstrip(),
                'tel2' : tds[3].text_content().rstrip()
            }
            scraperwiki.sqlite.save(unique_keys=["name"], data=data)
