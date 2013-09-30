import scraperwiki
import lxml.html
import urlparse

def getresults(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    tables = root.cssselect('table.data')
    homeside = tables[0]
    for tr in homeside.cssselect("table.data tr"):
        tds = tr.cssselect("td")
        if len(tds)==7:
            data = {
                'player' : tds[0].text_content(),
                'vanquisher' : tds[1].text_content(),
                'bowler' : tds[2].text_content(),
                'runs' : tds[3].text_content()
            }
            print data

def parsemenu(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tables = root.cssselect('table.data')
    matchtable = tables[0]    
    for tr in matchtable.cssselect("table.data tr"):
        tds = tr.cssselect("td")
        if len(tds)==8:          
            links = tds[7].cssselect("a")
            resultslink = base_url + links[0].attrib.get('href')
            print resultslink
            getresults(resultslink)

base_url='http://eapcl.play-cricket.com/scoreboard/'
results_url='http://eapcl.play-cricket.com/scoreboard/results.asp'
parsemenu(results_url)import scraperwiki
import lxml.html
import urlparse

def getresults(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    tables = root.cssselect('table.data')
    homeside = tables[0]
    for tr in homeside.cssselect("table.data tr"):
        tds = tr.cssselect("td")
        if len(tds)==7:
            data = {
                'player' : tds[0].text_content(),
                'vanquisher' : tds[1].text_content(),
                'bowler' : tds[2].text_content(),
                'runs' : tds[3].text_content()
            }
            print data

def parsemenu(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tables = root.cssselect('table.data')
    matchtable = tables[0]    
    for tr in matchtable.cssselect("table.data tr"):
        tds = tr.cssselect("td")
        if len(tds)==8:          
            links = tds[7].cssselect("a")
            resultslink = base_url + links[0].attrib.get('href')
            print resultslink
            getresults(resultslink)

base_url='http://eapcl.play-cricket.com/scoreboard/'
results_url='http://eapcl.play-cricket.com/scoreboard/results.asp'
parsemenu(results_url)