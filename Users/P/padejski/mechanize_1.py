###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

lotterygrantsurl = "http://pretraga2.apr.gov.rs/ObjedinjenePretrage/Search/Search"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(nr=0)
print br.form


br["SearchByRegistryCodeString"] ="1"
br["SelectedRegisterId"] = ""
#br["SearchByNameString"]  = "ana"


response = br.submit()
print response.read()


