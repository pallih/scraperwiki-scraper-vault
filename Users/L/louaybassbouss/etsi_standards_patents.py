####################################################
# scraper for http://webapp.etsi.org/ipr/IPRList.asp
####################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    form = soup.find("form", id = "form1")
    table = form.findAll("table")[1]
    rows = table.findAll("tr",recursive=False)
    i = 0
    record = None
    count = 0
    for row in rows:
        strong = row.find("strong", text = "Company")
        if strong:
            i = 1
            record = {}
            continue
        strong = row.find("strong", text = "Patent title")
        if strong:
            i = 2
        else:
            strong = row.find("strong", text = "Country of registration")
            if strong:
                i = 3

        if i == 1:
            cols = row.findAll("td",recursive=False)
            record['company'] = cols[1].text.strip()
            record['publication_no'] = cols[2].text.strip()
            record['application_no'] = cols[3].text.strip()
            record['deliverable_no'] = cols[4].text.strip()
            record['section'] = cols[5].text.strip()
            record['version'] = cols[6].text.strip()
            record['projects'] = cols[7].text.strip()
            record['declaration_date'] = cols[8].text.strip()
            i=0
        if i == 2:
            record['patent_title'] = strong.findNext(text=True).strip()
            i=0
        if i == 3:
            cols = row.findAll("tr")[1].findAll("td")
            record['country_of_registration'] = cols[1].text.strip()
            record['applicable_countries'] = cols[2].text.strip().split("&nbsp;-&nbsp;")
            scraperwiki.datastore.save(['company','publication_no','application_no','projects','declaration_date'], record)
            count = count+1
            i=0
    return count        
        
def run():
    url = "http://webapp.etsi.org/ipr/IPRList.asp?viewPage=1&toDisplay=100"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    form = soup.find("form", id = "form1")
    size = int(form.find("table").find('tr').findAll("td")[2].find("strong").text)
    for i in range(1, 2 + size/100):
        try:
            scrape_page("http://webapp.etsi.org/ipr/IPRList.asp?viewPage="+str(i)+"&toDisplay=100")
        except:
            pass

print "begin"
#scrape_page("http://webapp.etsi.org/ipr/IPRList.asp?viewPage=65&toDisplay=100")
run()
####################################################
# scraper for http://webapp.etsi.org/ipr/IPRList.asp
####################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    form = soup.find("form", id = "form1")
    table = form.findAll("table")[1]
    rows = table.findAll("tr",recursive=False)
    i = 0
    record = None
    count = 0
    for row in rows:
        strong = row.find("strong", text = "Company")
        if strong:
            i = 1
            record = {}
            continue
        strong = row.find("strong", text = "Patent title")
        if strong:
            i = 2
        else:
            strong = row.find("strong", text = "Country of registration")
            if strong:
                i = 3

        if i == 1:
            cols = row.findAll("td",recursive=False)
            record['company'] = cols[1].text.strip()
            record['publication_no'] = cols[2].text.strip()
            record['application_no'] = cols[3].text.strip()
            record['deliverable_no'] = cols[4].text.strip()
            record['section'] = cols[5].text.strip()
            record['version'] = cols[6].text.strip()
            record['projects'] = cols[7].text.strip()
            record['declaration_date'] = cols[8].text.strip()
            i=0
        if i == 2:
            record['patent_title'] = strong.findNext(text=True).strip()
            i=0
        if i == 3:
            cols = row.findAll("tr")[1].findAll("td")
            record['country_of_registration'] = cols[1].text.strip()
            record['applicable_countries'] = cols[2].text.strip().split("&nbsp;-&nbsp;")
            scraperwiki.datastore.save(['company','publication_no','application_no','projects','declaration_date'], record)
            count = count+1
            i=0
    return count        
        
def run():
    url = "http://webapp.etsi.org/ipr/IPRList.asp?viewPage=1&toDisplay=100"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    form = soup.find("form", id = "form1")
    size = int(form.find("table").find('tr').findAll("td")[2].find("strong").text)
    for i in range(1, 2 + size/100):
        try:
            scrape_page("http://webapp.etsi.org/ipr/IPRList.asp?viewPage="+str(i)+"&toDisplay=100")
        except:
            pass

print "begin"
#scrape_page("http://webapp.etsi.org/ipr/IPRList.asp?viewPage=65&toDisplay=100")
run()
