import scraperwiki           
from BeautifulSoup import BeautifulSoup, SoupStrainer
import mechanize
import re
import time

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#This is the part of the URL which all our pages share
base_url = 'http://dbpedia.org/page/'

#And here is a little set of companies with operations in India to complete the URLs
India_firms = ['3i_Infotech_Limited','Accenture','ACS','Actiance','Aditi_Technologies','Adobe_Systems','ADP','Adrenalin_eSystems','Affiliated_Computer_Services','Aftek','Agilent_Technologies','AKG_Soft_Infotech','Alcatel_Lucent']

#go through the India_firms list above, and for each ID...
for item in India_firms:
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    print next_link
    #(1) open the page
    # time.sleep(1) #will sleep for 1 second
    # br.open(next_link)


import scraperwiki           
from BeautifulSoup import BeautifulSoup, SoupStrainer
import mechanize
import re
import time

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#This is the part of the URL which all our pages share
base_url = 'http://dbpedia.org/page/'

#And here is a little set of companies with operations in India to complete the URLs
India_firms = ['3i_Infotech_Limited','Accenture','ACS','Actiance','Aditi_Technologies','Adobe_Systems','ADP','Adrenalin_eSystems','Affiliated_Computer_Services','Aftek','Agilent_Technologies','AKG_Soft_Infotech','Alcatel_Lucent']

#go through the India_firms list above, and for each ID...
for item in India_firms:
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    print next_link
    #(1) open the page
    # time.sleep(1) #will sleep for 1 second
    # br.open(next_link)


