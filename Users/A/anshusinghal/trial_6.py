import sys

from mechanize import ParseResponse, urlopen, urljoin

#if len(sys.argv) == 1:
uri = "http://wwwsearch.sourceforge.net/"
#else:
#    uri = sys.argv[1]

response = urlopen(urljoin(uri, "mechanize/example.html"))
forms = ParseResponse(response, backwards_compat=False)
form = forms[0]
print form
form["comments"] = "Thanks, Gisle"
form.set_value(["spam"], kind="singlelist", nr=0)

# form.click() returns a mechanize.Request object
# (see HTMLForm.click.__doc__ if you want to use only the forms support, and
# not the rest of mechanize)
#print urlopen().read()

control = form.find_control("cheeses", type="select")
print control.name, control.value, control.type
control.value = ["mascarpone", "curd"]
# ...and the Item instances from inside the Control
item = control.get("curd")
print item.name, item.selected, item.id, item.attrs
item.selected = False

a=form.set_value(["leicester" ], name="favorite_cheese")
print form
