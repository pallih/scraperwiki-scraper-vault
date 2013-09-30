"""
Started 2012-02-04
This monitors the adding and removal of bishops "in real time"
Data is from http://www.usccb.org/about/bishops-and-dioceses/all-dioceses.cfm
"""


import scraperwiki
from scraperwiki import scrape
import lxml.html


html = scrape('http://www.usccb.org/about/bishops-and-dioceses/all-dioceses.cfm')
root = lxml.html.fromstring(html)
print 'length of html', len(html)
tables = [atable for atable in root.cssselect('table')]
print 'number of tables', len(tables)

#for thetag in table0:
#    print thetag.tag
#for thetr in table0:
    # .cssselect("td.personnel")
#    for thetd in thetr:
#       print thetd.text

#for el in table0:           
 #   print el.tag
  #  for el2 in el:
  #      print "--", el2.tag, el2.attrib, el.text

#print lxml.html.tostring(table0)
all_bishops = []
#table0 = tables[0]
for atable in tables:
    for thetr in atable:
        thebishops = dict()
        theweb = thetr.cssselect('a.subtle')
        if len(theweb) == 1:
            thebishops['url'] = theweb # this has to be changed for the proper data 
        thetd0 = thetr.cssselect('td.personnel')
        #td class="personnel">
        #<strong>Archbishop Thomas J. Rodi </strong><br/>Archbishop of Mobile<br/><br/>
        #<strong>Archbishop Oscar H. Lipscomb </strong><br/>Archbishop Emeritus of Mobile<br/><br/>
        if len(thetd0) == 1:
            #thebishops = dict()
            for subel in thetd0[0]:
                if subel.tag == 'strong':
                    thebishops['bishop'] = subel.text
                else:
                    if len(thebishops) != 0:
                        thetext = lxml.html.tostring(subel)
                        if thetext.startswith('<br>') and len(thetext) > 4:
                             thebishops['position'] = thetext[4:]
                             all_bishops.append(thebishops)
                    

print 'number of bishops', len(all_bishops)
print all_bishops[0:4]

# STORE

# WEBPAGE UPDATE

# TWEET
import tweepy


         
           

        

       

   


    




"""
Started 2012-02-04
This monitors the adding and removal of bishops "in real time"
Data is from http://www.usccb.org/about/bishops-and-dioceses/all-dioceses.cfm
"""


import scraperwiki
from scraperwiki import scrape
import lxml.html


html = scrape('http://www.usccb.org/about/bishops-and-dioceses/all-dioceses.cfm')
root = lxml.html.fromstring(html)
print 'length of html', len(html)
tables = [atable for atable in root.cssselect('table')]
print 'number of tables', len(tables)

#for thetag in table0:
#    print thetag.tag
#for thetr in table0:
    # .cssselect("td.personnel")
#    for thetd in thetr:
#       print thetd.text

#for el in table0:           
 #   print el.tag
  #  for el2 in el:
  #      print "--", el2.tag, el2.attrib, el.text

#print lxml.html.tostring(table0)
all_bishops = []
#table0 = tables[0]
for atable in tables:
    for thetr in atable:
        thebishops = dict()
        theweb = thetr.cssselect('a.subtle')
        if len(theweb) == 1:
            thebishops['url'] = theweb # this has to be changed for the proper data 
        thetd0 = thetr.cssselect('td.personnel')
        #td class="personnel">
        #<strong>Archbishop Thomas J. Rodi </strong><br/>Archbishop of Mobile<br/><br/>
        #<strong>Archbishop Oscar H. Lipscomb </strong><br/>Archbishop Emeritus of Mobile<br/><br/>
        if len(thetd0) == 1:
            #thebishops = dict()
            for subel in thetd0[0]:
                if subel.tag == 'strong':
                    thebishops['bishop'] = subel.text
                else:
                    if len(thebishops) != 0:
                        thetext = lxml.html.tostring(subel)
                        if thetext.startswith('<br>') and len(thetext) > 4:
                             thebishops['position'] = thetext[4:]
                             all_bishops.append(thebishops)
                    

print 'number of bishops', len(all_bishops)
print all_bishops[0:4]

# STORE

# WEBPAGE UPDATE

# TWEET
import tweepy


         
           

        

       

   


    




