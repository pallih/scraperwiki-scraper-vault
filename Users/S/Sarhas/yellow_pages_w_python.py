import scraperwiki
import csv
import requests
import string
import time

from bs4 import BeautifulSoup
from types import *

def get_company_link(URL2):
    response2 = requests.get(URL2)

    if response2.status_code == 200:
        soup2 = BeautifulSoup(response2.text)
        temp = soup2.find("div", "cm_xboxcontentinfo")
        if not isinstance(temp,NoneType): # exception 2: No Company Page on Chamber directory
            temp2 = temp.find_all("td", "cm_infotext")
            if len(list(temp2)) == 2:
                return temp2[1].a['href']
            else:
                return "No Website"
        else:
            return "No Company Page"

def get_first_group(URL):
    # URL = 'http://chamber.sdncc.com/list/searchalpha/A.htm'
    response = requests.get(URL)
    links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text)
        for tag in soup.find_all("div","cm_member_name"):
            link = tag.a['href']
            name = ' '.join(tag.a.text.split())
            address_temp = tag.next_sibling.next_sibling.string.split('\n')
            address = ' '.join(address_temp[1].split())
            city =  ' '.join(address_temp[2].split())
            state =  ' '.join(address_temp[3].split())
            zip = ' '.join(address_temp[4].split())
            phone = ' '.join(tag.next_sibling.next_sibling.next_sibling.next_sibling.string.split())
            company_link = get_company_link(link)
            print "processing"
  
            links.append((name,link,address,city,state,zip,phone,company_link))
            #print address, "\n"

    for info in links:
        data = {
            'name' : info[0],
            'link' : info[1],
            'address' : info[2],
            'city' : info[3],
            'state' : info[4],
            'zip' : info[5],
            'phone' : info[6],
            'company_link' : info[7]
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        # print "Company Name: %s, URL: %s" % (info[0], info[1])

url_start = "http://chamber.sdncc.com/list/searchalpha/"
url_end = ".htm"
indices = ["0-9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for i in indices:
    URL = url_start + i + url_end
    get_first_group(URL)
    time.sleep(60)

