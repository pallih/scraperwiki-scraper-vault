import scraperwiki
import csv
import requests
import string

from bs4 import BeautifulSoup 
from types import *


def get_company_link(URL):
    response = requests.get(URL)

    if response.status_code == 200:
        soup2 = BeautifulSoup(response.text)
        temp = soup2.find("div", "cm_xboxcontentinfo")
        if not isinstance(temp,NoneType): # exception 2: No Company Page on Chamber Directory
            #temp2 = temp.a['hr
            temp2 = temp.find_all("td", "cm_infotext")
            if len(list(temp2)) == 2:  # exception 1: Company does not have website
                return temp2[1].a['href']  
            else:
                return "No Website"
        else:
            return "No Company Page"

        

get_company_link('http://chamber.sdncc.com/list/member/bernardo-heights-dental-group-san-diego-20055.htm')
import scraperwiki
import csv
import requests
import string

from bs4 import BeautifulSoup 
from types import *


def get_company_link(URL):
    response = requests.get(URL)

    if response.status_code == 200:
        soup2 = BeautifulSoup(response.text)
        temp = soup2.find("div", "cm_xboxcontentinfo")
        if not isinstance(temp,NoneType): # exception 2: No Company Page on Chamber Directory
            #temp2 = temp.a['hr
            temp2 = temp.find_all("td", "cm_infotext")
            if len(list(temp2)) == 2:  # exception 1: Company does not have website
                return temp2[1].a['href']  
            else:
                return "No Website"
        else:
            return "No Company Page"

        

get_company_link('http://chamber.sdncc.com/list/member/bernardo-heights-dental-group-san-diego-20055.htm')
