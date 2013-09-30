import scraperwiki
import lxml.html 
import re
import urllib2,sys
from BeautifulSoup import BeautifulSoup, NavigableString

n = 10

while n < 14:
    address='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S110'
    laskuriaddress = address + str(n)
    print 'Osoite: ', laskuriaddress, 'ja n: ', n 
    n = n +1
    html = urllib2.urlopen(laskuriaddress).read()
    soup = BeautifulSoup(html)
ps = soup.findAll('p') # get all the <td> tags
for p in ps:
    #print td # the full HTML tag
    print p.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE TWO LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for td in tds:
     record = { "p" : p.text } # column name and value
     scraperwiki.datastore.save(["p"], record) # save the records one by one
    
print "Onnistui tällä kertaa :)"
import scraperwiki
import lxml.html 
import re
import urllib2,sys
from BeautifulSoup import BeautifulSoup, NavigableString

n = 10

while n < 14:
    address='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S110'
    laskuriaddress = address + str(n)
    print 'Osoite: ', laskuriaddress, 'ja n: ', n 
    n = n +1
    html = urllib2.urlopen(laskuriaddress).read()
    soup = BeautifulSoup(html)
ps = soup.findAll('p') # get all the <td> tags
for p in ps:
    #print td # the full HTML tag
    print p.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE TWO LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for td in tds:
     record = { "p" : p.text } # column name and value
     scraperwiki.datastore.save(["p"], record) # save the records one by one
    
print "Onnistui tällä kertaa :)"
