# Extract package data from DSpace repository

# Working from these examples:
# http://datashare.is.ed.ac.uk/browse?type=dateissued&rpp=100
# http://www.era.lib.ed.ac.uk/browse?type=dateissued&rpp=100



import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
print 'foo'

offset = 0
dspace = 'http://datashare.is.ed.ac.uk/browse?type=dateissued&rpp=100'
print dspace
html = scraperwiki.scrape(dspace+'&offset=')

print dspace

soup = BeautifulSoup(html)


def package_extras(url):
    # get more package data including file locations from the description
    # e.g.
    # html = scraperwiki.scrape(url)
    # soup = BeautifulSoup(html)
    pass
     

def package_data(url):
    print url
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # get the package data
    items = soup.findAll('div',{'class':'artifact-description'})

    for i in items:
         # ugh

         item = {}
         title = i.find('div',{'class':'artifact-title'})
         
         try: item['title'] = title.text
         except: pass
         try: 
             item['handle'] = title.find('a')['href']
             package_extras(url)   
         
         except: item['title'] = None
         info = i.find('div',{'class':'artifact-info'})

         try: item['author'] = info.find('span',{'class':'author'}).text
         except: item['author'] = None

         try: item['publisher'] = info.find('span',{'class':'publisher'}).text
         except: item['publisher'] = None

         try: item['publisher_date'] = info.find('span',{'class':'publisher-date'}).text
         except: item['publisher_date'] = None

         try: item['date'] = info.find('span',{'class':'date'}).text
         except: item['date'] = None

         scraperwiki.sqlite.save(['handle'],item)



totals = soup.find('p',{'class':"pagination-info"})

match = re.search('of (\d+)',totals.text)
total = match.group().replace('of ','')
print total

while offset < int(total):
    print offset
    page = dspace+str(offset)
    package_data(page)
    offset = offset + 100



