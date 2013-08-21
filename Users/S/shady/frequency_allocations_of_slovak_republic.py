import scraperwiki
import urllib, lxml.html, re

url = 'http://www.vus.sk/ntfs/php/zobrazTabulku2.php?jazyk=slov&lower=0&higher=99999999999999&hz=1&idAlokacie=0%2C0&idAplikacie=0%2C0'

f = urllib.urlopen(url)
html = f.read()
f.close()

root = lxml.html.fromstring(html)
tabulka = root.cssselect('table')[0]

trs = tabulka.cssselect('tr')

data_links = ""
links = ""
id = 1

for tr in trs:
    if (len(tr.cssselect('th')) > 1):
        continue

    tds = tr.cssselect('td')

    allocprim = tr.cssselect('td.alokPRIM')
    allocsec = tr.cssselect('td.aloksec')
    if len(allocprim) != 0:
        allocated = allocprim[0].text.rstrip()

    if len(allocsec) != 0:
        allocated = allocsec[0].text.rstrip()

    civmil = tr.cssselect('td.civmil')
    app = tr.cssselect('td.aplikacia')

    trsforlinks = tr.cssselect('tr')
    linktrcount = len(trsforlinks)
    anchors = tr.cssselect('a')

    if (len(tds) > 2):
        frequency = tr.cssselect('td.frekvencia')
        if len(frequency) != 0:
            FREQUENCY = frequency[0].text

        CIVMIL = civmil[0].text.rstrip()
        APPLICATION = re.sub('^(\s)+', '', app[0].text).rstrip()
        COMMENT = tr.cssselect('td.koment')[0].text.rstrip()

    if linktrcount > 1:
        links = ""
    for trslinks in trsforlinks:
        if linktrcount == 1:
            if (len(anchors) == 0):
                data_links = links
                links = ""
                application = APPLICATION
                if (len(data_links) > 0):
                    application += "\n"+data_links.rstrip()
                data = {
                    'id' : id,
                    'frequency' : FREQUENCY,
                    'allocated' : allocated,
                    'civmil' : CIVMIL,
                    'application' : application,
                    'comment' : COMMENT
                }
                
                scraperwiki.sqlite.save(unique_keys=["id"], data=data)
                id = id + 1
                data_links = ""


            if (len(civmil) == 0 and (len(anchors) > 0)):
                for anchor in anchors:
                    sublink1 = anchor.text
                    sublink2 = anchor.get('href')
                    link = sublink1+" "+sublink2
                    links += link+"\n"
