import scraperwiki
import lxml.html
from lxml.html.clean import clean_html


# Blank Python
x=0
string = ''
apv = 0
apvtup=[0,0]
apvtop=0
for x in xrange(11750,11759):
    null= 0
    volumeb = 0
    priceb = 0
    alcb = 0
    apv = 0
    a= "http://www.humanatic.com/pages/whip.cfm?uid="+str(x)
    html = scraperwiki.scrape(a)
    string =''
    
    root = lxml.html.fromstring(html)
    tds = root.cssselect('div')

    string = lxml.html.tostring(root)
    string = clean_html(string)
    mlp = string.find('Jhen Totz')
    if mlp > 0:
        scraperwiki.sqlite.save(unique_keys=["a"], data={'a':[x]})
        
    if apv > apvtop:
        apvtop = apv
        apvtup = [x,apv]
        print apvtup
import scraperwiki
import lxml.html
from lxml.html.clean import clean_html


# Blank Python
x=0
string = ''
apv = 0
apvtup=[0,0]
apvtop=0
for x in xrange(11750,11759):
    null= 0
    volumeb = 0
    priceb = 0
    alcb = 0
    apv = 0
    a= "http://www.humanatic.com/pages/whip.cfm?uid="+str(x)
    html = scraperwiki.scrape(a)
    string =''
    
    root = lxml.html.fromstring(html)
    tds = root.cssselect('div')

    string = lxml.html.tostring(root)
    string = clean_html(string)
    mlp = string.find('Jhen Totz')
    if mlp > 0:
        scraperwiki.sqlite.save(unique_keys=["a"], data={'a':[x]})
        
    if apv > apvtop:
        apvtop = apv
        apvtup = [x,apv]
        print apvtup
