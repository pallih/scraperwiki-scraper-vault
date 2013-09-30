import scraperwiki

scraperwiki.sqlite.attach('test_scraper_7') 

print "<h1>Bücher mit Leseproben</h1>"
results = scraperwiki.sqlite.execute('select titel from "test_scraper_7".swdata WHERE "oyoleseprobe" <> ""')
for line in results["data"]:
 for item in line:
  print "<li>" + item + "</li>"

print "<h1>Anzahl Titel mit eBook</h1>"
epubresults = scraperwiki.sqlite.execute('SELECT COUNT(*) from "test_scraper_7".swdata WHERE "oyoepubpreis" <> ""')
pdfresults = scraperwiki.sqlite.execute('SELECT COUNT(*) from "test_scraper_7".swdata WHERE "oyopdfpreis" <> ""')
print "<li>EPUB: %s Titel</li>" % str(epubresults)
print "<li>PDF: %s Titel</li>" % str(pdfresults)

print "<h1>Titel ohne EPUB</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis from "test_scraper_7".swdata WHERE NOT "oyoepubpreis" ORDER BY platz')
print("<ol>")
for line in results["data"]:
 print "<li>" + line[0] + "</li>"
print("</ol>")

print "<h1>Preisgefüge EPUB/physisch</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis from "test_scraper_7".swdata WHERE "oyoepubpreis" <> "" ORDER BY platz')
print("<ol>")
for line in results["data"]:
 ratio = float(line[2].replace(",",".")) / float(line[1].replace(",","."))
 print "<li>" + line[0] + ": " + str(round(ratio*100,0)) + "%</li>"
print("</ol>")

print "<h1>Nur auf dem OYO?</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis,kindlepreis from "test_scraper_7".swdata WHERE oyoepubpreis AND NOT kindlepreis ORDER BY platz')
print("<ol>")
for line in results["data"]:
 if line[2] == "": line[2] = "-"
 if line[3] == "": line[3] = "-"
 print "<li>%s (OYO: %s, Kindle: %s)</li>" % (line[0], line[2], line[3])
print("</ol>")

print "<h1>Nur auf dem Kindle?</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis,kindlepreis from "test_scraper_7".swdata WHERE kindlepreis AND NOT oyoepubpreis ORDER BY platz')
print("<ol>")
for line in results["data"]:
 if line[2] == "": line[2] = "-"
 if line[3] == "": line[3] = "-"
 print "<li>%s (<a href='http://www.thalia.de/shop/ebook_start/suche/?sq=%s&sswg=EBOOK' target='_blank'>OYO</a>: %s, Kindle: %s)</li>" % (line[0], line[0], line[2], line[3])
print("</ol>")

print "<h1>Preisdifferenzen?</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis,kindlepreis from "test_scraper_7".swdata WHERE oyoepubpreis AND kindlepreis AND NOT "oyoepubpreis" = "kindlepreis" ORDER BY platz')
print("<ol>")
for line in results["data"]:
 if line[2] == "": line[2] = "-"
 if line[3] == "": line[3] = "-"
 print "<li>%s (OYO: %s, Kindle: %s)</li>" % (line[0], line[2], line[3])
print("</ol>")import scraperwiki

scraperwiki.sqlite.attach('test_scraper_7') 

print "<h1>Bücher mit Leseproben</h1>"
results = scraperwiki.sqlite.execute('select titel from "test_scraper_7".swdata WHERE "oyoleseprobe" <> ""')
for line in results["data"]:
 for item in line:
  print "<li>" + item + "</li>"

print "<h1>Anzahl Titel mit eBook</h1>"
epubresults = scraperwiki.sqlite.execute('SELECT COUNT(*) from "test_scraper_7".swdata WHERE "oyoepubpreis" <> ""')
pdfresults = scraperwiki.sqlite.execute('SELECT COUNT(*) from "test_scraper_7".swdata WHERE "oyopdfpreis" <> ""')
print "<li>EPUB: %s Titel</li>" % str(epubresults)
print "<li>PDF: %s Titel</li>" % str(pdfresults)

print "<h1>Titel ohne EPUB</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis from "test_scraper_7".swdata WHERE NOT "oyoepubpreis" ORDER BY platz')
print("<ol>")
for line in results["data"]:
 print "<li>" + line[0] + "</li>"
print("</ol>")

print "<h1>Preisgefüge EPUB/physisch</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis from "test_scraper_7".swdata WHERE "oyoepubpreis" <> "" ORDER BY platz')
print("<ol>")
for line in results["data"]:
 ratio = float(line[2].replace(",",".")) / float(line[1].replace(",","."))
 print "<li>" + line[0] + ": " + str(round(ratio*100,0)) + "%</li>"
print("</ol>")

print "<h1>Nur auf dem OYO?</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis,kindlepreis from "test_scraper_7".swdata WHERE oyoepubpreis AND NOT kindlepreis ORDER BY platz')
print("<ol>")
for line in results["data"]:
 if line[2] == "": line[2] = "-"
 if line[3] == "": line[3] = "-"
 print "<li>%s (OYO: %s, Kindle: %s)</li>" % (line[0], line[2], line[3])
print("</ol>")

print "<h1>Nur auf dem Kindle?</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis,kindlepreis from "test_scraper_7".swdata WHERE kindlepreis AND NOT oyoepubpreis ORDER BY platz')
print("<ol>")
for line in results["data"]:
 if line[2] == "": line[2] = "-"
 if line[3] == "": line[3] = "-"
 print "<li>%s (<a href='http://www.thalia.de/shop/ebook_start/suche/?sq=%s&sswg=EBOOK' target='_blank'>OYO</a>: %s, Kindle: %s)</li>" % (line[0], line[0], line[2], line[3])
print("</ol>")

print "<h1>Preisdifferenzen?</h1>"
results = scraperwiki.sqlite.execute('select titel,preis,oyoepubpreis,kindlepreis from "test_scraper_7".swdata WHERE oyoepubpreis AND kindlepreis AND NOT "oyoepubpreis" = "kindlepreis" ORDER BY platz')
print("<ol>")
for line in results["data"]:
 if line[2] == "": line[2] = "-"
 if line[3] == "": line[3] = "-"
 print "<li>%s (OYO: %s, Kindle: %s)</li>" % (line[0], line[2], line[3])
print("</ol>")