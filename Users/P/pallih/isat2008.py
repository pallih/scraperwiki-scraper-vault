import scraperwiki
import urllib2
import csv


scraperwiki.sqlite.attach("isic4-nace2")


selection_statement = '* from ISIC4_vs_NACE2'
isic4_nace2_codes = scraperwiki.sqlite.select(selection_statement)


#selection_statement = '* from ISIC4_vs_NACE2 WHERE NACE2code = "99.00"'
#codes = scraperwiki.sqlite.select(selection_statement)

#print isic4_nace2_codes

#value = any(d['NACE2code'] == '98.20' for d in codes)
#value = filter( lambda x: x['NACE2code']=='98.20', isic4_nace2_codes )
#print value[0]['ISIC4code']

url = 'http://data2.d8tabit.net/ISAT2008.csv'
fieldnames = ('ISAT2008', 'ISAT2008_string', 'section', 'sub_section','description_is', 'contains_is','also_contains_is', 'does_not_contain_is', 'description_en', 'contains_en', ' also_contains_en', 'does_not_contain_en')
req = urllib2.Request(url)
response = urllib2.urlopen(req)
data = response.read()

reader = csv.reader(data.splitlines())
reader = csv.DictReader(data.splitlines(),fieldnames=fieldnames) 
for row in reader:           
    if len(row['ISAT2008']) == 5:
        isic4 = filter( lambda x: x['NACE2code']==row['ISAT2008'], isic4_nace2_codes )
        row['ISIC4'] = isic4[0]['ISIC4code']
    #print row
    scraperwiki.sqlite.save(['ISAT2008'], data=row , table_name='ISAT2008')






import scraperwiki
import urllib2
import csv


scraperwiki.sqlite.attach("isic4-nace2")


selection_statement = '* from ISIC4_vs_NACE2'
isic4_nace2_codes = scraperwiki.sqlite.select(selection_statement)


#selection_statement = '* from ISIC4_vs_NACE2 WHERE NACE2code = "99.00"'
#codes = scraperwiki.sqlite.select(selection_statement)

#print isic4_nace2_codes

#value = any(d['NACE2code'] == '98.20' for d in codes)
#value = filter( lambda x: x['NACE2code']=='98.20', isic4_nace2_codes )
#print value[0]['ISIC4code']

url = 'http://data2.d8tabit.net/ISAT2008.csv'
fieldnames = ('ISAT2008', 'ISAT2008_string', 'section', 'sub_section','description_is', 'contains_is','also_contains_is', 'does_not_contain_is', 'description_en', 'contains_en', ' also_contains_en', 'does_not_contain_en')
req = urllib2.Request(url)
response = urllib2.urlopen(req)
data = response.read()

reader = csv.reader(data.splitlines())
reader = csv.DictReader(data.splitlines(),fieldnames=fieldnames) 
for row in reader:           
    if len(row['ISAT2008']) == 5:
        isic4 = filter( lambda x: x['NACE2code']==row['ISAT2008'], isic4_nace2_codes )
        row['ISIC4'] = isic4[0]['ISIC4code']
    #print row
    scraperwiki.sqlite.save(['ISAT2008'], data=row , table_name='ISAT2008')






