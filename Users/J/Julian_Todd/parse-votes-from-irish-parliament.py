import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

# we could potentially move the whole Kildare Street parser into here, 
# using a separate scraper for managing and converting names of members into unique-ids

url = "http://historical-debates.oireachtas.ie/D/0676/D.0676.200902240025.html"
# Equivalent page: http://www.kildarestreet.com/debates/?id=2009-02-24.536.0

# Note from John H at KildareStreet:  try this, it's what I use - 
# http://debates.oireachtas.ie/XML/D/2009/DAL20090224.XML 
# (unpublicised-cos-riddled-with-UKisms) KS API has 'oirpid' attribute on members which
# match 'pid' values in source XML


# this function will need to convert these voting members into their unique-ids
def cleanvotename(td):
    text = td[0].text
    if not text:
        return None
    text = text.strip()
    assert text[-1] == '.'
    return text[:-1]
    

def parsedivision(table):
    ayes = [ ]
    noes = [ ]
    for tr in table.cssselect('tr'):
        assert len(tr) == 2, lxml.etree.tostring(tr)
        if tr[0].get('colspan') == '2':
            assert tr[0][0].tag == 'p', lxml.etree.tostring(tr)
            if tr[0][0].text == u'T\xe1':
                clist = ayes
            elif tr[0][0].text == u'N\xedl':
                clist = noes
            else:
                clist = None
                print "TTTT", lxml.etree.tostring(tr)
        else:
            c1, c2 = cleanvotename(tr[0]), cleanvotename(tr[1])
            assert c1, lxml.etree.tostring(tr)
            clist.append(c1)
            if c2:
                clist.append(c2)

    print ""
    print "Ayes", len(ayes), ayes
    print "Noes", len(noes), noes


def Main():
    root = lxml.html.parse(url).getroot()
    navigatorbar = root.cssselect('table.navigator_bar')[0]
    item = navigatorbar.getnext()
    while item is not None:
        if item.tag == 'p':
            # this has the speeches (to parse later)
            pass
            #if len(item):
            #    print [ (s.get('class'), s.text_content())  for s in item ]

        elif item.tag == 'table':
            if item.get('class') == 'navigator_bar':
                pass  # the final row
            else:
                parsedivision(item)

        #else:
        #    print "pp", item.tag
        item = item.getnext()
    return

    for p in root.cssselect('p'):
        span = p.cssselect('span')
        if span:
            print [ (s.get('class'), s.text)  for s in span ]
        table = p.cssselect('table')
        if table:
            print lxml.etree.tostring(table)
    

        
Main()

                        

