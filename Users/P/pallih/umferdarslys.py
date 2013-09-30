#traffic accidents from WFS SERVER - **** WORK IN PROGRESS

import scraperwiki,re
from lxml import etree
import lxml.html


# *********
# - START OF INITAL COLLECTION FOR TABLE ACCIDENT_NIDS
# *********


#url = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&MAXFEATURES=300&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature'

# *** comment ***  YEAR URLS (only 2007-2010 is available - we could get them all in one go but it's easier on servers to divide the requests up)

# *** comment ***  Testing has shown that 2010 is available in one go without crashing the WFS server

#url_2010 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202009-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202011-01-01T00%3A00%3A00Z)'

# *** comment ***  2009 we divide into 2 parts (6 months each)

#url_2009_1 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202008-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202009-07-01T00%3A00%3A00Z)'

#url_2009_2 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202009-06-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202010-01-01T00%3A00%3A00Z)'

# *** comment ***  2008 we divide into 2 parts (6 months each)

#url_2008_1 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202007-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202008-07-01T00%3A00%3A00Z)'

#url_2008_2 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202008-06-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202009-01-01T00%3A00%3A00Z)'

# *** comment ***  we divide into 2 parts (6 months each)

#url_2007_1 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202006-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202007-07-01T00%3A00%3A00Z)'

#url_2007_2 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202007-06-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202008-01-01T00%3A00%3A00Z)'

#def scrape_year(year_url, year):
#   xml = scraperwiki.scrape(year_url)
#   parser = etree.XMLParser()
#   tree = etree.XML(xml, parser)
#   for node in tree.iter('{http://www.opengis.net/gml}featureMember'):
#        record = {}
#        for item in node.iter('{http://www.postgis.is}nid'):
#            record['nid'] =  item.text
#        for item in node.iter('{http://www.postgis.is}dags'):
#            record['dags'] =  item.text
#        for item in node.iter('{http://www.postgis.is}timi'):
#            record['timi'] =  item.text
#        for item in node.iter('{http://www.postgis.is}meidsli'):
#            record['meidsli'] =  item.text
#        for item in node.iter('{http://www.postgis.is}tegund'):
#            record['tegund'] =  item.text
#        for item in node.iter('{http://www.postgis.is}yfirflokkur'):
#            record['yfirflokkur'] =  item.text
#        for item in node.iter('{http://www.postgis.is}gmrotation'):
#            record['gmrotation'] =  item.text
#        for item in node.iter('{http://www.opengis.net/gml}coordinates'):
#            record['coordinates'] =  item.text
#        if not 'gmrotation' in record:
#            record['gmrotation'] =  ""
#        record['year'] =  year
#        record['detail_scraped'] =  '0'
#        print record
#        scraperwiki.sqlite.save(['nid'], data=record, table_name='accident_nids')

#  *** comment ***  Collect the years:

#scrape_year(url_2010, '2010')
#scrape_year(url_2009_1, '2009')
#scrape_year(url_2009_2, '2009')
#scrape_year(url_2008_1, '2008')
#scrape_year(url_2008_2, '2008')
#scrape_year(url_2007_1, '2007')
#scrape_year(url_2007_2, '2007')

# *********
# END OF INITAL COLLECTION FOR TABLE ACCIDENT_NIDS
# *********


# *********
# START OF COLLECTION FOR TABLE ACCIDENT_DETAILS - USES NID VALUE FROM FIRST SCRAPE
# *********

baseurl = 'http://www.loftmyndir.is/kortasja/us/usQuery_HTML.asp?NID='
nids = scraperwiki.sqlite.select("nid from accident_nids where detail_scraped=0")
if len(nids) == 0:
    print 'All accidents have been scraped'
else:
    print 'There are ' + str(len(nids)) + ' accidents left to scrape. Lets go!'

for i in nids:
    record ={}
    url = baseurl + i['nid']
    print 'Processing nid: ' + i['nid']
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tegund = root.xpath ( '//h3/text()')
    record['tegund'] = tegund[0]
    spans = root.xpath ('//span[@class="accidentInfo"]/text()')
    record['lysing'] = spans[1][2:]
    record['stadur'] = spans[3]
    okutaeki = root.xpath('//ol[1]/li/text()')
    if len(okutaeki) > 1:
        #Make a comma-seperated list if values are >1
        okutaeki = ', '.join(okutaeki)
    elif len(okutaeki) == 0:
        okutaeki = 'Vantar'
    else:
        okutaeki = okutaeki[0]
    record['okutaeki'] = okutaeki
    slys = root.xpath('//ol[2]/descendant-or-self::text()')
    if len(slys) == 0:
        slys = 'Engin slys á fólki'    
    else:
        #Silly newlines and tabs
        slys.remove('\r\n\t\t\t\t\t')
        #Make a comma-seperated list if values are >1
        slys = ', '.join(slys)
        #More silly newlines and tabs replacement
        slys = slys.replace("\r\n\t\t\t\t\t", '')

    record['slys_a_folki'] = slys
    mynd = root.xpath('//img/@src')
    record['mynd'] = mynd[0]
    record['nid'] = i['nid']
    print record
    scraperwiki.sqlite.execute("update accident_nids SET detail_scraped=1 where nid="+i['nid'])
    scraperwiki.sqlite.commit()
    scraperwiki.sqlite.save(['nid'], data=record, table_name='accident_details')

# *********
# END OF COLLECTION FOR TABLE ACCIDENT_DETAILS
# *********
#traffic accidents from WFS SERVER - **** WORK IN PROGRESS

import scraperwiki,re
from lxml import etree
import lxml.html


# *********
# - START OF INITAL COLLECTION FOR TABLE ACCIDENT_NIDS
# *********


#url = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&MAXFEATURES=300&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature'

# *** comment ***  YEAR URLS (only 2007-2010 is available - we could get them all in one go but it's easier on servers to divide the requests up)

# *** comment ***  Testing has shown that 2010 is available in one go without crashing the WFS server

#url_2010 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202009-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202011-01-01T00%3A00%3A00Z)'

# *** comment ***  2009 we divide into 2 parts (6 months each)

#url_2009_1 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202008-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202009-07-01T00%3A00%3A00Z)'

#url_2009_2 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202009-06-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202010-01-01T00%3A00%3A00Z)'

# *** comment ***  2008 we divide into 2 parts (6 months each)

#url_2008_1 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202007-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202008-07-01T00%3A00%3A00Z)'

#url_2008_2 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202008-06-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202009-01-01T00%3A00%3A00Z)'

# *** comment ***  we divide into 2 parts (6 months each)

#url_2007_1 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202006-12-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202007-07-01T00%3A00%3A00Z)'

#url_2007_2 = 'http://www.loftmyndir.is/kortasja/us/queryWFS.asp?TYPENAME=postgis%3Aslys&SERVICE=WFS&VERSION=1.0.0&REQUEST=GetFeature&CQL_FILTER=(dags%20AFTER%202007-06-31T00%3A00%3A00Z%20AND%20dags%20BEFORE%202008-01-01T00%3A00%3A00Z)'

#def scrape_year(year_url, year):
#   xml = scraperwiki.scrape(year_url)
#   parser = etree.XMLParser()
#   tree = etree.XML(xml, parser)
#   for node in tree.iter('{http://www.opengis.net/gml}featureMember'):
#        record = {}
#        for item in node.iter('{http://www.postgis.is}nid'):
#            record['nid'] =  item.text
#        for item in node.iter('{http://www.postgis.is}dags'):
#            record['dags'] =  item.text
#        for item in node.iter('{http://www.postgis.is}timi'):
#            record['timi'] =  item.text
#        for item in node.iter('{http://www.postgis.is}meidsli'):
#            record['meidsli'] =  item.text
#        for item in node.iter('{http://www.postgis.is}tegund'):
#            record['tegund'] =  item.text
#        for item in node.iter('{http://www.postgis.is}yfirflokkur'):
#            record['yfirflokkur'] =  item.text
#        for item in node.iter('{http://www.postgis.is}gmrotation'):
#            record['gmrotation'] =  item.text
#        for item in node.iter('{http://www.opengis.net/gml}coordinates'):
#            record['coordinates'] =  item.text
#        if not 'gmrotation' in record:
#            record['gmrotation'] =  ""
#        record['year'] =  year
#        record['detail_scraped'] =  '0'
#        print record
#        scraperwiki.sqlite.save(['nid'], data=record, table_name='accident_nids')

#  *** comment ***  Collect the years:

#scrape_year(url_2010, '2010')
#scrape_year(url_2009_1, '2009')
#scrape_year(url_2009_2, '2009')
#scrape_year(url_2008_1, '2008')
#scrape_year(url_2008_2, '2008')
#scrape_year(url_2007_1, '2007')
#scrape_year(url_2007_2, '2007')

# *********
# END OF INITAL COLLECTION FOR TABLE ACCIDENT_NIDS
# *********


# *********
# START OF COLLECTION FOR TABLE ACCIDENT_DETAILS - USES NID VALUE FROM FIRST SCRAPE
# *********

baseurl = 'http://www.loftmyndir.is/kortasja/us/usQuery_HTML.asp?NID='
nids = scraperwiki.sqlite.select("nid from accident_nids where detail_scraped=0")
if len(nids) == 0:
    print 'All accidents have been scraped'
else:
    print 'There are ' + str(len(nids)) + ' accidents left to scrape. Lets go!'

for i in nids:
    record ={}
    url = baseurl + i['nid']
    print 'Processing nid: ' + i['nid']
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tegund = root.xpath ( '//h3/text()')
    record['tegund'] = tegund[0]
    spans = root.xpath ('//span[@class="accidentInfo"]/text()')
    record['lysing'] = spans[1][2:]
    record['stadur'] = spans[3]
    okutaeki = root.xpath('//ol[1]/li/text()')
    if len(okutaeki) > 1:
        #Make a comma-seperated list if values are >1
        okutaeki = ', '.join(okutaeki)
    elif len(okutaeki) == 0:
        okutaeki = 'Vantar'
    else:
        okutaeki = okutaeki[0]
    record['okutaeki'] = okutaeki
    slys = root.xpath('//ol[2]/descendant-or-self::text()')
    if len(slys) == 0:
        slys = 'Engin slys á fólki'    
    else:
        #Silly newlines and tabs
        slys.remove('\r\n\t\t\t\t\t')
        #Make a comma-seperated list if values are >1
        slys = ', '.join(slys)
        #More silly newlines and tabs replacement
        slys = slys.replace("\r\n\t\t\t\t\t", '')

    record['slys_a_folki'] = slys
    mynd = root.xpath('//img/@src')
    record['mynd'] = mynd[0]
    record['nid'] = i['nid']
    print record
    scraperwiki.sqlite.execute("update accident_nids SET detail_scraped=1 where nid="+i['nid'])
    scraperwiki.sqlite.commit()
    scraperwiki.sqlite.save(['nid'], data=record, table_name='accident_details')

# *********
# END OF COLLECTION FOR TABLE ACCIDENT_DETAILS
# *********
