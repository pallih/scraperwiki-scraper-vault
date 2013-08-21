import scraperwiki
import BeautifulSoup
import urlparse
import re

from scraperwiki import datastore

# Regular expressions that match the text in hyperlinks
Jr=re.compile('Judge?ment')
PSr=re.compile('Press *Summary', re.I)


def get_page(href):
    # work through the page given and then all pages that are linked to through 'next'
    while True:
        print "Now parsing: %s" % href
        html = scraperwiki.scrape(href)
        page = BeautifulSoup.BeautifulSoup(html)
        yield([page, href])
        
        N=page.findAll('a', {'class' : 'active', 'title' : 'Next' })
        if len(N)==0:
            break
        else:
            print href, N
            href=urlparse.urljoin(href, N[0]['href'])
            
#find rows
def parse_page(page, url):
    for table in page.findAll('table', {'id':'caselist'}):
        for row in table.findAll('tr')[1:]:
            if row['class'].find('last') < 0:
                cells = row.findAll('td')
                
                handed_down = cells[0].string
                neutral_citation = cells[1].string
                case_id = cells[2].string            
                case_name = cells[3].contents[1].string
                court = ''                                    
     
                # return absolute urls, they are WAY more useful.
                judgment_pdf_link = urlparse.urljoin(url, cells[4].findAll('a', title=Jr)[0]['href'])
                press_summary_link = urlparse.urljoin(url, cells[4].findAll('a', title=PSr)[0]['href'])
    
            #save to datastore
            data = {
                    'case_name' : case_name,
                    'handed_down' : handed_down,
                    'case_id' : case_id,
                    'neutral_citation' : neutral_citation,
                    'judgment_pdf_link' : judgment_pdf_link,
                    'press_summary_link' : press_summary_link
                    }
            datastore.save(unique_keys=['case_id'], data=data)
    
for page, url in get_page('http://www.supremecourt.gov.uk/decided-cases/index.html'):
    parse_page(page, url)

