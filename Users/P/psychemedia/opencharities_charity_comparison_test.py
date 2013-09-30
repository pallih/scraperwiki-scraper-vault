import scraperwiki,csv,urllib2,json

charities=csv.DictReader((urllib2.urlopen('https://docs.google.com/spreadsheet/pub?key=0AirrQecc6H_vdFVlV0pyd3RVTktuR0xmTTlKY1gwZ3c&single=true&gid=1&output=csv')))

def opencharitiesLookup(id):
    url='http://opencharities.org/charities/'+id+'.json'
    jsondata=json.load(urllib2.urlopen(url))
    return jsondata

for charity in charities:
    #print charity
    data={'cid':charity['charity_number']}
    for tmp in ['title','activities']:
        data[tmp]=charity[tmp]

    jdata=opencharitiesLookup(charity['charity_number'])
    chdata=jdata['charity']
    fdata=chdata['financial_breakdown']

    for tmp in ['volunteers','employees']:
        data[tmp]=chdata[tmp]
    for tmp in ['assets','spending','income']:
        if fdata != None and tmp in fdata:
            for tmp2 in fdata[tmp]:
                data[tmp+'_'+tmp2]=fdata[tmp][tmp2]
    #print data
    scraperwiki.sqlite.save(unique_keys=['cid'], table_name='hospices', data=data)import scraperwiki,csv,urllib2,json

charities=csv.DictReader((urllib2.urlopen('https://docs.google.com/spreadsheet/pub?key=0AirrQecc6H_vdFVlV0pyd3RVTktuR0xmTTlKY1gwZ3c&single=true&gid=1&output=csv')))

def opencharitiesLookup(id):
    url='http://opencharities.org/charities/'+id+'.json'
    jsondata=json.load(urllib2.urlopen(url))
    return jsondata

for charity in charities:
    #print charity
    data={'cid':charity['charity_number']}
    for tmp in ['title','activities']:
        data[tmp]=charity[tmp]

    jdata=opencharitiesLookup(charity['charity_number'])
    chdata=jdata['charity']
    fdata=chdata['financial_breakdown']

    for tmp in ['volunteers','employees']:
        data[tmp]=chdata[tmp]
    for tmp in ['assets','spending','income']:
        if fdata != None and tmp in fdata:
            for tmp2 in fdata[tmp]:
                data[tmp+'_'+tmp2]=fdata[tmp][tmp2]
    #print data
    scraperwiki.sqlite.save(unique_keys=['cid'], table_name='hospices', data=data)