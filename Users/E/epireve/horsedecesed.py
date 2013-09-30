import scraperwiki
import urlparse
import lxml.html
import re
#print html

def scrape_table(root):
    rows = root.cssselect("tr")
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            horsename = re.findall('^[\w\s]*', table_cells[0].text_content())
            record['Horse'] = ''.join(horsename)

            #record['Date'] = table_cells[1].text_content()
            #record['Course'] = table_cells[2].text_content()
            #record['Cause of Death'] = table_cells[3].text_content()
            table_cellsurl = table_cells[0].cssselect("a")
            #record['URL'] = table_cellsurl[0].attrib.get('href')
            horseurl = 'http://www.horsedeathwatch.com/'+table_cellsurl[0].attrib.get('href')
            horseurl = horseurl.replace(" ","%20")
            record['FullURL'] = horseurl
            horsehtml = scraperwiki.scrape(horseurl)
            horseroot = lxml.html.fromstring(horsehtml)
            pars = horseroot.cssselect("p")
            print pars[0].text_content()
            
            record['Age'] = pars[0].text_content().strip("Age: ")
            record['Date'] = table_cells[1].text_content()
            record['Course'] = table_cells[2].text_content()
            record['Rating'] = pars[3].text_content().strip("Rating: ")
            record['Jockey'] = pars[4].text_content().strip("Name: ")
            country = re.findall('\([A-Z]*\)', table_cells[0].text_content())
            record['Country'] = ''.join(country).strip("()")
            record['Cause of Death'] = table_cells[3].text_content()
            
            print record, '******'
            scraperwiki.datastore.save(["Horse"], record)

def scrape_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #scrape_table(root)

base_url = 'http://www.horsedeathwatch.com/'
scrape_next_link(base_url)import scraperwiki
import urlparse
import lxml.html
import re
#print html

def scrape_table(root):
    rows = root.cssselect("tr")
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells: 
            horsename = re.findall('^[\w\s]*', table_cells[0].text_content())
            record['Horse'] = ''.join(horsename)

            #record['Date'] = table_cells[1].text_content()
            #record['Course'] = table_cells[2].text_content()
            #record['Cause of Death'] = table_cells[3].text_content()
            table_cellsurl = table_cells[0].cssselect("a")
            #record['URL'] = table_cellsurl[0].attrib.get('href')
            horseurl = 'http://www.horsedeathwatch.com/'+table_cellsurl[0].attrib.get('href')
            horseurl = horseurl.replace(" ","%20")
            record['FullURL'] = horseurl
            horsehtml = scraperwiki.scrape(horseurl)
            horseroot = lxml.html.fromstring(horsehtml)
            pars = horseroot.cssselect("p")
            print pars[0].text_content()
            
            record['Age'] = pars[0].text_content().strip("Age: ")
            record['Date'] = table_cells[1].text_content()
            record['Course'] = table_cells[2].text_content()
            record['Rating'] = pars[3].text_content().strip("Rating: ")
            record['Jockey'] = pars[4].text_content().strip("Name: ")
            country = re.findall('\([A-Z]*\)', table_cells[0].text_content())
            record['Country'] = ''.join(country).strip("()")
            record['Cause of Death'] = table_cells[3].text_content()
            
            print record, '******'
            scraperwiki.datastore.save(["Horse"], record)

def scrape_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #scrape_table(root)

base_url = 'http://www.horsedeathwatch.com/'
scrape_next_link(base_url)