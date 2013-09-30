import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', '1')

city = 'sale_Apartment_Kipseli-l573773'

spitogatosUrl = 'www.homegreekhome.com'

startUrl = spitogatosUrl + '/en/' + city 

html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)
#html = scraperwiki.scrape(link.encode('utf-8'))

for pageNo in range(1, 1 + 1):

    nextUrl = startUrl + str(pageNo)
    print 'page: ' + nextUrl
    html = scraperwiki.scrape(nextUrl)
    soup = BeautifulSoup.BeautifulSoup(html)

    items = []
    today = datetime.date.today()

    for div in soup.findAll('div', 'detail'):
            soup('li', limit=5)
        

        
items.append(realItem)
scraperwiki.datastore.save(unique_keys=['id'], data=realItem)
print 'items saved: ' + str(len(items))

import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', '1')

city = 'sale_Apartment_Kipseli-l573773'

spitogatosUrl = 'www.homegreekhome.com'

startUrl = spitogatosUrl + '/en/' + city 

html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)
#html = scraperwiki.scrape(link.encode('utf-8'))

for pageNo in range(1, 1 + 1):

    nextUrl = startUrl + str(pageNo)
    print 'page: ' + nextUrl
    html = scraperwiki.scrape(nextUrl)
    soup = BeautifulSoup.BeautifulSoup(html)

    items = []
    today = datetime.date.today()

    for div in soup.findAll('div', 'detail'):
            soup('li', limit=5)
        

        
items.append(realItem)
scraperwiki.datastore.save(unique_keys=['id'], data=realItem)
print 'items saved: ' + str(len(items))

