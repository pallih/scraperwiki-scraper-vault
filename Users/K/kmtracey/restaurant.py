import scraperwiki
import lxml.html
from dateutil import parser

base_url = 'http://ehs.ncpublichealth.info'
html = scraperwiki.scrape('%s/browsablemedia/' % base_url)
root = lxml.html.fromstring(html)

latest_datestamps = [None, None]
latest_hrefs = [None, None]

for el in root.cssselect("a"):
    href = el.attrib['href']
    if href.endswith('.ttx'):
        datestamp = href[-23:-4]
        index = None
        if 'MediaExportPart1' in href:
            index = 0
        elif 'MediaExportPart2' in href:
            index = 1

        if index is not None and (not latest_datestamps[index] or latest_datestamps[index] < datestamp):
            latest_datestamps[index] = datestamp
            latest_hrefs[index] = href

data = scraperwiki.scrape('%s%s' % (base_url, latest_hrefs[0]))
print 'Read %s bytes of data for part1.' % len(data)
lines = [[k.strip('"') for k in l.split('\t')] for l in [l for l in data.splitlines() if l]]
keys = lines[0]
fac_info = {}
for line in lines[1:]:
    ldict = dict(zip(keys, line))
    fac_id = ldict['FAC_ID']
    if fac_id not in fac_info:
        fac_info[fac_id] = ldict
    else:
        if fac_info[fac_id] != ldict:
            print 'Differing facility information for fac_id=%s, v1=%r, v2=%r' % (fac_id, fac_info[fac_id], ldict)

print 'Saving part1 data (%d establishments)' % len(fac_info)
for val in fac_info.values():
    del val['STATUS_CODE']
    scraperwiki.sqlite.save(unique_keys=['FAC_ID'], data=val, table_name='facinfo')
fac_info = {}


print 'Moving on to reading part2 data.'
data = scraperwiki.scrape('%s%s' % (base_url, latest_hrefs[1]))
print 'Read %s bytes of data for part2.' % len(data)
lines = ((k.strip('"') for k in l.split('\t')) for l in (l for l in data.splitlines() if l))

keys = list(lines.next())
print 'keys are: %r' % keys
#data = None

xtra_keys = set(keys) - set(['FAC_ID', 'STATUS_CODE', 'ACTIVITY_DATE', 'ACTIVITY_FINAL_SCORE'])

print 'Building insp_info dict'
insp_info = {}
for line in lines:
    line = list(line)
    ldict = dict(zip(keys, line))
    for k in xtra_keys:
        del ldict[k]  
    insp_date = parser.parse(ldict['ACTIVITY_DATE']).date()
    ldict['ACTIVITY_DATE'] = insp_date
    #ldict['ACTIVITY_ITEM_COMMENT'] = ldict['ACTIVITY_ITEM_COMMENT'].decode('iso-8859-1').encode('utf-8')
    key = (ldict['FAC_ID'], insp_date)
    if key not in insp_info:
           insp_info[key] = (ldict['ACTIVITY_FINAL_SCORE'], ldict['STATUS_CODE'])

lines = None
print 'insp_info dict has %d items, beginning save.' % len(insp_info)
try:
    for key, val in insp_info.items():
        score, status_code = val
        scraperwiki.sqlite.save(
            unique_keys=['FAC_ID', 'ACTIVITY_DATE'],
            data={'FAC_ID': key[0], 'ACTIVITY_DATE': key[1], 'ACTIVITY_FINAL_SCORE': score, 'STATUS_CODE': status_code},
            table_name='inspinfo',
        )
        del insp_info[key]
except scraperwiki.CPUTimeExceededError:
    print "CPU time exceeded exception caught"
except:
    print "Error, unexpected exception"
    raise
import scraperwiki
import lxml.html
from dateutil import parser

base_url = 'http://ehs.ncpublichealth.info'
html = scraperwiki.scrape('%s/browsablemedia/' % base_url)
root = lxml.html.fromstring(html)

latest_datestamps = [None, None]
latest_hrefs = [None, None]

for el in root.cssselect("a"):
    href = el.attrib['href']
    if href.endswith('.ttx'):
        datestamp = href[-23:-4]
        index = None
        if 'MediaExportPart1' in href:
            index = 0
        elif 'MediaExportPart2' in href:
            index = 1

        if index is not None and (not latest_datestamps[index] or latest_datestamps[index] < datestamp):
            latest_datestamps[index] = datestamp
            latest_hrefs[index] = href

data = scraperwiki.scrape('%s%s' % (base_url, latest_hrefs[0]))
print 'Read %s bytes of data for part1.' % len(data)
lines = [[k.strip('"') for k in l.split('\t')] for l in [l for l in data.splitlines() if l]]
keys = lines[0]
fac_info = {}
for line in lines[1:]:
    ldict = dict(zip(keys, line))
    fac_id = ldict['FAC_ID']
    if fac_id not in fac_info:
        fac_info[fac_id] = ldict
    else:
        if fac_info[fac_id] != ldict:
            print 'Differing facility information for fac_id=%s, v1=%r, v2=%r' % (fac_id, fac_info[fac_id], ldict)

print 'Saving part1 data (%d establishments)' % len(fac_info)
for val in fac_info.values():
    del val['STATUS_CODE']
    scraperwiki.sqlite.save(unique_keys=['FAC_ID'], data=val, table_name='facinfo')
fac_info = {}


print 'Moving on to reading part2 data.'
data = scraperwiki.scrape('%s%s' % (base_url, latest_hrefs[1]))
print 'Read %s bytes of data for part2.' % len(data)
lines = ((k.strip('"') for k in l.split('\t')) for l in (l for l in data.splitlines() if l))

keys = list(lines.next())
print 'keys are: %r' % keys
#data = None

xtra_keys = set(keys) - set(['FAC_ID', 'STATUS_CODE', 'ACTIVITY_DATE', 'ACTIVITY_FINAL_SCORE'])

print 'Building insp_info dict'
insp_info = {}
for line in lines:
    line = list(line)
    ldict = dict(zip(keys, line))
    for k in xtra_keys:
        del ldict[k]  
    insp_date = parser.parse(ldict['ACTIVITY_DATE']).date()
    ldict['ACTIVITY_DATE'] = insp_date
    #ldict['ACTIVITY_ITEM_COMMENT'] = ldict['ACTIVITY_ITEM_COMMENT'].decode('iso-8859-1').encode('utf-8')
    key = (ldict['FAC_ID'], insp_date)
    if key not in insp_info:
           insp_info[key] = (ldict['ACTIVITY_FINAL_SCORE'], ldict['STATUS_CODE'])

lines = None
print 'insp_info dict has %d items, beginning save.' % len(insp_info)
try:
    for key, val in insp_info.items():
        score, status_code = val
        scraperwiki.sqlite.save(
            unique_keys=['FAC_ID', 'ACTIVITY_DATE'],
            data={'FAC_ID': key[0], 'ACTIVITY_DATE': key[1], 'ACTIVITY_FINAL_SCORE': score, 'STATUS_CODE': status_code},
            table_name='inspinfo',
        )
        del insp_info[key]
except scraperwiki.CPUTimeExceededError:
    print "CPU time exceeded exception caught"
except:
    print "Error, unexpected exception"
    raise
