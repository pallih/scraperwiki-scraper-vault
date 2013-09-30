import scraperwiki
import requests

SITEPAGE = 'http://delibere.comune.sestri-levante.ge.it:89/ULISS-e/Bacheca/coatti02.aspx?bac_codice=50&SORT=DDPUB'

'''
def parse_page(url):
    s = requests.session()    
    print "parse page called"
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'} 
    response  = s.get(SITEPAGE)
    print response.content

def main():
    print "main called"
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    #scraperwiki.sqlite.commit()
    parse_page(SITEPAGE) 

main()
'''

s = requests.session()
r = s.get(SITEPAGE)
print "got r"
print r.content
import scraperwiki
import requests

SITEPAGE = 'http://delibere.comune.sestri-levante.ge.it:89/ULISS-e/Bacheca/coatti02.aspx?bac_codice=50&SORT=DDPUB'

'''
def parse_page(url):
    s = requests.session()    
    print "parse page called"
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'} 
    response  = s.get(SITEPAGE)
    print response.content

def main():
    print "main called"
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    #scraperwiki.sqlite.commit()
    parse_page(SITEPAGE) 

main()
'''

s = requests.session()
r = s.get(SITEPAGE)
print "got r"
print r.content
