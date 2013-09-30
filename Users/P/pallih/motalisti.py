import scraperwiki,re
from BeautifulSoup import BeautifulSoup

#url = 'http://www.ksi.is/mot/motalisti/'

# http://www.ksi.is/mot/motalisti/?flokkur=%25&tegund=%25&AR=2011&kyn=%25



yearlist = range(1912, 2012)

#Scrape year
def scrapeyear(url, year):
    seen_before = scraperwiki.metadata.get(url)
    if seen_before is not None:
        print "Seen before - skip: " + url
        return
    else:
        print "vinnum ur " + year
    data = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    
    table = soup.find('table', {'id' : 'mot-tafla'})
    trs = table.findAll('tr')
    for td in trs[1:]:
         items = td.findAll('td')
         slod = 'http://www.ksi.is/mot/motalisti/' + items[1].a['href']
         motanumer = re.sub('http:\//www.ksi.is\/mot\/motalisti\/urslit-stada/\?MotNumer=','',slod)
         mot = items[1].text
         flokkur = items[3].text
         data['slod'] = slod
         data['year'] = year
         data['motanumer'] = motanumer
         data['flokkur'] = flokkur
         data['mot'] = mot

         #print data
         print "vistum " + year
         scraperwiki.datastore.save(["mot", "year"], data) 
         scraperwiki.metadata.save(url,"1")  



#LETS GO!
for year in yearlist:
    scrapeyear('http://www.ksi.is/mot/motalisti/?flokkur=%25&tegund=%25&AR=' + str(year) + '&kyn=%25', str(year))

print "All done"import scraperwiki,re
from BeautifulSoup import BeautifulSoup

#url = 'http://www.ksi.is/mot/motalisti/'

# http://www.ksi.is/mot/motalisti/?flokkur=%25&tegund=%25&AR=2011&kyn=%25



yearlist = range(1912, 2012)

#Scrape year
def scrapeyear(url, year):
    seen_before = scraperwiki.metadata.get(url)
    if seen_before is not None:
        print "Seen before - skip: " + url
        return
    else:
        print "vinnum ur " + year
    data = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    
    table = soup.find('table', {'id' : 'mot-tafla'})
    trs = table.findAll('tr')
    for td in trs[1:]:
         items = td.findAll('td')
         slod = 'http://www.ksi.is/mot/motalisti/' + items[1].a['href']
         motanumer = re.sub('http:\//www.ksi.is\/mot\/motalisti\/urslit-stada/\?MotNumer=','',slod)
         mot = items[1].text
         flokkur = items[3].text
         data['slod'] = slod
         data['year'] = year
         data['motanumer'] = motanumer
         data['flokkur'] = flokkur
         data['mot'] = mot

         #print data
         print "vistum " + year
         scraperwiki.datastore.save(["mot", "year"], data) 
         scraperwiki.metadata.save(url,"1")  



#LETS GO!
for year in yearlist:
    scrapeyear('http://www.ksi.is/mot/motalisti/?flokkur=%25&tegund=%25&AR=' + str(year) + '&kyn=%25', str(year))

print "All done"