import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.shogi.or.jp/player/index.html")
root = lxml.html.fromstring(html)

kishilist = []

title = root.cssselect("table#title+table a")
for link in title:
    kishilist.append(link.attrib['href'])

kudan = root.cssselect("table#kudan+div a")
for link in kudan:
    kishilist.append(link.attrib['href'])

hachidan = root.cssselect("table#hachidan+div a")
for link in hachidan:
    kishilist.append(link.attrib['href'])

nanadan = root.cssselect("table#nanadan+div a")
for link in nanadan:
    kishilist.append(link.attrib['href'])

rokudan = root.cssselect("table#rokudan+div a")
for link in rokudan:
    kishilist.append(link.attrib['href'])

godan = root.cssselect("table#godan+div a")
for link in godan:
    kishilist.append(link.attrib['href'])

yodan = root.cssselect("table#yodan+div a")
for link in yodan:
    kishilist.append(link.attrib['href'])


for kishiurl in kishilist:
    try:
        kishihtml = scraperwiki.scrape("http://www.shogi.or.jp/player/"+kishiurl)
        root2 = lxml.html.fromstring(kishihtml)

        name = root2.cssselect("div.cont h3")[0]

        number = root2.cssselect("div.maintxt dl dd")[0]
        birth_r = root2.cssselect("div.maintxt dl dd")[1]
        ryuo = root2.cssselect("div.maintxt dl dd")[4]
        juni = root2.cssselect("div.maintxt dl dd")[5]
        

        data = {
            'name':name.text,
            'number':number.text,
            'birth':birth_r.text,
            'ryuo':ryuo.text,
            'juni':juni.text
        }

        scraperwiki.sqlite.save(unique_keys=['name'],data=data)

    except:
        print kishiurl
        continue
