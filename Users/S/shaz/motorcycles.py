import scraperwiki
import re
from bs4 import BeautifulSoup

site = scraperwiki.scrape('http://bikez.com/brands/index.php')
soup = BeautifulSoup(site)
brands = soup.table.table.table.find_all(attrs={'value' : re.compile("brand")})

manufacturers = {}
models = {}

for brand in brands:
    name = brand.string
    link = brand.get('value')
    #print name, link
    #scraperwiki.sqlite.save(unique_keys=['id'], data={'id': brands.index(brand), 'name': name}, table_name="manufacturers")
    manufacturers[(brands.index(brand))/2] = name 

    site = scraperwiki.scrape(link)
    soup = BeautifulSoup(site)
    models = soup.find_all('a', attrs={'href' : re.compile("\.\.\/motorcycles")})

    for model in models:
        if not model.img:
            m_name = model.string
            m_link = model.get('href')
            site = scraperwiki.scrape("http://bikez.com/%s" % (m_link[3:]))
            soup = BeautifulSoup(site)

            row = soup.find('b', text="Year:").parent
            m_year = row.next_sibling.string
            #print m_name, m_link, m_year
            #scraperwiki.sqlite.save(unique_keys=['id'], data={'id': (models.index(model))/2, 'name': m_name, 'year' : m_year}, table_name="models")
            x = [m_name, m_year]
            models[(models.index(model))/2] = x

print manufacturers
print models