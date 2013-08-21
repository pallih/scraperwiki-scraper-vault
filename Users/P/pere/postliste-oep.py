# -*- coding: UTF-8 -*-

import scraperwiki
import lxml.html
import datetime
import time
import resource
import httplib
import urllib2

# Try several times as the database get bigger
writetries = 8

# http://www.oep.no/search/resultSingle.html?journalPostId=1000000
# http://www.oep.no/search/resultSingle.html?journalPostId=3889259

#                 <table class="defaultTable">
#                     <tr>
#                         <th class="noLeftBorder" style="width: 20%;">Agency:</th>
#                         <td class="noRightBorder" style="width: 80%;">Kulturdepartementet</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Case:</th>
#                         <td class="noRightBorder">DNT Oslo og Omegn - rehabilitering og utvidelse av turisthytta SnÃ¸heim pÃ¥ Dovre - spillemidler til anlegg for friluftsliv i fjellet 2011</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Document title:</th>
#                         <td class="noRightBorder">DNT Oslo og Omegn - turisthytta SnÃ¸heim pÃ¥ Dovre - eventuelt navnebytte</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Case number:</th>
#                         <td class="noRightBorder">2010/04027</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Document number:</th>
#                         <td class="noRightBorder">4</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Document type:</th>
#                         <td class="noRightBorder">
#                             
#                                 
#                                 
#                                 Outgoing
#                                 
#                             
#                         </td>
#                     </tr>
#                     
#                     
#                         <tr>
#                             <th class="noLeftBorder">Recipient:</th>
#                             <td  class="noRightBorder">Den Norske Turistforening</td>
#                         </tr>
#                     
#                     <tr>
#                         <th class="noLeftBorder">Document date:</th>
#                         <td class="noRightBorder">2010-12-13</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Record entry date:</th>
#                         <td class="noRightBorder">
#                             
#                                 
#                                 
#                                     2010-12-14
#                                 
#                             
#                         </td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Published in OEP</th>
#                         <td class="noRightBorder">2011-01-03</td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder" title="Hvis dokumentet er unntatt offentlighet kan unntaket gjelde hele eller deler av dokumentet."><span class="dottedBorderBottom">Grounds for exemption, document:</span></th>
#                         <td  class="noRightBorder">
#                             
#                         </td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Archive code:</th>
#                         <td  class="noRightBorder">
#                             
#                         </td>
#                     </tr>
#                     <tr>
#                         <th class="noLeftBorder">Contact point:</th>
#                         <td class="noRightBorder">
#                              <br />
#                             Tel.:&nbsp;22 24 90 90<br />
#                             Email:&nbsp;<a href="mailto:postmottak@kud.dep.no" title="Send email">postmottak@kud.dep.no</a>
#                         </td>
#                     </tr>
#                 </table>

def cpu_spent():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return getattr(usage, 'ru_utime') + getattr(usage, 'ru_stime')

def url_from_id(id):
    return "http://www.oep.no/search/resultSingle.html?journalPostId=" + str(id)

def save(data):
    problem = False
    for run in range(0,writetries):
        try:
            scraperwiki.sqlite.save(unique_keys=['journalPostId'], data=data)
            if problem:
                print "Sqlite write succeeded"
            return
        except scraperwiki.sqlite.SqliteError, e:
            print "Sqlite write error, trying again: " + str(e)
            time.sleep(22)
            problem = True
    raise scraperwiki.sqlite.SqliteError("Unable to write to database, tried " + str(writetries) + " times")

def save_var(var, data):
    problem = False
    for run in range(0,writetries):
        try:
            scraperwiki.sqlite.save_var(var, data)
            if problem:
                print "Sqlite write succeeded"
            return
        except scraperwiki.sqlite.SqliteError, e:
            print "Sqlite write error, trying again: " + str(e)
            time.sleep(22)
            problem = True
    raise scraperwiki.sqlite.SqliteError("Unable to write variable " + var + " to database, tried " + str(writetries) + " times")

fieldmap = {
    'Agency'            : 'agency',
    'Record entry date' : 'recorddate',
    'Case'              : 'casedesc',
    'Case number'       : 'caseid',
    'Document number'   : 'casedocseq',
    'Document date'     : 'docdate',
    'Document title'    : 'docdesc',
    'Document type'     : 'doctype',
    'Grounds for exemption document' : 'exemption',
    'Recipient'         : 'recipient',
    'Sender'            : 'sender',
    'Published in OEP'  : 'recordpublishdate',
#    'Archive code',
#    'Contact point',
#    'journalPostId',
#    'scrapestamputc',
}

doctypemap = {
    'Incoming' : 'I',
    'Outgoing' : 'U',
    'internal' : 'X',
}

def fetch_oep_entry(id, datastorage):
    oepurl = url_from_id(id)
    html = scraperwiki.scrape(oepurl)
    root = lxml.html.fromstring(html.decode('utf-8'))
    data = { 'journalPostId' : id }
    for tr in root.cssselect("table.defaultTable tr"):
        vtype = tr.cssselect("th")[0].text_content().strip().replace(":", "").replace(",", "")
        value = tr.cssselect("td")[0].text_content().strip()
        #print '"' + vtype + '"', '"'+value+'"'
        if (vtype == 'Record entry date' and value == 'Not stated.') or \
            (vtype == 'Document type' and value == '-') or \
            (vtype == 'Case number' and value == ''):
            return -1
        if vtype in fieldmap:
            vtype = fieldmap[vtype]
        if 'doctype' == vtype:
            value = doctypemap[value]
        if 'caseid' == vtype:
            caseyear, caseseqnr = value.split("/")
            data['caseyear'] = caseyear
            data['caseseqnr'] =  caseseqnr
        data[vtype] = value
#    print str(id) + ": " + str(data)
    data['scrapestamputc'] = datetime.datetime.now()
#    print data['scrapestamputc']
#    exit ()

    datastorage.append(data)
#    scraperwiki.sqlite.save(unique_keys=['journalPostId'], data=data)
    return 0

def fetch_range(datastorage, first, last, step):
    myskiplimit = skiplimit
    skipped = 0
    fetched = 0
    min_id = first
    for id in range(first, last, step):
        if id < 0:
            break
        try:
            tries = 3
            while 0 < tries:
                tries = tries - 1
                try:
                    if -1 == fetch_oep_entry(id, datastorage):
                        skipped = skipped + 1
                        if skipped == myskiplimit and myskiplimit == skiplimit:
                            tmp = []
                            for limit  in [250, 500, 800, 1000, 1200, 1500, 1700, 2000, 3000, 5000, 7000]:
                                testid = id + limit * step
                                if -1 != fetch_oep_entry(testid, tmp):
                                    print "Looking "+str(limit)+" ahead, found " + url_from_id(testid)
                                    myskiplimit = skiplimit + limit + 1
                                    break
                        break
                    else:
                        fetched = fetched + 1
                        skipped = 0
                        myskiplimit = skiplimit
                        break
                except urllib2.HTTPError, e: # Because HTTPError lack reason due to bug
                    print "URLError triggered for url " + url_from_id(id) + ", trying again: " + str(e.msg)
                except urllib2.URLError, e:
                    print "URLError triggered for url " + url_from_id(id) + ", trying again: " + str(e.reason)
                except httplib.BadStatusLine, e:
                    # e.msg do not exist.  trying .reason 2012-06-25
                    print "BadStatusLine triggered for url " + url_from_id(id) + ", trying again: " + str(e.reason)

            if skipped >= myskiplimit:
                print "Reached end of list, exiting at " + str(id)
                break
            if 50 <= len(datastorage):
                save(data=datastorage)
                datastorage = []

            # Only do this for every 50 ID tested, to avoid spending too much CPU seconds updating the sqlite file
            if 0 == (id % 50):
                if id < min_id:
                    min_id = id
#                    print "Updating min_id to " + str(min_id)
                    save_var('min_tested_id', min_id)
                if cpu_spent() > 79:
                    print "Running short on CPU time, exiting at " + str(id)
                    break
            time.sleep(0.2)
        except scraperwiki.CPUTimeExceededError:
            if 0 < len(datastorage):
                save(data=datastorage)
                datastorage = []
            print "CPU exception caught"
            raise
        except:
            print "Error, unexpected exception"
            raise
    if 0 < len(datastorage):
        save(data=datastorage)
        datastorage = []
    return fetched

def rename_sql_columns():
    print "Dropping temp table"
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdatanew")
    print "Creating table"
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS swdatanew (agency text, recorddate text, casedesc text, caseid text, casedocseq integer, docdate text, docdesc text, doctype text, exemption text, recipient text, sender text, recordpublishdate text, `Archive code` text, `Contact point` text, `journalPostId` integer, scrapestamputc text)")
    print  "Copying table"
    scraperwiki.sqlite.execute("INSERT INTO swdatanew(agency, recorddate, casedesc, caseid, casedocseq, docdate, docdesc, doctype, exemption, recipient, sender, recordpublishdate, `Archive code`, `Contact point`, `journalPostId`, scrapestamputc) SELECT `Agency`, `Record entry date`, `Case`, `Case number`, `Document number`, `Document date`, `Document title`, `Document type`, `Grounds for exemption document`, `Recipient`, `Sender`, `Published in OEP`, `Archive code`, `Contact point`, `journalPostId`, `scrapestamputc` FROM swdata")

    scraperwiki.sqlite.execute("ALTER TABLE swdata RENAME TO swdataold")
    scraperwiki.sqlite.execute("ALTER TABLE swdatanew RENAME TO swdata")
    scraperwiki.sqlite.commit()
    exit(0)

def create_indexes():
    for field in ['doctype', 'agency', 'recorddate', 'caseid']:
        print "Creating %s index" % field
        scraperwiki.sqlite.execute("CREATE INDEX IF NOT EXISTS swdata_%s_index ON swdata (%s)" % (field, field))
        scraperwiki.sqlite.commit()

def update_doctypes():
    print "Updating doctype"
    agencies = []
    for agencyref in scraperwiki.sqlite.select("distinct agency from swdata"):
        agencies.append(agencyref['agency'])

    # Updating individual agencies to try to avoid SQL timeout
    for agency in agencies:
        print "Updating doctype for " + agency
        scraperwiki.sqlite.execute("UPDATE swdata set doctype = 'I' where agency = ? and doctype = 'Incoming'", (agency))
        scraperwiki.sqlite.execute("UPDATE swdata set doctype = 'U' where agency = ? and doctype = 'Outgoing'", (agency))
        scraperwiki.sqlite.execute("UPDATE swdata set doctype = 'X' where agency = ? and doctype = 'internal'", (agency))
        scraperwiki.sqlite.commit()
    exit(0)

def update_caseyear():
    print "Updating caseyear and caseseqnr"
    agencies = []
    for agencyref in scraperwiki.sqlite.select("distinct agency from swdata WHERE caseyear is NULL"):
        agencies.append(agencyref['agency'])

    # Updating individual agencies to try to avoid SQL timeout
    for agency in agencies:
        print "Updating caseyear for " + agency
        res = scraperwiki.sqlite.execute("select journalPostId, substr(caseid, 1, 4), substr(caseid, 6) from swdata where agency = ? and caseyear is NULL limit 2", (agency))
        print res
        scraperwiki.sqlite.execute("UPDATE swdata set caseyear = substr(caseid, 1, 4), caseseqnr = substr(caseid, 6) where agency = ? AND caseyear is NULL", (agency))
        scraperwiki.sqlite.commit()
    exit(0)

def remove_original():
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swdataold")
    scraperwiki.sqlite.commit()
    exit(0)

#update_caseyear()

#create_indexes()

#rename_sql_columns()
#remove_original()

# This one give me SQL timeout
#update_doctypes()

print "Starting to fetch journal entries " + str(datetime.datetime.now())
scraperwiki.scrape("http://www.oep.no/")
datastorage = []

# Update entries to handle <URL: https://rt.nuug.no:443/Ticket/Display.html?id=6342 >.
# Used 2012-09-17
#scraperwiki.sqlite.execute("DELETE from swdata where journalPostId = 638167")
#fetch_oep_entry(638167, datastorage)
#scraperwiki.sqlite.execute("DELETE from swdata where journalPostId = 638104")
#fetch_oep_entry(638104, datastorage)
#scraperwiki.sqlite.commit()

count = 10000
skiplimit = 500
# Random value fairly close to the most recent ID when this project started 2012-05-03
max = min = startid = 3889259
try:
    max = scraperwiki.sqlite.select("max(journalPostId) as max from swdata")[0]["max"]
    if 0 < scraperwiki.sqlite.get_var('min_tested_id'):
        saved_min = scraperwiki.sqlite.get_var('min_tested_id')
    else:
        saved_min = 0
    sql_min = scraperwiki.sqlite.select("min(journalPostId) as min from swdata")[0]["min"]
    print "Saved min: " + str(saved_min) + ", sql min: " + str(sql_min)
    if sql_min < saved_min:
        min = sql_min
    else:
        min = saved_min
    print "Scraping " + str(count) + " IDs below " + str(min) + " and above " + str(max)
except scraperwiki.sqlite.SqliteError:
    pass

fetched = fetch_range(datastorage, max + 1, max + count, 1)
print "Fetched " + str(fetched) + " new journal entries, cpu spent: " + str(cpu_spent())
if min >= 0:
    fetched = fetch_range(datastorage, min, min - count, -1)
    print "Fetched " + str(fetched) + " old journal entries, cpu spent: " + str(cpu_spent())

