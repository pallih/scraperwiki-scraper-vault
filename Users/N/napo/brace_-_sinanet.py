import scraperwiki
import urllib2
import zipfile
import os
import csv
from BeautifulSoup import BeautifulSoup
id = -1
anno = (2004,2005,2006,2007,2008,2009)
for p_anno in anno:
    p_comp = 6001
    p_comp_name = "PM2.5"
    p_reg =  "3"
    p_reg_name = "LOMBARDIA"
    URLDOWNLOAD="http://www.brace.sinanet.apat.it/zipper/download/"
    name = '%s%s_%s_%s.zip' % (URLDOWNLOAD,p_reg_name.upper(),p_comp_name.upper(),p_anno)
    genfile = "http://www.brace.sinanet.apat.it/zipper/servlet/zipper?p_comp=%s&p_comp_name=%s&p_reg=%s&p_reg_name=%s&p_anno=%s" % (p_comp,p_comp_name,p_reg,p_reg_name,p_anno)
    urlfile = scraperwiki.scrape(genfile) 
    soup = BeautifulSoup(urlfile)
    location = soup.find('script').contents[0].split('"')[1].replace("../download/","")
    urlfile = scraperwiki.scrape(URLDOWNLOAD + location)
    dz = open(location, "wb")
    for i in urlfile:
        dz.write(i)
    dz.close()
    zf = zipfile.ZipFile(location)
    for z in zf.namelist():
        zf.extract(z)
        reader = csv.reader(open(z, "r"))
        for row in reader:
            id +=1 
            data = {'id': id, 'regione': p_reg_name,'localita' : row[0], 'inquinante' : row[1],'data': row[2], 'quantita': row[3]}
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        os.remove(z)
    os.remove(location)
    

