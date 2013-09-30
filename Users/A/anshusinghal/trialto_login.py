import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

#uri="http://wwwsearch.sourceforge.net/mechanize/example.html"
uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/CensusDataOnline_Login.aspx"
response= urlopen(uri)
print response.read()
#forms = ParseResponse(response, backwards_compat=False)
#print forms
#form = forms[0]
#print form
#form.set_value("singhal1", name="txtUserID", kind="text")
#form.set_value("Dreams@2012", name="txtPassword", kind="text")
#content=urlopen(form.click())
#print content.read()
#forms = ParseResponse(content, backwards_compat=False)
#print forms
#form=forms[0]
#print form
#forms = ParseResponse(response, backwards_compat=False)
#form = forms[0]
#print form
#form["comments"] = "Thanks, Gisle"
#print form
#form.set_value(["gouda"], name="cheeses", kind="list")

import scraperwiki
import lxml.html
from mechanize import ParseResponse, urlopen, urljoin

#uri="http://wwwsearch.sourceforge.net/mechanize/example.html"
uri="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/CensusDataOnline_Login.aspx"
response= urlopen(uri)
print response.read()
#forms = ParseResponse(response, backwards_compat=False)
#print forms
#form = forms[0]
#print form
#form.set_value("singhal1", name="txtUserID", kind="text")
#form.set_value("Dreams@2012", name="txtPassword", kind="text")
#content=urlopen(form.click())
#print content.read()
#forms = ParseResponse(content, backwards_compat=False)
#print forms
#form=forms[0]
#print form
#forms = ParseResponse(response, backwards_compat=False)
#form = forms[0]
#print form
#form["comments"] = "Thanks, Gisle"
#print form
#form.set_value(["gouda"], name="cheeses", kind="list")

