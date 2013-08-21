import scraperwiki
import lxml.html

URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"

listpage = lxml.html.fromstring(scraperwiki.scrape(URL + "SchulListe.aspx"))
for tr in listpage.cssselect("#GridViewSchulen tr[class]"):
    cells = tr.cssselect("td")
    if cells[2].text_content() == "Gymnasien":
        data = {
            'SchulNr'    : cells[0].text_content(),
            'SchulName'  : cells[1].text_content(),
            'Schulzweig' : cells[2].text_content(),
            'Bezirk'     : cells[3].text_content(),
            'Ortsteil'   : cells[4].text_content(),
            'KursAnzahl' : 0
        }
        link = cells[0].cssselect("a")[0].attrib.get("href")
        detailpage = lxml.html.fromstring(scraperwiki.scrape(URL + link))
        conz = detailpage.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblLeistungskurse")
        if len(conz):
            amn = conz[0].text_content().split(', ')
            data['KursAnzahl'] = len(amn)
            for i in amn:
                if i == u'Franz\xf6sisch':
                    i = 'Franzoesisch'
                elif i == u'Bildende Kunst/Kunst':
                    i = 'Kunst'
                elif i == u'Informatik/Informationsverarbeitung':
                    i = 'Informatik'
                elif i == u'Wirtschaftswissenschaft/-lehre':
                    i = 'Wirtschaftswissenschaft'
                elif i == u'J\xfcdische Religion / Philosophie':
                    i = 'Juedische Religion'
                elif i == u'Sport/ Leibes\xfcbungen':
                    i = 'Sport'
                data[i.encode('ascii', 'ignore').replace('/', '')] = True
        scraperwiki.sqlite.save(unique_keys=['SchulNr'], data=data)

