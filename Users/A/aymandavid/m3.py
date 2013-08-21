# Blank Python
#################################################################
# BBC Weather Scraper                                            
#################################################################
import scraperwiki
from BeautifulSoup import BeautifulSoup

# URL for the region M3
#html = scraperwiki.scrape ('http://news.bbc.co.uk/weather/forecast/9?area=M3')

html = scraperwiki.scrape ('http://uk.weather.yahoo.com/england/greater-manchester/salford-27544944/')
print html

soup = BeautifulSoup(html)
days = soup.findAll('tr')
                    
for day in days:
    if day['class'].find('day') == -1:
            continue
    record = {
        'day': None,
        'summary': None,
        'temp_max_c': None,
        'temp_min_c': None,

    }              
    tds = day.findAll('td')
    for abbr in tds[0].findAll('abbr'):
        record['day'] = abbr.text
    for span in tds[2].findAll('span'):
        try:
            if span['class'].find('temp max') != -1:
                record['temp_max_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
        except:
            pass
    for span in tds[3].findAll('span'):
        try:
            if span['class'].find('temp min') != -1:
                record['temp_min_c'] = span.findAll('span',{'class':'cent'})[0].text[:-6]
        except:
            pass

    record['summary'] = day.findAll('div',{'class':'summary'})[0].findAll('strong')[0].text                                  
    print
    scraperwiki.datastore.save(["day"], record)
    
    
