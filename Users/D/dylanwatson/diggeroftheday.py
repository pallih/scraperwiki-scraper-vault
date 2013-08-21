#!/usr/bin/python

import scraperwiki

siteUrl = "http://www.awm.gov.au"

import lxml.html
import re
import urllib2

class Person:

    # A static copy of style information from the scraped page
    styleInfo = """<meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link type="text/css" rel="stylesheet" href="http://www.awm.gov.au/sites/default/files/css/css__c5mKe0-yfYp9B-9V727-n4s0fuGroBMaK1VpFXNdxQ.css" media="all" />
        <link type="text/css" rel="stylesheet" href="http://www.awm.gov.au/sites/default/files/css/css_rbPOVGSp56MWwJZO2b6piNmMTbmGpasvf0zhr9Kd1Zk.css" media="print" />
        <script type="text/javascript" src="http://www.awm.gov.au/sites/default/files/js/js_sW0Dntw3YXT4_7wek4Lqiseqb67ctm_oGmJWNMjiDI4.js"></script>
        <script type="text/javascript" src="http://www.awm.gov.au/sites/default/files/js/js_3ORzZuIaDnY49q_JZ6vmjALkS9efn3H_xYVA-5vzN9k.js"></script>"""

    fullHtml = ""
    displayName = ""
    fullName = ""
    category = ""
    url = ""
    informationHtml = ""
    storyHtml = ""
    images = ""
    links = ""

    def __init__(self, fullHtml, displayName, fullName, category, url, informationHtml, storyHtml, images, links):
        self.fullHtml = styleInfo + fullHtml
        self.displayName = displayName
        self.fullName = fullName
        self.category = category
        self.url = url
        self.informationHtml = informationHtml
        self.storyHtml = storyHtml
        self.images = images
        self.links = links

    def save(self):
        data = {
            'fullHtml' : self.fullHtml,
            'displayName' : self.displayName,
            'fullName' : self.fullName,
            'category' : self.category,
            'url' : self.url,
            'informationHtml' : self.informationHtml,
            'storyHtml' : self.storyHtml,
            'images' : self.images,
            'links' : self.links
            
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['displayName', 'url'], data=data)

    def printOut(self):
            print 'Name: ' + self.displayName
            print 'Full Name: ' + self.fullName
            print 'Category: ' + self.category
            print 'Url: ' + self.url
            print 'Information: ' + self.informationHtml
            print 'Story: ' + self.storyHtml
            print 'Images: ' + self.images
            print 'Links: ' + self.links

def getHtml(url):
    html = urllib2.urlopen(url)
    page = lxml.html.fromstring(html.read())
    html.close()

    return page

def replaceUrls(html):
    # this should replace all relative URLs with absolute URLs
    return html

def processProfile(name, category, url):
    page = getHtml(url).cssselect("div[id='content']")[0]

    fullHtml = replaceUrls(lxml.html.tostring(page))

    displayName = name
    fullName = ""
    try:
        fullName = page.cssselect("h2")[0].text_content()
    except IndexError:
        fullName = page.cssselect("h1")[0].text_content()
        
    category = category
    informationHtml = lxml.html.tostring(page.cssselect("p")[0])

    paragraphs = page.cssselect("p")
    numParas = len(paragraphs)
    storyHtml = ""
    if (numParas < 2):
        raise Exception('Expected more than 1 paragraph but only ' + numParas + ' paragraphs found for person ' + name + ' at Url: ' + url)
    else:
        #Start at the 2nd paragraph, 1st is the information
        storyHtml = ''.join([lxml.html.tostring(ps).strip() for ps in paragraphs[1:]])

    images = ''.join([lxml.html.tostring(img).strip() for img in page.cssselect("img")])
    links = ''.join([lxml.html.tostring(link).strip() for link in page.cssselect("ul li")])

    person = Person(fullHtml, displayName, fullName, category, url, informationHtml, storyHtml, images, links)
    #person.printOut()
    person.save()

def processPage(pageUrl):
    page = getHtml(pageUrl)

    columns = page.cssselect("div[id='content'] div[class='span3']")

    for column in columns[1:]:
        category = column.cssselect("h4")[0].text_content()

        links = column.cssselect("a")
        for link in links:
            name = link.text_content()
            url = siteUrl + link.get("href")
            processProfile(name, category, url)
            
#do actual scraping
processPage(siteUrl + '/people/')
#!/usr/bin/python

import scraperwiki

siteUrl = "http://www.awm.gov.au"

import lxml.html
import re
import urllib2

class Person:

    # A static copy of style information from the scraped page
    styleInfo = """<meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link type="text/css" rel="stylesheet" href="http://www.awm.gov.au/sites/default/files/css/css__c5mKe0-yfYp9B-9V727-n4s0fuGroBMaK1VpFXNdxQ.css" media="all" />
        <link type="text/css" rel="stylesheet" href="http://www.awm.gov.au/sites/default/files/css/css_rbPOVGSp56MWwJZO2b6piNmMTbmGpasvf0zhr9Kd1Zk.css" media="print" />
        <script type="text/javascript" src="http://www.awm.gov.au/sites/default/files/js/js_sW0Dntw3YXT4_7wek4Lqiseqb67ctm_oGmJWNMjiDI4.js"></script>
        <script type="text/javascript" src="http://www.awm.gov.au/sites/default/files/js/js_3ORzZuIaDnY49q_JZ6vmjALkS9efn3H_xYVA-5vzN9k.js"></script>"""

    fullHtml = ""
    displayName = ""
    fullName = ""
    category = ""
    url = ""
    informationHtml = ""
    storyHtml = ""
    images = ""
    links = ""

    def __init__(self, fullHtml, displayName, fullName, category, url, informationHtml, storyHtml, images, links):
        self.fullHtml = styleInfo + fullHtml
        self.displayName = displayName
        self.fullName = fullName
        self.category = category
        self.url = url
        self.informationHtml = informationHtml
        self.storyHtml = storyHtml
        self.images = images
        self.links = links

    def save(self):
        data = {
            'fullHtml' : self.fullHtml,
            'displayName' : self.displayName,
            'fullName' : self.fullName,
            'category' : self.category,
            'url' : self.url,
            'informationHtml' : self.informationHtml,
            'storyHtml' : self.storyHtml,
            'images' : self.images,
            'links' : self.links
            
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['displayName', 'url'], data=data)

    def printOut(self):
            print 'Name: ' + self.displayName
            print 'Full Name: ' + self.fullName
            print 'Category: ' + self.category
            print 'Url: ' + self.url
            print 'Information: ' + self.informationHtml
            print 'Story: ' + self.storyHtml
            print 'Images: ' + self.images
            print 'Links: ' + self.links

def getHtml(url):
    html = urllib2.urlopen(url)
    page = lxml.html.fromstring(html.read())
    html.close()

    return page

def replaceUrls(html):
    # this should replace all relative URLs with absolute URLs
    return html

def processProfile(name, category, url):
    page = getHtml(url).cssselect("div[id='content']")[0]

    fullHtml = replaceUrls(lxml.html.tostring(page))

    displayName = name
    fullName = ""
    try:
        fullName = page.cssselect("h2")[0].text_content()
    except IndexError:
        fullName = page.cssselect("h1")[0].text_content()
        
    category = category
    informationHtml = lxml.html.tostring(page.cssselect("p")[0])

    paragraphs = page.cssselect("p")
    numParas = len(paragraphs)
    storyHtml = ""
    if (numParas < 2):
        raise Exception('Expected more than 1 paragraph but only ' + numParas + ' paragraphs found for person ' + name + ' at Url: ' + url)
    else:
        #Start at the 2nd paragraph, 1st is the information
        storyHtml = ''.join([lxml.html.tostring(ps).strip() for ps in paragraphs[1:]])

    images = ''.join([lxml.html.tostring(img).strip() for img in page.cssselect("img")])
    links = ''.join([lxml.html.tostring(link).strip() for link in page.cssselect("ul li")])

    person = Person(fullHtml, displayName, fullName, category, url, informationHtml, storyHtml, images, links)
    #person.printOut()
    person.save()

def processPage(pageUrl):
    page = getHtml(pageUrl)

    columns = page.cssselect("div[id='content'] div[class='span3']")

    for column in columns[1:]:
        category = column.cssselect("h4")[0].text_content()

        links = column.cssselect("a")
        for link in links:
            name = link.text_content()
            url = siteUrl + link.get("href")
            processProfile(name, category, url)
            
#do actual scraping
processPage(siteUrl + '/people/')
