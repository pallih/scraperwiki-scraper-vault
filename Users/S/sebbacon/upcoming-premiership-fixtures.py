import scraperwiki
import BeautifulSoup

from scraperwiki import datastore
from datetime import datetime

#scrape page
html = scraperwiki.scrape('http://news.bbc.co.uk/sport1/hi/football/eng_prem/fixtures/default.stm')
page = BeautifulSoup.BeautifulSoup(html)


first = page.find(True, {'class':'mvb'})
date = first.findNext('b')
fixture = date.parent.nextSibling

while date:
    while fixture and getattr(fixture, 'name', '') != 'hr':
        try:
            time = fixture.contents[-1].string
            dateob = datetime.strptime(date.string + time.strip(), "%A, %d %B %Y, %H:%M")
            home = fixture.contents[0].string
            away = fixture.contents[2].string
            data = {'date':dateob,'home':home,'away':away}
            datastore.save(unique_keys=['date','home','away'], data=data)
            fixture = fixture.nextSibling
        except (AttributeError, IndexError):
            fixture = fixture.nextSibling
    date = date.findNext('b')
    if date:
        fixture = date.parent.nextSibling