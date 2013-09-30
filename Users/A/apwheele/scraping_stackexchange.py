#this scraper is intended to grab the addresses listed on the stackexchange profile pages,
#and then map them, taken from question http://meta.gis.stackexchange.com/questions/544/map-of-user-locations

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

#looping through the user pages
for i in (range(5)): #a bit hacky, if you want all the user pages, just insert 77 (as of 7/26/2011)!
    url = "http://gis.stackexchange.com/users?page=" + str(i)
    webpage = scraperwiki.scrape(url)
    soup = BeautifulSoup(webpage)
    user_details = soup.findAll("div","user-details") #within this set of tags is the info I want

#scraping the user info 
    for i in range(len(user_details)):
        temp_name = user_details[i].find(name = 'a',attrs={"href" : re.compile("/users/")})    
        data = {}
        data ['name'] = temp_name.string
        temp_location = user_details[i].find("span", "user-location")
        data['location'] = temp_location.string
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)    #saving the data


#this scraper is intended to grab the addresses listed on the stackexchange profile pages,
#and then map them, taken from question http://meta.gis.stackexchange.com/questions/544/map-of-user-locations

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

#looping through the user pages
for i in (range(5)): #a bit hacky, if you want all the user pages, just insert 77 (as of 7/26/2011)!
    url = "http://gis.stackexchange.com/users?page=" + str(i)
    webpage = scraperwiki.scrape(url)
    soup = BeautifulSoup(webpage)
    user_details = soup.findAll("div","user-details") #within this set of tags is the info I want

#scraping the user info 
    for i in range(len(user_details)):
        temp_name = user_details[i].find(name = 'a',attrs={"href" : re.compile("/users/")})    
        data = {}
        data ['name'] = temp_name.string
        temp_location = user_details[i].find("span", "user-location")
        data['location'] = temp_location.string
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)    #saving the data


