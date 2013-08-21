import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Administrative_Divisions/Area_of_India.aspx"

response= urlopen(uri)
print response.read()
#forms = ParseResponse(response, backwards_compat=False)

#form = forms[0]
#print(form)
#form.find_control("rdbState").items[0].selected = True
#content=urlopen(form.click())
#forms=ParseResponse(content, backwards_compat=False)
#form=forms[0]
#print(form)
