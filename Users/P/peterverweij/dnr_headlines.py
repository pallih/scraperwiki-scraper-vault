import scraperwiki
import urllib2
import re
from bs4 import BeautifulSoup as Soup

url = "http://nl.wikipedia.org/wiki/Lijst_van_huidige_burgemeesters_in_Nederland"  
     
#for num in range (0, 10):
 #   baseplusnr = base_url+str(num)
  #  url = baseplusnr
   # #print url


    
soup = Soup(url)
hl = soup.findAll("tr")
    #hlclean = hl.href.string
print hl
