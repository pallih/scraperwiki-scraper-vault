import scraperwiki           
import lxml.html
import datetime

html = scraperwiki.scrape("http://www3.tesouro.fazenda.gov.br/tesouro_direto/consulta_titulos/consultatitulos.asp")
root = lxml.html.fromstring(html)

print "hello"

print root
print root.cssselect("body")

table = root.cssselect("table center")[1]
content = lxml.html.tostring(table)
#print content
now = datetime.datetime.now();
data = {
    'date' : now.strftime("%Y-%m-%d %H:%M"),
    'html' : content,
}
scraperwiki.sqlite.save(unique_keys=['date'], data=data)


#for el in root.cssselect("table center"):           
#    print el
#    print lxml.html.tostring(el)


# /html/body/table[4]/tbody/tr/td[2]/table/tbody/tr/td[2]/center

