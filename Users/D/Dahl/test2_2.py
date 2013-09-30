#ERDETFREDAGSCRAPER

import scraperwiki
import urllib2
import lxml.html

print "Is it friday?"

url = 'http://erdetfredag.dk'
response = urllib2.urlopen(url)
html = response.read()

print "Lets find out!"
print html


root = lxml.html.fromstring(html) # turn our HTML into an lxml object
ERDET = root.cssselect('body') # get all the <h1> tags
for body in ERDET:
      #print lxml.html.tostring(body) # the full HTML tag
      print body.text                # just the text inside the HTML tag



#GEM TIL BASE KODEN

#for h1 in ERDET:
#     record = { "h1" : h1.text } # column name and value
#     scraperwiki.datastore.save(["h1"], record) # save the records one by one
#ERDETFREDAGSCRAPER

import scraperwiki
import urllib2
import lxml.html

print "Is it friday?"

url = 'http://erdetfredag.dk'
response = urllib2.urlopen(url)
html = response.read()

print "Lets find out!"
print html


root = lxml.html.fromstring(html) # turn our HTML into an lxml object
ERDET = root.cssselect('body') # get all the <h1> tags
for body in ERDET:
      #print lxml.html.tostring(body) # the full HTML tag
      print body.text                # just the text inside the HTML tag



#GEM TIL BASE KODEN

#for h1 in ERDET:
#     record = { "h1" : h1.text } # column name and value
#     scraperwiki.datastore.save(["h1"], record) # save the records one by one
