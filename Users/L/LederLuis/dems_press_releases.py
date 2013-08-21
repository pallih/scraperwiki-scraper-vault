import scraperwiki
import lxml.html

# Scrape the Democratic National Committee press releases


#Helper function in case of error
import urllib2
import time

def load(url):
    retries = 3
    for i in range(retries):
        try:
            handle = urllib2.urlopen(url)
            return handle.read()
        except urllib2.HTTPError :
            if i + 1 == retries:
                raise
            else:
                time.sleep(5)
    # never get here


#Find number of pages to scrape
# Their system goes by 8s
n = 336 #Found manually by looking to find end of http://www.democrats.org/bgviews/main-press-full/ chain
pages =['']
for i in range(1, n+1):
    if i%8 == 0:
        pages.append('P' + str(i))

# Make list of links
for i in pages:
    # Concatenate integer with base to make pagename
    pagename = 'http://www.democrats.org/bgviews/main-press-full/' + i
    #Scrape the page
    page = load(pagename)
    #Root the page
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('''div.entry-content a'''):    
        docpagename = link.attrib['href']
        docpage = load('http://democrats.org' + docpagename)
        docpageroot = lxml.html.fromstring(docpage)
        for d in docpageroot.cssselect('''div."entry-content cramped"'''):
            doc = d.text_content()
            #GOP uses # at end of docs
            #Grab document name
            docname = docpagename.split('/')[-1]
        for t in docpageroot.cssselect('div * time'):
            date = t.attrib['datetime']
        data = {'Date': date, 'Document': docname + ' ' + doc}
        scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)


import scraperwiki
import lxml.html

# Scrape the Democratic National Committee press releases


#Helper function in case of error
import urllib2
import time

def load(url):
    retries = 3
    for i in range(retries):
        try:
            handle = urllib2.urlopen(url)
            return handle.read()
        except urllib2.HTTPError :
            if i + 1 == retries:
                raise
            else:
                time.sleep(5)
    # never get here


#Find number of pages to scrape
# Their system goes by 8s
n = 336 #Found manually by looking to find end of http://www.democrats.org/bgviews/main-press-full/ chain
pages =['']
for i in range(1, n+1):
    if i%8 == 0:
        pages.append('P' + str(i))

# Make list of links
for i in pages:
    # Concatenate integer with base to make pagename
    pagename = 'http://www.democrats.org/bgviews/main-press-full/' + i
    #Scrape the page
    page = load(pagename)
    #Root the page
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('''div.entry-content a'''):    
        docpagename = link.attrib['href']
        docpage = load('http://democrats.org' + docpagename)
        docpageroot = lxml.html.fromstring(docpage)
        for d in docpageroot.cssselect('''div."entry-content cramped"'''):
            doc = d.text_content()
            #GOP uses # at end of docs
            #Grab document name
            docname = docpagename.split('/')[-1]
        for t in docpageroot.cssselect('div * time'):
            date = t.attrib['datetime']
        data = {'Date': date, 'Document': docname + ' ' + doc}
        scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)


