import scraperwiki
from BeautifulSoup import BeautifulSoup

def get_soup(url):
    html = scraperwiki.scrape(url)
    return BeautifulSoup(html)

# fields are currently:
# category
# position
# description
# location

soup = get_soup('http://www6.sfgov.org/index.aspx?page=42')
alinks = soup.find('div', {'id': '_ctl0_content'}).findAll('a')
links = dict([(a.text, a.get('href')) for a in alinks])
print links

for title, link in links.items():
    # "datastore" is deprecated use "sqlite" instead
    scraperwiki.sqlite.save(['title'], {'title': title, 'link': link})

# Now we have a dict of sites to keyed on their page titles, which we can special case here:
