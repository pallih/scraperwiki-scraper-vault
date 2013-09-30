import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re

# Blank Python
# HANSARD_ARCHIVE = 'http://www.parlimen.gov.my/index.php?modload=sidang&uweb=dr&doc=op&arkib=yes'
HANSARD_ARCHIVE = 'http://www.parlimen.gov.my/index.php?modload=sidang&uweb=dr&doc=op&arkib=yes&lang=en'
def extract_url(href):
    remove_js = href.replace('javascript:loadResult','').replace(';','')
    remove_paren = remove_js.replace('(','').replace(')','')
    splitted = remove_paren.split(',')[0]
    return splitted.replace("'",'')

def main():
    page = urllib2.urlopen(HANSARD_ARCHIVE)
    soup = BeautifulSoup(page)
    #cr = soup.findAll('tr',{'class':'child-row2011'})
    cr = soup.findAll('tr',{'class':re.compile('child\-row201*')})
    for i in cr:
        href = i.findAll('td')[1].find('a')
        dt = href.text
        href_str = href['href']
        url = extract_url(href_str)
        scraperwiki.sqlite.save(unique_keys=['date'],data={'date':dt,'url':url})


main()
import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re

# Blank Python
# HANSARD_ARCHIVE = 'http://www.parlimen.gov.my/index.php?modload=sidang&uweb=dr&doc=op&arkib=yes'
HANSARD_ARCHIVE = 'http://www.parlimen.gov.my/index.php?modload=sidang&uweb=dr&doc=op&arkib=yes&lang=en'
def extract_url(href):
    remove_js = href.replace('javascript:loadResult','').replace(';','')
    remove_paren = remove_js.replace('(','').replace(')','')
    splitted = remove_paren.split(',')[0]
    return splitted.replace("'",'')

def main():
    page = urllib2.urlopen(HANSARD_ARCHIVE)
    soup = BeautifulSoup(page)
    #cr = soup.findAll('tr',{'class':'child-row2011'})
    cr = soup.findAll('tr',{'class':re.compile('child\-row201*')})
    for i in cr:
        href = i.findAll('td')[1].find('a')
        dt = href.text
        href_str = href['href']
        url = extract_url(href_str)
        scraperwiki.sqlite.save(unique_keys=['date'],data={'date':dt,'url':url})


main()
