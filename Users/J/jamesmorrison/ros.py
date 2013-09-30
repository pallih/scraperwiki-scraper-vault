import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

url = "http://www.ros.gov.uk/shp_info.html"
url2 = "https://www.eservices.ros.gov.uk/shp/ros/shp/presentation/ui/pageflows/advancedSearchResult.do"
url3 = "https://www.eservices.ros.gov.uk/shp/ros/shp/presentation/ui/pageflows/loadingPleaseWait.do"
data = "Content-Type: application/x-www-form-urlencoded Content-Length: 553 %7BactionForm.postcode%7D=HS2&%7BactionForm.postcode2%7D=0&%7BactionForm.streetName%7D=&%7BactionForm.district%7D=&%7BactionForm.town%7D=&wlw-select_key%3A%7BactionForm.fromMonth%7DOldValue=true&wlw-select_key%3A%7BactionForm.fromMonth%7D=January&wlw-select_key%3A%7BactionForm.fromYear%7DOldValue=true&wlw-select_key%3A%7BactionForm.fromYear%7D=2011&wlw-select_key%3A%7BactionForm.toMonth%7DOldValue=true&wlw-select_key%3A%7BactionForm.toMonth%7D=April&wlw-select_key%3A%7BactionForm.toYear%7DOldValue=true&wlw-select_key%3A%7BactionForm.toYear%7D=2011"

def Main():
    scrapePage()

def scrapePage():
    br = mechanize.Browser()
    br.set_handle_robots(False) # robots.txt doesn't exist, don't waste time looking for it
    br.open(url)
    response1 = list(br.links())[-9].url
    print response1
    br.open(response1)
    br.select_form(name="termsForm")
    response2 = br.submit()
    print response2.read()
    response3 = br.open(url2,data).read()
    response4 = br.open(url2).read()
    print response3
##  contents = urllib.urlopen(response2).read()
##  print contents

Main()

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

url = "http://www.ros.gov.uk/shp_info.html"
url2 = "https://www.eservices.ros.gov.uk/shp/ros/shp/presentation/ui/pageflows/advancedSearchResult.do"
url3 = "https://www.eservices.ros.gov.uk/shp/ros/shp/presentation/ui/pageflows/loadingPleaseWait.do"
data = "Content-Type: application/x-www-form-urlencoded Content-Length: 553 %7BactionForm.postcode%7D=HS2&%7BactionForm.postcode2%7D=0&%7BactionForm.streetName%7D=&%7BactionForm.district%7D=&%7BactionForm.town%7D=&wlw-select_key%3A%7BactionForm.fromMonth%7DOldValue=true&wlw-select_key%3A%7BactionForm.fromMonth%7D=January&wlw-select_key%3A%7BactionForm.fromYear%7DOldValue=true&wlw-select_key%3A%7BactionForm.fromYear%7D=2011&wlw-select_key%3A%7BactionForm.toMonth%7DOldValue=true&wlw-select_key%3A%7BactionForm.toMonth%7D=April&wlw-select_key%3A%7BactionForm.toYear%7DOldValue=true&wlw-select_key%3A%7BactionForm.toYear%7D=2011"

def Main():
    scrapePage()

def scrapePage():
    br = mechanize.Browser()
    br.set_handle_robots(False) # robots.txt doesn't exist, don't waste time looking for it
    br.open(url)
    response1 = list(br.links())[-9].url
    print response1
    br.open(response1)
    br.select_form(name="termsForm")
    response2 = br.submit()
    print response2.read()
    response3 = br.open(url2,data).read()
    response4 = br.open(url2).read()
    print response3
##  contents = urllib.urlopen(response2).read()
##  print contents

Main()

