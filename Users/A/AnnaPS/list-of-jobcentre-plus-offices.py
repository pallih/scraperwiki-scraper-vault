###################################################################################
# Scrapes the list of Jobcentre Plus offices available on Directgov.
# Because these are behind a 'lookup by postcode' form, we have to first
# pull in a fairly comprehensive list of postcodes (from a UK schools scraper)
# and then submit them one by one.
# Uses mechanize to deal with the forms, and pyquery to do the actual scraping.
####################################################################################

import mechanize 
import scraperwiki
from pyquery import PyQuery as pq
import json, urllib

# Order the data columns in a sensible way
scraperwiki.metadata.save('data_columns', ['name', 'postcode', 'address', 'email'])

# Scrape the results page
def scrape_results(results_page):
    formwraps = results_page("div.formwrap") 
    #formwraps.each(lambda each_div: process(each_div))
    for i in range (len(formwraps)):
        e = formwraps.eq(i)
        name = e("h3").text()
        print "Name: " + name
        address = e.find("p").text()
        #print "Address: " + address
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        #print "Postcode: " + str(postcode)
        email = e.find('a').attr("href")
        #print "Email: " + email
        data = {'name': name,
            'address': address,
            'postcode': postcode,
            'email': email,
           }
        unique_keys = ['name', 'address']
        scraperwiki.datastore.save(unique_keys, data)
    
def get_postcodes():
    offset = 0
    postcodes = ['initial']
    while postcodes != []:    
        POSTCODE_URL = "http://api.scraperwiki.com/api/1.0/datastore/getdata?key=45eb2b099d5c78a46696fd2653c12dfd&format=json&name=edubase-schools-data&limit=500&offset=" + str(offset)
        postcodes = json.load(urllib.urlopen(POSTCODE_URL), encoding='latin-1')
        for item in postcodes:
            try: 
                br.open(url)
                br.select_form(nr=0) 
                print "using postcode: " + item["Postcode"]
                if item["Postcode"] != "":
                    br["ctl00$ContentPlaceHolder1$Postcode"] = item["Postcode"]
                    response = br.submit()
                    results_page = pq(response.read())
                    scrape_results(results_page)
            except:
                print "no postcode found"
        offset += 500

url = "http://los.direct.gov.uk/default.aspx"
br = mechanize.Browser()
get_postcodes()
###################################################################################
# Scrapes the list of Jobcentre Plus offices available on Directgov.
# Because these are behind a 'lookup by postcode' form, we have to first
# pull in a fairly comprehensive list of postcodes (from a UK schools scraper)
# and then submit them one by one.
# Uses mechanize to deal with the forms, and pyquery to do the actual scraping.
####################################################################################

import mechanize 
import scraperwiki
from pyquery import PyQuery as pq
import json, urllib

# Order the data columns in a sensible way
scraperwiki.metadata.save('data_columns', ['name', 'postcode', 'address', 'email'])

# Scrape the results page
def scrape_results(results_page):
    formwraps = results_page("div.formwrap") 
    #formwraps.each(lambda each_div: process(each_div))
    for i in range (len(formwraps)):
        e = formwraps.eq(i)
        name = e("h3").text()
        print "Name: " + name
        address = e.find("p").text()
        #print "Address: " + address
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        #print "Postcode: " + str(postcode)
        email = e.find('a').attr("href")
        #print "Email: " + email
        data = {'name': name,
            'address': address,
            'postcode': postcode,
            'email': email,
           }
        unique_keys = ['name', 'address']
        scraperwiki.datastore.save(unique_keys, data)
    
def get_postcodes():
    offset = 0
    postcodes = ['initial']
    while postcodes != []:    
        POSTCODE_URL = "http://api.scraperwiki.com/api/1.0/datastore/getdata?key=45eb2b099d5c78a46696fd2653c12dfd&format=json&name=edubase-schools-data&limit=500&offset=" + str(offset)
        postcodes = json.load(urllib.urlopen(POSTCODE_URL), encoding='latin-1')
        for item in postcodes:
            try: 
                br.open(url)
                br.select_form(nr=0) 
                print "using postcode: " + item["Postcode"]
                if item["Postcode"] != "":
                    br["ctl00$ContentPlaceHolder1$Postcode"] = item["Postcode"]
                    response = br.submit()
                    results_page = pq(response.read())
                    scrape_results(results_page)
            except:
                print "no postcode found"
        offset += 500

url = "http://los.direct.gov.uk/default.aspx"
br = mechanize.Browser()
get_postcodes()
