from datetime import datetime, timedelta
from os import path
import lxml.html
import scraperwiki

PICTUREHOUSES_URL = "http://www.picturehouses.co.uk"
WEEKLY_LISTING_URL = "Whats_On/All/This_Week/"
DAILY_LISTING_URL = "Whats_On/All/Date_%s/"


def element_classes(element):
    """List of an elements classes"""
    return element.attrib.get('class', '').split(' ') or []


def cinema_list():
    """URLs for listed cinemas"""
    src = scraperwiki.scrape(PICTUREHOUSES_URL)
    root = lxml.html.fromstring(src)
    #return [path.join(PICTUREHOUSES_URL, url) for url in root.cssselect('ul.cinemas li a')[0].attrib['href']]
    return [path.join(PICTUREHOUSES_URL, elem.attrib['href']) for elem in root.cssselect('ul.cinemas li a')]


class Cinema(object):
    def __init__(self, root_url):
        self.root_url = root_url

    def tomorrows_films(self):
        """Return a list of film and times today"""
        today = datetime.utcnow() + timedelta(days=1)
        ## Pull listing and parse
        src = scraperwiki.scrape(path.join(self.root_url, DAILY_LISTING_URL % today.strftime('%d_%m_%Y')))
        root = lxml.html.fromstring(src)
        listings = root.cssselect('.largelist .item')
        films = [self._scrape_daily_listing(listing) for listing in listings]
        print films
        return films

    def _scrape_daily_listing(self, listing):
        """Given an lxml element from a daily listing page, extract film details"""
        data = {}
        data['url'] = path.join(PICTUREHOUSES_URL, listing.cssselect('.left.a a')[0].attrib['href'])
        print 'URL: %s' % data['url']
        data['title'] = listing.cssselect('.left.b .movielink')[0].text
        print 'TITLE: %s' % data['title']
        #data['rating'] = [c for c in element_classes(listing.cssselect('.left.b .left')) if 'rating' in c][0]
        data['screenings'] = []
        for screening in listing[2].cssselect('a'):
            try:
                data['screenings'].append(datetime.fromtimestamp(screening.attrib['epoch']))
            except Exception:
                pass ##TODO: log this
        return data



def main():
    cinemas = cinema_list()
    print 'Cinemas: %s' % cinemas
    for url in cinemas:
        print url
        cinema = Cinema(url)
        print cinema.tomorrows_films()


main()
from datetime import datetime, timedelta
from os import path
import lxml.html
import scraperwiki

PICTUREHOUSES_URL = "http://www.picturehouses.co.uk"
WEEKLY_LISTING_URL = "Whats_On/All/This_Week/"
DAILY_LISTING_URL = "Whats_On/All/Date_%s/"


def element_classes(element):
    """List of an elements classes"""
    return element.attrib.get('class', '').split(' ') or []


def cinema_list():
    """URLs for listed cinemas"""
    src = scraperwiki.scrape(PICTUREHOUSES_URL)
    root = lxml.html.fromstring(src)
    #return [path.join(PICTUREHOUSES_URL, url) for url in root.cssselect('ul.cinemas li a')[0].attrib['href']]
    return [path.join(PICTUREHOUSES_URL, elem.attrib['href']) for elem in root.cssselect('ul.cinemas li a')]


class Cinema(object):
    def __init__(self, root_url):
        self.root_url = root_url

    def tomorrows_films(self):
        """Return a list of film and times today"""
        today = datetime.utcnow() + timedelta(days=1)
        ## Pull listing and parse
        src = scraperwiki.scrape(path.join(self.root_url, DAILY_LISTING_URL % today.strftime('%d_%m_%Y')))
        root = lxml.html.fromstring(src)
        listings = root.cssselect('.largelist .item')
        films = [self._scrape_daily_listing(listing) for listing in listings]
        print films
        return films

    def _scrape_daily_listing(self, listing):
        """Given an lxml element from a daily listing page, extract film details"""
        data = {}
        data['url'] = path.join(PICTUREHOUSES_URL, listing.cssselect('.left.a a')[0].attrib['href'])
        print 'URL: %s' % data['url']
        data['title'] = listing.cssselect('.left.b .movielink')[0].text
        print 'TITLE: %s' % data['title']
        #data['rating'] = [c for c in element_classes(listing.cssselect('.left.b .left')) if 'rating' in c][0]
        data['screenings'] = []
        for screening in listing[2].cssselect('a'):
            try:
                data['screenings'].append(datetime.fromtimestamp(screening.attrib['epoch']))
            except Exception:
                pass ##TODO: log this
        return data



def main():
    cinemas = cinema_list()
    print 'Cinemas: %s' % cinemas
    for url in cinemas:
        print url
        cinema = Cinema(url)
        print cinema.tomorrows_films()


main()
