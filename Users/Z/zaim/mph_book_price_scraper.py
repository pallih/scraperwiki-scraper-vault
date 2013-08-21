""" MPH Book Price Scraper for ScraperWiki
"""

import scraperwiki
import re
import urlparse
import logging
import resource

from datetime import date
from lxml.html import soupparser


zaim = scraperwiki.utils.swimport('zaim_scraper_library')

log = logging.getLogger('zaim_scraper_library')


MPH_BASE_URL = "http://www.mphonline.com"

PRICE_REGEX  = re.compile(r'\D*(?P<price>\d+\.\d{2})')

ISBN_QS_KEY  = 'pcode'


def parse_price_text(text):
    match = PRICE_REGEX.match(text)
    if match:
        price_str = match.group('price')
        return float(price_str)
    return 0

def parse_isbn_url(url):
    """ Parse isbn from url querystring
    """
    parts = urlparse.urlparse(url)
    query = urlparse.parse_qs(parts.query)
    if ISBN_QS_KEY in query and len(query[ISBN_QS_KEY]):
        return query[ISBN_QS_KEY][0]


class BooklistingParser(zaim.Parser):
    selectors = {
        'books': '#MPHOnline_ContentPlaceHolder1_LblContentVal table.booklisting'
    }

    def elements(self, matches):
        return iter(matches['books'])

    def transform(self, elem):
        book = {}

        # 1. get book link <A> element, and ISBN code
        
        try:
            link = elem.cssselect('td[valign="top"][height="50"] > a[href]')[0]
        except IndexError:
            raise AssertionError('table.booklisting is missing a book title <A> element')

        url = unicode(link.attrib['href']).strip()

        assert url, 'table.booklistng book title <A> element yielded an empty HREF'

        book['isbn'] = parse_isbn_url(url)

        assert book['isbn'], 'table.booklisting book title <A> element contains no ISBN code'

        # 2. get book price

        bookdesc_tds = elem.cssselect('td.bookdesc')
        try:
            price_td = bookdesc_tds[1]
            # NOTE: bookdesc_tds[0] is a td with the book's description, we ignore this
            # on purpose, we'll get detailed book info later using other APIs, now we're
            # only interested in price listings.
        except IndexError:
            raise AssertionError('table.booklisting has incorrect number of td.bookdesc, cannot get price')
        else:
            pt = price_td.text_content()
            book['price_normal'] = parse_price_text(pt)
            book['__pnt'] = pt

        # 3. get other price listing (e.g. online price)

        if len(bookdesc_tds) > 2:
            # online price is usually the 3rd td.bookdesc
            op = bookdesc_tds[2].text_content()
            book['price_online'] = parse_price_text(op)
            book['__pot'] = op

        return book


class ThumbnailParser(zaim.Parser):
    selectors = {
        'titles': '#MPHOnline_ContentPlaceHolder1_LblContentVal td.para > table span.title',
        'prices': '#MPHOnline_ContentPlaceHolder1_LblContentVal td.para > span.title > font[color="#5A564E"]'
    }

    def elements(self, matches):
        titles = matches['titles']
        prices = matches['prices']
        if not len(titles) == len(prices):
            raise AssertionError('title and price element counts do not match')
        return zip(titles, prices)

    def transform(self, elem):
        title, price = elem
        book  = {}
        price_text = unicode(price.text_content()).strip()
        book['price_normal'] = parse_price_text(price_text)
        book['__pnt'] = price_text
        try:
            link_a = title.cssselect('a[href]')[0]
        except IndexError, err:
            raise AssertionError('td.para has no <A> element')
        else:
            url = unicode(link_a.attrib['href']).strip()
            assert url, 'td.para book title <A> element yielded an empty HREF'
            book['isbn']  = parse_isbn_url(url)
            assert book['isbn'], 'td.para book title <A> element contains no ISBN code'
        return book


class TotalAvailableBooksParser(zaim.Parser):
    selectors = {
        'product_count': '#MPHOnline_ContentPlaceHolder1_LblContentVal td.disproduct > font[color="#cc0033"] > b'
    }

    def elements(self, matches):
        return iter(matches['product_count'])

    def transform(self, elem):
        try:
            return int(elem.text_content())
        except (ValueError, TypeError):
            return 0

    def get_value(self, html):
        counts = [c for c in self.parse(html)]
        if counts:
            return max(counts)
        return 0


class MPHScraper(zaim.Scraper):
    parser_classes = (BooklistingParser, ThumbnailParser)
    perpage_input_name = 'MPHOnline$ContentPlaceHolder1$HFTotalPage'
    form_data = {
        '__EVENTTARGET': 'MPHOnline$ContentPlaceHolder1$ReloadSBut',
        '__EVENTARGUMENT': ''
    }

    def tag(self, book):
        if self.tags:
            book['tags'] = self.tags
        return book

    def scrape(self):
        self.log('starting %s', self.__class__.__name__)
        self.open()

        root = soupparser.fromstring(self.body())

        # get total available books
        totals = TotalAvailableBooksParser()
        total_books = totals.get_value(root)
        total_books_str = str(total_books)

        if not total_books:
            raise AssertionError('Could not parse for total books in %s' % self._url)

        self.log('total books = %d', total_books)

        perpage_inputs = root.cssselect('input[name^="%s"]' % self.perpage_input_name)

        if len(perpage_inputs):
            form = {}

            for ppi in perpage_inputs:
                name = ppi.attrib['name']
                try:
                    value = int(ppi.attrib['value'])
                except (TypeError, ValueError):
                    continue
                if value < total_books:
                    form[name] = total_books_str

            # if a hidden 'per page' input is changed this means there are
            # more than 1 page of results, otherwise all available books are
            # already in this 1 initial page
            if form:
                # load all books and reparse response
                self.submit(form)
                root = soupparser.fromstring(self.body())

        self.log('scraping for book prices')

        books = []
        for cls in self.parser_classes:
            self.log('... using %s', cls.__name__)
            parser = cls()
            pbooks = [self.tag(b) for b in parser.parse(root)]
            books.extend(pbooks)
            self.log('... found %d books (total = %d)', len(pbooks), len(books))
        return books


class BestellersScraper(MPHScraper):
    tags = 'be'
    uri = '/books/bestseller.aspx'
    parser_classes = (BooklistingParser,)

class NewarrivalScraper(MPHScraper):
    tags = 'ne'
    uri = '/books/newarrival.aspx'
    parser_classes = (ThumbnailParser,)

class BargainScraper(MPHScraper):
    tags = 'ba'
    uri = '/offers/bargain.aspx'
    parser_classes = (BooklistingParser,)

class PrereleaseScraper(MPHScraper):
    tags = 'pr'
    uri = '/books/prerelease.aspx'
    parser_classes = (BooklistingParser,)

class PreorderScraper(MPHScraper):
    tags = 'po'
    uri = '/offers/preorder.aspx'
    parser_classes = (BooklistingParser,)
    perpage_input_name = 'MPHOnline$ContentPlaceHolder1$HFTotalPPage'

class ClicknsaveScraper(MPHScraper):
    tags = 'cl'
    uri = '/offers/clicknsave.aspx'
    parser_classes = (BooklistingParser,)
    perpage_input_name = 'MPHOnline$ContentPlaceHolder1$HFTotalPPage'

class HottitlesScraper(MPHScraper):
    tags = 'ho'
    uri = '/books/hot_titles.aspx'
    parser_classes = (BooklistingParser,)
    perpage_input_name = 'MPHOnline$ContentPlaceHolder1$HFTotalPPage'


book_table_fields = {
    'isbn': unicode,
    'price_normal': float,
    'price_online': float,
    'tags': unicode
}


def sanitize(book, d):
    # sanitize and prepare book dict for saving
    data = {}
    for f in book_table_fields:
        data_type = book_table_fields[f]
        data[f] = data_type(book.get(f, data_type()))
    data['date'] = d
    return data

def run():
    scrapers = [
        BestellersScraper,
        NewarrivalScraper,
        BargainScraper,
        PrereleaseScraper,
        PreorderScraper,
        ClicknsaveScraper,
        HottitlesScraper
    ]
    books = []
    for cls in scrapers:
        url = urlparse.urljoin(MPH_BASE_URL, cls.uri)
        scraper = cls(url)
        books.extend(scraper.scrape())
    save(books)

def save(books):
    log.info('saving total %d books', len(books))
    rundate = date.today()
    savebooks = [sanitize(b, rundate) for b in books]
    scraperwiki.sqlite.save(['isbn'], savebooks, 'books')


run() # Forrest, run!
