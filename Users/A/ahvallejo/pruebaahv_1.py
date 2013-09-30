###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 
import urllib
import urllib2
import urllib2, cookielib
from BeautifulSoup import BeautifulSoup

# set things up
jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)



# for letra in range(ord("n"),ord("y")+1):

#http://www.pmstudy.com/2011PMP/sim1/1ans.asp
pmiurl = "http://www.pmstudy.com/memberlogin.asp"
br = mechanize.Browser()
response = br.open(pmiurl)
#print "All forms:", [ form.name  for form in br.forms() ]
#page = br.post("http://www.pmstudy.com/verifylogin1.asp",{"payer_email" => "ahvallejohotmail.com","pass" => "hola1hola1"})
url = 'http://www.pmstudy.com/verifylogin1.asp'
values = {'payer_email' : 'ahvallejo@hotmail.com',
          'pass' : 'hola1hola1' }
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
#print "the login page is",the_page
inicio=100
for i in range(100):
    ansurl="http://www.pmstudy.com/2011PMP/sim4/"
    ansurl=ansurl + str(i+1+inicio) + "ans.asp"
    #print ansurl
    req = urllib2.Request(ansurl)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page)
    soup.prettify()
    #print "the page ",i+1+inicio,"is",the_page
    print soup
    data = { 'ans' : str(i+1+inicio), 'html' : soup }
    scraperwiki.sqlite.save(unique_keys=['ans'], data=data);

#print response.read()
#br.select_form(name="myform")
#print br.form
#print response.read()
#br["payer_email"] = "ahvallejo@hotmail.com"
#br["pass"] = "hola1hola1"
#response = br.submit()
#print page
#doc=lh.fromstring(response.read())
#print doc
#       scraperwiki.sqlite.save(unique_keys=['Indice'], data=data)

###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful Mechanize library. Documentation is here:
# http://wwwsearch.sourceforge.net/mechanize/
###############################################################################
import mechanize
import scraperwiki
import lxml.html as lh 
import urllib
import urllib2
import urllib2, cookielib
from BeautifulSoup import BeautifulSoup

# set things up
jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)



# for letra in range(ord("n"),ord("y")+1):

#http://www.pmstudy.com/2011PMP/sim1/1ans.asp
pmiurl = "http://www.pmstudy.com/memberlogin.asp"
br = mechanize.Browser()
response = br.open(pmiurl)
#print "All forms:", [ form.name  for form in br.forms() ]
#page = br.post("http://www.pmstudy.com/verifylogin1.asp",{"payer_email" => "ahvallejohotmail.com","pass" => "hola1hola1"})
url = 'http://www.pmstudy.com/verifylogin1.asp'
values = {'payer_email' : 'ahvallejo@hotmail.com',
          'pass' : 'hola1hola1' }
data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
#print "the login page is",the_page
inicio=100
for i in range(100):
    ansurl="http://www.pmstudy.com/2011PMP/sim4/"
    ansurl=ansurl + str(i+1+inicio) + "ans.asp"
    #print ansurl
    req = urllib2.Request(ansurl)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page)
    soup.prettify()
    #print "the page ",i+1+inicio,"is",the_page
    print soup
    data = { 'ans' : str(i+1+inicio), 'html' : soup }
    scraperwiki.sqlite.save(unique_keys=['ans'], data=data);

#print response.read()
#br.select_form(name="myform")
#print br.form
#print response.read()
#br["payer_email"] = "ahvallejo@hotmail.com"
#br["pass"] = "hola1hola1"
#response = br.submit()
#print page
#doc=lh.fromstring(response.read())
#print doc
#       scraperwiki.sqlite.save(unique_keys=['Indice'], data=data)

