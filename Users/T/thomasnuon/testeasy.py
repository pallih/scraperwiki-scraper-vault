import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.easyswitch.nl/energie/vergelijk-energie/overzicht?isBusiness=false&form=&postcode=9724%20EM&home=3&old_postcode=&old_home=&connection=null&single_meter=true&electricity=3500&usage-category=&electricity-night=&gas=1800&old-supplier=5&552b176013071c7f51d20e82b0610934=88218781eecda4f342fc7e9a68f16661&__utma=40708022.1126211654.1360070469.1360070469.1360070469.1&__utmb=40708022.2.10.1360070469&__utmc=40708022&__utmz=40708022.1360070469.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)&Itemid=38&ref=")
print html
root = lxml.html.fromstring(html)

for tr in root.cssselect("div result-table tr"):
    tds = tr.cssselect("td")
    if len(tds)==7:
        data = {
            'aanbieding' : tds[2].text_content()
        }
        print data.text_content()
import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.easyswitch.nl/energie/vergelijk-energie/overzicht?isBusiness=false&form=&postcode=9724%20EM&home=3&old_postcode=&old_home=&connection=null&single_meter=true&electricity=3500&usage-category=&electricity-night=&gas=1800&old-supplier=5&552b176013071c7f51d20e82b0610934=88218781eecda4f342fc7e9a68f16661&__utma=40708022.1126211654.1360070469.1360070469.1360070469.1&__utmb=40708022.2.10.1360070469&__utmc=40708022&__utmz=40708022.1360070469.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)&Itemid=38&ref=")
print html
root = lxml.html.fromstring(html)

for tr in root.cssselect("div result-table tr"):
    tds = tr.cssselect("td")
    if len(tds)==7:
        data = {
            'aanbieding' : tds[2].text_content()
        }
        print data.text_content()
