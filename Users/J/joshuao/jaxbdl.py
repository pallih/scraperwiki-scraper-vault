import scraperwiki

# Blank Python
import re
import mechanize
import lxml.html

html = scraperwiki.scrape("http://m.southwest.com")
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):  
    if el.text.find('Air Reservations') <> -1:
     print el.text     
     print el.get('href')
     bookair = el.get('href')
    

html = scraperwiki.scrape(bookair)
root = lxml.html.fromstring(html, )
for el in root.cssselect("a"):  
    if el.text.find('Book Air') <> -1:
     print el.text     
     print el.get('href')
     reserve = el.get('href')

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(reserve)
br.select_form(nr=0)
print br.title()
print br.geturl()

br["listboxtriptype"] = ["0"]  # (the method here is __setitem__)
br["listboxfrom"] = ["35"]
br["listboxto"] = ["31"]
br["listboxdepmon"] = ["6"]
br["listboxdepday"] = ["3"]

# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()
resp = response2.read()
print resp
p = re.compile('\$\d{1,3}')
min = 5000
for price in p.findall(resp):  
    if min > float(price.strip('$')):
     print float(price.strip('$'))
     min = float(price.strip('$'))

print min
import scraperwiki

# Blank Python
import re
import mechanize
import lxml.html

html = scraperwiki.scrape("http://m.southwest.com")
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):  
    if el.text.find('Air Reservations') <> -1:
     print el.text     
     print el.get('href')
     bookair = el.get('href')
    

html = scraperwiki.scrape(bookair)
root = lxml.html.fromstring(html, )
for el in root.cssselect("a"):  
    if el.text.find('Book Air') <> -1:
     print el.text     
     print el.get('href')
     reserve = el.get('href')

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(reserve)
br.select_form(nr=0)
print br.title()
print br.geturl()

br["listboxtriptype"] = ["0"]  # (the method here is __setitem__)
br["listboxfrom"] = ["35"]
br["listboxto"] = ["31"]
br["listboxdepmon"] = ["6"]
br["listboxdepday"] = ["3"]

# Submit current form.  Browser calls .close() on the current response on
# navigation, so this closes response1
response2 = br.submit()
resp = response2.read()
print resp
p = re.compile('\$\d{1,3}')
min = 5000
for price in p.findall(resp):  
    if min > float(price.strip('$')):
     print float(price.strip('$'))
     min = float(price.strip('$'))

print min
