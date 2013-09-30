###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

lotterygrantsurl = "http://skanska.taleo.net/careersection/2/moresearch.ftl?lang=sv"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]
###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

lotterygrantsurl = "http://skanska.taleo.net/careersection/2/moresearch.ftl?lang=sv"

br = mechanize.Browser()
response = br.open(lotterygrantsurl)

print "All forms:", [ form.name  for form in br.forms() ]
