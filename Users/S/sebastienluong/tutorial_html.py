import scraperwiki
import re
from bs4 import BeautifulSoup

url =  "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
#Crawl the url
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://unstats.un.org/unsd/demographic/products/socind/education.htm'
# finds all td in html file with 2 attributes
td = soup.findAll(lambda tag: len(tag.attrs) == 2 and 'td')
#country = soup.findAll(lambda tag: len(tag.attrs)==1 and 'height=19' )

'''
#restrict by css class
tr=soup.find("tr",{"class": "tcont"})
td=tr.findNext("td")
#next argument grabs the string
country=td.next
#restrict by arguments
year=tr.findNext(align="right").next
#movement to next relevant data
total=tr.findNext(width="71").string
male=tr.findNext(width="72").string
female=tr.findNext(width="64").string
'''
record={}
tr=soup.findAll("tr",{"class": "tcont"})
# tr is a list therefore use loop to grab all items within
for item in tr: 
    country=item.find("td").next
    year=item.find(align="right").next
    total=item.find(align="right").next
    print total
    male=item.find(align="right").next
    female=item.find(align="right").next


    record["Country"]=country
    record["Year"]=year
    record["Total"]=total
    record["Male"]=male
    record["Female"]=female

    scraperwiki.sqlite.save([], record)    

#td=tr.find("td")

'''
record["Country"]= country
record["Year"]=year 
record["Total years"]=total
record["Male Years"]=male
record["Female Years"]=female

for i in record: 
    print i+": "+record[i]
'''
#print soup.prettify()
'''for i in country:
    record["Country"]=td.find(height=19)
    record["Year"]=td.find(align=right)
'''import scraperwiki
import re
from bs4 import BeautifulSoup

url =  "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
#Crawl the url
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://unstats.un.org/unsd/demographic/products/socind/education.htm'
# finds all td in html file with 2 attributes
td = soup.findAll(lambda tag: len(tag.attrs) == 2 and 'td')
#country = soup.findAll(lambda tag: len(tag.attrs)==1 and 'height=19' )

'''
#restrict by css class
tr=soup.find("tr",{"class": "tcont"})
td=tr.findNext("td")
#next argument grabs the string
country=td.next
#restrict by arguments
year=tr.findNext(align="right").next
#movement to next relevant data
total=tr.findNext(width="71").string
male=tr.findNext(width="72").string
female=tr.findNext(width="64").string
'''
record={}
tr=soup.findAll("tr",{"class": "tcont"})
# tr is a list therefore use loop to grab all items within
for item in tr: 
    country=item.find("td").next
    year=item.find(align="right").next
    total=item.find(align="right").next
    print total
    male=item.find(align="right").next
    female=item.find(align="right").next


    record["Country"]=country
    record["Year"]=year
    record["Total"]=total
    record["Male"]=male
    record["Female"]=female

    scraperwiki.sqlite.save([], record)    

#td=tr.find("td")

'''
record["Country"]= country
record["Year"]=year 
record["Total years"]=total
record["Male Years"]=male
record["Female Years"]=female

for i in record: 
    print i+": "+record[i]
'''
#print soup.prettify()
'''for i in country:
    record["Country"]=td.find(height=19)
    record["Year"]=td.find(align=right)
'''