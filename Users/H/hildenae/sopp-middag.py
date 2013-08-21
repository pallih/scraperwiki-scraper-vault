import scraperwiki # retriving html
import lxml.html # parsing html
import re # parsing arkivsaksnr
middag="http://sopp.no/index.php?option=com_content&view=article&id=56&Itemid=67"

html = scraperwiki.scrape(middag)
root = lxml.html.fromstring(html)

for el in root.cssselect("div.content table.contentpaneopen table"):
    tableSource = lxml.html.tostring(el)
    if "Ukedag" in tableSource:
        for tr in el.cssselect("tr"):
            trs = lxml.html.tostring(tr)
            if "Ukedag" in trs and "Matrix" in trs and "Mathilde" in trs:
                continue
            stuff = []
            for td in tr.cssselect("td"):
                tds = lxml.html.tostring(td);
                matchObj = re.match(r'.*((Man|Tirs|Ons|Tors|Fre)dag).*$', tds, re.DOTALL)
                if matchObj:
                    stuff.append(matchObj.group(1))
                    continue
                tds = tds.replace("<br>", ", ");
                td = lxml.html.fromstring(tds)
                stuff.append(td.text_content().strip())
            print ";".join(stuff)