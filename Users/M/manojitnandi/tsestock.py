import scraperwiki
import mechanize
import re
from bs4 import BeautifulSoup
# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://www.tse.ir/en/stats.aspx'
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

response = br.open(url)
list_forms = [ form for form in br.forms() ]
br.select_form(nr=0)

br['_ctl0:mainContent:Date4']='20080620'
br['_ctl0:mainContent:Date5']='20120625'

response = br.submit()
soup = BeautifulSoup(response)
print soup.prettify()

