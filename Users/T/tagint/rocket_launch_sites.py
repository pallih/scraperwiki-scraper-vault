import scraperwiki


# Blank Python

#import lxml.etree
#import urllib

# http://blog.scraperwiki.com/2011/12/07/how-to-scrape-and-parse-wikipedia/

#title = "Aquamole Pot"

#params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
#params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
#qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#url = "http://en.wikipedia.org/w/api.php?%s" % qs
#tree = lxml.etree.parse(urllib.urlopen(url))
#revs = tree.xpath('//rev')

#print "The Wikipedia text for", title, "is"
#print revs[-1].text





#########
# Works but doesn't get to table
#import lxml.etree
#import urllib

#title = "List of rocket launch sites"


#params = { "format":"xml", "action":"query", "prop":"extracts"}
#params["titles"] = urllib.quote(title.encode("utf8"))
#qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#url = "http://en.wikipedia.org/w/api.php?%s" % qs

#print url


#tree = lxml.etree.parse(urllib.urlopen(url))
#revs = tree.xpath('//rev')


#import xml.etree.cElementTree as etree


#textXpath = tree.xpath('(.|.//*[not(name()="script")][not(name()="style")])/text()')

#print textXpath

#root = tree.getroot()

#print len(root)

#for child in root:
#    print(child.tag, child.attrib)


#print root[0][0][0][0].tag
#print root[0][0][0][0].attrib
#print root[0][0][0][0].text



#########
# Works but doesn't get to table
import lxml.etree
import urllib

title = "List of rocket launch sites"
title2 = "List of wineries in South Africa"

#params = { "format":"xml", "action":"query", "prop":"extracts"}
#params["titles"] = urllib.quote(title.encode("utf8"))
#qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#url = "http://en.wikipedia.org/w/api.php?%s" % qs


params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://en.wikipedia.org/w/api.php?%s" % qs
tree = lxml.etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')



print url


tree = lxml.etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')




import xml.etree.cElementTree as etree


textXpath = tree.xpath('(.|.//*[not(name()="script")][not(name()="style")])/text()')

textXpath2 = tree.xpath('(//tr[text()="Reggane"])/text()')

print textXpath
#print textXpath2

root = tree.getroot()

#print len(root)

#for child in root[0]:
    #print(child.tag, child.attrib)
    #for child2 in child:
        #print(child2.tag, child2.attrib)
        #for child3 in child2:
            #print(child3.tag, child3.attrib)


print root[0][0][1][0][0].text





#tables = tree.xpath("//table[@class='wikitable']")
#rows = tables.xpath('//tr')
#print rows.size


#print root[0][0][0].tag
#print root[0][0][0].attrib
#print root[0][0][0].text









import scraperwiki


# Blank Python

#import lxml.etree
#import urllib

# http://blog.scraperwiki.com/2011/12/07/how-to-scrape-and-parse-wikipedia/

#title = "Aquamole Pot"

#params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
#params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
#qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#url = "http://en.wikipedia.org/w/api.php?%s" % qs
#tree = lxml.etree.parse(urllib.urlopen(url))
#revs = tree.xpath('//rev')

#print "The Wikipedia text for", title, "is"
#print revs[-1].text





#########
# Works but doesn't get to table
#import lxml.etree
#import urllib

#title = "List of rocket launch sites"


#params = { "format":"xml", "action":"query", "prop":"extracts"}
#params["titles"] = urllib.quote(title.encode("utf8"))
#qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#url = "http://en.wikipedia.org/w/api.php?%s" % qs

#print url


#tree = lxml.etree.parse(urllib.urlopen(url))
#revs = tree.xpath('//rev')


#import xml.etree.cElementTree as etree


#textXpath = tree.xpath('(.|.//*[not(name()="script")][not(name()="style")])/text()')

#print textXpath

#root = tree.getroot()

#print len(root)

#for child in root:
#    print(child.tag, child.attrib)


#print root[0][0][0][0].tag
#print root[0][0][0][0].attrib
#print root[0][0][0][0].text



#########
# Works but doesn't get to table
import lxml.etree
import urllib

title = "List of rocket launch sites"
title2 = "List of wineries in South Africa"

#params = { "format":"xml", "action":"query", "prop":"extracts"}
#params["titles"] = urllib.quote(title.encode("utf8"))
#qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
#url = "http://en.wikipedia.org/w/api.php?%s" % qs


params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://en.wikipedia.org/w/api.php?%s" % qs
tree = lxml.etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')



print url


tree = lxml.etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')




import xml.etree.cElementTree as etree


textXpath = tree.xpath('(.|.//*[not(name()="script")][not(name()="style")])/text()')

textXpath2 = tree.xpath('(//tr[text()="Reggane"])/text()')

print textXpath
#print textXpath2

root = tree.getroot()

#print len(root)

#for child in root[0]:
    #print(child.tag, child.attrib)
    #for child2 in child:
        #print(child2.tag, child2.attrib)
        #for child3 in child2:
            #print(child3.tag, child3.attrib)


print root[0][0][1][0][0].text





#tables = tree.xpath("//table[@class='wikitable']")
#rows = tables.xpath('//tr')
#print rows.size


#print root[0][0][0].tag
#print root[0][0][0].attrib
#print root[0][0][0].text









