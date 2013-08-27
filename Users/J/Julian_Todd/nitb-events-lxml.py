# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


# change these values to the target url 
# and the example text you want to find the path to
url = "http://www.discovernorthernireland.com/events/"
searchpathfor = "Mea"



def Main():
    root = lxml.html.parse(url).getroot()
    root1 = root
    r = 0
    while root1 is not None:
        print "*** root ***", r
        FindContentsRecurse(root1)
        root1 = root1.getnext()
        r += 1

    # place your cssselection case here and extract the values
    #for tr in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
    #    print list(tr), lxml.etree.tostring(tr)
    

    
    
# Delete the functions below when you are done with them

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
    regexp = re.compile(searchpathfor)
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
        
        
Main()

                        

