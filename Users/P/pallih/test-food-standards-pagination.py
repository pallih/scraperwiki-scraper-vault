import scraperwiki
import mechanize
import lxml.html

url = 'http://ratings.food.gov.uk/QuickSearch.aspx?q=po30&lang=en-GB'
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(url)
response = br.response().read()
print 'First response: ', response
print
root = lxml.html.fromstring(response)
current_page = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxCurrentPage"]/.')
total_pages = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxPageCount"]/.')

print 'Total pages: ', total_pages[0].text
print 'Current page: ', current_page[0].text
print

for form in br.forms():
    print 'First form: ', form
    print

br.select_form(nr=0) #Select the first (and only) form - it has no name so we reference by number
br.form.set_all_readonly(False) # set readonly on values to false - if we want to change anything (it's unneccessary for this example)


#The form has 5 submit buttons - we want to submit the next one:
response = br.submit(name='ctl00$ContentPlaceHolder1$uxResults$uxNext').read()  #"Press" the next submit button

print 'Second response: ', response
for form in br.forms():
    print 'Second form: ', form
    print

root = lxml.html.fromstring(response)
current_page = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxCurrentPage"]/.')
total_pages = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxPageCount"]/.')

print 'Total pages: ', total_pages[0].text
print 'Current page: ', current_page[0].text

import scraperwiki
import mechanize
import lxml.html

url = 'http://ratings.food.gov.uk/QuickSearch.aspx?q=po30&lang=en-GB'
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(url)
response = br.response().read()
print 'First response: ', response
print
root = lxml.html.fromstring(response)
current_page = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxCurrentPage"]/.')
total_pages = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxPageCount"]/.')

print 'Total pages: ', total_pages[0].text
print 'Current page: ', current_page[0].text
print

for form in br.forms():
    print 'First form: ', form
    print

br.select_form(nr=0) #Select the first (and only) form - it has no name so we reference by number
br.form.set_all_readonly(False) # set readonly on values to false - if we want to change anything (it's unneccessary for this example)


#The form has 5 submit buttons - we want to submit the next one:
response = br.submit(name='ctl00$ContentPlaceHolder1$uxResults$uxNext').read()  #"Press" the next submit button

print 'Second response: ', response
for form in br.forms():
    print 'Second form: ', form
    print

root = lxml.html.fromstring(response)
current_page = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxCurrentPage"]/.')
total_pages = root.xpath ('//span[@id="ctl00_ContentPlaceHolder1_uxResults_uxPageCount"]/.')

print 'Total pages: ', total_pages[0].text
print 'Current page: ', current_page[0].text

