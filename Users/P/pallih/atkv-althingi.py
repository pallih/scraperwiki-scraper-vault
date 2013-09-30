import scraperwiki
import lxml.html

#atkvaedagreidslur yfirstandandi þingi (140)



def scrape_links(thingnumer):
    html = scraperwiki.scrape('http://www.althingi.is/dba-bin/f-nafnak.pl?s_lt=0&lthing='+str(thingnumer)+'&dags=&mfl=0&malnr=&skjalnr=&umr=&embaett=&nefnd=&sam_fel=&skrad=&nja=&nnei=&satuhj=&fjarv=&thmsk=&atkv=')
    root = lxml.html.fromstring(html)
    table = root.xpath('//a')
    tablename = str(thingnumer) + '_urls'
    for link in table:
        record = {}
        if 'atkvgr.pl?' in link.get('href'):
            record['url'] = 'http://www.althingi.is' + link.get('href')
            scraperwiki.sqlite.save(['url'], data=record, table_name=tablename, verbose=2)


scrape_links(140)
print 'done'
exit()

urls = scraperwiki.sqlite.select("* from '140_urls'") 
 
for url in urls:
   print url       

import scraperwiki
import lxml.html

#atkvaedagreidslur yfirstandandi þingi (140)



def scrape_links(thingnumer):
    html = scraperwiki.scrape('http://www.althingi.is/dba-bin/f-nafnak.pl?s_lt=0&lthing='+str(thingnumer)+'&dags=&mfl=0&malnr=&skjalnr=&umr=&embaett=&nefnd=&sam_fel=&skrad=&nja=&nnei=&satuhj=&fjarv=&thmsk=&atkv=')
    root = lxml.html.fromstring(html)
    table = root.xpath('//a')
    tablename = str(thingnumer) + '_urls'
    for link in table:
        record = {}
        if 'atkvgr.pl?' in link.get('href'):
            record['url'] = 'http://www.althingi.is' + link.get('href')
            scraperwiki.sqlite.save(['url'], data=record, table_name=tablename, verbose=2)


scrape_links(140)
print 'done'
exit()

urls = scraperwiki.sqlite.select("* from '140_urls'") 
 
for url in urls:
   print url       

