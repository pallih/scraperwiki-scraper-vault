# Parses victorian ALP media releases


from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser

import scraperwiki
import lxml.html
import urlparse

# starting point
url = "http://www.premier.vic.gov.au/media-centre/media-releases.html"
base = "http://www.premier.vic.gov.au"


# the number of pages of media releases we should page through
numpages = 10

for x in range(0, numpages):
    print url
    
    html = scraperwiki.scrape(url)
              
    root = lxml.html.fromstring(html)

    nextpage = root.xpath(".//a[@title='Next']")[0].attrib['href']
    print nextpage
    
    for item in root.cssselect("div.item"):
        title = item.cssselect("h2 a")[0].text_content()
        title = " ".join(title.split())
        link =  base + item.cssselect("h2 a")[0].attrib['href']
        guid = link
        author = "unknown"
        date = item.cssselect("dd.create")[0].text
        published = dateutil.parser.parse(date)
        print published
        description = item.cssselect("dl")[0].xpath("following-sibling::p | following-sibling::div")[0].text_content()
        print description
        
        # now fetch the page and get the text
        page = scraperwiki.scrape(link)
        pagesoup = BeautifulSoup(page)
        page_content = pagesoup.find("div", { "class" : "item-page" })
        
        for tag in page_content.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(link, tag['href'])    

        [x.extract() for x in page_content.findAll('script')] #remove script tags
        [x.extract() for x in page_content.findAll('button')] #remove extra
        [x.extract() for x in page_content.findAll('fb:like')]
        [x.extract() for x in page_content.findAll('a', {"class" : "twitter-share-button"})]
        [x.extract() for x in page_content.findAll('p', {"class" : "buttonheading"})]
        [x.extract() for x in page_content.findAll('div', {"id" : "socialbut"})]
        [x.extract() for x in page_content.findAll('div', {"class" : "tt-tags"})]
    
        new_page_content = page_content.findAll(['p','h1','h2','h3','h4','b','i','strong','em','a','div'])

        
    
        print new_page_content
        new_page_text = unicode.join(u'\n',map(unicode,new_page_content))
    
    
        pdflink = ""

        # try and get the link to the pdf file if there is one
        pdf_file = page_content.find("a", {"class" : "wf_file"})
        if pdf_file:
            pdflink = pdf_file["href"]
        
        print pdf_file

        
        
    
        record = {"link" : link,
                  "title" : title,
                  "author" : author,
                  "published" : published,
                  "description" : description,
                  "fulltext" : new_page_text,
                  "pdf" : pdflink}
    
        if re.search(ur'media-release', link):
            scraperwiki.sqlite.save(unique_keys=["link"], data=record)
        
    url = base + nextpage



# Parses victorian ALP media releases


from bs4 import BeautifulSoup
import feedparser
import re
import dateutil.parser

import scraperwiki
import lxml.html
import urlparse

# starting point
url = "http://www.premier.vic.gov.au/media-centre/media-releases.html"
base = "http://www.premier.vic.gov.au"


# the number of pages of media releases we should page through
numpages = 10

for x in range(0, numpages):
    print url
    
    html = scraperwiki.scrape(url)
              
    root = lxml.html.fromstring(html)

    nextpage = root.xpath(".//a[@title='Next']")[0].attrib['href']
    print nextpage
    
    for item in root.cssselect("div.item"):
        title = item.cssselect("h2 a")[0].text_content()
        title = " ".join(title.split())
        link =  base + item.cssselect("h2 a")[0].attrib['href']
        guid = link
        author = "unknown"
        date = item.cssselect("dd.create")[0].text
        published = dateutil.parser.parse(date)
        print published
        description = item.cssselect("dl")[0].xpath("following-sibling::p | following-sibling::div")[0].text_content()
        print description
        
        # now fetch the page and get the text
        page = scraperwiki.scrape(link)
        pagesoup = BeautifulSoup(page)
        page_content = pagesoup.find("div", { "class" : "item-page" })
        
        for tag in page_content.findAll('a', href=True):
            tag['href'] = urlparse.urljoin(link, tag['href'])    

        [x.extract() for x in page_content.findAll('script')] #remove script tags
        [x.extract() for x in page_content.findAll('button')] #remove extra
        [x.extract() for x in page_content.findAll('fb:like')]
        [x.extract() for x in page_content.findAll('a', {"class" : "twitter-share-button"})]
        [x.extract() for x in page_content.findAll('p', {"class" : "buttonheading"})]
        [x.extract() for x in page_content.findAll('div', {"id" : "socialbut"})]
        [x.extract() for x in page_content.findAll('div', {"class" : "tt-tags"})]
    
        new_page_content = page_content.findAll(['p','h1','h2','h3','h4','b','i','strong','em','a','div'])

        
    
        print new_page_content
        new_page_text = unicode.join(u'\n',map(unicode,new_page_content))
    
    
        pdflink = ""

        # try and get the link to the pdf file if there is one
        pdf_file = page_content.find("a", {"class" : "wf_file"})
        if pdf_file:
            pdflink = pdf_file["href"]
        
        print pdf_file

        
        
    
        record = {"link" : link,
                  "title" : title,
                  "author" : author,
                  "published" : published,
                  "description" : description,
                  "fulltext" : new_page_text,
                  "pdf" : pdflink}
    
        if re.search(ur'media-release', link):
            scraperwiki.sqlite.save(unique_keys=["link"], data=record)
        
    url = base + nextpage



