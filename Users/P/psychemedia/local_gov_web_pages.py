import scraperwiki

import csv, urllib

def ascii(s): return "".join(i for i in s if ord(i)<128)

def vstr(s):
    if s:
        try:
            return unicode(s)
        except UnicodeDecodeError:
            return str(s)
    else:
        return u''


def getLocalGovURLS():
    url='http://local.direct.gov.uk/Data/local_authority_service_details.csv'
    f=urllib.urlopen(url)
    csvReader = csv.DictReader(f)
    #scraperwiki.sqlite.execute('drop table "localgovpages"')
    #exit(-1)
    for row in csvReader:
        data={}
        for k in row:
            kk=k.replace(' ','')
            data[kk]=ascii(row[k])
        #print row,data
        scraperwiki.sqlite.save(unique_keys=[], table_name='localgovpages', data=data)

#getLocalGovURLs()

def getServiceListDesc():
    url='http://doc.esd.org.uk/Downloads/Mapping.ashx?type=text%2fcsv&from=http%3a%2f%2fid.esd.org.uk%2fLocalGovernmentServiceList%2f3.14&to=http%3a%2f%2fid.esd.org.uk%2fIPSV%2f2.00&predicate=http%3a%2f%2fwww.w3.org%2f2004%2f02%2fskos%2fcore%23mappingRelation'
    f=urllib.urlopen(url)
    csvReader = csv.DictReader(f)
    for row in csvReader:
        data={}
        for k in row:
            kk=k.replace(' ','')
            data[kk]=ascii(row[k])
        scraperwiki.sqlite.save(unique_keys=[], table_name='serviceDesc', data=data)

getServiceListDesc()