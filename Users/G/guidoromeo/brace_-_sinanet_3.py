import scraperwiki
import zipfile
import os
import csv
from BeautifulSoup import BeautifulSoup
from urllib import urlencode


#id = -1
years = range(2004, 2010)
URL_PREFIX = "http://www.brace.sinanet.apat.it/zipper/"

# comps = {6001: "PM2.5"}
p_comp = 6001
p_comp_name = "PM2.5"
p_reg =  "3"
p_reg_name = "LOMBARDIA"


# for p_comp, p_comp_name in comps.items():
for year in years:
    name = '%sdownload/%s_%s_%s.zip' % (
        URL_PREFIX,
        p_reg_name.upper(),
        p_comp_name.upper(),
        year
    )
    query = urlencode({
        'p_comp': p_comp,
        'p_comp_name': p_comp_name,
        'p_reg': p_reg,
        'p_reg_name': p_reg_name,
        'p_anno': year,
    })
    genfile = "%(prefix)sservlet/zipper?%(query)s" % {
        'prefix': URL_PREFIX,
        'query': query,
    }
    
    print "get", genfile
    urlfile = scraperwiki.scrape(genfile)
    soup = BeautifulSoup(urlfile)
    location = soup.find('script').contents[0].split('"'
        )[1].replace("../download/","")
    urlfile = scraperwiki.scrape("%(prefix)sdownload/%(location)s" % {
        'prefix': URL_PREFIX,
        'location': location
    })

    with open(location, "wb") as dz:
        for i in urlfile:
            dz.write(i)

    zf = zipfile.ZipFile(location)
    for z in zf.namelist():
        print "extracting", z
        zf.extract(z)
        reader = csv.reader(open(z, "r"))
        for row in reader:
            #id += 1
            #print row
            data = {'regione': p_reg_name,'localita' : row[0],
                    'inquinante' : row[1],'data': row[2], 'quantita': row[3]}
            scraperwiki.sqlite.save(
                unique_keys=['regione', 'localita', 'data', 'inquinante'],
                data=data
            )
        os.remove(z)
    os.remove(location)


