import scraperwiki, httplib

#scraperwiki.sqlite.attach('nvwa_approved_establishments','src')
#print scraperwiki.sqlite.show_tables('src')
#print scraperwiki.sqlite.table_info('src.ApprovedEstablishments')
#print scraperwiki.sqlite.select('* from src.ApprovedEstablishments limit 10',verbose=1)

data = [{u'ApprovalNumber': 549, u'EstablishmentName': u'MLler Transport Bv', u'City': u'HOLTEN'},
{u'ApprovalNumber': 6700, u'EstablishmentName': u'Hoeve "Vrij en Blij"', u'City': u'DEN HOORN TEXEL'},
{u'ApprovalNumber': 1003, u'EstablishmentName': u'Slagerij De Valk Bv', u'City': u'VOORSCHOTEN'},
{u'ApprovalNumber': 102, u'EstablishmentName': u'Meat Friends Logistiek', u'City': u'BEST'}]

conn = httplib.HTTPSConnection("api.openkvk.nl")


for rec in data:
    q = "/py/SELECT kvk.kvk,kvk.bedrijfsnaam,kvk.adres,kvk.postcode,kvk.plaats,kvk.type,kvk.kvks,kvk.sub FROM sphinx_searchIndex('" + rec['EstablishmentName'] + " " + rec['City'] + "','openkvk') AS fts, kvk where kvk.kvk=fts.id LIMIT 10;"
    print q
    conn.request("GET", q)
    #res = conn.getresponse()
    #print res.status, res.reason
    adres = conn.getresponse().read()
    print adres
    

import scraperwiki, httplib

#scraperwiki.sqlite.attach('nvwa_approved_establishments','src')
#print scraperwiki.sqlite.show_tables('src')
#print scraperwiki.sqlite.table_info('src.ApprovedEstablishments')
#print scraperwiki.sqlite.select('* from src.ApprovedEstablishments limit 10',verbose=1)

data = [{u'ApprovalNumber': 549, u'EstablishmentName': u'MLler Transport Bv', u'City': u'HOLTEN'},
{u'ApprovalNumber': 6700, u'EstablishmentName': u'Hoeve "Vrij en Blij"', u'City': u'DEN HOORN TEXEL'},
{u'ApprovalNumber': 1003, u'EstablishmentName': u'Slagerij De Valk Bv', u'City': u'VOORSCHOTEN'},
{u'ApprovalNumber': 102, u'EstablishmentName': u'Meat Friends Logistiek', u'City': u'BEST'}]

conn = httplib.HTTPSConnection("api.openkvk.nl")


for rec in data:
    q = "/py/SELECT kvk.kvk,kvk.bedrijfsnaam,kvk.adres,kvk.postcode,kvk.plaats,kvk.type,kvk.kvks,kvk.sub FROM sphinx_searchIndex('" + rec['EstablishmentName'] + " " + rec['City'] + "','openkvk') AS fts, kvk where kvk.kvk=fts.id LIMIT 10;"
    print q
    conn.request("GET", q)
    #res = conn.getresponse()
    #print res.status, res.reason
    adres = conn.getresponse().read()
    print adres
    

