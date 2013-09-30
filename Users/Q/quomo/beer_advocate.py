import scraperwiki
import lxml.html
import mechanize

beerindex = 'http://beeradvocate.com/beer/style/' #url that lists all styles
styleLinks = []

br = mechanize.Browser()

#response = br.open(beerindex)

#print response.read()

'''get all link info from beer style page'''
scrape = scraperwiki.scrape(beerindex)

root = lxml.html.fromstring(scrape)

for el in root.cssselect("table td a"):
    '''save all style link id to a list'''
    styleLinks.append(beerindex + el.attrib['href'][12:])

#print styleIds

'''open each link and get their contents -- each style has a table in which beers are listed'''
for i in styleLinks:

    result = scraperwiki.scrape(i)
    styleTable = lxml.html.fromstring(result)
    
    for el in styleTable.cssselect('b'):
        print el.text_content()



import scraperwiki
import lxml.html
import mechanize

beerindex = 'http://beeradvocate.com/beer/style/' #url that lists all styles
styleLinks = []

br = mechanize.Browser()

#response = br.open(beerindex)

#print response.read()

'''get all link info from beer style page'''
scrape = scraperwiki.scrape(beerindex)

root = lxml.html.fromstring(scrape)

for el in root.cssselect("table td a"):
    '''save all style link id to a list'''
    styleLinks.append(beerindex + el.attrib['href'][12:])

#print styleIds

'''open each link and get their contents -- each style has a table in which beers are listed'''
for i in styleLinks:

    result = scraperwiki.scrape(i)
    styleTable = lxml.html.fromstring(result)
    
    for el in styleTable.cssselect('b'):
        print el.text_content()



import scraperwiki
import lxml.html
import mechanize

beerindex = 'http://beeradvocate.com/beer/style/' #url that lists all styles
styleLinks = []

br = mechanize.Browser()

#response = br.open(beerindex)

#print response.read()

'''get all link info from beer style page'''
scrape = scraperwiki.scrape(beerindex)

root = lxml.html.fromstring(scrape)

for el in root.cssselect("table td a"):
    '''save all style link id to a list'''
    styleLinks.append(beerindex + el.attrib['href'][12:])

#print styleIds

'''open each link and get their contents -- each style has a table in which beers are listed'''
for i in styleLinks:

    result = scraperwiki.scrape(i)
    styleTable = lxml.html.fromstring(result)
    
    for el in styleTable.cssselect('b'):
        print el.text_content()



import scraperwiki
import lxml.html
import mechanize

beerindex = 'http://beeradvocate.com/beer/style/' #url that lists all styles
styleLinks = []

br = mechanize.Browser()

#response = br.open(beerindex)

#print response.read()

'''get all link info from beer style page'''
scrape = scraperwiki.scrape(beerindex)

root = lxml.html.fromstring(scrape)

for el in root.cssselect("table td a"):
    '''save all style link id to a list'''
    styleLinks.append(beerindex + el.attrib['href'][12:])

#print styleIds

'''open each link and get their contents -- each style has a table in which beers are listed'''
for i in styleLinks:

    result = scraperwiki.scrape(i)
    styleTable = lxml.html.fromstring(result)
    
    for el in styleTable.cssselect('b'):
        print el.text_content()



