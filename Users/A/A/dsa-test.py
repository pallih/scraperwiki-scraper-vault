###############################################################################
# scraper, concept from http://scraperwiki.com/scrapers/postcode-uploader/edit/
###############################################################################

import csv
import urllib
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError

base_url = "http://finddrivinginstructor.direct.gov.uk/DSAFindNearestWebApp/findNearest.form"
postcode_dir = "http://seagrass.goatchurch.org.uk/~julian/postcodes/data/CSV/"

def Main():
    # get list of files
    d = urllib.urlopen(postcode_dir).read()
    postcodefiles = re.findall('<a href="(.*?\.csv)">', d)

    print len(postcodefiles), postcodefiles
    
    # iterate through each file (recording progress in metadata)
    nprog = int(scraperwiki.metadata.get("nprog", "0"))
    for n in range(nprog, len(postcodefiles)):
        fl = postcodefiles[n]
        print n, fl
        s = urllib.urlopen(postcode_dir + fl)
        c = csv.reader(s.readlines())
        for row in c:
            postcode = row[0]
            get_instructors(postcode)
        scraperwiki.metadata.save("nprog", n+1)

                     
def get_instructors(postcode):
    #print postcode
    scraperwiki.metadata.save("postcode", postcode)
    qs = urllib.urlencode({'postcode':postcode})
    url = "%s?%s" % (base_url, qs)
    scrape_and_look_for_next_link(url)
    
    
def scrape_and_look_for_next_link(url):
    html = None
    try:
        html = scraperwiki.scrape(url)
    except:
        print 'Error: %s' %(url)
    if html: 
        soup = BeautifulSoup(html)
        scrape_table(soup)
        next_link = soup.find("a", { "class" : "next" })
        #print next_link
        if next_link:
            next_url = base_url + next_link['href']
            #print next_url
            scrape_and_look_for_next_link(next_url)
    
    
def scrape_table(soup):
    data_table = soup.find("table", { "id" : "result" })
    if data_table:
        rows = data_table.findAll("tr")
        for row in rows:
            record = {}
            table_cells = row.findAll("td")
            if table_cells: 
                distance = table_cells[4].text[:3]
                #print distance
                if distance == '0.0':
                    record['Name'] = table_cells[1].text
                    record['Number'] = table_cells[2].text
                    record['Email'] = table_cells[3].text
                    record['Postcode'] = scraperwiki.metadata.get("postcode", "")
                    # Print out the data we've gathered
                    print record, '------------'
                    scraperwiki.datastore.save(["Name"], record)
    else:
        print "Table not found"

scraperwiki.metadata.save("nprog", 0)
Main()
    
    
    
    ###############################################################################
# scraper, concept from http://scraperwiki.com/scrapers/postcode-uploader/edit/
###############################################################################

import csv
import urllib
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError

base_url = "http://finddrivinginstructor.direct.gov.uk/DSAFindNearestWebApp/findNearest.form"
postcode_dir = "http://seagrass.goatchurch.org.uk/~julian/postcodes/data/CSV/"

def Main():
    # get list of files
    d = urllib.urlopen(postcode_dir).read()
    postcodefiles = re.findall('<a href="(.*?\.csv)">', d)

    print len(postcodefiles), postcodefiles
    
    # iterate through each file (recording progress in metadata)
    nprog = int(scraperwiki.metadata.get("nprog", "0"))
    for n in range(nprog, len(postcodefiles)):
        fl = postcodefiles[n]
        print n, fl
        s = urllib.urlopen(postcode_dir + fl)
        c = csv.reader(s.readlines())
        for row in c:
            postcode = row[0]
            get_instructors(postcode)
        scraperwiki.metadata.save("nprog", n+1)

                     
def get_instructors(postcode):
    #print postcode
    scraperwiki.metadata.save("postcode", postcode)
    qs = urllib.urlencode({'postcode':postcode})
    url = "%s?%s" % (base_url, qs)
    scrape_and_look_for_next_link(url)
    
    
def scrape_and_look_for_next_link(url):
    html = None
    try:
        html = scraperwiki.scrape(url)
    except:
        print 'Error: %s' %(url)
    if html: 
        soup = BeautifulSoup(html)
        scrape_table(soup)
        next_link = soup.find("a", { "class" : "next" })
        #print next_link
        if next_link:
            next_url = base_url + next_link['href']
            #print next_url
            scrape_and_look_for_next_link(next_url)
    
    
def scrape_table(soup):
    data_table = soup.find("table", { "id" : "result" })
    if data_table:
        rows = data_table.findAll("tr")
        for row in rows:
            record = {}
            table_cells = row.findAll("td")
            if table_cells: 
                distance = table_cells[4].text[:3]
                #print distance
                if distance == '0.0':
                    record['Name'] = table_cells[1].text
                    record['Number'] = table_cells[2].text
                    record['Email'] = table_cells[3].text
                    record['Postcode'] = scraperwiki.metadata.get("postcode", "")
                    # Print out the data we've gathered
                    print record, '------------'
                    scraperwiki.datastore.save(["Name"], record)
    else:
        print "Table not found"

scraperwiki.metadata.save("nprog", 0)
Main()
    
    
    
    