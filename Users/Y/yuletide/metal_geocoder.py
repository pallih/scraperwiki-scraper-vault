import scraperwiki
import unidecode, unicodedata
import requests

key='Fmjtd%7Cluua2qu22q%2C20%3Do5-hzzaq'

# Blank Python

scraperwiki.sqlite.attach("metal")

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

for band in scraperwiki.sqlite.select("* from swdata WHERE location NOT NULL AND location <> '0' ORDER BY scraped DESC"):
    if band['location'] and band['location'] != 'N/A':
        if band['location'].find('/') > 0:
            band['location'] = band['location'].split('/')[0].strip()
        band['place_raw'] = band['location'] + ', ' + band['country']
    else:
        band['place_raw'] = band['country']
    band['location'] = band['location'].encode ('ISO-8859-1').decode('utf-8')
    band['place'] = band['place_raw'].encode ('ISO-8859-1').decode('utf-8')
    #print band['place']
    band['place_clean'] = remove_accents(band['place'])
    scraperwiki.sqlite.save(unique_keys=['id'], data=band, table_name='bands')






import scraperwiki
import unidecode, unicodedata
import requests

key='Fmjtd%7Cluua2qu22q%2C20%3Do5-hzzaq'

# Blank Python

scraperwiki.sqlite.attach("metal")

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

for band in scraperwiki.sqlite.select("* from swdata WHERE location NOT NULL AND location <> '0' ORDER BY scraped DESC"):
    if band['location'] and band['location'] != 'N/A':
        if band['location'].find('/') > 0:
            band['location'] = band['location'].split('/')[0].strip()
        band['place_raw'] = band['location'] + ', ' + band['country']
    else:
        band['place_raw'] = band['country']
    band['location'] = band['location'].encode ('ISO-8859-1').decode('utf-8')
    band['place'] = band['place_raw'].encode ('ISO-8859-1').decode('utf-8')
    #print band['place']
    band['place_clean'] = remove_accents(band['place'])
    scraperwiki.sqlite.save(unique_keys=['id'], data=band, table_name='bands')






