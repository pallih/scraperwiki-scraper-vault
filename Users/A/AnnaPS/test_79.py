# Blank Python
import mechanize
from lxml.html import fromstring, parse, fragments_fromstring
from lxml import etree
from BeautifulSoup import BeautifulSoup



canonical_url = "http://www.islington.gov.uk/Northgate/Online/EGov/License_Registers/StdDetails.aspx?PT=&TYPE=LicenceRegistersFullDetailsPK&PARAM0='LN/000002950'&PARAM1=0&XSLT=/Northgate/SiteFiles/Skins/Islington//xslt/Licensing/LicenceRegistersDetails.xsl&FT=LicenceDetails&LAYOUT=UE&DAURI=EGov"
 
normal_url = 'http://www.islington.gov.uk'

br = mechanize.Browser()
br.set_handle_robots(False)   
br.set_handle_refresh(False) 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(canonical_url)
response_string = response.read()
print response_string
#doc = fragments_fromstring(response.read())
#doc = parse(response)
#print doc
#etree.tostring(doc)
soup = BeautifulSoup(response_string)
print soup.find("ul", { "class" : "list" })