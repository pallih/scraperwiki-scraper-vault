
import scraperwiki     
import lxml.html        
html = scraperwiki.scrape("http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Liste_Adresses.asp?PROV=VOIE")

        
root = lxml.html.fromstring(html)
for link in root.xpath('//a'): # select the url in href for all a tags(links)
    name = link.text
    if (name != "Aide"):
        data = { 'name' : name }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
import scraperwiki     
import lxml.html        
html = scraperwiki.scrape("http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Liste_Adresses.asp?PROV=VOIE")

        
root = lxml.html.fromstring(html)
for link in root.xpath('//a'): # select the url in href for all a tags(links)
    name = link.text
    if (name != "Aide"):
        data = { 'name' : name }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)