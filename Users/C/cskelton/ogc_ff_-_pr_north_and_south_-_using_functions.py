###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
# Maybe use Outwit Hub to grab URLs first? Next doesn't work, but could just cycle through pages as it grabs URLs; then put in a list for PDF scraper
# Ignoring readonly on page number lets me cycle through pages
# *** Remember the "even row" and "odd row" tagging; need to grab both otherwise only getting half the data
# as written, this is pulling the same PDF multiple times I think
# think I need to define variables to clear this up

# doesn't have error correction here if it reaches last page; that would be better than having to check manually to see how many pages of data there are (it seems to change semi-regularly)

import mechanize 
import lxml.html
import time
import urllib2
import scraperwiki

def scrape_pdf(url):

    time.sleep(5)

    pdfdata = urllib2.urlopen(url).read()
    
    print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    
    print "After converting to xml it has %d bytes" % len(xmldata)
    
    root = lxml.etree.fromstring(xmldata)
    
    # this line uses xpath to find <text tags
    
    # this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text>tags and put them all in a list variable called 'lines'
    
    lines = root.findall('.//text[@font="3"]//b')
    
    record={}
    
    try:
        record["date"] = lines[12].text
    except:
        record["date"] = ""
    try:
        record["province"] = lines[13].text
    except:
        record["province"] = ""
    try:
        record["region"] = lines[14].text
    except:
        record["region"] = ""
    try:
        record["long"] = lines[20].text
    except:
        record["long"] = ""
    try:
        record["lat"] = lines[21].text
    except:
        record["lat"] = ""
    try:
        record["water"] = lines[16].text
    except:
        record["water"] = ""
    try:
        record["operator"] = lines[18].text
    except:
        record["operator"] = ""
    try:
        record["wellname"] = lines[19].text
    except:
        record["wellname"] = ""
    try:
        record["url"] = url
    except:
        record["url"] = ""
    try:
        record["wellnumber"] = lines[17].text # new
    except:
        record["wellnumber"] = ""
    try:
        record["longlatproj"] = lines[22].text # new
    except:
        record["longlatproj"] = ""
    try:
        record["producttype"] = lines[23].text #new
    except:
        record["producttype"] = ""
    try:
        record["tvd"] = lines[15].text #new
    except:
        record["tvd"] = ""
    
    print record
    
    scraperwiki.sqlite.save(['url'], record)
    
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

page = 0 # jog back to zero later

while page < 28: # set to 33 when ready to go for Peace River North, set to 20 for Peace River South

    url = "http://fracfocus.ca/find_well/BC"
    response = br.open(url)
    
    print response.read()
    
    #for form in br.forms():
    #    print "Form name:", form.name
    #    print form
    
    br.form = list(br.forms())[0]
    br.form.set_all_readonly(False) # allow changing the .value of all controls, lets me change page number to cycle through them
    
    br["dropdown_region"] = ["Peace River North"] # selects Peace River North Region or Peace River South; no wells in any other B.C. region - checked 
    br["page"] = str(page) # selects Peace River North Region (think Gord said there are only any in Peace River)
    
    response = br.submit()
    
    html = response.read()
    
    page = page + 1

    print 'Peace River North:' + str(page)
    
    print html
    
    root = lxml.html.fromstring(html)
    
    oddrows = root.cssselect("tr.odd")
    evenrows = root.cssselect("tr.even")
     
    print 'Odd'
    
    for tr in oddrows:
        link = tr.cssselect("a")[0]
        site = link.attrib.get('href')
        url = 'http://fracfocus.ca' + site
        print url
        scrape_pdf(url)
        
    print 'Even'
    
    for tr in evenrows:
        link = tr.cssselect("a")[0]
        site = link.attrib.get('href')
        url = 'http://fracfocus.ca' + site
        print url
        scrape_pdf(url)

page = 0 # jog back to zero later

while page < 18: # set to 33 when ready to go for Peace River North, set to 20 for Peace River South

    url = "http://fracfocus.ca/find_well/BC"
    response = br.open(url)
    
    print response.read()
    
    #for form in br.forms():
    #    print "Form name:", form.name
    #    print form
    
    br.form = list(br.forms())[0]
    br.form.set_all_readonly(False) # allow changing the .value of all controls, lets me change page number to cycle through them
    
    br["dropdown_region"] = ["Peace River South"] # selects Peace River North Region or Peace River South; no wells in any other B.C. region - checked 
    br["page"] = str(page) # selects Peace River North Region (think Gord said there are only any in Peace River)
    
    response = br.submit()
    
    html = response.read()
    
    page = page + 1

    print 'Peace River South:' + str(page)
    
    print html
    
    root = lxml.html.fromstring(html)
    
    oddrows = root.cssselect("tr.odd")
    evenrows = root.cssselect("tr.even")
     
    print 'Odd'
    
    for tr in oddrows:
        link = tr.cssselect("a")[0]
        site = link.attrib.get('href')
        url = 'http://fracfocus.ca' + site
        print url
        scrape_pdf(url)
        
    print 'Even'
    
    for tr in evenrows:
        link = tr.cssselect("a")[0]
        site = link.attrib.get('href')
        url = 'http://fracfocus.ca' + site
        print url
        scrape_pdf(url)
