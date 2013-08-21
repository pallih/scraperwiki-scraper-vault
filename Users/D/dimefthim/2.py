import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', 'Εμβαδον')

#city = 'γαλατσι'

#propertyUrl = 'www.property.gr'

#startUrl = propertyUrl + '/πωλησεις|κατοικιες|' + city + '|3086687'
startUtl = http://www.property.gr/%CF%80%CF%89%CE%BB%CE%B7%CF%83%CE%B5%CE%B9%CF%82%7C%CE%BA%CE%B1%CF%84%CE%BF%CE%B9%CE%BA%CE%B9%CE%B5%CF%82%7C%CE%B3%CE%B1%CE%BB%CE%B1%CF%84%CF%83%CE%B9%7C3086687.html

html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)
#html = scraperwiki.scrape(link.encode('utf-8'))

items = []
today = datetime.date.today()

print 'page: ' + startURL

soup.findAll('table')

for tr in table.findAll('tr'):
        tr.findALL ('td')
        realItem ['Εμβαδον']=td.String

items.append(realItem)
scraperwiki.datastore.save(data=realItem)
print 'items saved: '+ str(len(items))
      
        

        
       
      



