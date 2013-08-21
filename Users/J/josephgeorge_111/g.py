import scraperwiki
html = scraperwiki.scrape("http://www.guardian.co.uk/news/datablog/2009/sep/17/afghanistan-casualties-dead-wounded-british-data")
print html 
import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)
for td in soup.findAll('td'):
    print td.string
for td in soup.findAll('td'):
    scraperwiki.datastore.save(unique_keys=['table_cell'], data={'table_cell':td.string})





