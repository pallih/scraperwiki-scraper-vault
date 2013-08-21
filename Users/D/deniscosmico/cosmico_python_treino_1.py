# Cosmico Python treino 1
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

import lxml.html
root = lxml.html.fromstring(html)
#dados = {}
for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    dados = {
      'Pais' : tds[0].text_content(),
      'Media de anos na escola' : int(tds[4].text_content()),
      'homem' : tds[7].text_content(),
      'mulher' : tds[9].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['Pais'], data=dados)
    print tds[0].text_content()
    print int(tds[4].text_content())




