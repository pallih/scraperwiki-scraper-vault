###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
# Maybe use Outwit Hub to grab URLs first? Next doesn't work, but could just cycle through pages as it grabs URLs; then put in a list for PDF scraper

import mechanize 
import lxml.html

url = "http://fracfocus.ca/find_well/BC"

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

print response.read()

for form in br.forms():
    print "Form name:", form.name
    print form

br.form = list(br.forms())[0]
form.set_all_readonly(False) # allow changing the .value of all controls, lets me change page number to cycle through them

br["dropdown_region"] = ["Peace River North"] # selects Peace River North Region (think Gord said there are only any in Peace River)
br["page"] = "21" # selects Peace River North Region (think Gord said there are only any in Peace River)

response = br.submit()

html = response.read()

print html

root = lxml.html.fromstring(html)

oddrows = root.cssselect("tr.odd")
 
print 'Odd'

for tr in oddrows:
    link = tr.cssselect("a")[0]
    URL = link.attrib.get('href')
    print URL

evenrows = root.cssselect("tr.even")

print 'Even'

for tr in evenrows:
    link = tr.cssselect("a")[0]
    URL = link.attrib.get('href')
    print URL

#for link in br.links():
#    print link.text, link.url

