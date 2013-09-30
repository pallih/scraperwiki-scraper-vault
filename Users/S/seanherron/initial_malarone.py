###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

labels_proprietary_name_url = "http://labels.fda.gov/proprietaryname.cfm"

br = mechanize.Browser()
response = br.open(labels_proprietary_name_url)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(nr=1)
print br.form

br["searchfield"] = "Malarone"


response = br.submit()
print response.read()


###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

labels_proprietary_name_url = "http://labels.fda.gov/proprietaryname.cfm"

br = mechanize.Browser()
response = br.open(labels_proprietary_name_url)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(nr=1)
print br.form

br["searchfield"] = "Malarone"


response = br.submit()
print response.read()


###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

labels_proprietary_name_url = "http://labels.fda.gov/proprietaryname.cfm"

br = mechanize.Browser()
response = br.open(labels_proprietary_name_url)

print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(nr=1)
print br.form

br["searchfield"] = "Malarone"


response = br.submit()
print response.read()


