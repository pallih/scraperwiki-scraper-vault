import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

import mechanize 

url = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

br.select_form("aspnetForm")
br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link

