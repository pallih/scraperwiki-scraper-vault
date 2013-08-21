###############################################################################
# This does both Peace River North and Peace River South pages
# ** PAGE NUMBERS ARE SET MANUALLY HERE; NEED TO CHECK LAST PAGE ON FRACFOCUS.CA AND THEN SET TO ONE MORE THAN THAT ON COUNTERS BELOW **
# *** Remember the "even row" and "odd row" tagging; need to grab both otherwise only getting half the data
# doesn't have error correction here if it reaches last page; that would be better than having to check manually to see how many pages of data there are (it seems to change semi-regularly)

import mechanize 
import lxml.html
import time
import urllib2
import scraperwiki
from datetime import datetime

def scrape_pdf(url, riding, pagenum):

    time.sleep(5)

    try:
        pdfdata = urllib2.urlopen(url).read()
    except: # helps skip over weird URL resolution errors
        time.sleep(60)
        pdfdata = urllib2.urlopen(url).read()                  

    print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    
    print "After converting to xml it has %d bytes" % len(xmldata)
    
    root = lxml.etree.fromstring(xmldata)
    
    # this line uses xpath to find <text> tags
    
    # this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text>tags and put them all in a list variable called 'lines'
    
    lines = root.findall('.//text[@font="3"]//b')
    
    record={}

    record["riding"] = riding

    record["pagenum"] = pagenum
    
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

    page = 0

    while page < 10:
        page = page + 1
        pagestring = './/page[@number="' + str(page) + '"]'
        pagedata = root.find(pagestring)
        if pagedata != None:
            xpathtopvalue = 0
            while xpathtopvalue < 1000:
                record["Ingredients"] = ""
                record["ChemAbstract"] = ""
                record["MaxIngredientAdditive"] = ""
                record["MaxIngredientFluid"] = ""    
                xpathtopvalue = xpathtopvalue + 1
                xpathtext = './/text[@top="' + str(xpathtopvalue) + '"]'
                texttags = pagedata.findall(xpathtext)
                for text in texttags:
            
                    left = text.attrib.get('left')
                    leftinteger = int(left)
            
                    if leftinteger == 469:
                        record ["Ingredients"] = text.text
                        print record
                    
                    if leftinteger == 665:
                        record ["ChemAbstract"] = text.text
                        print record
                    
                    if 810 < leftinteger < 818:
                        record ["MaxIngredientAdditive"] = text.text
                        print record
                    
                    if 885 < leftinteger < 905:
                        record ["MaxIngredientFluid"] = text.text
                        print record
                
                if record["Ingredients"] != "":
            
                    uniqueid = str(datetime.now())
                    record["uniqueid"] = uniqueid                                
                    scraperwiki.sqlite.save(['uniqueid'], record)    
                
# don't need to reset record as blank here because it's done at the very top and we *don't* want to reset well data as it cycles through ingredients

    
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

page = 0 # jog back to zero later

while page < 27: # set at maximum pages for Peace River North; page 0 is first page
    
    riding = "Peace River North" # added region identifier for output

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
        scrape_pdf(url, riding, page)
        
    print 'Even'
    
    for tr in evenrows:
        link = tr.cssselect("a")[0]
        site = link.attrib.get('href')
        url = 'http://fracfocus.ca' + site
        print url
        scrape_pdf(url, riding, page)

page = 0 # jog back to zero later

while page < 26: # set one more than Peace River South last page

    riding = "Peace River South" # added region identifier for output

    url = "http://fracfocus.ca/find_well/BC"
    response = br.open(url)
    
    print response.read()
    
    # for form in br.forms():
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
        scrape_pdf(url, riding, page)
        
    print 'Even'
    
    for tr in evenrows:
        link = tr.cssselect("a")[0]
        site = link.attrib.get('href')
        url = 'http://fracfocus.ca' + site
        print url
        scrape_pdf(url, riding, page)
