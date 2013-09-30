import scraperwiki
import pytz
import datetime
import lxml.html
import dateutil.parser
import hashlib

URL = 'http://67.32.159.27/webcad/webcad.asp' # redirect from http://67.32.159.27/ frame from http://lafayette911.org/
tz = pytz.timezone('CST6CDT') # site is for a specific geographical region
RUNLIMIT = datetime.timedelta(seconds = 45) # don't run more than this often
scrapeat = datetime.datetime.now(tz) # instance time

lastrun = scraperwiki.sqlite.get_var('lastrun')
lastrun = dateutil.parser.parse(lastrun) if lastrun is not None else tz.localize(datetime.datetime.combine(datetime.date.today(),datetime.time()))
sincelastrun = scrapeat - lastrun

print 'last run ' + str(sincelastrun) + ' ago... ',
if sincelastrun < RUNLIMIT:
    print 'EXIT'
    raise SystemExit
else:
    print 'RUN'
    scraperwiki.sqlite.save_var('lastrun', scrapeat.isoformat())

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html)

statusat = root.cssselect('h4 center')[0].text.strip()
statusat = tz.localize(dateutil.parser.parse(statusat))

report = {
    'scrapeat': scrapeat,
    'statusat': statusat
}

incidentlist = [] 
try:
    incidents = root.cssselect('center table')[1]
    labels = tuple(x.text_content().lower().replace(' ', '') for x in incidents.cssselect('tr:first-child td'))
    for row in incidents.cssselect('tr:nth-child(1n+2)'):
        incident = dict(zip(labels, (x.text_content().strip() for x in row.getchildren())))
        location = incident.pop('locatedat').split(None,-1)
        city, state = location.pop().split(',')
        address = ' '.join(location)
        incident.update({
            'address': address, 'city': city, 'state': state,
            'reportedat': tz.localize(dateutil.parser.parse(incident['reportedat'])),
            'fire': True if 'F' in incident['assisting'] else False,
            'medical': True if 'M' in incident['assisting'] else False,
            'sheriff': True if 'S' in incident['assisting'] else False,
            'police': True if 'P' in incident['assisting'] else False
        })
        del incident['assisting']
        incident['id'] = hashlib.sha1(str(sorted(incident.iteritems()))).hexdigest()
        incidentlist.append(incident)
        scraperwiki.sqlite.save(unique_keys = ['id'], data = incidentlist, table_name = 'incidents')
except IndexError:
    pass

report.update({'incidentcount': len(incidentlist)})
report['id'] = hashlib.sha1(str(sorted(report.iteritems()))).hexdigest()
scraperwiki.sqlite.save(unique_keys = ['id'], data = report, table_name = 'reports')
reportincidentlist = []
for i in (x['id'] for x in incidentlist):
    ri = {'reportid': report['id'], 'incidentid': i}
    try:
        scraperwiki.sqlite.execute('CREATE TABLE `reportedincidents` (`reportid` text, `incidentid` text, `firstseen` text)')
        scraperwiki.sqlite.commit()
    except scraperwiki.sqlite.SqliteError:
        pass
    ri['firstseen'] = dateutil.parser.parse(scraperwiki.sqlite.select('COALESCE(min(r.statusat),?) firstseen from reports r join reportedincidents ri on ri.reportid = r.id and ri.incidentid = ?', [report['statusat'].isoformat(),i])[0]['firstseen'])
    reportincidentlist.append(ri)
if reportincidentlist:
    scraperwiki.sqlite.save(unique_keys = ['reportid', 'incidentid'], data = reportincidentlist, table_name = 'reportedincidents')

import scraperwiki
import pytz
import datetime
import lxml.html
import dateutil.parser
import hashlib

URL = 'http://67.32.159.27/webcad/webcad.asp' # redirect from http://67.32.159.27/ frame from http://lafayette911.org/
tz = pytz.timezone('CST6CDT') # site is for a specific geographical region
RUNLIMIT = datetime.timedelta(seconds = 45) # don't run more than this often
scrapeat = datetime.datetime.now(tz) # instance time

lastrun = scraperwiki.sqlite.get_var('lastrun')
lastrun = dateutil.parser.parse(lastrun) if lastrun is not None else tz.localize(datetime.datetime.combine(datetime.date.today(),datetime.time()))
sincelastrun = scrapeat - lastrun

print 'last run ' + str(sincelastrun) + ' ago... ',
if sincelastrun < RUNLIMIT:
    print 'EXIT'
    raise SystemExit
else:
    print 'RUN'
    scraperwiki.sqlite.save_var('lastrun', scrapeat.isoformat())

html = scraperwiki.scrape(URL)
root = lxml.html.fromstring(html)

statusat = root.cssselect('h4 center')[0].text.strip()
statusat = tz.localize(dateutil.parser.parse(statusat))

report = {
    'scrapeat': scrapeat,
    'statusat': statusat
}

incidentlist = [] 
try:
    incidents = root.cssselect('center table')[1]
    labels = tuple(x.text_content().lower().replace(' ', '') for x in incidents.cssselect('tr:first-child td'))
    for row in incidents.cssselect('tr:nth-child(1n+2)'):
        incident = dict(zip(labels, (x.text_content().strip() for x in row.getchildren())))
        location = incident.pop('locatedat').split(None,-1)
        city, state = location.pop().split(',')
        address = ' '.join(location)
        incident.update({
            'address': address, 'city': city, 'state': state,
            'reportedat': tz.localize(dateutil.parser.parse(incident['reportedat'])),
            'fire': True if 'F' in incident['assisting'] else False,
            'medical': True if 'M' in incident['assisting'] else False,
            'sheriff': True if 'S' in incident['assisting'] else False,
            'police': True if 'P' in incident['assisting'] else False
        })
        del incident['assisting']
        incident['id'] = hashlib.sha1(str(sorted(incident.iteritems()))).hexdigest()
        incidentlist.append(incident)
        scraperwiki.sqlite.save(unique_keys = ['id'], data = incidentlist, table_name = 'incidents')
except IndexError:
    pass

report.update({'incidentcount': len(incidentlist)})
report['id'] = hashlib.sha1(str(sorted(report.iteritems()))).hexdigest()
scraperwiki.sqlite.save(unique_keys = ['id'], data = report, table_name = 'reports')
reportincidentlist = []
for i in (x['id'] for x in incidentlist):
    ri = {'reportid': report['id'], 'incidentid': i}
    try:
        scraperwiki.sqlite.execute('CREATE TABLE `reportedincidents` (`reportid` text, `incidentid` text, `firstseen` text)')
        scraperwiki.sqlite.commit()
    except scraperwiki.sqlite.SqliteError:
        pass
    ri['firstseen'] = dateutil.parser.parse(scraperwiki.sqlite.select('COALESCE(min(r.statusat),?) firstseen from reports r join reportedincidents ri on ri.reportid = r.id and ri.incidentid = ?', [report['statusat'].isoformat(),i])[0]['firstseen'])
    reportincidentlist.append(ri)
if reportincidentlist:
    scraperwiki.sqlite.save(unique_keys = ['reportid', 'incidentid'], data = reportincidentlist, table_name = 'reportedincidents')

