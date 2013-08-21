import scraperwiki           
import lxml.html
from unidecode import unidecode

raw = scraperwiki.scrape("http://www.centredoc.csst.qc.ca/alswww1.dll/APS_ZONES?fn=showprofile&q=Nouveau_enquetes&Lang=FRE")
raw = raw.decode('utf-8')
html = lxml.html.fromstring(raw)
for result in html.xpath('//div[@class="inRoundBox"]'):
    dough = {}
    for item in result.xpath('table/tr/td[4]/table/tr'):
        key, value = map(lambda x: unicode(x.text_content().strip()), item.xpath('td'))
        key = unidecode(key)
        key = key.lower()
        if key == 'titre':
            url = 'http://www.centredoc.csst.qc.ca/alswww1.dll/' + item.xpath('td')[1].xpath('a')[0].get('href')
            dough['url'] = url
        dough[key] = value
    scraperwiki.sqlite.save(unique_keys=['cote'], data=dough)