# Blank Python
import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'divdata'
    #there's more than one div, so we need to specify the class="Data", represented by the full stop
    divdata = root.cssselect("div.Data")
    for pars in divdata:
        #Create a new empty record
        record = {}
        #Assign the contents of <td> to a new object called 'table_cells'
        lines = pars.cssselect("p")
        spans = pars.cssselect("p span")
        #If there's anything
#TO ADD: AN ELSE TO ADDRESS DATE/URLCODE WHICH ARE 'OUT OF RANGE' ON SOME PAGES        
        if lines:
            #Put the contents of the first <p> into a record in the column 'pubdate'
            record['pubdate'] = spans[0].text
            record['noticecode'] = spans[1].text
            record['name'] = spans[3].text
            record['company number'] = spans[4].text
            record['trading as'] = spans[5].text
            record['nature of business'] = spans[6].text 
            record['trade classification'] = spans[7].text 
            record['date of appointment'] = spans[8].text
            record['adminstrator details'] = lines[11].text
            record['court'] = spans[2].text
#           record['date'] = lines[13].text
#           record['urlcode'] = lines[14].text
            record['ID'] = item
            print record, '------------'
            #Save in the SQLite database, with the ID code to be used as the unique reference
            scraperwiki.sqlite.save(["ID"], record)
        

#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://www.london-gazette.co.uk/issues/'
#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes =['60049/notices/1522342', '60100/notices/1559415', '59795/notices/1367954', '59823/notices/1381261']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)




