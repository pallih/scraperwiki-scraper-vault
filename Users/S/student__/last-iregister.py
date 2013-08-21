import scraperwiki
import mechanize
import re
import lxml.html  
# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://iregister.hpcsa.co.za/PractitionerView.aspx?FILENO='
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)
ind=0
for i in xrange(2000000000):
    p_url = url+str(i+1900000000)
    print p_url
    response = br.open(url)
    html = response.read()
    root = lxml.html.fromstring(html)
    for el in root.cssselect("span.ctl00_ContentPlaceHolder1_lblFullname"):
        print el.text_content()
        ind+=1
    if ind>100:
        break