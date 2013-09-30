import scraperwiki

# Blank Python

#https://www.stswr.ca/Eligibility.aspx?Page=School

import mechanize
import cookielib
import lxml.html

# Browser
br = mechanize.Browser()

r = br.open ('https://www.stswr.ca/Eligibility.aspx?Page=School')

#show available forms 
for f in br.forms():
    print f

br.select_form(name="aspnetForm")
print br.form

#br["ctl00$CPHPageBody$streetNum"] = ["73"]
#br["ctl00$CPHPageBody$streetName"] = ["ARLINGTON BLVD"]
#br["ctl00$CPHPageBody$dlMunicipality"] = ["KITCHENER"]
#br["ctl00$CPHPageBody$dlDistrict"] = ["WRDSB"]
#sUBMIT IT 

#br.submit()
#print br.response().read()

#<TextControl(ctl00$CPHPageBody$streetNum=)>
 # <TextControl(ctl00$CPHPageBody$streetName=)>
 # <SelectControl(ctl00$CPHPageBody$dlMunicipality=
#<SelectControl(ctl00$CPHPageBody$dlDistrict=[*, PROV WRDSB, WCDSB, WRDSB, PROV WCDSB])>



import scraperwiki

# Blank Python

#https://www.stswr.ca/Eligibility.aspx?Page=School

import mechanize
import cookielib
import lxml.html

# Browser
br = mechanize.Browser()

r = br.open ('https://www.stswr.ca/Eligibility.aspx?Page=School')

#show available forms 
for f in br.forms():
    print f

br.select_form(name="aspnetForm")
print br.form

#br["ctl00$CPHPageBody$streetNum"] = ["73"]
#br["ctl00$CPHPageBody$streetName"] = ["ARLINGTON BLVD"]
#br["ctl00$CPHPageBody$dlMunicipality"] = ["KITCHENER"]
#br["ctl00$CPHPageBody$dlDistrict"] = ["WRDSB"]
#sUBMIT IT 

#br.submit()
#print br.response().read()

#<TextControl(ctl00$CPHPageBody$streetNum=)>
 # <TextControl(ctl00$CPHPageBody$streetName=)>
 # <SelectControl(ctl00$CPHPageBody$dlMunicipality=
#<SelectControl(ctl00$CPHPageBody$dlDistrict=[*, PROV WRDSB, WCDSB, WRDSB, PROV WCDSB])>



