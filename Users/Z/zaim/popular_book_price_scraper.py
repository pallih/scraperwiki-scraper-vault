""" POPULAR Book Price Scraper for ScraperWiki

    TODO

        - Check if book already exist. Only overwrite if different price,
          otherwise the `date` field will always be overridden and we can't
          keep track of new/old data...
"""

import scraperwiki
import urlparse
import re

from datetime import date


BASE_URL = 'http://www.popular.com.my'

ISBN_RE  = re.compile(r'\d{13}')

PRICE_RE = re.compile(r'RM\s*(\d{1,}\.\d{2})')

zaim = scraperwiki.utils.swimport('zaim_scraper_library')

log = zaim.log


class CategoryParser(zaim.Parser):
    selectors = {
        'links': '#divRightSideContent td.writeup a.links3'
    }

    def elements(self, matches):
        return iter(matches['links'])

    def transform(self, elem):
        return (unicode(elem.text_content()), elem.attrib['href'])


class PagesParser(zaim.Parser):
    selectors = {
        'pager': '#divPagingSelection td.writeup span.copyright a'
    }

    def elements(self, matches):
        return iter(matches['pager'])

    def transform(self, elem):
        return (int(elem.text_content()), elem.attrib['href'])


class BookParser(zaim.Parser):
    selectors = {
        'isbn': 'span.t9'
    }

    def elements(self, matches):
        for elem in matches['isbn']:
            # get prices
            price_spans = elem.xpath('../span[@class="text1"]/span[@class="title2"]')
            prices = set()
            for p in price_spans:
                m = PRICE_RE.match(unicode(p.text))
                if m:
                    prices.add(float(m.group(1)))
            # get isbn codes
            isbn_text = unicode(elem.text_content())
            isbn_matches = ISBN_RE.findall(isbn_text)
            for isbn in isbn_matches:
                yield (isbn, prices)

    def transform(self, e):
        isbn, prices = e
        book = { 'isbn': isbn }
        for i, price in enumerate(prices):
            book['price_%d' % i] = price
        return book


RUN_TIME = None

def scrape_section(d, url):
    log.info('scraping section: %s', url)
    html = scraperwiki.utils.scrape(url)
    category_parser = CategoryParser()
    categories = category_parser.parse(html)
    books = []
    for title, cat_url in categories:
        cat_url = urlparse.urljoin(BASE_URL, cat_url)
        books.extend(scrape_category(d, title, cat_url))
    return books

def scrape_category(d, title, url):
    log.info('scraping category: %s: %s', title, url)
    html = scraperwiki.utils.scrape(url)
    pages_parser = PagesParser()
    pages = pages_parser.parse(html)
    books = []
    for num, page_url in pages:
        page = html if num == 1 else None
        page_url = urlparse.urljoin(BASE_URL, page_url)
        books.extend(scrape_page(d, page_url, page))
    return books

def scrape_page(d, url, html=None):
    log.info('scraping page: %s', url)
    if not html:
        html = scraperwiki.utils.scrape(url)
    parser = BookParser()
    books = []
    for book in parser.parse(html):
        #log.info(book)
        book['date'] = d
        books.append(book)
    log.info('found %d books', len(books))
    return books

def save(books):
    log.info('saving total %d books', len(books))
    scraperwiki.sqlite.save(['isbn'], books, 'books')

def run():
    run_date = date.today()
    sections = [
        'Item_Main.aspx?IT=1',  # english/malay books
        'Item_Main.aspx?IT=2',  # chinese books
    ]
    books = []
    for s in sections:
        url = urlparse.urljoin(BASE_URL, s)
        books.extend(scrape_section(run_date, url))
    save(books)

run() # Lola, run!
