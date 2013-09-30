import scraperwiki
import lxml.html 
import urllib
import string

html = scraperwiki.scrape("http://www.infoplease.com/ipa/A0763098.html")
root = lxml.html.fromstring(html)

## goes over each row in the table of City Population and prints out its content
for tr in root.cssselect("table[class='tableizer-table'] tr")[1:]:

    tds = tr.cssselect("td")

    name = tds[0].cssselect("a")[0].text   ## gets name of city
    ## state = tds[0].text
    pop2011 = tds[1].text                  ## gets population of city in 2011
    percentchange = tds[6].text            ## gets percent change in population, 1990-2000
    sizerank = tds[10].text                ## gets rank size of city

    search = scraperwiki.scrape("http://api.geonames.org/search?name_equals=" + name + "&maxRows=1&username=jpalapuz")
    print search
    ## prints data in a column/row 
    data = {
        'Name' : name,
        ## 'State' : state,
        '2011 Population' : pop2011,
        'Percent Change 1990-2000' : percentchange,
        'Size Rank 2010' : sizerank
    }
    
    scraperwiki.sqlite.save(unique_keys=['Name'],data=data)
    
import scraperwiki
import lxml.html 
import urllib
import string

html = scraperwiki.scrape("http://www.infoplease.com/ipa/A0763098.html")
root = lxml.html.fromstring(html)

## goes over each row in the table of City Population and prints out its content
for tr in root.cssselect("table[class='tableizer-table'] tr")[1:]:

    tds = tr.cssselect("td")

    name = tds[0].cssselect("a")[0].text   ## gets name of city
    ## state = tds[0].text
    pop2011 = tds[1].text                  ## gets population of city in 2011
    percentchange = tds[6].text            ## gets percent change in population, 1990-2000
    sizerank = tds[10].text                ## gets rank size of city

    search = scraperwiki.scrape("http://api.geonames.org/search?name_equals=" + name + "&maxRows=1&username=jpalapuz")
    print search
    ## prints data in a column/row 
    data = {
        'Name' : name,
        ## 'State' : state,
        '2011 Population' : pop2011,
        'Percent Change 1990-2000' : percentchange,
        'Size Rank 2010' : sizerank
    }
    
    scraperwiki.sqlite.save(unique_keys=['Name'],data=data)
    
