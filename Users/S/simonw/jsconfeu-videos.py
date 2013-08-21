import scraperwiki
import lxml.html           
from dateutil import parser

urls = [
    "http://blip.tv/jsconf",
    "http://blip.tv/jsconfeu",
]

for url in urls:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for div in root.cssselect("div.EpisodeListCard"):
        title = div.cssselect("h3 a")[0].text_content()
        url = "http://blip.tv" + div.cssselect("h3 a")[0].attrib['href']
        posted = parser.parse(div.cssselect("li.ReleaseDate h6")[0].text_content())
        scraperwiki.sqlite.save(unique_keys=['url'], data={'title': title, 'url': url, 'posted': posted})

