import scraperwiki
import requests
import lxml.html
import string
import random

#scraperwiki.sqlite.execute("drop table if exists gardur")
#exit()

almanak_url = 'http://gardur.is/leit_einfalt.php?action=leita&ifornafn=&starfsh=&f_dag=&f_manudur=allir&f_ar=&d_dag=&d_manudur=allir&d_ar=&stadsetning=000&&sumarblom_help=&umhirdu_beidni_help=&show='

next_int = scraperwiki.sqlite.get_var('next_int')
#scraperwiki.sqlite.save_var('next_int', 0)
#exit()

def process(next_int):
    result = requests.get(almanak_url+str(next_int)).text
    root = lxml.html.fromstring(result)
    daudir = root.xpath('//table[@width="95%"]/tr')
    batch = []
    for daudur in daudir[1:]:
        record = {}
        record['nafn'] = daudur[0].text_content().strip()
        record['url'] = daudur[0][0][0].attrib['href']
        record['faedingardagur'] = daudur[1].text_content().strip()
        record['danardagur'] = daudur[2].text_content().strip()
        record['upplysingar'] = daudur[3].text_content().strip()
        record['kirkjugardur'] = daudur[4].text_content().strip()       
        batch.append(record)
    #print batch
    scraperwiki.sqlite.save(['nafn','faedingardagur','danardagur','upplysingar','url'], batch, table_name="gardur")
    #scraperwiki.sqlite.save_var('next_int', next_int+20)
    #next = root.xpath('//img[@src="hnappar/orafram.gif"]')
    #if next:
        #return next_int
        #next_int = next_int +20
        #next_link = 'http://gardur.is/almanak.php' + next[0].getparent().attrib['href']
        #process(next_int)


while next_int < 134737:
    process(next_int)
    next_int = next_int+20
    scraperwiki.sqlite.save_var('next_int', next_int)

