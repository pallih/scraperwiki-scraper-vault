import scraperwiki

import mechanize
br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
url = "http://www.independer.nl/autoverzekering/selecteerdekking.aspx"

response = br.open(url)
print response.read()
for form in br.forms():
    print "Form name:", form.name
    print form
br.select_form("aspnetForm")

for control in br.form.controls:
    print control
    print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
    
br["ctl00$MainContent$qqControl$selectCar$txtKenteken"] = "76-FT-SX"
br["ctl00$MainContent$qqControl$postcodeTextbox"] = "1095 CH"
br["ctl00$MainContent$qqControl$geboortedatumTextbox"] = "31-08-1986"
br["ctl00$MainContent$qqControl$schadevrijejarenTextbox"] = "5"
br["ctl00$MainContent$qqControl$svjHulp$jarenVerzekerdTextbox"]="5"
br["ctl00$MainContent$qqControl$selectCar$radioLicense"]='licenseUnknownRadio'
