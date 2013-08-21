import mechanize
import scraperwiki
import re


regex = re.compile(".*XMLLoc=(.+).xml")
starturl = 'http://www.islington.gov.uk/Northgate/Online/EGov/License_Registers/Registers_Criteria.aspx'

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open(starturl)
response = br.response().read()
br.select_form(nr=0) 
br.form.set_all_readonly(False)
control = br.form.find_control("ddLiceType")
control.value = ["LPRE"] #license type LPRE, use LTEN for temporary notices
response = br.submit()
html = response.read()
xml = regex.findall(html)
xmlfile= "http://www.islington.gov.uk" + xml[0] + ".xml"
xmlcontent = scraperwiki.scrape(xmlfile)

print xmlcontent