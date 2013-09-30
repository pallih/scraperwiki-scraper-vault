import scraperwiki                  
import lxml.html
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import re                           # Gotta have my regex
import time                         # time is on my side. (date operations)
from decimal import *
import sys
import urllib
import datetime
import nltk
from nltk import WordPunctTokenizer
from BeautifulSoup import BeautifulSoup

def GetContractPage(x):
    url = 'http://www.defense.gov/contracts/contract.aspx?contractid=%d' % x
    html = urllib.urlopen(url).read()
    if re.search("The Official Home of the Department of Defense", html):
        return
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    tableA = tables[-3]
    valA = tableA.cssselect("td")
    stableA = lxml.html.tostring(tableA)
    assert len(valA) == 2 and valA[0][0].tag == "strong" and valA[1][0].tag == "strong", stableA
    s1, s2 = valA[0][0], valA[1][0]
    assert s1.text == "FOR RELEASE AT" and s1[0].tag == "br", lxml.html.tostring(s1)
    t1 = s1[0].tail
    assert s2[0].tag == "br", stableA
    n1 = s2.text
    d1 = s2[0].tail
    dt1 = "%s %s" % (d1, t1.replace(".", ""))
    d1a = datetime.datetime.strptime(dt1, "%B %d, %Y %I %p ET")
    print (t1, n1, d1, d1a)
    tableB = tables[-2]
    assert n1[:4] == 'No. '
    data = { "date":d1a, "Nom":n1[4:], "url":url, "x":x }
    data["tableB"] = lxml.html.tostring(tableB)
    scraperwiki.sqlite.save(["url"], data)
    tableC = tables[-1]
    valC = tableC.lxml.tag("p")
    stableB = lxml.html.tostring(tableB)
    #[(word, tag) = WordPunctTokenizer().tokenize(stableB)]
    print stableB
    print valC    

    # The following lines manipulate the HTML in several ways to account for different formatting methods
    html = re.sub("<div><span>","<p>",html)
    html = re.sub('<div align="center"><strong>','<p><strong>',html)
    html = re.sub('div style="MARGIN: 0in 0in 0pt"','p',html)
    html = re.sub(r'<(/?)b>',r'<\1strong>',html)
    html = re.sub(r'(?i)<H(3|4)>(.*)</H\1>',r'<p><strong>\2</strong></p>',html)
    html = re.sub(r'[\n\r]',' ', html)
    html = re.sub('<div STYLE="font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000;">','<P>',html)
    print html
    #scrape_and_move_on(html,starting_url)                                      # this runs the scrape function above


def Main():
    furl = 'http://www.defense.gov/contracts'
    html = urllib.urlopen(furl).read()
    lastcontracts = re.search('contractid=(\d{4,})', html)
    lastcontracts = int(lastcontracts.group(1))

    firstcontracts = scraperwiki.sqlite.get_var('last_page', 391)
    if firstcontracts >= lastcontracts:
        print "no new contracts"
        return

    for x in range(firstcontracts+1,lastcontracts+1):
        GetContractPage(x)
        scraperwiki.sqlite.save_var('last_page', x)

Main()import scraperwiki                  
import lxml.html
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import re                           # Gotta have my regex
import time                         # time is on my side. (date operations)
from decimal import *
import sys
import urllib
import datetime
import nltk
from nltk import WordPunctTokenizer
from BeautifulSoup import BeautifulSoup

def GetContractPage(x):
    url = 'http://www.defense.gov/contracts/contract.aspx?contractid=%d' % x
    html = urllib.urlopen(url).read()
    if re.search("The Official Home of the Department of Defense", html):
        return
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    tableA = tables[-3]
    valA = tableA.cssselect("td")
    stableA = lxml.html.tostring(tableA)
    assert len(valA) == 2 and valA[0][0].tag == "strong" and valA[1][0].tag == "strong", stableA
    s1, s2 = valA[0][0], valA[1][0]
    assert s1.text == "FOR RELEASE AT" and s1[0].tag == "br", lxml.html.tostring(s1)
    t1 = s1[0].tail
    assert s2[0].tag == "br", stableA
    n1 = s2.text
    d1 = s2[0].tail
    dt1 = "%s %s" % (d1, t1.replace(".", ""))
    d1a = datetime.datetime.strptime(dt1, "%B %d, %Y %I %p ET")
    print (t1, n1, d1, d1a)
    tableB = tables[-2]
    assert n1[:4] == 'No. '
    data = { "date":d1a, "Nom":n1[4:], "url":url, "x":x }
    data["tableB"] = lxml.html.tostring(tableB)
    scraperwiki.sqlite.save(["url"], data)
    tableC = tables[-1]
    valC = tableC.lxml.tag("p")
    stableB = lxml.html.tostring(tableB)
    #[(word, tag) = WordPunctTokenizer().tokenize(stableB)]
    print stableB
    print valC    

    # The following lines manipulate the HTML in several ways to account for different formatting methods
    html = re.sub("<div><span>","<p>",html)
    html = re.sub('<div align="center"><strong>','<p><strong>',html)
    html = re.sub('div style="MARGIN: 0in 0in 0pt"','p',html)
    html = re.sub(r'<(/?)b>',r'<\1strong>',html)
    html = re.sub(r'(?i)<H(3|4)>(.*)</H\1>',r'<p><strong>\2</strong></p>',html)
    html = re.sub(r'[\n\r]',' ', html)
    html = re.sub('<div STYLE="font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000;">','<P>',html)
    print html
    #scrape_and_move_on(html,starting_url)                                      # this runs the scrape function above


def Main():
    furl = 'http://www.defense.gov/contracts'
    html = urllib.urlopen(furl).read()
    lastcontracts = re.search('contractid=(\d{4,})', html)
    lastcontracts = int(lastcontracts.group(1))

    firstcontracts = scraperwiki.sqlite.get_var('last_page', 391)
    if firstcontracts >= lastcontracts:
        print "no new contracts"
        return

    for x in range(firstcontracts+1,lastcontracts+1):
        GetContractPage(x)
        scraperwiki.sqlite.save_var('last_page', x)

Main()