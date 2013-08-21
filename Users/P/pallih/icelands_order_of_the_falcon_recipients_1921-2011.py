import scraperwiki,re
from BeautifulSoup import BeautifulSoup

#url = 'http://falkadb.forseti.is/orduskra/fal03.php?rod=nafn&valid_ar=1921'

#Scrape year
def scrapeyear(url, year):
    data = {}   
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    
    tr = soup.findAll('tr')
    for td in tr[1:]:
        items = td.findAll('td')
        data['year'] = year
        data['name'] = items[1].text
        data['occupation'] = items[2].text.partition(';')[0].strip()
        if items[2].text.partition(';')[2]: 
            data['reason'] = items[2].text.partition(';')[2].strip()
        data['citizenship'] = items[3].text
        data['date'] = items[4].text
        data['award'] = items[5].text  
        print data      
        #scraperwiki.datastore.save(["name", "date"], data, verbose=1)    

for year in range(1921, 2014):
    scrapeyear('http://falkadb.forseti.is/orduskra/fal03.php?rod=nafn&valid_ar=' + str(year), str(year))


