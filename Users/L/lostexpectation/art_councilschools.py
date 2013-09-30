import re
import mechanize

br = mechanize.Browser()
br.open("http://www.artscouncil.ie/en/we_funded.aspx")
# follow second link with element text matching regular expression
response1 = br.follow_link(text_regex=r"cheese\s*shop", nr=1)
assert br.viewing_html()
print br.title()
print response1.geturl()
print response1.info()  # headers
print response1.read()  # body

br.select_form(name="order")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm.
br["cheeses"] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()

# print currently selected form (don't call .submit() on this, use br.submit())
print br.form

response3 = br.back()  # back to cheese shop (same data as response1)
# the history mechanism returns cached response objects
# we can still use the response, even though it was .close()d
response3.get_data()  # like .seek(0) followed by .read()
response4 = br.reload()  # fetches from server

for form in br.forms():
    print form
# .links() optionally accepts the keyword args of .follow_/.find_link()
for link in br.links(url_regex="python.org"):
    print link
    br.follow_link(link)  # takes EITHER Link instance OR keyword args
    br.back()
import re
import mechanize

br = mechanize.Browser()
br.open("http://www.artscouncil.ie/en/we_funded.aspx")
# follow second link with element text matching regular expression
response1 = br.follow_link(text_regex=r"cheese\s*shop", nr=1)
assert br.viewing_html()
print br.title()
print response1.geturl()
print response1.info()  # headers
print response1.read()  # body

br.select_form(name="order")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm.
br["cheeses"] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()

# print currently selected form (don't call .submit() on this, use br.submit())
print br.form

response3 = br.back()  # back to cheese shop (same data as response1)
# the history mechanism returns cached response objects
# we can still use the response, even though it was .close()d
response3.get_data()  # like .seek(0) followed by .read()
response4 = br.reload()  # fetches from server

for form in br.forms():
    print form
# .links() optionally accepts the keyword args of .follow_/.find_link()
for link in br.links(url_regex="python.org"):
    print link
    br.follow_link(link)  # takes EITHER Link instance OR keyword args
    br.back()
import re
import mechanize

br = mechanize.Browser()
br.open("http://www.artscouncil.ie/en/we_funded.aspx")
# follow second link with element text matching regular expression
response1 = br.follow_link(text_regex=r"cheese\s*shop", nr=1)
assert br.viewing_html()
print br.title()
print response1.geturl()
print response1.info()  # headers
print response1.read()  # body

br.select_form(name="order")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm.
br["cheeses"] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()

# print currently selected form (don't call .submit() on this, use br.submit())
print br.form

response3 = br.back()  # back to cheese shop (same data as response1)
# the history mechanism returns cached response objects
# we can still use the response, even though it was .close()d
response3.get_data()  # like .seek(0) followed by .read()
response4 = br.reload()  # fetches from server

for form in br.forms():
    print form
# .links() optionally accepts the keyword args of .follow_/.find_link()
for link in br.links(url_regex="python.org"):
    print link
    br.follow_link(link)  # takes EITHER Link instance OR keyword args
    br.back()
import re
import mechanize

br = mechanize.Browser()
br.open("http://www.artscouncil.ie/en/we_funded.aspx")
# follow second link with element text matching regular expression
response1 = br.follow_link(text_regex=r"cheese\s*shop", nr=1)
assert br.viewing_html()
print br.title()
print response1.geturl()
print response1.info()  # headers
print response1.read()  # body

br.select_form(name="order")
# Browser passes through unknown attributes (including methods)
# to the selected HTMLForm.
br["cheeses"] = ["mozzarella", "caerphilly"]  # (the method here is __setitem__)
# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()

# print currently selected form (don't call .submit() on this, use br.submit())
print br.form

response3 = br.back()  # back to cheese shop (same data as response1)
# the history mechanism returns cached response objects
# we can still use the response, even though it was .close()d
response3.get_data()  # like .seek(0) followed by .read()
response4 = br.reload()  # fetches from server

for form in br.forms():
    print form
# .links() optionally accepts the keyword args of .follow_/.find_link()
for link in br.links(url_regex="python.org"):
    print link
    br.follow_link(link)  # takes EITHER Link instance OR keyword args
    br.back()
