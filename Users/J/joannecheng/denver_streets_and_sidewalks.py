import scraperwiki
import urllib
import urllib2
import re
import simplejson
import time
import datetime
import requests
from bs4 import BeautifulSoup

# TODO -
#   Geocode addresses
#   Parse start/end date
#   Give each entry a unique ID

def get_pdf_link():
    root_url = "http://www.denvergov.org"
    closures_page = requests.get(root_url + "/streetclosures")

    soup = BeautifulSoup(closures_page.text)
    return root_url + soup.find(id='dnn_ctr499298_HtmlModule_lblContent').find('a').get('href')

def get_dates(date_string):
    re_date = "Start Date:\s+(\d+\/\d+\/\d+)\s+-\s+End Date:\s+(\d+\/\d+\/\d+)"
    regex = re.compile(re_date)
    r = regex.search(date_string)
    return r.groups()

url = get_pdf_link()
xml = scraperwiki.pdftoxml(urllib2.urlopen(url).read())
print xml
parsed = BeautifulSoup(xml).text.split("\n")
filtered_list = parsed[parsed.index('Location: '):]
closures = []

i = 0
current_closure = -1
print len(filtered_list)
while i < len(filtered_list):
    text = filtered_list[i]
    if text == "Location: ":
        closures.append({})
        current_closure = len(closures) - 1
        i += 1
        closures[current_closure]['location'] = filtered_list[i]
    elif text == "Type: ":
        i += 1
        closures[current_closure]['type'] = filtered_list[i]
    elif text == "Date: ":
        i += 1
        dates = get_dates(filtered_list[i])
        closures[current_closure]['start_date'] = datetime.datetime.strptime(dates[0], '%m/%d/%Y')
        closures[current_closure]['end_date'] = datetime.datetime.strptime(dates[1], '%m/%d/%Y')
    elif text == "Time: ":
        i += 1
        closures[current_closure]['time'] = filtered_list[i]
    elif text == "Purpose: ":
        i += 1
        closures[current_closure]['purpose'] = filtered_list[i]
    elif text == "Contractor: ":
        closures[current_closure]['contractor'] = filtered_list[i]
    
    i+= 1


for closure in closures:
    print closure['location']
    #scraperwiki.sqlite.save(unique_keys=['location'], data=closure)