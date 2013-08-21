import scraperwiki
import lxml.etree
import urllib
import re

# this only handles the modern one.  Would like to get everything, 
# but requires pagenating and iterating through categories

def ScrapeWP(title):
    d = {"action":"query", "prop":"revisions", "titles":"API|%s" % title.encode("utf8"), 
         "rvprop":"timestamp|user|comment|content", "format":"xml"}
    wurl = "http://en.wikipedia.org/w/api.php?"+urllib.urlencode(d)
    xml = urllib.urlopen(wurl).read()
    root = lxml.etree.fromstring(xml)
    return root.findall("query/pages/page/revisions/rev")[1].text

itext = ScrapeWP("List_of_United_Kingdom_Parliament_constituencies")
for wptitle, name in re.findall("\[\[([^\]]*? \(UK Parliament constituency\))\|([^\]]*)\]\]", itext):
    data = { "wptitle":wptitle, "name":name }
    data["content"] = ScrapeWP(wptitle)
    scraperwiki.sqlite.save(unique_keys=["wptitle"], data=data)

import scraperwiki
import lxml.etree
import urllib
import re

# this only handles the modern one.  Would like to get everything, 
# but requires pagenating and iterating through categories

def ScrapeWP(title):
    d = {"action":"query", "prop":"revisions", "titles":"API|%s" % title.encode("utf8"), 
         "rvprop":"timestamp|user|comment|content", "format":"xml"}
    wurl = "http://en.wikipedia.org/w/api.php?"+urllib.urlencode(d)
    xml = urllib.urlopen(wurl).read()
    root = lxml.etree.fromstring(xml)
    return root.findall("query/pages/page/revisions/rev")[1].text

itext = ScrapeWP("List_of_United_Kingdom_Parliament_constituencies")
for wptitle, name in re.findall("\[\[([^\]]*? \(UK Parliament constituency\))\|([^\]]*)\]\]", itext):
    data = { "wptitle":wptitle, "name":name }
    data["content"] = ScrapeWP(wptitle)
    scraperwiki.sqlite.save(unique_keys=["wptitle"], data=data)

import scraperwiki
import lxml.etree
import urllib
import re

# this only handles the modern one.  Would like to get everything, 
# but requires pagenating and iterating through categories

def ScrapeWP(title):
    d = {"action":"query", "prop":"revisions", "titles":"API|%s" % title.encode("utf8"), 
         "rvprop":"timestamp|user|comment|content", "format":"xml"}
    wurl = "http://en.wikipedia.org/w/api.php?"+urllib.urlencode(d)
    xml = urllib.urlopen(wurl).read()
    root = lxml.etree.fromstring(xml)
    return root.findall("query/pages/page/revisions/rev")[1].text

itext = ScrapeWP("List_of_United_Kingdom_Parliament_constituencies")
for wptitle, name in re.findall("\[\[([^\]]*? \(UK Parliament constituency\))\|([^\]]*)\]\]", itext):
    data = { "wptitle":wptitle, "name":name }
    data["content"] = ScrapeWP(wptitle)
    scraperwiki.sqlite.save(unique_keys=["wptitle"], data=data)

import scraperwiki
import lxml.etree
import urllib
import re

# this only handles the modern one.  Would like to get everything, 
# but requires pagenating and iterating through categories

def ScrapeWP(title):
    d = {"action":"query", "prop":"revisions", "titles":"API|%s" % title.encode("utf8"), 
         "rvprop":"timestamp|user|comment|content", "format":"xml"}
    wurl = "http://en.wikipedia.org/w/api.php?"+urllib.urlencode(d)
    xml = urllib.urlopen(wurl).read()
    root = lxml.etree.fromstring(xml)
    return root.findall("query/pages/page/revisions/rev")[1].text

itext = ScrapeWP("List_of_United_Kingdom_Parliament_constituencies")
for wptitle, name in re.findall("\[\[([^\]]*? \(UK Parliament constituency\))\|([^\]]*)\]\]", itext):
    data = { "wptitle":wptitle, "name":name }
    data["content"] = ScrapeWP(wptitle)
    scraperwiki.sqlite.save(unique_keys=["wptitle"], data=data)

import scraperwiki
import lxml.etree
import urllib
import re

# this only handles the modern one.  Would like to get everything, 
# but requires pagenating and iterating through categories

def ScrapeWP(title):
    d = {"action":"query", "prop":"revisions", "titles":"API|%s" % title.encode("utf8"), 
         "rvprop":"timestamp|user|comment|content", "format":"xml"}
    wurl = "http://en.wikipedia.org/w/api.php?"+urllib.urlencode(d)
    xml = urllib.urlopen(wurl).read()
    root = lxml.etree.fromstring(xml)
    return root.findall("query/pages/page/revisions/rev")[1].text

itext = ScrapeWP("List_of_United_Kingdom_Parliament_constituencies")
for wptitle, name in re.findall("\[\[([^\]]*? \(UK Parliament constituency\))\|([^\]]*)\]\]", itext):
    data = { "wptitle":wptitle, "name":name }
    data["content"] = ScrapeWP(wptitle)
    scraperwiki.sqlite.save(unique_keys=["wptitle"], data=data)

