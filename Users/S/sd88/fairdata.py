# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)

import scraperwiki

samplehtml = scraperwiki.scrape('http://www.messeninfo.de/Algier-X15-S1-Messen-Algier.html')
#samplehtml = scraperwiki.scrape('http://www.messeninfo.de/Alesund-X2197-S1-Messen-Alesund.html')

root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
summary = root.cssselect('span[class="summary"]')   # returns summary
description = root.cssselect('span[class="description"]')
dtstart = root.cssselect('span[class="dtstart"]')

dtend = root.cssselect('span[class="dtend"]')
locality = root.cssselect('span[class="locality"]')
countryname = root.cssselect('span[class="country-name"]')

#//span[@class='summary']|
#//span[@class='description']|
#//span[@class='dtstart']|
#//span[@class='dtend']|
#//span[@class='locality']|
#//span[@class='country-name'

print summary

print "summary:",len(summary)
print "description:",len(description)
print "dtstart:" ,len(dtstart )
print "dtend:" ,len(dtend)
print "locality:" ,len(locality)
print "countryname:" ,len(countryname)

#for s, ds, de in zip(summary, dtstart, dtend):
#    print (l.text,c.text,s.text,d.text,ds.text,de.text)
#    print (s.text,ds.text,de.text)


for s, d, ds, de, l, c in zip(summary, description, dtstart, dtend, locality, countryname):
#    print (l.text,c.text,s.text,d.text,ds.text,de.text)
#    print (s.text,ds.text,de.text)
#    record = { "loc" : l.text } # column name and value
#    scraperwiki.sqlite.save(["loc"], record) # save the records one by one
#    record = { "country" : c.text } # column name and value
#    scraperwiki.sqlite.save(["country"], record) # save the records one by one
#    record = { "sum" : s.text } # column name and value
#    scraperwiki.sqlite.save(["sum"], record) # save the records one by one
#    record = { "desc" : d.text } # column name and value
#    scraperwiki.sqlite.save(["desc"], record) # save the records one by one
#    record = { "dstart" : ds.text } # column name and value
#    scraperwiki.sqlite.save(["dstart"], record) # save the records one by one
#    record = { "dend" : de.text } # column name and value
#    scraperwiki.sqlite.save(["dend"], record) # save the records one by one
    scraperwiki.sqlite.save(unique_keys=["sum"], data={"loc": l.text, "country": c.text, "sum": s.text, "desc": d.text, "dstart": ds.text, "dend": de.text})
#    scraperwiki.sqlite.save(unique_keys=["sum"], data={"loc": l.text, "country": c.text, "sum": s.text, "desc": d.text})

#for s, d, l, c in zip(summary, description, locality, countryname):
#    print (l.text,c.text,s.text,d.text)
#    scraperwiki.sqlite.save(unique_keys=["sum"], data={"loc": l.text, "country": c.text, "sum": s.text, "desc": d.text})


#    print 'Ort:\t', l.text
#    print 'Land:\t', c.text
#    print 'Name:\t', s.text
#    print 'Beschr:\t', d.text
#    print 'Start:\t', ds.text
#    print 'Ende:\t', de.text

#print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
#linimble = root.cssselect("ul #nimble")[0]
#help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
#print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)

import scraperwiki

samplehtml = scraperwiki.scrape('http://www.messeninfo.de/Algier-X15-S1-Messen-Algier.html')
#samplehtml = scraperwiki.scrape('http://www.messeninfo.de/Alesund-X2197-S1-Messen-Alesund.html')

root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
summary = root.cssselect('span[class="summary"]')   # returns summary
description = root.cssselect('span[class="description"]')
dtstart = root.cssselect('span[class="dtstart"]')

dtend = root.cssselect('span[class="dtend"]')
locality = root.cssselect('span[class="locality"]')
countryname = root.cssselect('span[class="country-name"]')

#//span[@class='summary']|
#//span[@class='description']|
#//span[@class='dtstart']|
#//span[@class='dtend']|
#//span[@class='locality']|
#//span[@class='country-name'

print summary

print "summary:",len(summary)
print "description:",len(description)
print "dtstart:" ,len(dtstart )
print "dtend:" ,len(dtend)
print "locality:" ,len(locality)
print "countryname:" ,len(countryname)

#for s, ds, de in zip(summary, dtstart, dtend):
#    print (l.text,c.text,s.text,d.text,ds.text,de.text)
#    print (s.text,ds.text,de.text)


for s, d, ds, de, l, c in zip(summary, description, dtstart, dtend, locality, countryname):
#    print (l.text,c.text,s.text,d.text,ds.text,de.text)
#    print (s.text,ds.text,de.text)
#    record = { "loc" : l.text } # column name and value
#    scraperwiki.sqlite.save(["loc"], record) # save the records one by one
#    record = { "country" : c.text } # column name and value
#    scraperwiki.sqlite.save(["country"], record) # save the records one by one
#    record = { "sum" : s.text } # column name and value
#    scraperwiki.sqlite.save(["sum"], record) # save the records one by one
#    record = { "desc" : d.text } # column name and value
#    scraperwiki.sqlite.save(["desc"], record) # save the records one by one
#    record = { "dstart" : ds.text } # column name and value
#    scraperwiki.sqlite.save(["dstart"], record) # save the records one by one
#    record = { "dend" : de.text } # column name and value
#    scraperwiki.sqlite.save(["dend"], record) # save the records one by one
    scraperwiki.sqlite.save(unique_keys=["sum"], data={"loc": l.text, "country": c.text, "sum": s.text, "desc": d.text, "dstart": ds.text, "dend": de.text})
#    scraperwiki.sqlite.save(unique_keys=["sum"], data={"loc": l.text, "country": c.text, "sum": s.text, "desc": d.text})

#for s, d, l, c in zip(summary, description, locality, countryname):
#    print (l.text,c.text,s.text,d.text)
#    scraperwiki.sqlite.save(unique_keys=["sum"], data={"loc": l.text, "country": c.text, "sum": s.text, "desc": d.text})


#    print 'Ort:\t', l.text
#    print 'Land:\t', c.text
#    print 'Name:\t', s.text
#    print 'Beschr:\t', d.text
#    print 'Start:\t', ds.text
#    print 'Ende:\t', de.text

#print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
#linimble = root.cssselect("ul #nimble")[0]
#help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
#print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
