
import scraperwiki
html = scraperwiki.scrape('://www.guardian.co.uk/news/datablog/2010/sep/10/phone-hacking-victims-list')
print html
import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)
for td in soup.findAll('td'):
    print td.string

for td in soup.findAll('td'):
    scraperwiki.datastore.save(unique_keys=['table_cell'], data={'table_cell':td.string})