import scraperwiki           
html = scraperwiki.scrape("http://www.berlin.de/ba-tempelhof-schoeneberg/organisationseinheit/planen/abgeschlossene_b-plaene.html")
print html 

import lxml.html       
root = lxml.html.fromstring(html) 

listitem=''
for li in root.cssselect("ul class=bacontent c2"):
    print(li)

  #  tds = [td.text_content().strip().encode('UTF-8') for td in tds]
   # if tds[0]!='':
    #    datum=tds[0]
   # else: 
    #    tds[0]=datum 
    #if tds[1]!='' and tds[0]!='Jahr': 
     #   data = {'Jahr' : tds[0], 'Datum' : tds[1], 'Land' : tds[2], 'Art' : tds[3], 'Turnus' : tds[4]   }    
      #  print data 
       # scraperwiki.sqlite.save(unique_keys=['Jahr', 'Datum', 'Land', 'Art', 'Turnus' ], data=data)
#")
#print html 

#import lxml.html       
#root = lxml.html.fromstring(html) 

#Datum=''
#for tr in root.cssselect("table tr"): 
#    tds = tr.cssselect("td")     
#    tds = [td.text_content().strip().encode('UTF-8') for td in tds]
#    if tds[0]!='':
#        datum=tds[0]
#    else: 
#        tds[0]=datum 
#    if tds[1]!='' and tds[0]!='Jahr': 
#        data = {'Jahr' : tds[0], 'Datum' : tds[1], 'Land' : tds[2], 'Art' : tds[3], 'Turnus' : tds[4]   }    
#        print data 
#        scraperwiki.sqlite.save(unique_keys=['Jahr', 'Datum', 'Land', 'Art', 'Turnus' ], data=data)
import scraperwiki           
html = scraperwiki.scrape("http://www.berlin.de/ba-tempelhof-schoeneberg/organisationseinheit/planen/abgeschlossene_b-plaene.html")
print html 

import lxml.html       
root = lxml.html.fromstring(html) 

listitem=''
for li in root.cssselect("ul class=bacontent c2"):
    print(li)

  #  tds = [td.text_content().strip().encode('UTF-8') for td in tds]
   # if tds[0]!='':
    #    datum=tds[0]
   # else: 
    #    tds[0]=datum 
    #if tds[1]!='' and tds[0]!='Jahr': 
     #   data = {'Jahr' : tds[0], 'Datum' : tds[1], 'Land' : tds[2], 'Art' : tds[3], 'Turnus' : tds[4]   }    
      #  print data 
       # scraperwiki.sqlite.save(unique_keys=['Jahr', 'Datum', 'Land', 'Art', 'Turnus' ], data=data)
#")
#print html 

#import lxml.html       
#root = lxml.html.fromstring(html) 

#Datum=''
#for tr in root.cssselect("table tr"): 
#    tds = tr.cssselect("td")     
#    tds = [td.text_content().strip().encode('UTF-8') for td in tds]
#    if tds[0]!='':
#        datum=tds[0]
#    else: 
#        tds[0]=datum 
#    if tds[1]!='' and tds[0]!='Jahr': 
#        data = {'Jahr' : tds[0], 'Datum' : tds[1], 'Land' : tds[2], 'Art' : tds[3], 'Turnus' : tds[4]   }    
#        print data 
#        scraperwiki.sqlite.save(unique_keys=['Jahr', 'Datum', 'Land', 'Art', 'Turnus' ], data=data)
