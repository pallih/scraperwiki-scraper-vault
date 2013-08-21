import scraperwiki,simplejson,urllib


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

'''
{"petition":{"closing_datetime":"2012-02-04T15:07:57Z","title":"resign","creato
r_name":"Nigel Woodcock","response":null,"last_update_datetime":"2012-02-01T20:5
5:09Z","department_name":"Cabinet Office","id":10,"state":"open","created_dateti
me":"2011-07-28T23:35:39Z","description":"We, the people of the United Kingdom o
f Great Britain and Northern Ireland, call upon Prime Minister David Cameron to 
resign with immediate effect and to call a general election. This is required du
e to his lack of mandate, the Conservative Party having gained only 36% of the v
ote in the 2010 general election. It is doubtful that anyone who voted Liberal D
emocrat would endorse the neoliberal policies currently being pursued by the coa
lition government. Therefore a general election is required in order to validate
 or repudiate current governmental policies. ","signature_count":1848}}
'''

def getPetitionData(pID):
    table='ep'+str(pID)
    dropper(table)
    url='http://epetitions.direct.gov.uk/api/petitions/'+str(pID)+'.json '
    data=simplejson.load(urllib.urlopen(url))
    for pc in data['petition']['postal_districts']:
        pcdata={'postcodeArea':pc,'count':data['petition']['postal_districts'][pc]}
        scraperwiki.sqlite.save(unique_keys=[], table_name=table, data=pcdata)

dropper('epetitions')

bigpetitions=[]
#also need to drop the petitioner data tables?
url='http://epetitions.direct.gov.uk/api/petitions.json'
data=simplejson.load(urllib.urlopen(url))
for petition in data:
    scraperwiki.sqlite.save(unique_keys=[], table_name='epetitions', data=petition['petition'])
    #if petition['petition']['signature_count']>1000: bigpetitions.append(petition['petition']['id'])

'''
print bigpetitions
pIDs=[11]
for pID in pIDs:
    if pID in bigpetitions:    
        getPetitionData(pID)
'''
'''
PO30    NEWPORT        Isle of Wight
PO31    COWES    Cowes, Gurnard    Isle of Wight
PO32    EAST COWES    East Cowes, Whippingham    Isle of Wight
PO33    RYDE        Isle of Wight
PO34    SEAVIEW    Seaview    Isle of Wight
PO35    BEMBRIDGE    Bembridge, Whitecliff Bay    Isle of Wight
PO36    SANDOWN        Isle of Wight
PO37    SHANKLIN        Isle of Wight
PO38    VENTNOR        Isle of Wight
PO39    TOTLAND BAY    Totland Bay, Alum Bay    Isle of Wight
PO40    FRESHWATER    Freshwater    Isle of Wight
PO41    YARMOUTH    
'''

