import scraperwiki
import lxml.html
import re

urls = ['http://www.fussball-lux.lu/Nationalspieler1.html','http://www.fussball-lux.lu/Nationalspieler2.html']
baseurl = 'http://www.fussball-lux.lu/'


def process_player(url,name):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    trs = root.xpath ('//tr/td')
    #for tr in trs[2:5]:
    for tr in trs:
        #tds = tr.xpath ('td')
        print tr.text_content()
        #for td in tds:
        #    print td.text_content()

def get_players(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    links = root.xpath ('//a')
    for link in links:
        detail_url = baseurl + link.attrib['href']
        name = link.text
        process_player(detail_url,name)

for url in urls:
    get_players(url)