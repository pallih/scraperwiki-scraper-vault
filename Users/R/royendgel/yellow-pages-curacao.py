#####################################################################################################
#Imports 

import scraperwiki
import urllib, urllib2
from bs4 import BeautifulSoup


#####################################################################################################
#Link Configuration

link = "http://yellowpages-curacao.com/categories/"
category1 = "automotive-marine"
category2 = "batteries"
name = ""
phone = ""
address = ""
url = ""
zipcode = ""
email = ""


#####################################################################################################
#Link Build

buildlink = link + category1 + '/' + category2



#####################################################################################################
# Call the url

read = urllib2.urlopen(buildlink).read()


#####################################################################################################
#Call BS4

scrap = BeautifulSoup(read)


totalrecords = scrap.find("div", {"class":"content-inside"}).find("h3")

showingrecords = totalrecords.find_next()
showingrecords = showingrecords.text
totalrecords = totalrecords.text
print showingrecords
print totalrecords
#####################################################################################################
res = scrap.find("table", {"class": "resultados"})
#####################################################################################################
#companyname text
companyname = res.find("td", {"class": "titulo"}).text

#####################################################################################################
#Company adress
companyaddress = res.find("td", {"class": "address"}).text
print companyaddress

#
