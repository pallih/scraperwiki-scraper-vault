import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.domain.hu/domain/varolista/ido.html')
root = lxml.html.fromstring(html)
data = []
for row in root.cssselect("table.tt tr"):           
    cells = row.cssselect('td')
    if cells:
        data.append(dict(domain=cells[1].text_content(), owner=cells[2].text_content(), date=cells[3].text_content()))
scraperwiki.sqlite.save(unique_keys=['domain', 'date'], data=data)
import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.domain.hu/domain/varolista/ido.html')
root = lxml.html.fromstring(html)
data = []
for row in root.cssselect("table.tt tr"):           
    cells = row.cssselect('td')
    if cells:
        data.append(dict(domain=cells[1].text_content(), owner=cells[2].text_content(), date=cells[3].text_content()))
scraperwiki.sqlite.save(unique_keys=['domain', 'date'], data=data)
