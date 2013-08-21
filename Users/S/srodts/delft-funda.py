import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', ['id', 'date', 'street', 'city', 'postcode', 'livingspace', 'otherspace', 'rooms','agent', 'price'])

city = 'delft'
minPrice=str(00000)
maxPrice=str(1500000)
minOpp=str(15)

fundaUrl = 'http://www.funda.nl/europe/'
# startUrl = fundaUrl + '/koop/' + city + '/' + minPrice + '-' + maxPrice + '/' + minOpp + '+woonopp' + '/' + 'woonhuis' + '/' + 'bestaande-bouw' + '/'
startUrl = fundaUrl + '/koop/' + city +  '/' + 'woonhuis' + '/' + 'bestaande-bouw' + '/'
baseUrl = startUrl + 'p'

html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)

# get number of pages
pages = soup.findAll(attrs={'id' : 'ctl00_CPHResultaat_ZoekResultaatLijst_ctl00_ctl30_ha'})
#numberOfpages = int(pages[len(pages)].string)

items = []
today = datetime.date.today()

for pageNo in range(1, numberOfpages + 1):
 
    nextUrl = baseUrl + str(pageNo)
    print 'page: ' + nextUrl
    html = scraperwiki.scrape(nextUrl)
    soup = BeautifulSoup.BeautifulSoup(html)
    
    for tr in soup.findAll('tr', 'nvm'):
        realItem = {'date' : today}
        
        for item in tr.findAll('a', 'item'):
            realItem['street'] = item.string
            realItem['id'] = fundaUrl + item['href']
        
        for spec in tr.findAll('p', 'specs'):
            realItem['postcode'] = spec('span', limit=2)[0].string.strip()
            realItem['city'] = spec('span', limit=2)[1].string.strip()
            if spec.find(title='Woonoppervlakte'):
                realItem['livingspace'] = spec.find(title='Woonoppervlakte').string.replace('&nbsp;m&sup2;', '').strip()
            else:
                realItem['livingspace'] = ''
            if spec.find(title='Perceeloppervlakte'):
                realItem['otherspace'] = spec.find(title='Perceeloppervlakte').string.replace('&nbsp;m&sup2;', '').strip()
            else:
                realItem['otherspace'] = ''
            if spec.find(title='Aantal kamers'):
                realItem['rooms'] = spec.find(title='Aantal kamers').string.replace('&nbsp;kamers', '').strip()
            else:
                realItem['rooms'] = ''            
            if spec.find(title='Makelaardij'):
                realItem['agent'] = spec.find(title='Makelaardij').string.replace('&nbsp;', '').strip()
            else:
                realItem['agent'] = ''
        for price in tr.findAll('span', 'price'):
            realItem['price'] = price.string.replace('&euro;&nbsp;', '').strip().replace('.', '')
        
        items.append(realItem)
        scraperwiki.datastore.save(unique_keys=['id'], data=realItem)
        print 'items saved: ' + str(len(items))



import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', ['id', 'date', 'street', 'city', 'postcode', 'livingspace', 'otherspace', 'rooms','price'])

city = 'delft'
minPrice=str(00000)
maxPrice=str(1500000)
minOpp=str(10)

fundaUrl = 'http://www.funda.nl'
# startUrl = fundaUrl + '/koop/' + city + '/' + minPrice + '-' + maxPrice + '/' + minOpp + '+woonopp' + '/' + 'woonhuis' + '/' + 'bestaande-bouw' + '/'
startUrl = fundaUrl + '/koop/' + city +  '/' + 'woonhuis' + '/' + 'bestaande-bouw' + '/'
baseUrl = startUrl + 'p'

html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)

# get number of pages
pages = soup.findAll(attrs={'id' : 'ctl00_CPHResultaat_ZoekResultaatLijst_ctl00_ctl30_ha'})
numberOfpages = int(pages[len(pages) - 2].string)

items = []
today = datetime.date.today()

for pageNo in range(1, numberOfpages + 1):
 
    nextUrl = baseUrl + str(pageNo)
    print 'page: ' + nextUrl
    html = scraperwiki.scrape(nextUrl)
    soup = BeautifulSoup.BeautifulSoup(html)
    
    for tr in soup.findAll('tr', 'nvm'):
        realItem = {'date' : today}
        
        for item in tr.findAll('a', 'item'):
            realItem['street'] = item.string
            realItem['id'] = fundaUrl + item['href']
        
        for spec in tr.findAll('p', 'specs'):
            realItem['postcode'] = spec('span', limit=2)[0].string.strip()
            realItem['city'] = spec('span', limit=2)[1].string.strip()
            if spec.find(title='Woonoppervlakte'):
                realItem['livingspace'] = spec.find(title='Woonoppervlakte').string.replace('&nbsp;m&sup2;', '').strip()
            else:
                realItem['livingspace'] = ''
            if spec.find(title='Perceeloppervlakte'):
                realItem['otherspace'] = spec.find(title='Perceeloppervlakte').string.replace('&nbsp;m&sup2;', '').strip()
            else:
                realItem['otherspace'] = ''
        for price in tr.findAll('span', 'price'):
            realItem['price'] = price.string.replace('&euro;&nbsp;', '').strip().replace('.', '')
        
        items.append(realItem)
        scraperwiki.datastore.save(unique_keys=['id'], data=realItem)
        print 'items saved: ' + str(len(items))
