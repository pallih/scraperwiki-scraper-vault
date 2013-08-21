# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

def parseForAnchor(s):
    if s == None:
        return
    m = re.match(".*href=(\".*?\")", s)    
    if m:
        return m.group(1)

def ScrapeYWList(url):
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    root1 = lxml.etree.fromstring(root.text)
    
    for t in root1:
        print t, t[3].text, list(t)
        lat = t[3].text
        lon = t[4].text
        t6 = t[6].text
        m = re.match(".*(\d+/\d+/\d\d\d\d).*(\d+/\d+/\d\d\d\d)", t6)
        if m:
            startdate = m.group(1)
            finishdate = m.group(2)
        else:
            startdate = "n/a"
            finishdate = "n/a"
    
        # last paragraph might say something on what they are doing
        m = re.match(".*\<p\>(.*)\<\/p\>", t6)
        description = m and m.group(1) or "n/a"
        unique = hash("%s%s%s%s" % (lat, lon, startdate, finishdate))
        data = {'unique':unique, 'startdate': startdate, 'finishdate': finishdate, 'description': description}
    
        ltt = list(t)
        anchors = [ ]
        for tt in ltt:
            a = parseForAnchor(tt.text)
            if a and a not in anchors:
                anchors.append(a)
        data['links'] = anchors
        scraperwiki.datastore.save(unique_keys=['unique'], data=data, latlng=[float(lat), float(lon)])

    

# change these values to the target url
# and the example text you want to find the path to
#url = "http://www.yorkshirewater.com/InYourArea.asmx/Roadworks_List?Longitude=-1&Latitude=53"
#ScrapeYWList(url)
url = "http://www.yorkshirewater.com/InYourArea.asmx/Incidents_List?Longitude=-0.4&Latitude=54.2"
ScrapeYWList(url)

print 8888
#print lxml.etree.tostring(tree)

def Main():
    root = lxml.html.parse(url).getroot()
    FindContentsRecurse(root)


    # Now make your selection, and disassemble your data

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
#    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
#        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
#        lurl, ltext, title = node[1][0].get('href'), node[1][0].text, node[2][0].text
#        rurl = urlparse.urljoin(url, lurl)
    

    
    
# Delete functions below when you are done hacking them

def GetPath(node):
    path = [ ]
    while node is not None:
        sux = [ "."+x  for x in node.get("class", "").split() ]
        sux.extend([ '#'+x  for x in node.get("id", "").split() ])
        if len(sux) == 0:
            path.append(node.tag)
        elif len(sux) == 1:
            path.append(node.tag + sux[0])
        else:
            path.append("%s[%s]" % (node.tag, ", ".join(sux)))
        node = node.getparent()
    path.reverse()
    return " ".join(path)
    
def PPath(typ, node, ts):
    return "%s\n  %s\n\n\n\n  %s" % (typ, GetPath(node), ts)
    
def FindContentsRecurse(node):
    ts =lxml.etree.tostring(node)

    if node.text and regexp.search(node.text):
        print PPath("Text",node, ts)
    if node.tail and regexp.search(node.tail):
        print PPath("Tail",node, ts)

    for k, v in node.attrib.items():
        if regexp.search(k):
            print PPath("key",node, ts)
        if regexp.search(v):
            print PPath("Value",node, ts)

    if regexp.search(ts):
        print PPath("Branch",node, ts)
    
    for subnode in node:
        FindContentsRecurse(subnode)
        
        
                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

def parseForAnchor(s):
    if s == None:
        return
    m = re.match(".*href=(\".*?\")", s)    
    if m:
        return m.group(1)

def ScrapeYWList(url):
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    root1 = lxml.etree.fromstring(root.text)
    
    for t in root1:
        print t, t[3].text, list(t)
        lat = t[3].text
        lon = t[4].text
        t6 = t[6].text
        m = re.match(".*(\d+/\d+/\d\d\d\d).*(\d+/\d+/\d\d\d\d)", t6)
        if m:
            startdate = m.group(1)
            finishdate = m.group(2)
        else:
            startdate = "n/a"
            finishdate = "n/a"
    
        # last paragraph might say something on what they are doing
        m = re.match(".*\<p\>(.*)\<\/p\>", t6)
        description = m and m.group(1) or "n/a"
        unique = hash("%s%s%s%s" % (lat, lon, startdate, finishdate))
        data = {'unique':unique, 'startdate': startdate, 'finishdate': finishdate, 'description': description}
    
        ltt = list(t)
        anchors = [ ]
        for tt in ltt:
            a = parseForAnchor(tt.text)
            if a and a not in anchors:
                anchors.append(a)
        data['links'] = anchors
        scraperwiki.datastore.save(unique_keys=['unique'], data=data, latlng=[float(lat), float(lon)])

    

# change these values to the target url
# and the example text you want to find the path to
#url = "http://www.yorkshirewater.com/InYourArea.asmx/Roadworks_List?Longitude=-1&Latitude=53"
#ScrapeYWList(url)
url = "http://www.yorkshirewater.com/InYourArea.asmx/Incidents_List?Longitude=-0.4&Latitude=54.2"
ScrapeYWList(url)

print 8888
#print lxml.etree.tostring(tree)

def Main():
    root = lxml.html.parse(url).getroot()
    FindContentsRecurse(root)


    # Now make your selection, and disassemble your data

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
#    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
#        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
#        lurl, ltext, title = node[1][0].get('href'), node[1][0].text, node[2][0].text
#        rurl = urlparse.urljoin(url, lurl)
    

    
    
# Delete functions below when you are done hacking them

def GetPath(node):
    path = [ ]
    while node is not None:
        sux = [ "."+x  for x in node.get("class", "").split() ]
        sux.extend([ '#'+x  for x in node.get("id", "").split() ])
        if len(sux) == 0:
            path.append(node.tag)
        elif len(sux) == 1:
            path.append(node.tag + sux[0])
        else:
            path.append("%s[%s]" % (node.tag, ", ".join(sux)))
        node = node.getparent()
    path.reverse()
    return " ".join(path)
    
def PPath(typ, node, ts):
    return "%s\n  %s\n\n\n\n  %s" % (typ, GetPath(node), ts)
    
def FindContentsRecurse(node):
    ts =lxml.etree.tostring(node)

    if node.text and regexp.search(node.text):
        print PPath("Text",node, ts)
    if node.tail and regexp.search(node.tail):
        print PPath("Tail",node, ts)

    for k, v in node.attrib.items():
        if regexp.search(k):
            print PPath("key",node, ts)
        if regexp.search(v):
            print PPath("Value",node, ts)

    if regexp.search(ts):
        print PPath("Branch",node, ts)
    
    for subnode in node:
        FindContentsRecurse(subnode)
        
        
                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

def parseForAnchor(s):
    if s == None:
        return
    m = re.match(".*href=(\".*?\")", s)    
    if m:
        return m.group(1)

def ScrapeYWList(url):
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    root1 = lxml.etree.fromstring(root.text)
    
    for t in root1:
        print t, t[3].text, list(t)
        lat = t[3].text
        lon = t[4].text
        t6 = t[6].text
        m = re.match(".*(\d+/\d+/\d\d\d\d).*(\d+/\d+/\d\d\d\d)", t6)
        if m:
            startdate = m.group(1)
            finishdate = m.group(2)
        else:
            startdate = "n/a"
            finishdate = "n/a"
    
        # last paragraph might say something on what they are doing
        m = re.match(".*\<p\>(.*)\<\/p\>", t6)
        description = m and m.group(1) or "n/a"
        unique = hash("%s%s%s%s" % (lat, lon, startdate, finishdate))
        data = {'unique':unique, 'startdate': startdate, 'finishdate': finishdate, 'description': description}
    
        ltt = list(t)
        anchors = [ ]
        for tt in ltt:
            a = parseForAnchor(tt.text)
            if a and a not in anchors:
                anchors.append(a)
        data['links'] = anchors
        scraperwiki.datastore.save(unique_keys=['unique'], data=data, latlng=[float(lat), float(lon)])

    

# change these values to the target url
# and the example text you want to find the path to
#url = "http://www.yorkshirewater.com/InYourArea.asmx/Roadworks_List?Longitude=-1&Latitude=53"
#ScrapeYWList(url)
url = "http://www.yorkshirewater.com/InYourArea.asmx/Incidents_List?Longitude=-0.4&Latitude=54.2"
ScrapeYWList(url)

print 8888
#print lxml.etree.tostring(tree)

def Main():
    root = lxml.html.parse(url).getroot()
    FindContentsRecurse(root)


    # Now make your selection, and disassemble your data

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
#    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
#        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
#        lurl, ltext, title = node[1][0].get('href'), node[1][0].text, node[2][0].text
#        rurl = urlparse.urljoin(url, lurl)
    

    
    
# Delete functions below when you are done hacking them

def GetPath(node):
    path = [ ]
    while node is not None:
        sux = [ "."+x  for x in node.get("class", "").split() ]
        sux.extend([ '#'+x  for x in node.get("id", "").split() ])
        if len(sux) == 0:
            path.append(node.tag)
        elif len(sux) == 1:
            path.append(node.tag + sux[0])
        else:
            path.append("%s[%s]" % (node.tag, ", ".join(sux)))
        node = node.getparent()
    path.reverse()
    return " ".join(path)
    
def PPath(typ, node, ts):
    return "%s\n  %s\n\n\n\n  %s" % (typ, GetPath(node), ts)
    
def FindContentsRecurse(node):
    ts =lxml.etree.tostring(node)

    if node.text and regexp.search(node.text):
        print PPath("Text",node, ts)
    if node.tail and regexp.search(node.tail):
        print PPath("Tail",node, ts)

    for k, v in node.attrib.items():
        if regexp.search(k):
            print PPath("key",node, ts)
        if regexp.search(v):
            print PPath("Value",node, ts)

    if regexp.search(ts):
        print PPath("Branch",node, ts)
    
    for subnode in node:
        FindContentsRecurse(subnode)
        
        
                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

def parseForAnchor(s):
    if s == None:
        return
    m = re.match(".*href=(\".*?\")", s)    
    if m:
        return m.group(1)

def ScrapeYWList(url):
    root = lxml.etree.parse(urllib.urlopen(url)).getroot()
    root1 = lxml.etree.fromstring(root.text)
    
    for t in root1:
        print t, t[3].text, list(t)
        lat = t[3].text
        lon = t[4].text
        t6 = t[6].text
        m = re.match(".*(\d+/\d+/\d\d\d\d).*(\d+/\d+/\d\d\d\d)", t6)
        if m:
            startdate = m.group(1)
            finishdate = m.group(2)
        else:
            startdate = "n/a"
            finishdate = "n/a"
    
        # last paragraph might say something on what they are doing
        m = re.match(".*\<p\>(.*)\<\/p\>", t6)
        description = m and m.group(1) or "n/a"
        unique = hash("%s%s%s%s" % (lat, lon, startdate, finishdate))
        data = {'unique':unique, 'startdate': startdate, 'finishdate': finishdate, 'description': description}
    
        ltt = list(t)
        anchors = [ ]
        for tt in ltt:
            a = parseForAnchor(tt.text)
            if a and a not in anchors:
                anchors.append(a)
        data['links'] = anchors
        scraperwiki.datastore.save(unique_keys=['unique'], data=data, latlng=[float(lat), float(lon)])

    

# change these values to the target url
# and the example text you want to find the path to
#url = "http://www.yorkshirewater.com/InYourArea.asmx/Roadworks_List?Longitude=-1&Latitude=53"
#ScrapeYWList(url)
url = "http://www.yorkshirewater.com/InYourArea.asmx/Incidents_List?Longitude=-0.4&Latitude=54.2"
ScrapeYWList(url)

print 8888
#print lxml.etree.tostring(tree)

def Main():
    root = lxml.html.parse(url).getroot()
    FindContentsRecurse(root)


    # Now make your selection, and disassemble your data

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
#    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
#        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
#        lurl, ltext, title = node[1][0].get('href'), node[1][0].text, node[2][0].text
#        rurl = urlparse.urljoin(url, lurl)
    

    
    
# Delete functions below when you are done hacking them

def GetPath(node):
    path = [ ]
    while node is not None:
        sux = [ "."+x  for x in node.get("class", "").split() ]
        sux.extend([ '#'+x  for x in node.get("id", "").split() ])
        if len(sux) == 0:
            path.append(node.tag)
        elif len(sux) == 1:
            path.append(node.tag + sux[0])
        else:
            path.append("%s[%s]" % (node.tag, ", ".join(sux)))
        node = node.getparent()
    path.reverse()
    return " ".join(path)
    
def PPath(typ, node, ts):
    return "%s\n  %s\n\n\n\n  %s" % (typ, GetPath(node), ts)
    
def FindContentsRecurse(node):
    ts =lxml.etree.tostring(node)

    if node.text and regexp.search(node.text):
        print PPath("Text",node, ts)
    if node.tail and regexp.search(node.tail):
        print PPath("Tail",node, ts)

    for k, v in node.attrib.items():
        if regexp.search(k):
            print PPath("key",node, ts)
        if regexp.search(v):
            print PPath("Value",node, ts)

    if regexp.search(ts):
        print PPath("Branch",node, ts)
    
    for subnode in node:
        FindContentsRecurse(subnode)
        
        
                        

