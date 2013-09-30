import scraperwiki
import mechanize
import urllib
import lxml.html           

cookies = mechanize.CookieJar()
minint_admin_url = "http://amministratori.interno.it/amministratori/ServletVisualxCom3"

opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                     ("Referer", "http://amministratori.interno.it/amministratori/ServletVisualxCom2")]


data = urllib.urlencode({'comune': '06/06/2011*AGRIGENTO*0400*5880*SCIACCA',
                       'SubmitE': 'Conferma Ente'}) 
resp = opener.open(minint_admin_url, data)

root = lxml.html.fromstring(resp.read())
tables = root.cssselect("div#datiente table")

t_giunta = tables[0]
for tr in t_giunta.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) > 0:
        last_name_link = tds[0].cssselect("a")[0]
        data = {
          'institution_type': 'giunta',
          'politician_link': last_name_link.get('href'),
          'last_name' : tds[0].text_content(),
          'first_name' : tds[1].text_content(),
          'charge' : tds[2].text_content(),
          'party' : tds[3].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['politician_link'], data=data)
        print data

t_consiglio = tables[1]
for tr in t_consiglio.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) > 0:
        last_name_link = tds[0].cssselect("a")[0]
        data = {
          'institution_type': 'consiglio',
          'politician_link': last_name_link.get('href'),
          'last_name' : tds[0].text_content(),
          'first_name' : tds[1].text_content(),
          'charge' : tds[2].text_content(),
          'party' : tds[3].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['politician_link'], data=data)
        print data

import scraperwiki
import mechanize
import urllib
import lxml.html           

cookies = mechanize.CookieJar()
minint_admin_url = "http://amministratori.interno.it/amministratori/ServletVisualxCom3"

opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                     ("Referer", "http://amministratori.interno.it/amministratori/ServletVisualxCom2")]


data = urllib.urlencode({'comune': '06/06/2011*AGRIGENTO*0400*5880*SCIACCA',
                       'SubmitE': 'Conferma Ente'}) 
resp = opener.open(minint_admin_url, data)

root = lxml.html.fromstring(resp.read())
tables = root.cssselect("div#datiente table")

t_giunta = tables[0]
for tr in t_giunta.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) > 0:
        last_name_link = tds[0].cssselect("a")[0]
        data = {
          'institution_type': 'giunta',
          'politician_link': last_name_link.get('href'),
          'last_name' : tds[0].text_content(),
          'first_name' : tds[1].text_content(),
          'charge' : tds[2].text_content(),
          'party' : tds[3].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['politician_link'], data=data)
        print data

t_consiglio = tables[1]
for tr in t_consiglio.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) > 0:
        last_name_link = tds[0].cssselect("a")[0]
        data = {
          'institution_type': 'consiglio',
          'politician_link': last_name_link.get('href'),
          'last_name' : tds[0].text_content(),
          'first_name' : tds[1].text_content(),
          'charge' : tds[2].text_content(),
          'party' : tds[3].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['politician_link'], data=data)
        print data

