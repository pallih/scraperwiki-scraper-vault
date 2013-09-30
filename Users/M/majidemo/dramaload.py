###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import scraperwiki
import mechanize 
import lxml.html
import lxml.etree

def link(url):
    br = mechanize.Browser()
    response = br.open(url)
    br.select_form(nr=2)
    #print br.form
    br["usernamelogin"] = "majidemo"
    br["passwordlogin"] = "supbro"
    response = br.submit()
    #print response.read()

    html = response.read()
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('div.download-links a') # get all the <td> tags
    for td in tds:
        font = "".join(map(lxml.etree.tostring, list(td)))
        print td.text + font
        record = { "title" : td.text + font, "link" : td.attrib['href'],} # column name and value
        scraperwiki.sqlite.save(["title"], record) # save the records one by one

def xlist(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('td a') # get all the <td> tags
    for td in tds:
        record = { "title" : td.text, "link" : td.attrib['href'],} # column name and value
        scraperwiki.sqlite.save(["link"], record) # save the records one by one
        ep = td.attrib['href']
        eplist(ep)

def eplist(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('div.drama-download-online:not([id="drama-watch"]) a') # get all the <td> tags
    for td in tds:
        #record = { "title" : td.text, "link" : td.attrib['href'],} # column name and value
        #scraperwiki.sqlite.save(["link"], record) # save the records one by one
        epl = td.attrib['href']
        link(epl)

xlist("http://www.dramaload.com/drama-list/")

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import scraperwiki
import mechanize 
import lxml.html
import lxml.etree

def link(url):
    br = mechanize.Browser()
    response = br.open(url)
    br.select_form(nr=2)
    #print br.form
    br["usernamelogin"] = "majidemo"
    br["passwordlogin"] = "supbro"
    response = br.submit()
    #print response.read()

    html = response.read()
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('div.download-links a') # get all the <td> tags
    for td in tds:
        font = "".join(map(lxml.etree.tostring, list(td)))
        print td.text + font
        record = { "title" : td.text + font, "link" : td.attrib['href'],} # column name and value
        scraperwiki.sqlite.save(["title"], record) # save the records one by one

def xlist(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('td a') # get all the <td> tags
    for td in tds:
        record = { "title" : td.text, "link" : td.attrib['href'],} # column name and value
        scraperwiki.sqlite.save(["link"], record) # save the records one by one
        ep = td.attrib['href']
        eplist(ep)

def eplist(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('div.drama-download-online:not([id="drama-watch"]) a') # get all the <td> tags
    for td in tds:
        #record = { "title" : td.text, "link" : td.attrib['href'],} # column name and value
        #scraperwiki.sqlite.save(["link"], record) # save the records one by one
        epl = td.attrib['href']
        link(epl)

xlist("http://www.dramaload.com/drama-list/")

