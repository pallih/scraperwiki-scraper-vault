from BeautifulSoup import BeautifulSoup
import re
import urllib2

# download the page
response = urllib2.urlopen("http://www.boattrader.com/search-results/Type-any/Make-mako/Length-17,25/Zip-02445/Radius-100/Sort-Length:DESC/")
html = response.read()

# create a beautiful soup object
soup = BeautifulSoup(html)

# all links to detailed boat information have class lfloat
links = soup.findAll("a", { "class" : "lfloat" })
for link in links:
 print link['href']
 print link.string

# all prices are spans and have the class rfloat
prices = soup.findAll("span", { "class" : "rfloat" })
for price in prices:
 print price
 print price.string

# all boat images have attribute height=105
images = soup.findAll("img",height="105")
for image in images:
 print image            # print the whole image tag
 print image['src']    # print the url of the image only
