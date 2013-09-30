###############################################################################
#
# Scrape fun, cheap events from funcheapsf.com
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://sf.funcheap.com/category/event/top-pick/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
div = soup.find('div', {'id':'page'}) 
print div
div2 = div.find('div', {'class':'clearfloat'})
print div2
div3 = div2.find('div', {'class':'tanbox'})
print div3

#for dept_row in dept_rows[1:]:
#    cab_name = ''
    
    ###############################################################################
#
# Scrape fun, cheap events from funcheapsf.com
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://sf.funcheap.com/category/event/top-pick/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
div = soup.find('div', {'id':'page'}) 
print div
div2 = div.find('div', {'class':'clearfloat'})
print div2
div3 = div2.find('div', {'class':'tanbox'})
print div3

#for dept_row in dept_rows[1:]:
#    cab_name = ''
    
    