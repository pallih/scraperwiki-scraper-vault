import re
import mechanize
import lxml.html      

br = mechanize.Browser()
br.open("http://www.verkkokauppa.com/")
# follow second link with element text matching regular expression

assert br.viewing_html()
print br.title()


br.select_form("quicksearch")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm.

br["q"] = "macbook"  # (the method here is __setitem__)
# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()
print response2.geturl()
print response2.info()  # headers
html = response2.read()  # body

print html
         
root = lxml.html.fromstring(html)
print root
for div in root.cssselect("div.productList div.productRow div.pInfo div.prodId"):
    print div.text_content()import re
import mechanize
import lxml.html      

br = mechanize.Browser()
br.open("http://www.verkkokauppa.com/")
# follow second link with element text matching regular expression

assert br.viewing_html()
print br.title()


br.select_form("quicksearch")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm.

br["q"] = "macbook"  # (the method here is __setitem__)
# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()
print response2.geturl()
print response2.info()  # headers
html = response2.read()  # body

print html
         
root = lxml.html.fromstring(html)
print root
for div in root.cssselect("div.productList div.productRow div.pInfo div.prodId"):
    print div.text_content()