from bs4 import BeautifulSoup
import dateutil.parser as parser
import re
import scraperwiki
import urlparse

# Return a soup with all links turned absolute.
# See: http://stackoverflow.com/a/4468467/715866
def absolute_soup(html, encoding, base):
    soup = BeautifulSoup(html, from_encoding=encoding)
    for tag in soup.findAll('a', href=True):
        tag['href'] = urlparse.urljoin(base, tag['href'])
    return soup

# Reformat markup to remove arbitrary linebreaks.
def oneline(html):
    return re.sub('\s+', ' ', html)

apod_base = 'http://apod.nasa.gov/apod/'
apod_archive_url = apod_base + 'archivepix.html'
apod_encoding = 'latin-1'

archive_soup = absolute_soup(scraperwiki.scrape(apod_archive_url), apod_encoding, apod_base)
archive_links = archive_soup.find_all(href=re.compile('ap[0-9]+\.html'))

for archive_link in archive_links:
    page_soup = absolute_soup(scraperwiki.scrape(archive_link['href']), apod_encoding, apod_base)

    # URL
    url = archive_link['href']

    # Date
    date_raw = archive_link.previous_sibling[:-3]
    date = parser.parse(date_raw).strftime('%Y-%m-%d')

    # Title
    title = archive_link.text

    # Explanation
    page_html = str(page_soup) # The raw HTML, but with links turned absolute.
    explanation_ugly = re.search('<(b|(h3))>.*?Explanation.*?</(b|(h3))>\s*(.*?)\s*(</p>)?<p>', page_html, re.DOTALL | re.IGNORECASE).group(5)
    explanation = oneline(explanation_ugly)

    # Picture URL. Check that there actually is a picture, as NASA sometimes
    # publishes videos instead.
    picture_link = page_soup.find(href=re.compile(apod_base + 'image/'))
    if picture_link:
        picture_url = picture_link['href']
        picture_found = True
    else:
        picture_found = False

    # Save!
    if picture_found:
        record = {'url': url, 'date': date, 'title': title, 'explanation': explanation, 'picture_url': picture_url}
        scraperwiki.sqlite.save(['url'], record)from bs4 import BeautifulSoup
import dateutil.parser as parser
import re
import scraperwiki
import urlparse

# Return a soup with all links turned absolute.
# See: http://stackoverflow.com/a/4468467/715866
def absolute_soup(html, encoding, base):
    soup = BeautifulSoup(html, from_encoding=encoding)
    for tag in soup.findAll('a', href=True):
        tag['href'] = urlparse.urljoin(base, tag['href'])
    return soup

# Reformat markup to remove arbitrary linebreaks.
def oneline(html):
    return re.sub('\s+', ' ', html)

apod_base = 'http://apod.nasa.gov/apod/'
apod_archive_url = apod_base + 'archivepix.html'
apod_encoding = 'latin-1'

archive_soup = absolute_soup(scraperwiki.scrape(apod_archive_url), apod_encoding, apod_base)
archive_links = archive_soup.find_all(href=re.compile('ap[0-9]+\.html'))

for archive_link in archive_links:
    page_soup = absolute_soup(scraperwiki.scrape(archive_link['href']), apod_encoding, apod_base)

    # URL
    url = archive_link['href']

    # Date
    date_raw = archive_link.previous_sibling[:-3]
    date = parser.parse(date_raw).strftime('%Y-%m-%d')

    # Title
    title = archive_link.text

    # Explanation
    page_html = str(page_soup) # The raw HTML, but with links turned absolute.
    explanation_ugly = re.search('<(b|(h3))>.*?Explanation.*?</(b|(h3))>\s*(.*?)\s*(</p>)?<p>', page_html, re.DOTALL | re.IGNORECASE).group(5)
    explanation = oneline(explanation_ugly)

    # Picture URL. Check that there actually is a picture, as NASA sometimes
    # publishes videos instead.
    picture_link = page_soup.find(href=re.compile(apod_base + 'image/'))
    if picture_link:
        picture_url = picture_link['href']
        picture_found = True
    else:
        picture_found = False

    # Save!
    if picture_found:
        record = {'url': url, 'date': date, 'title': title, 'explanation': explanation, 'picture_url': picture_url}
        scraperwiki.sqlite.save(['url'], record)