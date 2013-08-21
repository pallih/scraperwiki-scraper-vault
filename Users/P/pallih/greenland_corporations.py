# Greenland legal entities

# For Opencorporate - www.opencorporates.com

# -*- coding: utf-8 -*

import scraperwiki
import urllib2
import lxml.html
import re
import time

legal_entities_url = 'http://soeg.ger.gl/ger-soeg/resultat.asp?soeg=JE&sprog=E&GERNR=&DNR=&navn=*&COnavn=&adr=&BNR=&postnr=&komkode=&tlfnr=&driftsform=&branche=&status=all'

operating_unit_url = 'http://soeg.ger.gl/ger-soeg/resultat.asp?soeg=DE&sprog=E&GERNR=&DNR=&navn=*&COnavn=&adr=&BNR=&postnr=&komkode=&tlfnr=&driftsform=&branche=&status=all'


# CLEAN UP POSTAL PARTS (v/, c/o and so forth)


regex = re.compile("((?i)v\/.+|v7.+|v\..+|v\s\/.+|c\/o.+)")

#regex.findall(string)

'''legal = scraperwiki.sqlite.select("* from greenland_legal_entities")

for l in legal:
    name = l['name']
    GERnr = l['GER-nr']
    splitarray = re.split(regex, name)
    if len(splitarray) >1:
        replace_name = splitarray[0]
        replace_name = replace_name.strip()
        print splitarray[0], ' ------ ', splitarray[1]
        update_statement = 'UPDATE greenland_legal_entities SET name="'+ replace_name + '" WHERE "GER-nr"= "'+ GERnr + '"'
        #print update_statement
        scraperwiki.sqlite.execute(update_statement)

    else: 
        print name

exit()
'''

print '*** Now doing legal entities ***' 
try:
    resp = urllib2.urlopen(legal_entities_url,'20')
    html = resp.read()
except urllib2.HTTPError, error:
    print 'The server could  not fulfill the request.'
    print 'Error code: ', error.code
except URLError, error:
    print 'We failed to reach a server.'
    print 'Reason: ', error.reason
root = lxml.html.fromstring(html)

results = root.xpath('//tr[@id="idRow"]/.')

for tr in results:
    record = {}
    record['GER-nr'] = tr[0].text_content()
    name = tr[1].text_content()
    name = name.strip()
    info = ''
    splitarray = re.split(regex, name)
    if len(splitarray) >1:
        name = splitarray[0]
        name = name.strip()
        info = splitarray[1]
        info = info.strip()
    record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
    record ['name'] = name
    record ['info'] = info        
    record['url'] = 'http://soeg.ger.gl/ger-soeg/' + tr[0][0].get('href')
    #print record
    scraperwiki.sqlite.save(['GER-nr', 'name'], data=record, table_name='greenland_legal_entities')

print
print 'Done with legal entities - now doing operating units'

try:
    resp = urllib2.urlopen(operating_unit_url,'20')
    html = resp.read()
except urllib2.HTTPError, error:
    print 'The server could  not fulfill the request.'
    print 'Error code: ', error.code
except URLError, error:
    print 'We failed to reach a server.'
    print 'Reason: ', error.reason
root = lxml.html.fromstring(html)

results = root.xpath('//tr[@id="idRow"]/.')

for tr in results:
    record = {}
    record ['D-nr'] = tr[0].text_content()
    record['GER-nr'] = tr[1].text_content()
    record['url'] = 'http://soeg.ger.gl/ger-soeg/' + tr[0][0].get('href')
    name = tr[2].text_content()
    name = name.strip()
    info = ''
    splitarray = re.split(regex, name)
    if len(splitarray) >1:
        name = splitarray[0]
        name = name.strip()
        info = splitarray[1]
        info = info.strip()
    record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
    record ['name'] = name
    record ['info'] = info
    scraperwiki.sqlite.save(['D-nr', 'GER-nr', 'name'], data=record, table_name='greenland_operating_units')

print
print 'All done!'

