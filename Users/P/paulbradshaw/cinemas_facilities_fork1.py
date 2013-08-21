# Data stored on individual pages not accessible from one single page
# typical URL is http://www.myvue.com/cinemas/facilities/cinema/aberdeen
# Need to cycle through a list of URLs, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url' (line 52 or so)

#import the 2 libraries we need
import scraperwiki
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'divs'
    #there's more than one div, so we need to specify the class="cinemainfo_facilities_item_copy", represented by the full stop
#SOLVE: HITS AN ERROR AT MERTHYR-TYDFIL (ONLY 2 DIVS) - IS IT ALWAYS THE LAST ONE?
    divs = root.cssselect("div.cinemainfo_facilities_item_copy")
    #This grabs the text content (minus HTML) of the last div
    print divs[-1].text_content()
    #create a new variable to act as a unique ID for each entry
    refid = 0
    lastdiv = divs[-1].text_content()
    allhtml = divs[-1].text
    print lastdiv
    record = {}
    record['alltext'] = lastdiv
    record['allhtml'] = allhtml
    lastdivlxml = lxml.html.fromstring(lastdiv)
    print lastdivlxml
#    record['heading2'] = lastdivlxml.cssselect("h2")
    print record
    record['URL'] = item
    scraperwiki.sqlite.save(["URL"], record)

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new lxml object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.myvue.com/cinemas/facilities/cinema/'
#And these are the strings which we need to complete that URL to make each individual URL
#This list has been compiled using the =JOIN formula in Google Docs on a column of URLs
cinemaIDs = ['aberdeen','accrington','acton','basingstoke-festival-place','birkenhead','birmingham','blackburn','bolton','bristol-cribbs-causeway','bristol-longwell-green','bury-the-rock','camberley','cambridge','cardiff','carlisle','cheshire-oaks','cleveleys','croydon-grants','croydon-purley-way','cwmbran','dagenham','doncaster','dublin','eastleigh','edinburgh-ocean-terminal','edinburgh-omni-centre','exeter','finchley-road-o2-centre','fulham-broadway','hamilton','harrow','hartlepool','hull-princes-quay','inverness','islington','lancaster','leeds-kirkstall-road','leeds-the-light','leicester','livingston','manchester-lowry','merthyr-tydfil','newbury','newcastle-under-lyme','north-finchley','northampton','norwich','oxford','plymouth','portsmouth','preston','reading','romford','scunthorpe','sheffield','shepherds-bush','southport','staines','stirling','swansea','thurrock','watford','west-end-leicester-square','westfield','stratford','westwood-cross-thanet','wood-green','worcester','york']
#go through the list above, and for each item...
for item in cinemaIDs:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)

# Data stored on individual pages not accessible from one single page
# typical URL is http://www.myvue.com/cinemas/facilities/cinema/aberdeen
# Need to cycle through a list of URLs, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url' (line 52 or so)

#import the 2 libraries we need
import scraperwiki
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'divs'
    #there's more than one div, so we need to specify the class="cinemainfo_facilities_item_copy", represented by the full stop
#SOLVE: HITS AN ERROR AT MERTHYR-TYDFIL (ONLY 2 DIVS) - IS IT ALWAYS THE LAST ONE?
    divs = root.cssselect("div.cinemainfo_facilities_item_copy")
    #This grabs the text content (minus HTML) of the last div
    print divs[-1].text_content()
    #create a new variable to act as a unique ID for each entry
    refid = 0
    lastdiv = divs[-1].text_content()
    allhtml = divs[-1].text
    print lastdiv
    record = {}
    record['alltext'] = lastdiv
    record['allhtml'] = allhtml
    lastdivlxml = lxml.html.fromstring(lastdiv)
    print lastdivlxml
#    record['heading2'] = lastdivlxml.cssselect("h2")
    print record
    record['URL'] = item
    scraperwiki.sqlite.save(["URL"], record)

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new lxml object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.myvue.com/cinemas/facilities/cinema/'
#And these are the strings which we need to complete that URL to make each individual URL
#This list has been compiled using the =JOIN formula in Google Docs on a column of URLs
cinemaIDs = ['aberdeen','accrington','acton','basingstoke-festival-place','birkenhead','birmingham','blackburn','bolton','bristol-cribbs-causeway','bristol-longwell-green','bury-the-rock','camberley','cambridge','cardiff','carlisle','cheshire-oaks','cleveleys','croydon-grants','croydon-purley-way','cwmbran','dagenham','doncaster','dublin','eastleigh','edinburgh-ocean-terminal','edinburgh-omni-centre','exeter','finchley-road-o2-centre','fulham-broadway','hamilton','harrow','hartlepool','hull-princes-quay','inverness','islington','lancaster','leeds-kirkstall-road','leeds-the-light','leicester','livingston','manchester-lowry','merthyr-tydfil','newbury','newcastle-under-lyme','north-finchley','northampton','norwich','oxford','plymouth','portsmouth','preston','reading','romford','scunthorpe','sheffield','shepherds-bush','southport','staines','stirling','swansea','thurrock','watford','west-end-leicester-square','westfield','stratford','westwood-cross-thanet','wood-green','worcester','york']
#go through the list above, and for each item...
for item in cinemaIDs:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)

# Data stored on individual pages not accessible from one single page
# typical URL is http://www.myvue.com/cinemas/facilities/cinema/aberdeen
# Need to cycle through a list of URLs, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url' (line 52 or so)

#import the 2 libraries we need
import scraperwiki
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'divs'
    #there's more than one div, so we need to specify the class="cinemainfo_facilities_item_copy", represented by the full stop
#SOLVE: HITS AN ERROR AT MERTHYR-TYDFIL (ONLY 2 DIVS) - IS IT ALWAYS THE LAST ONE?
    divs = root.cssselect("div.cinemainfo_facilities_item_copy")
    #This grabs the text content (minus HTML) of the last div
    print divs[-1].text_content()
    #create a new variable to act as a unique ID for each entry
    refid = 0
    lastdiv = divs[-1].text_content()
    allhtml = divs[-1].text
    print lastdiv
    record = {}
    record['alltext'] = lastdiv
    record['allhtml'] = allhtml
    lastdivlxml = lxml.html.fromstring(lastdiv)
    print lastdivlxml
#    record['heading2'] = lastdivlxml.cssselect("h2")
    print record
    record['URL'] = item
    scraperwiki.sqlite.save(["URL"], record)

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new lxml object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.myvue.com/cinemas/facilities/cinema/'
#And these are the strings which we need to complete that URL to make each individual URL
#This list has been compiled using the =JOIN formula in Google Docs on a column of URLs
cinemaIDs = ['aberdeen','accrington','acton','basingstoke-festival-place','birkenhead','birmingham','blackburn','bolton','bristol-cribbs-causeway','bristol-longwell-green','bury-the-rock','camberley','cambridge','cardiff','carlisle','cheshire-oaks','cleveleys','croydon-grants','croydon-purley-way','cwmbran','dagenham','doncaster','dublin','eastleigh','edinburgh-ocean-terminal','edinburgh-omni-centre','exeter','finchley-road-o2-centre','fulham-broadway','hamilton','harrow','hartlepool','hull-princes-quay','inverness','islington','lancaster','leeds-kirkstall-road','leeds-the-light','leicester','livingston','manchester-lowry','merthyr-tydfil','newbury','newcastle-under-lyme','north-finchley','northampton','norwich','oxford','plymouth','portsmouth','preston','reading','romford','scunthorpe','sheffield','shepherds-bush','southport','staines','stirling','swansea','thurrock','watford','west-end-leicester-square','westfield','stratford','westwood-cross-thanet','wood-green','worcester','york']
#go through the list above, and for each item...
for item in cinemaIDs:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)

