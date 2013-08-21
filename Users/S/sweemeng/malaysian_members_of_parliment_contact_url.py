import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re

# Blank Python
URL = 'http://www.parlimen.gov.my/index.php?modload=ahlidewan&uweb=dr'
BASE_URL = 'http://www.parlimen.gov.my/'

def main():
    page = urllib2.urlopen(URL)
    soup = BeautifulSoup(page)

    tb = soup.find('tbody',{'class':'tablecontentsmallXx'})
    tr = tb.findAll('tr')
    for i in tr:
        key = i.findAll('td')[0].text
        href = i.findAll('td')[1].find('a')
        name = href.text
        url = href['href']
        url = BASE_URL+url
        scraperwiki.sqlite.save(unique_keys=['key'],data={'key':key,'mp_name':name,'url':url})


main()
