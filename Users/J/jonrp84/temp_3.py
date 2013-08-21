import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup








ad_list=urlopen('http://www.legacy.com/ns/obitfinder/obituary-search.aspx?daterange=Last1Yrs&firstname=John&lastname=Smith&countryid=1&stateid=0&affiliateid=all').read()
soup=BeautifulSoup(ad_list)
print soup

ad_link=soup.findAll("div", {"class":"obitName"})
print ad_link


    



#for row in ad_link:
#    link = row.findAll('a', href=True)
#    data = link.strip()
#    print link
#    print data















#links = ad_link.findAll('a', href=True) # find <a> with a defined href attribute
#for link in links:
#    print link['href']
#-->http://www.gumtree.com/p/flats-houses/2-bed-penthouse-apartment-to-let-15th-floor/100656268
