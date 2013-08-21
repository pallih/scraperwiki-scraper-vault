import scraperwiki
import lxml.html
import urllib2
import unicodedata
import gzip
import StringIO


if 0:
    url = "https://sites.google.com/site/argentinacompra132/files/proveedores.%d-%d.txt.gz?attredirects=0&d=1"

    ranges = (
        (1,17693), 
        (17693,20000),
        (20000,25000),
        (25000,30000),
        (30000,40000),
        (40000,45000),
        (45000,50000),
        (50000,60000),
    )

    for range in ranges:
        try:
            src = urllib2.urlopen(url % range)
            src = StringIO.StringIO(src.read())
            src = gzip.GzipFile(fileobj=src)
        except Exception, e:
            print "Failed to retrieve range %d-%d.\n%r" % (range[0], range[1], e)
        try:
            last = scraperwiki.sqlite.select("max(IdPerson) as last from swdata where (IdPerson>%d) and (IdPerson<%d)" % range)
            last = last[0]['last']
        except:
            last = 0
    
        print "Importing range %d-%d from %s..." % (range[0],range[1], last)
    
        count = 0
        while 1:
            try:
                item = eval(src.readline())
            except:
                break
            if not item: break
            try:
                if item['IdPerson'] > last:
                    scraperwiki.sqlite.save(unique_keys=['Cuit','IdPerson'], data=item)
                    count += 1
            except:
                pass
    
        print "Imported %d entries." % count
else:

    url = "https://www.argentinacompra.gov.ar/prod/onc/sitio/Perfiles/PUB/prv_detalle_proveedor.asp?IdPrv=1&IdPerson=%d"
    try:
        last = scraperwiki.sqlite.select("max(IdPerson) as last from swdata")
        last = last[0]['last']
    except:
        last = 0
    
    i = last + 1
    
    none = 0
    print "Starting from #%d." % i
    while none < 200:
        if 1:
            gotit = False
            errs = 0
            while not gotit:
                try:
                    html = urllib2.urlopen(url % i, None, 120).read()
                    gotit = True
                except:
                    errs += 1
                    print "Error #%d requesting IdPerson=%d.\n" % (errs, i)
                    if errs == 5:
                        raise
        else:
            html = urllib2.urlopen(url % i, None, 180).read()
        root = lxml.html.fromstring(html)
    
        tds = root.cssselect("td.Etiqueta")
    
        item = {}
        for td in tds:
            name = td.text.split(':')[0].title().replace(' ','')
            name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
            value = td.getnext().text
            item[name] = value
    
        item['IdPerson'] = i
        if not item['Cuit']:
            none += 1
        else:
            none = 0
            scraperwiki.sqlite.save(unique_keys=['Cuit','IdPerson'], data=item)
        i += 1

