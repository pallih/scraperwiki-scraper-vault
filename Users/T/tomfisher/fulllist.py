import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.portalguiaescolas.com.br/resultados-busca?ie=&cidade=&mensalidade=&x=44&y=23')

root = lxml.html.fromstring(html) # turn our HTML into an lxml object

a = 1 
for el in root.cssselect("div.busca_cidade a"):
    #print el.text
    #print el.attrib['href']
    a +=1
    fulllink = "http://www.portalguiaescolas.com.br/"+el.attrib['href']
    scraperwiki.sqlite.save(unique_keys=["schoolname"], data={"schoolname":el.text, "link":fulllink, "ID":a})
import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.portalguiaescolas.com.br/resultados-busca?ie=&cidade=&mensalidade=&x=44&y=23')

root = lxml.html.fromstring(html) # turn our HTML into an lxml object

a = 1 
for el in root.cssselect("div.busca_cidade a"):
    #print el.text
    #print el.attrib['href']
    a +=1
    fulllink = "http://www.portalguiaescolas.com.br/"+el.attrib['href']
    scraperwiki.sqlite.save(unique_keys=["schoolname"], data={"schoolname":el.text, "link":fulllink, "ID":a})
