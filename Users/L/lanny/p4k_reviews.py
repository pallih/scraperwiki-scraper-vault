import scraperwiki
import lxml.html
import dateutil.parser
import re

DOMAIN = 'pitchfork.com'
PROTOCOL = 'http'
BASE_URL = '/reviews/albums/'

html = scraperwiki.scrape('%s://%s%s' % (PROTOCOL, DOMAIN, BASE_URL))
root = lxml.html.fromstring(html)
review_re = re.compile('\/reviews\/albums\/\d+-.+\/$')
byline_re = re.compile('by (.+)')

for link in root.xpath('//div[@id="main"]//a'):
    if review_re.match(link.attrib.get('href', '')):
        review_url = link.attrib['href']
        duplicate = scraperwiki.sqlite.select("* FROM reviews WHERE url=? LIMIT 1", (review_url,))

        if duplicate:
            continue

        artwork_html = link.xpath('div[@class="artwork"]/div')[0].attrib.get('data-content')

        tdata = {
            'url': review_url,
            'artwork_url': lxml.html.fromstring(artwork_html).attrib.get('src'),
            'artist': link.xpath('div[@class="info"]/h1')[0].text,
            'album': link.xpath('div[@class="info"]/h2')[0].text,
            'reviewer': byline_re.match(link.xpath('div[@class="info"]/h3')[0].text).group(1),
            'published': dateutil.parser.parse(link.xpath('div[@class="info"]/h4')[0].text).date()
        }

        review_html = scraperwiki.scrape('%s://%s%s' % (PROTOCOL, DOMAIN, tdata['url']))
        review_root = lxml.html.fromstring(review_html)

        tdata['review_text'] = review_root.xpath('//div[@class="editorial"]')[0].text_content()

        scraperwiki.sqlite.save(unique_keys=['url'], data=tdata, table_name="reviews")import scraperwiki
import lxml.html
import dateutil.parser
import re

DOMAIN = 'pitchfork.com'
PROTOCOL = 'http'
BASE_URL = '/reviews/albums/'

html = scraperwiki.scrape('%s://%s%s' % (PROTOCOL, DOMAIN, BASE_URL))
root = lxml.html.fromstring(html)
review_re = re.compile('\/reviews\/albums\/\d+-.+\/$')
byline_re = re.compile('by (.+)')

for link in root.xpath('//div[@id="main"]//a'):
    if review_re.match(link.attrib.get('href', '')):
        review_url = link.attrib['href']
        duplicate = scraperwiki.sqlite.select("* FROM reviews WHERE url=? LIMIT 1", (review_url,))

        if duplicate:
            continue

        artwork_html = link.xpath('div[@class="artwork"]/div')[0].attrib.get('data-content')

        tdata = {
            'url': review_url,
            'artwork_url': lxml.html.fromstring(artwork_html).attrib.get('src'),
            'artist': link.xpath('div[@class="info"]/h1')[0].text,
            'album': link.xpath('div[@class="info"]/h2')[0].text,
            'reviewer': byline_re.match(link.xpath('div[@class="info"]/h3')[0].text).group(1),
            'published': dateutil.parser.parse(link.xpath('div[@class="info"]/h4')[0].text).date()
        }

        review_html = scraperwiki.scrape('%s://%s%s' % (PROTOCOL, DOMAIN, tdata['url']))
        review_root = lxml.html.fromstring(review_html)

        tdata['review_text'] = review_root.xpath('//div[@class="editorial"]')[0].text_content()

        scraperwiki.sqlite.save(unique_keys=['url'], data=tdata, table_name="reviews")import scraperwiki
import lxml.html
import dateutil.parser
import re

DOMAIN = 'pitchfork.com'
PROTOCOL = 'http'
BASE_URL = '/reviews/albums/'

html = scraperwiki.scrape('%s://%s%s' % (PROTOCOL, DOMAIN, BASE_URL))
root = lxml.html.fromstring(html)
review_re = re.compile('\/reviews\/albums\/\d+-.+\/$')
byline_re = re.compile('by (.+)')

for link in root.xpath('//div[@id="main"]//a'):
    if review_re.match(link.attrib.get('href', '')):
        review_url = link.attrib['href']
        duplicate = scraperwiki.sqlite.select("* FROM reviews WHERE url=? LIMIT 1", (review_url,))

        if duplicate:
            continue

        artwork_html = link.xpath('div[@class="artwork"]/div')[0].attrib.get('data-content')

        tdata = {
            'url': review_url,
            'artwork_url': lxml.html.fromstring(artwork_html).attrib.get('src'),
            'artist': link.xpath('div[@class="info"]/h1')[0].text,
            'album': link.xpath('div[@class="info"]/h2')[0].text,
            'reviewer': byline_re.match(link.xpath('div[@class="info"]/h3')[0].text).group(1),
            'published': dateutil.parser.parse(link.xpath('div[@class="info"]/h4')[0].text).date()
        }

        review_html = scraperwiki.scrape('%s://%s%s' % (PROTOCOL, DOMAIN, tdata['url']))
        review_root = lxml.html.fromstring(review_html)

        tdata['review_text'] = review_root.xpath('//div[@class="editorial"]')[0].text_content()

        scraperwiki.sqlite.save(unique_keys=['url'], data=tdata, table_name="reviews")