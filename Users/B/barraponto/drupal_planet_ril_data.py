import scraperwiki
from lxml.html import parse
from urlparse import urlparse

feeds = []
dom = parse('http://drupal.org/planet').getroot()

for line in dom.cssselect('#block-drupalorg_news-planet-list .item-list li'):
    links = line.cssselect('a')
    feeds.append({
        'title': links[0].text_content(),
        'domain': urlparse(links[0].get('href'))[1],
        'feed': links[1].get('href'),
    })

scraperwiki.sqlite.save(['feed', 'title'], feeds)
import scraperwiki
from lxml.html import parse
from urlparse import urlparse

feeds = []
dom = parse('http://drupal.org/planet').getroot()

for line in dom.cssselect('#block-drupalorg_news-planet-list .item-list li'):
    links = line.cssselect('a')
    feeds.append({
        'title': links[0].text_content(),
        'domain': urlparse(links[0].get('href'))[1],
        'feed': links[1].get('href'),
    })

scraperwiki.sqlite.save(['feed', 'title'], feeds)
