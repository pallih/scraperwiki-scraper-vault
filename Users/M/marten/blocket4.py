##############################################################################
# MI Interpreters - the Python Version
#
# This script starts on the first page and then
# scrapes it and all subsequent pages by calling
# 'scrape_and_look_for_next_link' over and over
# again.
#
###############################################################################
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments

## NOTE: required before any other code (comments not included)
import scraperwiki
import lxml.html
from lxml import etree
from datetime import datetime
import time
import os, base64
import string

## YOU_SHOULD_KNOW: this is where you put your target url(s)
BASE_URL  = 'http://www.blocket.se'
FIRST_EXT = '/mi/interpreters?g=MI'
FIRST_EXT = '/hela_sverige/bilar?q=volvo&cg=1020&st=s&l=0&ca=11&w=3&f=a&o=1'
FIRST_EXT = '/hela_sverige/bilar?cg=1020&st=s&l=0&ca=11&w=3&sp=1&f=a&o=1'
FIRST_EXT = '/hela_sverige/bilar?ca=4&s=1&w=3&cg=1020&cb=3'
FIRST_EXT = '/hela_sverige/bilar?cg=1020&st=s&l=0&cb=3&ca=14&w=3&sp=1&f=a&o=1'
#FIRST_EXT = '/kristianstad/Bmw_525_96a_38787774.htm?ca=4&w=3'
MAX_PAGES    = 0  ## set to 0 for unlimited
CURRENT_PAGE = 0  ## keeps track of current page

COUNTER = 0
ITEM_URL = ""
ITEM_TITLE = ""
ITEM_DATA = ""
ITEM_PRICE = ''
ITEM_BODY = ""
ITEM_MODELLYEAR = ""
ITEM_GEAR =""
ITEM_MILEAGE =""
ITEM_MANUFACTUREYEAR = ""
ITEM_FUEL =""
ITEM_BRAND =""

keywords = {
    'ITEM_PRICE' : 'Pris',
    'ITEM_MODELYEAR' : u'Modell\xe5r',
    'ITEM_GEAR' : u'V\xe4xell\xe5da',
    'ITEM_MILEAGE' : 'Miltal',
    'ITEM_MANUFACTURERYEAR' : u'Tillverknings\xe5r',
    'ITEM_FUEL' : u'Br\xe4nsle',
    'ITEM_BRAND' : u'M\xe4rke',
    'ITEM_MODEL' : 'Modell',
}

item_data = {
    'ITEM_URL' : '',
    'ITEM_TITLE' : '',
    'ITEM_PRICE' : '',
    'ITEM_MODELYEAR' : '',
    'ITEM_GEAR' : '',
    'ITEM_MILEAGE' : '',
    'ITEM_MANUFACTURERYEAR' : '',
    'ITEM_FUEL' : '',
    'ITEM_BRAND' : '',
    'ITEM_MODEL' : '',
}

## NOTE: the intermediate function "check_data()" was required because
## not all the fields are filled for all businesses and I was getting
## errors when trying to add the data.
def check_data(data):
    if len(data) > 0:
        ## NOTE: pull out first element, get its text, remove end whitespace
        ## and then remove trailing ',' if it exists (like on addresses)
        return data[0].text_content().rstrip().rstrip(',')
    else:
        ## NOTE: otherwise, return 'n/a'
        return "n/a"


#def scrape_item_data(root, cssselect, string):
    #item = td.text_content()

def get_root(page_url):
    print "fn: get_root "
    page = scraperwiki.scrape(page_url)
    return lxml.html.fromstring(page)

def get_item(root, cssselect1, cssselect2):
    print "fn: get_item "
    count = 0
    for y in root.cssselect('.breadcrumb_top_container'):
        ITEM_DATA = y.cssselect('a')
        print "bread", ITEM_DATA

        for j in ITEM_DATA:
            count +=1
            item = j.text_content()
            brandlist = [['BMW',2], ['Volvo',2],['Volkswagen',2]]
            for bl in brandlist:
                if bl[0] in item:
                    #print "BMW!"
                    #print "get_item -> item: ", item
                    print "get_item -> brand: ", bl[0]
                    if bl[1]>1:
                        print "get_item -> model:"
                            

    for x in root.cssselect('.details'):
        # 'strong' contains all car specific data 
        # Extract all 'strong' elements
        #ITEM_DATA = x.cssselect('strong')
        ITEM_DATA = x.cssselect('td')

        #print ITEM_DATA
        for i in ITEM_DATA:
            count +=1
            item = i.text_content()
            if 'Pris' in item: 
                price = item[7:]
                print "PRICE!"
                #print "get_item -> item: ", item
                print "get_item -> price: ", price

            elif u'Modell\xe5r' in item:
                modelyear = item[11:16]
                print "MODEL YEAR!"
                #print "get_item -> item: ", item
                print "get_item -> modelyear: ", modelyear

            elif u'V\xe4xell\xe5da' in item:
                gearbox = item[12:]
                print "GEARBOX!"
                #print "get_item -> item: ", item
                print "get_item -> gearbox: ", gearbox

            elif u'Miltal' in item:
                milage = item[9:]
                print "MILAGE!"
                #print "get_item -> item: ", item
                print "get_item -> milage: ", milage

            elif u'Br\xe4nsle' in item:
                fuel = item[9:]
                print "FUEL!"
                #print "get_item -> item: ", item
                print "get_item -> fuel: ", fuel


            elif u'Tillverknings\xe5r' in item:
                manufacturingyear = item[18:]
                print "MANUFACTURINGYEAR!"
                #print "get_item -> item: ", item
                print "get_item -> manufacturingyear: ", manufacturingyear

    print "fn: get_item: END...%d" % count
           # if item.find(keywords.get('ITEM_PRICE')):
           #     keywords['ITEM_MODELYEAR']= item
           #     print "keywords ITEM = item: ", item

def scrape_item(page_url):
    ## NOTE: first, scrape the page
    global COUNTER
    COUNTER += 1
    page = scraperwiki.scrape(page_url)
    print page_url
    root = lxml.html.fromstring(page)


    for x in root.cssselect('.details'):
        global ITEM_DATA, ITEM_BODY, ITEM_PRICE
        ITEM_DATA = check_data(x.cssselect('.params.underlined_links'))
        ITEM_BODY = check_data(x.cssselect('.body'))

        #print "TEST", x.cssselect('.params.underlined_links')
        #for td in x.cssselect('.tbody'):
        #    print "td", td
        ITEM_DATA = x.cssselect('td')
        #test = x.cssselect('td').text.content()
        
        #print "item_price:", ITEM_PRICE.text.content()
        count = 0
        for td in ITEM_DATA:
            
            pris = u'Pris:'
            year = u'Modellår' ### detta måste fixas!!!!!
            gearbox = u'Växellåda'
            mileage = u'Miltal:'
            madeyear = u'Tillverkningsår'
            fuel = u'Bränsle:'
            
            brand = u'Märke:'
            model = u'Modell:'

            item = td.text_content()

#            if ages.has_key('Sue'):
#                    print "Sue is in the dictionary. She is", ages['Sue'], "years old"
#                else:
#                    print "Sue is not in the dictionary"
            #print ">>>> ITEM >>", item
            # Iterate over dict keys values
            count += 1
            #print "Keywords ->", keywords.get('ITEM_MODELYEAR')
            if item.find(keywords.get('ITEM_MODELYEAR')):
                #print "T-år 1: %s " % (count)
                keywords['ITEM_MODELYEAR']= item


            
## NOTE: scrape_table function gets passed an individual page to scrape
def scrape_table(page_url):

    ## NOTE: first, scrape the page
    page = scraperwiki.scrape(page_url)

    ## NOTE: next, parse the scraped page
    root = lxml.html.fromstring(page)

    

    ## NOTE: loop through each listing block delimited by 'div="desc"'
    for x in root.cssselect('.desc'):
        ## DEBUG: make sure we are seeing the correct data
        #print "SEE %s" % x
        #desc = check_data(x.cssselect('.desc'))
        #ITEM_TITLE = check_data(x.cssselect('.desc'))
        
        ITEM_TITLE = check_data(x.cssselect('.item_link'))
        for link in x.cssselect('a'):
            #link_text_content = link.text_content()
            ITEM_URL = link.get('href')
        list_price = check_data(x.cssselect('.list_price'))
        
        scrape_item(ITEM_URL)

        print "ITEM URL......... %s" % ITEM_URL
        print "ITEM_TITLE....... %s" % ITEM_TITLE
        print "LIST_PRICE....... %s" % list_price
        print "ITEM BODY........ %s" % ITEM_BODY
        print "*** NEW ITEM ***"


        ## NOTE: the intermediate function "check_data()" was required because
        ## not all the fields are filled for all businesses and I was getting
        ## errors when trying to add the data.

        UNIQ_ID = base64.b64encode(os.urandom(8))
        print "ID", UNIQ_ID[:-2]

        data = {
        # 'ID' : UNIQ_ID,
          'URL' : ITEM_URL,
          'TITLE' : ITEM_TITLE,
          'PRICE' : ITEM_PRICE,
          'DATA' : ITEM_DATA,
          'BODY' : ITEM_BODY,

        }
        scraperwiki.sqlite.save(unique_keys=['URL'], data=data)

## root = lxml.html.fromstring(html)
## for tr in root.cssselect("div[align='left'] tr.tcont"):
##     tds = tr.cssselect("td")
##     data = {
##       'country' : tds[0].text_content(),
##       'years_in_school' : int(tds[4].text_content())
##     }
##     print data


# <div align="left">
#   <table align="left" cellpadding="0" cellspacing="0">
#     <tbody>
#       <tr class="bar1">
#       <tr>
#         <tr bgcolor="#bce6f8">
#           <tr class="lheader">
#             <tr class="tcont">
#               <td height="19">Afghanistan</td>
#               <td height="19" align="right">2004</td>


    ## YOU_SHOULD_KNOW: if you would like to a global variable, be sure
    ## to define the variable locally with 'global' (like below).  If
    ## you only plan on reading the variable, there is no need to set
    ## the global definition (like with MAX_PAGES below)
    global CURRENT_PAGE
    ## DEBUG: print "A: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    CURRENT_PAGE += 1
    next_link = None
    ## NOTE: check to see if there are more links to follow
    if MAX_PAGES == CURRENT_PAGE:
        next_link = None
    else:
        for links in root.cssselect('li.next a'):
            next_link = "%s%s" % (BASE_URL, links.get('href'))

    print "B: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    return next_link


## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    print 'scraping: '+url
    next_url = scrape_table(url)

    if next_url:
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = "%s%s" % (BASE_URL,FIRST_EXT)
## DEBUG: make sure I found the page
print "I SEE URL: %s" % starting_url

root = get_root('http://www.blocket.se/varmland/BMW_116_Privatleasing_Nya_BMW_1_serien_Fran_3_36478675.htm?ca=14&w=3')
get_item(root, 'cssselect1', 'cssselect2')

scrape_and_look_for_next_link(starting_url)
##############################################################################
# MI Interpreters - the Python Version
#
# This script starts on the first page and then
# scrapes it and all subsequent pages by calling
# 'scrape_and_look_for_next_link' over and over
# again.
#
###############################################################################
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments

## NOTE: required before any other code (comments not included)
import scraperwiki
import lxml.html
from lxml import etree
from datetime import datetime
import time
import os, base64
import string

## YOU_SHOULD_KNOW: this is where you put your target url(s)
BASE_URL  = 'http://www.blocket.se'
FIRST_EXT = '/mi/interpreters?g=MI'
FIRST_EXT = '/hela_sverige/bilar?q=volvo&cg=1020&st=s&l=0&ca=11&w=3&f=a&o=1'
FIRST_EXT = '/hela_sverige/bilar?cg=1020&st=s&l=0&ca=11&w=3&sp=1&f=a&o=1'
FIRST_EXT = '/hela_sverige/bilar?ca=4&s=1&w=3&cg=1020&cb=3'
FIRST_EXT = '/hela_sverige/bilar?cg=1020&st=s&l=0&cb=3&ca=14&w=3&sp=1&f=a&o=1'
#FIRST_EXT = '/kristianstad/Bmw_525_96a_38787774.htm?ca=4&w=3'
MAX_PAGES    = 0  ## set to 0 for unlimited
CURRENT_PAGE = 0  ## keeps track of current page

COUNTER = 0
ITEM_URL = ""
ITEM_TITLE = ""
ITEM_DATA = ""
ITEM_PRICE = ''
ITEM_BODY = ""
ITEM_MODELLYEAR = ""
ITEM_GEAR =""
ITEM_MILEAGE =""
ITEM_MANUFACTUREYEAR = ""
ITEM_FUEL =""
ITEM_BRAND =""

keywords = {
    'ITEM_PRICE' : 'Pris',
    'ITEM_MODELYEAR' : u'Modell\xe5r',
    'ITEM_GEAR' : u'V\xe4xell\xe5da',
    'ITEM_MILEAGE' : 'Miltal',
    'ITEM_MANUFACTURERYEAR' : u'Tillverknings\xe5r',
    'ITEM_FUEL' : u'Br\xe4nsle',
    'ITEM_BRAND' : u'M\xe4rke',
    'ITEM_MODEL' : 'Modell',
}

item_data = {
    'ITEM_URL' : '',
    'ITEM_TITLE' : '',
    'ITEM_PRICE' : '',
    'ITEM_MODELYEAR' : '',
    'ITEM_GEAR' : '',
    'ITEM_MILEAGE' : '',
    'ITEM_MANUFACTURERYEAR' : '',
    'ITEM_FUEL' : '',
    'ITEM_BRAND' : '',
    'ITEM_MODEL' : '',
}

## NOTE: the intermediate function "check_data()" was required because
## not all the fields are filled for all businesses and I was getting
## errors when trying to add the data.
def check_data(data):
    if len(data) > 0:
        ## NOTE: pull out first element, get its text, remove end whitespace
        ## and then remove trailing ',' if it exists (like on addresses)
        return data[0].text_content().rstrip().rstrip(',')
    else:
        ## NOTE: otherwise, return 'n/a'
        return "n/a"


#def scrape_item_data(root, cssselect, string):
    #item = td.text_content()

def get_root(page_url):
    print "fn: get_root "
    page = scraperwiki.scrape(page_url)
    return lxml.html.fromstring(page)

def get_item(root, cssselect1, cssselect2):
    print "fn: get_item "
    count = 0
    for y in root.cssselect('.breadcrumb_top_container'):
        ITEM_DATA = y.cssselect('a')
        print "bread", ITEM_DATA

        for j in ITEM_DATA:
            count +=1
            item = j.text_content()
            brandlist = [['BMW',2], ['Volvo',2],['Volkswagen',2]]
            for bl in brandlist:
                if bl[0] in item:
                    #print "BMW!"
                    #print "get_item -> item: ", item
                    print "get_item -> brand: ", bl[0]
                    if bl[1]>1:
                        print "get_item -> model:"
                            

    for x in root.cssselect('.details'):
        # 'strong' contains all car specific data 
        # Extract all 'strong' elements
        #ITEM_DATA = x.cssselect('strong')
        ITEM_DATA = x.cssselect('td')

        #print ITEM_DATA
        for i in ITEM_DATA:
            count +=1
            item = i.text_content()
            if 'Pris' in item: 
                price = item[7:]
                print "PRICE!"
                #print "get_item -> item: ", item
                print "get_item -> price: ", price

            elif u'Modell\xe5r' in item:
                modelyear = item[11:16]
                print "MODEL YEAR!"
                #print "get_item -> item: ", item
                print "get_item -> modelyear: ", modelyear

            elif u'V\xe4xell\xe5da' in item:
                gearbox = item[12:]
                print "GEARBOX!"
                #print "get_item -> item: ", item
                print "get_item -> gearbox: ", gearbox

            elif u'Miltal' in item:
                milage = item[9:]
                print "MILAGE!"
                #print "get_item -> item: ", item
                print "get_item -> milage: ", milage

            elif u'Br\xe4nsle' in item:
                fuel = item[9:]
                print "FUEL!"
                #print "get_item -> item: ", item
                print "get_item -> fuel: ", fuel


            elif u'Tillverknings\xe5r' in item:
                manufacturingyear = item[18:]
                print "MANUFACTURINGYEAR!"
                #print "get_item -> item: ", item
                print "get_item -> manufacturingyear: ", manufacturingyear

    print "fn: get_item: END...%d" % count
           # if item.find(keywords.get('ITEM_PRICE')):
           #     keywords['ITEM_MODELYEAR']= item
           #     print "keywords ITEM = item: ", item

def scrape_item(page_url):
    ## NOTE: first, scrape the page
    global COUNTER
    COUNTER += 1
    page = scraperwiki.scrape(page_url)
    print page_url
    root = lxml.html.fromstring(page)


    for x in root.cssselect('.details'):
        global ITEM_DATA, ITEM_BODY, ITEM_PRICE
        ITEM_DATA = check_data(x.cssselect('.params.underlined_links'))
        ITEM_BODY = check_data(x.cssselect('.body'))

        #print "TEST", x.cssselect('.params.underlined_links')
        #for td in x.cssselect('.tbody'):
        #    print "td", td
        ITEM_DATA = x.cssselect('td')
        #test = x.cssselect('td').text.content()
        
        #print "item_price:", ITEM_PRICE.text.content()
        count = 0
        for td in ITEM_DATA:
            
            pris = u'Pris:'
            year = u'Modellår' ### detta måste fixas!!!!!
            gearbox = u'Växellåda'
            mileage = u'Miltal:'
            madeyear = u'Tillverkningsår'
            fuel = u'Bränsle:'
            
            brand = u'Märke:'
            model = u'Modell:'

            item = td.text_content()

#            if ages.has_key('Sue'):
#                    print "Sue is in the dictionary. She is", ages['Sue'], "years old"
#                else:
#                    print "Sue is not in the dictionary"
            #print ">>>> ITEM >>", item
            # Iterate over dict keys values
            count += 1
            #print "Keywords ->", keywords.get('ITEM_MODELYEAR')
            if item.find(keywords.get('ITEM_MODELYEAR')):
                #print "T-år 1: %s " % (count)
                keywords['ITEM_MODELYEAR']= item


            
## NOTE: scrape_table function gets passed an individual page to scrape
def scrape_table(page_url):

    ## NOTE: first, scrape the page
    page = scraperwiki.scrape(page_url)

    ## NOTE: next, parse the scraped page
    root = lxml.html.fromstring(page)

    

    ## NOTE: loop through each listing block delimited by 'div="desc"'
    for x in root.cssselect('.desc'):
        ## DEBUG: make sure we are seeing the correct data
        #print "SEE %s" % x
        #desc = check_data(x.cssselect('.desc'))
        #ITEM_TITLE = check_data(x.cssselect('.desc'))
        
        ITEM_TITLE = check_data(x.cssselect('.item_link'))
        for link in x.cssselect('a'):
            #link_text_content = link.text_content()
            ITEM_URL = link.get('href')
        list_price = check_data(x.cssselect('.list_price'))
        
        scrape_item(ITEM_URL)

        print "ITEM URL......... %s" % ITEM_URL
        print "ITEM_TITLE....... %s" % ITEM_TITLE
        print "LIST_PRICE....... %s" % list_price
        print "ITEM BODY........ %s" % ITEM_BODY
        print "*** NEW ITEM ***"


        ## NOTE: the intermediate function "check_data()" was required because
        ## not all the fields are filled for all businesses and I was getting
        ## errors when trying to add the data.

        UNIQ_ID = base64.b64encode(os.urandom(8))
        print "ID", UNIQ_ID[:-2]

        data = {
        # 'ID' : UNIQ_ID,
          'URL' : ITEM_URL,
          'TITLE' : ITEM_TITLE,
          'PRICE' : ITEM_PRICE,
          'DATA' : ITEM_DATA,
          'BODY' : ITEM_BODY,

        }
        scraperwiki.sqlite.save(unique_keys=['URL'], data=data)

## root = lxml.html.fromstring(html)
## for tr in root.cssselect("div[align='left'] tr.tcont"):
##     tds = tr.cssselect("td")
##     data = {
##       'country' : tds[0].text_content(),
##       'years_in_school' : int(tds[4].text_content())
##     }
##     print data


# <div align="left">
#   <table align="left" cellpadding="0" cellspacing="0">
#     <tbody>
#       <tr class="bar1">
#       <tr>
#         <tr bgcolor="#bce6f8">
#           <tr class="lheader">
#             <tr class="tcont">
#               <td height="19">Afghanistan</td>
#               <td height="19" align="right">2004</td>


    ## YOU_SHOULD_KNOW: if you would like to a global variable, be sure
    ## to define the variable locally with 'global' (like below).  If
    ## you only plan on reading the variable, there is no need to set
    ## the global definition (like with MAX_PAGES below)
    global CURRENT_PAGE
    ## DEBUG: print "A: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    CURRENT_PAGE += 1
    next_link = None
    ## NOTE: check to see if there are more links to follow
    if MAX_PAGES == CURRENT_PAGE:
        next_link = None
    else:
        for links in root.cssselect('li.next a'):
            next_link = "%s%s" % (BASE_URL, links.get('href'))

    print "B: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    return next_link


## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    print 'scraping: '+url
    next_url = scrape_table(url)

    if next_url:
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = "%s%s" % (BASE_URL,FIRST_EXT)
## DEBUG: make sure I found the page
print "I SEE URL: %s" % starting_url

root = get_root('http://www.blocket.se/varmland/BMW_116_Privatleasing_Nya_BMW_1_serien_Fran_3_36478675.htm?ca=14&w=3')
get_item(root, 'cssselect1', 'cssselect2')

scrape_and_look_for_next_link(starting_url)
