import scraperwiki
import mechanize
import lxml.html
from lxml.etree import tostring

#setup browser
br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


response = br.open('http://www.ait.gov.uk/Public/unreportedResults.aspx')

#do a search
br.form = list(br.forms())[0]
response = br.submit()

br.form = list(br.forms())[0]
br.set_all_readonly(False)
br["__EVENTTARGET"] = 'pager1'
br["__EVENTARGUMENT"] = '1'

response = br.submit()
print response.read()
