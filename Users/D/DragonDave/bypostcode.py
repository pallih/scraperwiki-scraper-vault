import scraperwiki
lazycache=scraperwiki.swimport('lazycache')

def download(url='http://download.ordnancesurvey.co.uk/open/CODEPO/201205/CSV/codepo_gb.zip?sr=b&st=2012-05-21T10:16:04Z&se=2012-05-24T10:16:04Z&si=opendata_policy&sig=IJy5fc8DrqT%2BlmWahNzQWxsfZWg0UsD2slqGi%2BOinhI%3D'):
    return lazycache.lazycache(url, verbose=1)

def lazyint(num):
    try:
        return int(num)
    except:
        return None

def zip2sql():
    import scraperwiki,base64,StringIO,zipfile,csv

    ### code to get from zip to sql - may time out, may need to run twice.
    
    headers=['postcode','quality','easting','northing']
    
    zipdata=download()
    print "Got data"
    fh=StringIO.StringIO(base64.b64decode(zipdata))
    with zipfile.ZipFile(fh, 'r') as myzip:
        for archivefile in myzip.namelist():
            if '.csv' not in archivefile: continue
            if '/Data/' not in archivefile: continue
            print archivefile
            indifile=myzip.open(archivefile).read()
            print indifile[:100]
            csvness=csv.reader(indifile.split('\n'))
            csvdata=[dict(zip(headers,row)) for row in csvness if len(row)>1]
            builder=[]
            for row in csvness:
                print row[1]
                exit()
            scraperwiki.sqlite.save(table_name='all',data=data,unique_keys=['postcode'])
print 'go'
zip2sql()import scraperwiki
lazycache=scraperwiki.swimport('lazycache')

def download(url='http://download.ordnancesurvey.co.uk/open/CODEPO/201205/CSV/codepo_gb.zip?sr=b&st=2012-05-21T10:16:04Z&se=2012-05-24T10:16:04Z&si=opendata_policy&sig=IJy5fc8DrqT%2BlmWahNzQWxsfZWg0UsD2slqGi%2BOinhI%3D'):
    return lazycache.lazycache(url, verbose=1)

def lazyint(num):
    try:
        return int(num)
    except:
        return None

def zip2sql():
    import scraperwiki,base64,StringIO,zipfile,csv

    ### code to get from zip to sql - may time out, may need to run twice.
    
    headers=['postcode','quality','easting','northing']
    
    zipdata=download()
    print "Got data"
    fh=StringIO.StringIO(base64.b64decode(zipdata))
    with zipfile.ZipFile(fh, 'r') as myzip:
        for archivefile in myzip.namelist():
            if '.csv' not in archivefile: continue
            if '/Data/' not in archivefile: continue
            print archivefile
            indifile=myzip.open(archivefile).read()
            print indifile[:100]
            csvness=csv.reader(indifile.split('\n'))
            csvdata=[dict(zip(headers,row)) for row in csvness if len(row)>1]
            builder=[]
            for row in csvness:
                print row[1]
                exit()
            scraperwiki.sqlite.save(table_name='all',data=data,unique_keys=['postcode'])
print 'go'
zip2sql()