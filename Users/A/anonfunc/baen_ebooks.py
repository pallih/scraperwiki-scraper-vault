import requests
import scraperwiki           
import lxml.html           
import re


urlBase = "http://www.baenebooks.com/"

r = requests.get(urlBase)


def emitData(bookPage):
    for bookTr in bookPage.cssselect("td.maintext tr tr")[1:]:
        columns = bookTr.getchildren()
#        print "Looking at " + bookTr.text_content()
        if len(columns) == 4:
            titleLink = columns[1].cssselect("a")[0]
            title = titleLink.text_content()
            if 'Bundle' in title:
                continue
            if 'Night Shade Books' in title:
                continue
            if 'Gazette' in title:
                continue

            titleUrl = titleLink.attrib['href']
            priceText = columns[2].text_content()
            priceMatch = re.findall('(?<=\$)\d+.\d+', priceText)
            if len(priceMatch) > 0:
                price = priceMatch[-1]
            else:
                price = "0.00"
            
            data = { "author": author,
                     "title" : title,
                     "price" : price,
                     "detailUrl" : urlBase+titleUrl }
#            print data
            scraperwiki.sqlite.save(unique_keys=['detailUrl'], data=data)


# Find author links.

root = lxml.html.fromstring(r.text)
for link in root.cssselect("#departments a"):
    author = link.text_content()
    authorPage = link.attrib['href']
    # print "Author is " + author + ", Link is " + authorPage
    r = requests.get(urlBase + authorPage)
    authorPage = lxml.html.fromstring(r.text)
    emitData(authorPage) # is first page of books.
    pages = authorPage.cssselect("a.PageNumber")
    # Skip first row, as it is the header.
    seen = set()
    for pageLink in pages:
        pageNum = pageLink.text
        if pageNum not in seen:
            print "Fetching page " + pageNum
            seen.add(pageNum)
            page = requests.get(urlBase + pageLink.attrib['href'])
            emitData(lxml.html.fromstring(page.text))
        else:
            print "Already been to page" + pageNumimport requests
import scraperwiki           
import lxml.html           
import re


urlBase = "http://www.baenebooks.com/"

r = requests.get(urlBase)


def emitData(bookPage):
    for bookTr in bookPage.cssselect("td.maintext tr tr")[1:]:
        columns = bookTr.getchildren()
#        print "Looking at " + bookTr.text_content()
        if len(columns) == 4:
            titleLink = columns[1].cssselect("a")[0]
            title = titleLink.text_content()
            if 'Bundle' in title:
                continue
            if 'Night Shade Books' in title:
                continue
            if 'Gazette' in title:
                continue

            titleUrl = titleLink.attrib['href']
            priceText = columns[2].text_content()
            priceMatch = re.findall('(?<=\$)\d+.\d+', priceText)
            if len(priceMatch) > 0:
                price = priceMatch[-1]
            else:
                price = "0.00"
            
            data = { "author": author,
                     "title" : title,
                     "price" : price,
                     "detailUrl" : urlBase+titleUrl }
#            print data
            scraperwiki.sqlite.save(unique_keys=['detailUrl'], data=data)


# Find author links.

root = lxml.html.fromstring(r.text)
for link in root.cssselect("#departments a"):
    author = link.text_content()
    authorPage = link.attrib['href']
    # print "Author is " + author + ", Link is " + authorPage
    r = requests.get(urlBase + authorPage)
    authorPage = lxml.html.fromstring(r.text)
    emitData(authorPage) # is first page of books.
    pages = authorPage.cssselect("a.PageNumber")
    # Skip first row, as it is the header.
    seen = set()
    for pageLink in pages:
        pageNum = pageLink.text
        if pageNum not in seen:
            print "Fetching page " + pageNum
            seen.add(pageNum)
            page = requests.get(urlBase + pageLink.attrib['href'])
            emitData(lxml.html.fromstring(page.text))
        else:
            print "Already been to page" + pageNum