import mechanize 

url = "http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

# br.select_form("aspnetForm")
br.select_form("frmSearch")
# br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
br["pd_respondent"] = "GERMANY"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print linkimport mechanize 

url = "http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en"

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(url)

allforms = list(br.forms())
print "There are %d forms" % len(allforms)

for i, form in enumerate(allforms):
    print i, form.name, form

# br.select_form("aspnetForm")
br.select_form("frmSearch")
# br["ctl00$phMainContent$txtRecipientName"] = "Liverpool"
br["pd_respondent"] = "GERMANY"
response = br.submit()
print response.read()

alllinks = list(br.links())
for link in alllinks[:10]:
    print link