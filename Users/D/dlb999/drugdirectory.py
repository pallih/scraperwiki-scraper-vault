# Blank Python
import scraperwiki
sourcescraper = 'nci_drugdictionary'           
scraperwiki.sqlite.attach("nci_drugdictionary")
data = scraperwiki.sqlite.select(           
    '''* from nci_drugdictionary.swdata 
    order by name asc limit 10'''
)
print data