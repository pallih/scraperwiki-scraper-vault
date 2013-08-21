###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here: 
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize 
import lxml.html

csurl = "https://secure.citysocialising.com/auth/login"

bws = mechanize.Browser()
response = bws.open(csurl)

print "All forms:", [ form.name  for form in bws.forms() ]

bws.select_form(nr=0)
print bws.form

bws["user_login_username"] = "a"
bws["user_login_password"] = "a"


response = bws.submit()
html = response.read()
print html
root = lxml.html.fromstring(html)
unameobj = root.cssselect("p.logout-buttons a")[0]
print unameobj.text