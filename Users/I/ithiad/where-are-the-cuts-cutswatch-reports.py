import scraperwiki
from BeautifulSoup import BeautifulSoup

############################################################################################
# Helper function to scrape a reports list page and store records.
############################################################################################

def scrape_page(url):
    page = BeautifulSoup(scraperwiki.scrape(url))
    
    # The reports are in the body rows of the first table 
    reports = page.findAll('div', { "class" : "report_row1" }) 
    for report in reports:
        fields = report.findAll('div')
        title = fields[1].find('h3')
        link = title.find('a')['href']
        title.extract()
        standfirst = fields[1].text
        
        record = { "title" : title.text,
                 "date" : fields[2].text,
                 "location" : fields[3].text,
                 "url" : link,
                  "standfirst" : standfirst,
                 "verified" : fields[4].text
                  }
        
        scraperwiki.datastore.save(["url"], record)
    
    return page



    
############################################################################################
# Scrape the first reports list page - this also tells us how many more pages to scrape.
############################################################################################

html = scrape_page('http://wherearethecuts.org/reports?page=1')

# How many pages in total?
num_pages = int(html.find('ul', { "class" : "pager" }).findAll('li')[-1].text)

for i in range(2, num_pages+1):
    scrape_page('http://wherearethecuts.org/reports?page=%s' % i)

