import scraperwiki
import lxml.html

def centrum():
    html = scraperwiki.scrape("http://static.verkehrsinfo.hamburg.de/virh/pls/liste_centrum.html")
    pls_color = {'gruen':'Hafen/Michel', 'rot':'Mönckebergstraße', 'gelb':'Jungfernstieg', 'space16':'kein'}
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr[align='center']"):
        tds = tr.cssselect("td")
        tds_img = tr.cssselect("td img")
        data = {
          'parkhaus_name' : tds[0].text_content(),
          'plaetze_gesamt' : tds[1].text_content(),
          'plaetze_belegt' : tds[2].text_content(),
          'tendenz' : tds_img[0].attrib['src'].replace('img/tendenz_','').replace('.gif',''),
          'status' : tds[4].text_content(),
          'uhrzeit' : tds[5].text_content(),
#      pls -> parkleitsystem
          'pls' : tds_img[1].attrib['src'].replace('img/','').replace('.gif',''),
    }
        print data

def airport():
    import urllib2
    req = urllib2.Request('http://www.ham.airport.de/dynamic/parkingsearch.php?locale=de&PH01=1520')
    response = urllib2.urlopen(req)
    page = response.read()
#    print page
    import json
    jbody = json.loads(page)
    body = jbody['results']['result']
    print body
    root = lxml.html.fromstring(body)
    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td img")
        tds1 = tr.cssselect("td")
        print tds1[1][0].text_content(),
        print tds1[2].text_content()

        data = {
              'parkhaus_name' : tds[0].attrib['alt'],
              'plaetze_frei' : tds1[1][1].text_content(),
        }
        print data




centrum()
#airport()