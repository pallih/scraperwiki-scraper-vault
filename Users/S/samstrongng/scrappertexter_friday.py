import scraperwiki
html = scraperwiki.scrape("http://www.buzzle.com/articles/list-of-disney-movies.html")
print html 
import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)
for td in soup.findAll('td'):
    print td.string
for td in soup.findAll('td'):
    scraperwiki.datastore.save(unique_keys=['year_cell'], data={'year_cell':td.string})
import scraperwiki
html = scraperwiki.scrape("http://www.buzzle.com/articles/list-of-disney-movies.html")
print html 
import BeautifulSoup
soup = BeautifulSoup.BeautifulSoup(html)
for td in soup.findAll('td'):
    print td.string
for td in soup.findAll('td'):
    scraperwiki.datastore.save(unique_keys=['year_cell'], data={'year_cell':td.string})
