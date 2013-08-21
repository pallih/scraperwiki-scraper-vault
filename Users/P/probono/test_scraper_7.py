#
# Bestseller
#

import scraperwiki
import lxml.html
import urllib2

data = []

def scrape(url, typ, data):    
 html = scraperwiki.scrape(url)
          
 root = lxml.html.fromstring(html)
 i = 0
 for td in root.cssselect("td[class='info buch']"):
  i = i + 1
  if i == 101: 
   exit(0) ############### for debugging
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
  # print preis

  # Now that we know about the book, let's check the OYO store
  oyoepubpreis = ""
  oyopdfpreis = ""
  suchtext = urllib2.quote(titel.encode('latin-1') + " " + autor.encode('latin-1')).replace("%20", "+")
  print "* Searching OYO %s" % (suchtext)
  oyosuchurl = "http://server.meinoyo.com/ThaliaShopServlet/shop/search.jsp?search_complex=" + suchtext + "&page=0"
  oyosuchhtml = scraperwiki.scrape(oyosuchurl)
  oyosuchroot = lxml.html.fromstring(oyosuchhtml)
  for a in oyosuchroot.cssselect("a[style='display: block;']"):
   oyolink = a.attrib['href']

   # Now that we have an articleId, check what format it is, what the price is, and whether there is a sample
   print "* Checking %s" % (oyolink)
   oyoarticleurl = "http://server.meinoyo.com/ThaliaShopServlet/shop/" + oyolink
   oyoarticlehtml = scraperwiki.scrape(oyoarticleurl)
   oyoarticleroot = lxml.html.fromstring(oyoarticlehtml)
   oyopreis =""
   for h2 in oyoarticleroot.cssselect("div[class='price'] h2"):
    oyopreis = h2.text.replace(" EUR", "").replace(",", ".")
    # print oyopreis
   for div in oyoarticleroot.cssselect("div[class='information']"):
    if ": PDF" in div.text_content():
     oyopdfpreis = oyopreis
    elif ": EPUB" in div.text_content():
     oyoepubpreis = oyopreis
   oyoleseprobe = ""
   for a in oyoarticleroot.cssselect("a[class='button-small try']"):
    oyoleseprobe = a.attrib['href']
    print "* LESEPROBE GEFUNDEN"

  # Now that we know about the book, let's check the Kindle store
  kindlepreis = ""
  suchtext = urllib2.quote(titel.encode('latin-1') + " " + autor.encode('latin-1')).replace("%20", "+")
  print "* Searching Kindle %s" % (suchtext)
  kindlesuchurl = "http://www.amazon.de/s/ref=nb_sb_noss?url=search-alias%3Ddigital-text&field-keywords=" + suchtext + "&x=0&y=0"
  kindlesuchhtml = scraperwiki.scrape(kindlesuchurl)
  kindlesuchroot = lxml.html.fromstring(kindlesuchhtml)
  for notfound in kindlesuchroot.cssselect("span[class='noResultsTitleKeyword']"):
   print "* Kindle does not have " + notfound.text
  for kindleresult in kindlesuchroot.cssselect("div[id='atfResults']"):
   #print "* KINDLE MATCH"
   for span in kindleresult.cssselect("div[class='newPrice'] span"):
    kindlepreis = span.text_content().replace("EUR ", "").replace(",", ".")

  print "* Appending data"
  data = {
 'typ' : typ,
 'platz' : platz,
 'art' : art,
 #'cover' : cover,
 'titel' : titel,
 'autor' : autor,
 'verlag' : verlag,
 'preis' : preis,
 'eanphysisch' : eanphysisch,
 'oyoepubpreis' : oyoepubpreis,
 'oyopdfpreis' : oyopdfpreis,
 'oyoleseprobe' : oyoleseprobe,
 'kindlepreis' : kindlepreis
 }
  scraperwiki.sqlite.save(unique_keys=['titel'], data=data)

scrape("http://www.spiegel.de/kultur/charts/0,1518,458992,00.html", "Taschenbücher", data)
scrape("http://www.spiegel.de/kultur/charts/0,1518,458991,00.html", "Hardcover", data)

