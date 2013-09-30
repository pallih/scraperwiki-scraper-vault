import scraperwiki
from BeautifulSoup import BeautifulSoup

############################################################################################
# Helper function to scrape a reports list page and store records.
############################################################################################

def scrape_page(url):
    page = BeautifulSoup(scraperwiki.scrape(url))
    
    # The reports are in the body rows of the first table 
    reports = page.find('tbody').findAll('tr') 
    for report in reports:
        fields = report.findAll('td')
        title = fields[0].find('h3')
        link = title.find('a')['href']
        title.extract()
        standfirst = fields[0].text
        
        record = { "title" : title.text,
                 "date" : fields[1].text,
                 "location" : fields[2].text,
                 "url" : link,
                  "standfirst" : standfirst,
                 "verified" : fields[3].text
                  }
        scraperwiki.datastore.save(["url"], record)
    
    return page



    
############################################################################################
# Scrape the first reports list page - this also tells us how many more pages to scrape.
############################################################################################

html = scrape_page('http://cutswatch.guardian.co.uk/ushahidi/reports?page=1')

# How many pages in total?
num_pages = int(html.find('ul', { "class" : "pager" }).findAll('li')[-1].text)

for i in range(2, num_pages+1):
    scrape_page('http://cutswatch.guardian.co.uk/ushahidi/reports?page=%s' % i)


import scraperwiki
from BeautifulSoup import BeautifulSoup

############################################################################################
# Helper function to scrape a reports list page and store records.
############################################################################################

def scrape_page(url):
    page = BeautifulSoup(scraperwiki.scrape(url))
    
    # The reports are in the body rows of the first table 
    reports = page.find('tbody').findAll('tr') 
    for report in reports:
        fields = report.findAll('td')
        title = fields[0].find('h3')
        link = title.find('a')['href']
        title.extract()
        standfirst = fields[0].text
        
        record = { "title" : title.text,
                 "date" : fields[1].text,
                 "location" : fields[2].text,
                 "url" : link,
                  "standfirst" : standfirst,
                 "verified" : fields[3].text
                  }
        scraperwiki.datastore.save(["url"], record)
    
    return page



    
############################################################################################
# Scrape the first reports list page - this also tells us how many more pages to scrape.
############################################################################################

html = scrape_page('http://cutswatch.guardian.co.uk/ushahidi/reports?page=1')

# How many pages in total?
num_pages = int(html.find('ul', { "class" : "pager" }).findAll('li')[-1].text)

for i in range(2, num_pages+1):
    scrape_page('http://cutswatch.guardian.co.uk/ushahidi/reports?page=%s' % i)


