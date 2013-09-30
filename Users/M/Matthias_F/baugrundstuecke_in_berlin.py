import scraperwiki
import urllib
import lxml.html
import urlparse
import mechanize
import cookielib
import urllib2

#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

url = "http://fbinter.stadt-berlin.de/blm/index.jsp?loginkey=sachdaten"
br = mechanize.Browser()
html = br.open(url).read()
print html
print list(br.forms())
root = lxml.html.fromstring(html)
frame = root.cssselect("frame")[0]
print lxml.html.tostring(frame)
urlf = urlparse.urljoin(url, frame.attrib.get("src")+"&java=false")
print urlf
htmlf = br.open(urlf).read()
print htmlf
br.form = list(br.forms())[0]
htmlr = br.submit().read()
print htmlr
br.select_form("Sachdatenfilter")
htmlt = br.submit(name="uebernehmen").read()
#print htmlt
root = lxml.html.fromstring(htmlt)
rows = root.cssselect("table.map_tabelle tr")
headers = [ td.text  for td in rows[0] ]
print headers
#assert headers == 
#[u'Baufl\xe4chennummer', 'Bezirk', u'Stra\xdfe', u'Flurst\xfccksnummer', u'Gr\xf6\xdfe Baufl\xe4che ges.\n      in qm', u'Gr\xf6\xdfe\n      Flurst\xfcck ges. in qm']
headers = ['Bauflaechennummer', 'Bezirk', 'Strasse', 'Flurstuecksnummer', 'Groesse Bauflaeche ges in qm', 'Groesse Flurstueck ges in qm']
print headers
for row in rows[1:]:
    drow = [ td.text for td in row ]
    drow[0] = row[0][0].text
    data = dict(zip(headers, drow))
    scraperwiki.sqlite.save(["Flurstuecksnummer"], data)
    #print data
import scraperwiki
import urllib
import lxml.html
import urlparse
import mechanize
import cookielib
import urllib2

#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

url = "http://fbinter.stadt-berlin.de/blm/index.jsp?loginkey=sachdaten"
br = mechanize.Browser()
html = br.open(url).read()
print html
print list(br.forms())
root = lxml.html.fromstring(html)
frame = root.cssselect("frame")[0]
print lxml.html.tostring(frame)
urlf = urlparse.urljoin(url, frame.attrib.get("src")+"&java=false")
print urlf
htmlf = br.open(urlf).read()
print htmlf
br.form = list(br.forms())[0]
htmlr = br.submit().read()
print htmlr
br.select_form("Sachdatenfilter")
htmlt = br.submit(name="uebernehmen").read()
#print htmlt
root = lxml.html.fromstring(htmlt)
rows = root.cssselect("table.map_tabelle tr")
headers = [ td.text  for td in rows[0] ]
print headers
#assert headers == 
#[u'Baufl\xe4chennummer', 'Bezirk', u'Stra\xdfe', u'Flurst\xfccksnummer', u'Gr\xf6\xdfe Baufl\xe4che ges.\n      in qm', u'Gr\xf6\xdfe\n      Flurst\xfcck ges. in qm']
headers = ['Bauflaechennummer', 'Bezirk', 'Strasse', 'Flurstuecksnummer', 'Groesse Bauflaeche ges in qm', 'Groesse Flurstueck ges in qm']
print headers
for row in rows[1:]:
    drow = [ td.text for td in row ]
    drow[0] = row[0][0].text
    data = dict(zip(headers, drow))
    scraperwiki.sqlite.save(["Flurstuecksnummer"], data)
    #print data
