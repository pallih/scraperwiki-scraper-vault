import scraperwiki           
from BeautifulSoup import BeautifulSoup, SoupStrainer
import mechanize
import re
import time

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#This is the part of the URL which all our pages share
base_url = 'http://www.quine.org/zip-all-'

#And these are the numbers which we need to complete that URL to make each individual URL
zips_range = ['00001','01000','04700','06400','10000','12500','15000','17500','20000','22000','25000','28000','30000','33000','36500','40000','42500','45000','47500','50000','54000','56000','60000','63000','67000','70000','73000','77000','80000','85000','90000','94000','97000']

#go through the zips_range list above, and for each ID...
for item in zips_range:
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item+'.html'
    # print next_link
    #(1) open the page
    time.sleep(1) #will sleep for 1 second
    br.open(next_link)


    #get HTML:
    html = br.response().read()

    #parse only the <p> tags
    ps = SoupStrainer('p[3]')

    # create a list
    p_tags = [tag for tag in BeautifulSoup(html, parseOnlyThese=ps)]

    # debug: show all the p_tags lines
    for line in p_tags :
        print( line )
import scraperwiki           
from BeautifulSoup import BeautifulSoup, SoupStrainer
import mechanize
import re
import time

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#This is the part of the URL which all our pages share
base_url = 'http://www.quine.org/zip-all-'

#And these are the numbers which we need to complete that URL to make each individual URL
zips_range = ['00001','01000','04700','06400','10000','12500','15000','17500','20000','22000','25000','28000','30000','33000','36500','40000','42500','45000','47500','50000','54000','56000','60000','63000','67000','70000','73000','77000','80000','85000','90000','94000','97000']

#go through the zips_range list above, and for each ID...
for item in zips_range:
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item+'.html'
    # print next_link
    #(1) open the page
    time.sleep(1) #will sleep for 1 second
    br.open(next_link)


    #get HTML:
    html = br.response().read()

    #parse only the <p> tags
    ps = SoupStrainer('p[3]')

    # create a list
    p_tags = [tag for tag in BeautifulSoup(html, parseOnlyThese=ps)]

    # debug: show all the p_tags lines
    for line in p_tags :
        print( line )
