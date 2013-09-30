import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
from BeautifulSoup import BeautifulSoup

# Getting Eurovision 2012 Participants
# scraperwiki.sqlite.save(unique_keys=["country"], data={"country":el.text})
# scraperwiki.sqlite.save(unique_keys=["contestant"], data={"country":el.text))

url = "http://www.eurovision.tv/page/malmo-2013/about/shows/participants"           
#scraperwiki.sqlite.execute("delete from swdata") 

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

soup = BeautifulSoup(''.join(html))
#print [elm.a.text for elm in soup.findAll('tr', {'class': 'nowinner'})]
countries=soup.findAll('tr',{'class':'nowinner'})
count = 0
for country in countries:
    if count < 16:
        semi = "1"
    elif count >= 16 and count < 33:
        semi = "2"
    else:
        semi = "0"

    song = country.findAll('td')[3].contents
    singers=country.findAll("span", {'itemprop':'name'}) 
          
    scraperwiki.sqlite.save(unique_keys=["country"], data={"country":country.a.text, "singer":singers[0].text, "song": song[0], "semi": semi})
    count = count + 1
    print country.a.text
    print singers[0].text
    print song[0]import scraperwiki
import lxml.html
import urllib   
import simplejson
import urllib2
from BeautifulSoup import BeautifulSoup

# Getting Eurovision 2012 Participants
# scraperwiki.sqlite.save(unique_keys=["country"], data={"country":el.text})
# scraperwiki.sqlite.save(unique_keys=["contestant"], data={"country":el.text))

url = "http://www.eurovision.tv/page/malmo-2013/about/shows/participants"           
#scraperwiki.sqlite.execute("delete from swdata") 

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

soup = BeautifulSoup(''.join(html))
#print [elm.a.text for elm in soup.findAll('tr', {'class': 'nowinner'})]
countries=soup.findAll('tr',{'class':'nowinner'})
count = 0
for country in countries:
    if count < 16:
        semi = "1"
    elif count >= 16 and count < 33:
        semi = "2"
    else:
        semi = "0"

    song = country.findAll('td')[3].contents
    singers=country.findAll("span", {'itemprop':'name'}) 
          
    scraperwiki.sqlite.save(unique_keys=["country"], data={"country":country.a.text, "singer":singers[0].text, "song": song[0], "semi": semi})
    count = count + 1
    print country.a.text
    print singers[0].text
    print song[0]