import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.veikkausliiga.com/pelaajatilastot.asp")
root = lxml.html.fromstring(html)
names = []
dp = []

for sel in root.cssselect('select[name="Nimi"] option'):
    #scraperwiki.sqlite.save(unique_keys=["name"], data={"name":sel.text_content()})
    names.append(sel.text_content())

names.remove("")
#names.remove("End Patrick")
#names.remove("Helmke Hendrik")
#names.remove("Hofvendahl Björn".decode("utf-8"))

i = 1710

for name in names[1716:]:
    uname = name.replace(" ", "%20").encode("iso-8859-1")
    print uname
    html = scraperwiki.scrape("http://www.veikkausliiga.com/pelaajatilastot.asp?Nimi=" + uname)
    root = lxml.html.fromstring(html)

    d = root.cssselect("span[style='font-size:8.0pt;color:black']")[0].text
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":i, "dp":d})
    i = i + 1

