# data is from:  
    #2011:  TBC
    #2010: http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/released-documents/041-releases-2010
    #2009: http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/released-documents/042-releases-2009
    #2008: http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/released-documents/043-releases-2008
    #2007: http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/released-documents/044-releases-2007

# each page contains a number of repeating H1 elements:

#Need to 
#  (1) open each page 
#  (2) scrape the page with all FOI releases in it
#  (3) save to data store.

       
import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer



# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'http://www.fco.gov.uk/en/publications-and-documents/freedom-of-information/released-documents/041-releases-2010'
starting_url = base_url # + 'xxxxx.htm'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#(1) open the page
br.open(starting_url)

#debug:
print "1"

#get HTML:
html = br.response().read()


#debug:
print "2"

#parse only the <h4> tags
h4s = SoupStrainer('h4')

# create a list
h4_tags = [tag for tag in BeautifulSoup(html, parseOnlyThese=h4s)]

# debug: show all the p_tags lines
for line in h4_tags :
    print( line )


