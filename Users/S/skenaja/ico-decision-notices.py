###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer


#Need to 
#  (1) open the DN page 
#  (2) Submit the form with all form parameters as per default values 
#  (3) scrape the next page with all DNs in it
#  (4) iterate through the results & save to data store.




        
# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------


base_url = 'http://www.ico.gov.uk/tools_and_resources/'
starting_url = base_url + 'decision_notices.aspx'
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#(1) open the page
br.open(starting_url)

# Show the available forms
#for f in br.forms():
#    print f

br.select_form(nr=0)

#(2) click the DN Search button:
req = br.click(type="submit", nr=2)
br.open(req)

#debug:
print "1"

#get results of DN search:
html = br.response().read()

#debug:
print "2"

#parse only the <p> tags
paragraphs = SoupStrainer('p')

# create a list
p_tags = [tag for tag in BeautifulSoup(html, parseOnlyThese=paragraphs)]

#need only the ones matching <p><strong>... (p_tags(nr=4) onwards)
# should be able to extract the relevant data with a regex

# debug: show all the p_tags lines
for line in p_tags :
    print( line )

    
#soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
#tds = soup.findAll('p') # get all the <td> tags
#for td in tds:
#    print td # the full HTML tag
#    print td.text # just the text inside the HTML tag

# start scraping
# DNs are just after <a name="dn"></a>
# they finish before <div class="hr" style="margin-top: 2em;"><hr></div>
# <p><strong>Case Ref: FS50069396</strong>
# <br><strong>Date: 01/03/2006</strong>
# <br><strong>Public Authority: Cyngor Cymuned Llandysul</strong>
# <br><strong>Summary:</strong> The complainant requested the sight ...
# <br><strong>Section of Act/EIR &amp; Finding:</strong> FOI 11 - Complaint Upheld    
# <br><a href="/upload/documents/decisionnotices/2006/decision_notice_69396d.pdf" target="_blank" title="Link opens in new window">View PDF of Decision Notice FS50069396</a></p>
# [repeats <p>]


