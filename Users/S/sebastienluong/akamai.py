from urlparse import urljoin
import scraperwiki
import re
from bs4 import BeautifulSoup

#scraperwiki.sqlite.execute('DROP TABLE `swdata`')

#scrape_table function passes to an individual page to scrape
def scrape_table(root):
    for i in root:
        td=i.findAll('td')
    
    for i in td:
        name=i.find('a')  
        if name:
            record ={}  
            record["Company"]= name.get_text()
            record["Date"]= name.find_next("td").get_text()
            record["Share held"]= name.find_all_next("td")[1].get_text()
            record["Change percent"]=name.findAllNext("td")[3].get_text()
            #print record, '--------------'
            scraperwiki.sqlite.save([], record)

def scrape_and_look_for_next_link(url):
    soup = BeautifulSoup(scraperwiki.scrape(url))
    fields = soup.find_all(class_="certain-width")
    scrape_table(fields)
    next_link=soup.find(text=re.compile('next >'))
    next_link_parent=next_link.find_parent("a")
    if next_link_parent:
        next_url = urljoin(base_url, next_link_parent.attrs.get('href'))
        scrape_and_look_for_next_link(next_url)

# Main

base_url = "http://www.nasdaq.com/symbol/akam/institutional-holdings"
scrape_and_look_for_next_link(base_url)from urlparse import urljoin
import scraperwiki
import re
from bs4 import BeautifulSoup

#scraperwiki.sqlite.execute('DROP TABLE `swdata`')

#scrape_table function passes to an individual page to scrape
def scrape_table(root):
    for i in root:
        td=i.findAll('td')
    
    for i in td:
        name=i.find('a')  
        if name:
            record ={}  
            record["Company"]= name.get_text()
            record["Date"]= name.find_next("td").get_text()
            record["Share held"]= name.find_all_next("td")[1].get_text()
            record["Change percent"]=name.findAllNext("td")[3].get_text()
            #print record, '--------------'
            scraperwiki.sqlite.save([], record)

def scrape_and_look_for_next_link(url):
    soup = BeautifulSoup(scraperwiki.scrape(url))
    fields = soup.find_all(class_="certain-width")
    scrape_table(fields)
    next_link=soup.find(text=re.compile('next >'))
    next_link_parent=next_link.find_parent("a")
    if next_link_parent:
        next_url = urljoin(base_url, next_link_parent.attrs.get('href'))
        scrape_and_look_for_next_link(next_url)

# Main

base_url = "http://www.nasdaq.com/symbol/akam/institutional-holdings"
scrape_and_look_for_next_link(base_url)