#
# Bestseller
#

import scraperwiki
import lxml.html

data = []

def scrape(url, typ, data):    
 html = scraperwiki.scrape(url)
# print html

          
 root = lxml.html.fromstring(html)
 i = 0
 for td in root.cssselect("td[class='info buch']"):
  i = i + 1
  platz = i
  if i % 2 == 0:
   art = "Sachbuch"
  else:
   art = "Belletristik"    
  #for img in td.cssselect("div[class='cover'] img"):
  # cover = img.attrib['src']
  # # print cover
  for a in td.cssselect("h5[class='bsttitel'] a"):
   titel = a.text
   print titel
  for a in td.cssselect("h5[class='bstautor'] a"):
   autor = a.text
   eanphysisch = a.attrib['href'].split("=")[-1]
  for p in td.cssselect("div[class='zus'] p"):
   try:
    if p.text.endswith(" Euro"):
     preis = p.text.replace(" Euro", "").replace(",", ".")
    elif p.text != "":
     verlag = p.text
   except:
    pass
  print preis
  data.append ({
 'typ' : typ,
 'platz' : platz,
 'art' : art,
 #'cover' : cover,
 'titel' : titel,
 'autor' : autor,
 'verlag' : verlag,
 'preis' : preis,
 'eanphysisch' : eanphysisch
 })

scrape("http://www.spiegel.de/kultur/charts/0,1518,458992,00.html", "Taschenbücher", data)
scrape("http://www.spiegel.de/kultur/charts/0,1518,458991,00.html", "Hardcover", data)

scraperwiki.sqlite.save(unique_keys=['titel'], data=data)#
# Bestseller
#

import scraperwiki
import lxml.html

data = []

def scrape(url, typ, data):    
 html = scraperwiki.scrape(url)
# print html

          
 root = lxml.html.fromstring(html)
 i = 0
 for td in root.cssselect("td[class='info buch']"):
  i = i + 1
  platz = i
  if i % 2 == 0:
   art = "Sachbuch"
  else:
   art = "Belletristik"    
  #for img in td.cssselect("div[class='cover'] img"):
  # cover = img.attrib['src']
  # # print cover
  for a in td.cssselect("h5[class='bsttitel'] a"):
   titel = a.text
   print titel
  for a in td.cssselect("h5[class='bstautor'] a"):
   autor = a.text
   eanphysisch = a.attrib['href'].split("=")[-1]
  for p in td.cssselect("div[class='zus'] p"):
   try:
    if p.text.endswith(" Euro"):
     preis = p.text.replace(" Euro", "").replace(",", ".")
    elif p.text != "":
     verlag = p.text
   except:
    pass
  print preis
  data.append ({
 'typ' : typ,
 'platz' : platz,
 'art' : art,
 #'cover' : cover,
 'titel' : titel,
 'autor' : autor,
 'verlag' : verlag,
 'preis' : preis,
 'eanphysisch' : eanphysisch
 })

scrape("http://www.spiegel.de/kultur/charts/0,1518,458992,00.html", "Taschenbücher", data)
scrape("http://www.spiegel.de/kultur/charts/0,1518,458991,00.html", "Hardcover", data)

scraperwiki.sqlite.save(unique_keys=['titel'], data=data)