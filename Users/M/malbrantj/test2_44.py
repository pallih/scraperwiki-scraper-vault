import scraperwiki
import re
import mechanize
import cookielib
import lxml.html
from bs4 import BeautifulSoup
from types import *

br = mechanize.Browser()
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open("http://es.investing.com/equities/tenaris-technical?cid=13302")
assert br.viewing_html()
print br.title()
#print response.read()
soup = BeautifulSoup(response)
price = soup.find(id="last_last")
print price.get_text()

indicadores = soup.find_all(id="open_0")
for indicador in indicadores:
    if type(indicador.get('class')) != NoneType:
        if indicador.get('class')[0] == 'right':
            print indicador.get_text()

indicador = soup.find(id="open_1")
print indicador.get_text()

indicador = soup.find(id="open_2")
print indicador.get_text()

indicador = soup.find(id="open_3")
print indicador.get_text()

indicador = soup.find(id="open_4")
print indicador.get_text()

indicador = soup.find(id="open_5")
print indicador.get_text()

indicador = soup.find(id="open_6")
print indicador.get_text()

indicador = soup.find(id="open_7")
print indicador.get_text()

indicador = soup.find(id="open_8")
print indicador.get_text()

indicador = soup.find(id="open_9")
print indicador.get_text()

indicador = soup.find(id="open_10")
print indicador.get_text()

#print(soup.prettify())

#el = root.cssselect("span#last_last strong")[0]           
#print el
#print el.text


#html = scraperwiki.scrape('http://es.investing.com/equities/tenaris?cid=13302')
#print htmlimport scraperwiki
import re
import mechanize
import cookielib
import lxml.html
from bs4 import BeautifulSoup
from types import *

br = mechanize.Browser()
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open("http://es.investing.com/equities/tenaris-technical?cid=13302")
assert br.viewing_html()
print br.title()
#print response.read()
soup = BeautifulSoup(response)
price = soup.find(id="last_last")
print price.get_text()

indicadores = soup.find_all(id="open_0")
for indicador in indicadores:
    if type(indicador.get('class')) != NoneType:
        if indicador.get('class')[0] == 'right':
            print indicador.get_text()

indicador = soup.find(id="open_1")
print indicador.get_text()

indicador = soup.find(id="open_2")
print indicador.get_text()

indicador = soup.find(id="open_3")
print indicador.get_text()

indicador = soup.find(id="open_4")
print indicador.get_text()

indicador = soup.find(id="open_5")
print indicador.get_text()

indicador = soup.find(id="open_6")
print indicador.get_text()

indicador = soup.find(id="open_7")
print indicador.get_text()

indicador = soup.find(id="open_8")
print indicador.get_text()

indicador = soup.find(id="open_9")
print indicador.get_text()

indicador = soup.find(id="open_10")
print indicador.get_text()

#print(soup.prettify())

#el = root.cssselect("span#last_last strong")[0]           
#print el
#print el.text


#html = scraperwiki.scrape('http://es.investing.com/equities/tenaris?cid=13302')
#print html