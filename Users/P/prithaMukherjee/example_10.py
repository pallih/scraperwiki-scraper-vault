from mechanize import ParseResponse, urlopen, urljoin

uri = "http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Online_Migration/By_Place_of_Birth.aspx"
response = urlopen(uri)
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
print form
form.set_value(["rdbState"], kind="singlelist", nr=0)
print urlopen(form.click()).read()

url1=urlopen(form.click())
print url1

form.set_value(["parmesan", "leicester", "cheddar"], name="cheeses")

