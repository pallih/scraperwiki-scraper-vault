import scraperwiki
import string
import re
from BeautifulSoup import BeautifulSoup

BEERMAD_URL = 'http://beermad.org.uk'
BREWERY_INDEX_URL = BEERMAD_URL + '/brewerylist/%(character)s'
BREWERY_URL_RE = re.compile(r'/brewery/\d+')

def main():
    urls = (BREWERY_INDEX_URL % {'character' : c} for c in string.uppercase + string.digits)
    for url in urls:
        print(url)
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        for brewery_a_tag in soup.findAll('a', attrs={'href' : BREWERY_URL_RE}):
            href = brewery_a_tag['href'] # ie '/brewery/3917'
            id = href.split('/')[-1]
            brewery_name = brewery_a_tag.getText()
            #print(brewery_a_tag)
            data = {'url': BEERMAD_URL + href,
                    'id': id,
                    'brewery_name': brewery_name}
            scraperwiki.sqlite.save(unique_keys=['id', 'url'], data=data)

main()
import scraperwiki
import string
import re
from BeautifulSoup import BeautifulSoup

BEERMAD_URL = 'http://beermad.org.uk'
BREWERY_INDEX_URL = BEERMAD_URL + '/brewerylist/%(character)s'
BREWERY_URL_RE = re.compile(r'/brewery/\d+')

def main():
    urls = (BREWERY_INDEX_URL % {'character' : c} for c in string.uppercase + string.digits)
    for url in urls:
        print(url)
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        for brewery_a_tag in soup.findAll('a', attrs={'href' : BREWERY_URL_RE}):
            href = brewery_a_tag['href'] # ie '/brewery/3917'
            id = href.split('/')[-1]
            brewery_name = brewery_a_tag.getText()
            #print(brewery_a_tag)
            data = {'url': BEERMAD_URL + href,
                    'id': id,
                    'brewery_name': brewery_name}
            scraperwiki.sqlite.save(unique_keys=['id', 'url'], data=data)

main()
