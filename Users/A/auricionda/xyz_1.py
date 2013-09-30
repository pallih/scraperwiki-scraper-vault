import scraperwiki
import lxml.html
a=['ahJzfmdvb2dsZS1zb2x2ZWZvcnhyEAsSCE1vb25zaG90GOHUAww/solve-for-x-shawn-douglas-on-targeted-therapeutics', 
'ahJzfmdvb2dsZS1zb2x2ZWZvcnhyEAsSCE1vb25zaG90GImeAww/team-vor-tek-wendy-schmidt-oil-cleanup-x-challenge'
]
b=0
problema=str
tecnologia=str
solucion=str
while b !=2: 
    html = scraperwiki.scrape("http://www.solveforx.com/moonshots/"+str(a[b]))
    root = lxml.html.fromstring(html)
    print root
    for el in root.cssselect("div.section")[3]:
        for el2 in el.cssselect("div.column"):
            for el3 in el2.cssselect("div.group p")[0]:
                problema=el3.text
            for el3 in el2.cssselect("div.group p")[1]:
                tecnologia=el3.text
            for el3 in el2.cssselect("div.group p")[2]:
                solucion=el3.text
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'problema':problema,'tecnologia':tecnologia,'solucion':solucion})
    b=b+1
        

import scraperwiki
import lxml.html
a=['ahJzfmdvb2dsZS1zb2x2ZWZvcnhyEAsSCE1vb25zaG90GOHUAww/solve-for-x-shawn-douglas-on-targeted-therapeutics', 
'ahJzfmdvb2dsZS1zb2x2ZWZvcnhyEAsSCE1vb25zaG90GImeAww/team-vor-tek-wendy-schmidt-oil-cleanup-x-challenge'
]
b=0
problema=str
tecnologia=str
solucion=str
while b !=2: 
    html = scraperwiki.scrape("http://www.solveforx.com/moonshots/"+str(a[b]))
    root = lxml.html.fromstring(html)
    print root
    for el in root.cssselect("div.section")[3]:
        for el2 in el.cssselect("div.column"):
            for el3 in el2.cssselect("div.group p")[0]:
                problema=el3.text
            for el3 in el2.cssselect("div.group p")[1]:
                tecnologia=el3.text
            for el3 in el2.cssselect("div.group p")[2]:
                solucion=el3.text
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'problema':problema,'tecnologia':tecnologia,'solucion':solucion})
    b=b+1
        

