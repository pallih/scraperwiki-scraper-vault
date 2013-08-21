###################################################
# This scrapes the website has-sante.fr to look   #
# for information about the efficiency of several #
# drugs sold on the French market.                #
###################################################

import scraperwiki
import re
import random
import math
import time
import urllib
from BeautifulSoup import BeautifulSoup
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "interet-medical-2"

scraperwiki.metadata.save('data_columns', ['Name', 'page_url', 'pdf_url', 'interet_sante'])

# This function looks for the actual pdf, parses it and looks for keywords
def parse_pdf(url, name, page_url):
    url = url.encode('ascii')
    name = name.encode('utf-8')
    print name
    pdf_url = "http://www.has-sante.fr/portail/" + url
    avis = " "
    avis2 = " "
    
    #follows the first link
    a = scraperwiki.scrape(pdf_url)
    a = a.lower()    

    #finds the actual link (there's a redirect)
    soup = BeautifulSoup(a)
    
    pdf_url = soup.find("meta")

    pdf_url = pdf_url['content']
    pdf_url = pdf_url.replace("0; url='../../../../", "http://www.has-sante.fr/portail/")
    pdf_url = pdf_url[:-1]
    pdf_url = pdf_url.encode('ascii')
    
    #now for the real pdf
    try:
        b = scraperwiki.scrape(pdf_url)
        s = BeautifulSoup(scraperwiki.pdftoxml(b))
    
        #some basic regex to extract meaningful info
        for t in s.findAll('text'):
            if t.text != " ": 
                pattern = '^.*?int.r.t de sant. publique.*?faible.*?$'
                pattern2 = '^.*?service m.dical rendu par.*?$'
                if (re.search(pattern, t.text)):
                    avis = t.text
                    avis = avis.encode('utf-8')
                    print avis
                elif(re.search(pattern2, t.text)):
                    avis2 = t.text
                    avis2 = avis2.encode('utf-8')
                    print avis2
    
        #now we've got everything, we're adding it to the DB
        data = {}
        medoc_name = name
        data['Name'] = medoc_name
        data['pdf_url'] = pdf_url
        data['page_url'] = page_url
        data['interet_sante'] = avis + "\n" + avis2
        data[medoc_name] = medoc_name
        scraperwiki.datastore.save(['Name'], data)

    except: 
        print "Error" + pdf_url

#this function looks for the url that will lead us to the pdf in the details page
def extract_info(url):
    url = "http://www.has-sante.fr/portail/" + url 
    url = url.encode('ascii')
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    #gets the drug's name
    Name = soup.find("h1")
    Name = Name.contents[0]

    #gets the link to the pdf
    pdf_url = soup.find("li", { "class" : "pdf" })
    pdf_url = pdf_url.a['href']
    parse_pdf(pdf_url, Name, url)
    
#this function gets the links to the details pages
def scrape_names_and_links(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    #finds all occurences of the drugs on the page    
    subpages_url = soup.findAll("dt", { "class" : "result" })
    for subpage_url in subpages_url:
        subpage = subpage_url.a['href']
        extract_info(subpage)

#finds how many records are in the DB already
keys = getKeys(sourcescraper)
start = math.floor(len(keys) / 10)*10
start = int(start)
print start

#now for the trigger
count = start
max = start + 50

while (count<=max):
    count_str = str(count)
    #countr_str = count_str[:-2]
    url = "http://www.has-sante.fr/portail/jcore/portal/ajaxPortal.jsp?portletId=c_63468&usage=full&start=" + count_str
    print url
    time.sleep(random.random()*2)
    scrape_names_and_links(url)
    count += 10