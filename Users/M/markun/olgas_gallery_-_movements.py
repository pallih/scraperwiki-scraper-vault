import scraperwiki
from lxml.html import parse


def getMovements():
    soup = parse('http://www.abcgallery.com/movemind.html').getroot()
    lista = soup.cssselect("body > p")
    results = []
    movement = '?'
    for a in lista:
        links = a.cssselect("a")
        if links and links[0].get("href"):
             for m in a.cssselect("a"):
                 result = {}
                 result['movement'] = movement
                 result['url'] = "http://www.abcgallery.com/" + m.get("href")
                 result['name'] = m.text.strip()
                 result['period'] = m.tail.strip()
                 results.append(result)
        else:
            movement = a.text_content().strip()

    return results

mov = getMovements()
for data in mov:
    scraperwiki.sqlite.save(["url"], data)
import scraperwiki
from lxml.html import parse


def getMovements():
    soup = parse('http://www.abcgallery.com/movemind.html').getroot()
    lista = soup.cssselect("body > p")
    results = []
    movement = '?'
    for a in lista:
        links = a.cssselect("a")
        if links and links[0].get("href"):
             for m in a.cssselect("a"):
                 result = {}
                 result['movement'] = movement
                 result['url'] = "http://www.abcgallery.com/" + m.get("href")
                 result['name'] = m.text.strip()
                 result['period'] = m.tail.strip()
                 results.append(result)
        else:
            movement = a.text_content().strip()

    return results

mov = getMovements()
for data in mov:
    scraperwiki.sqlite.save(["url"], data)
