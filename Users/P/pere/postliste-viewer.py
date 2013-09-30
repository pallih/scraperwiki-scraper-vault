import scraperwiki
import cgi, os
import re

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
#print paramdict

if 'source' in paramdict:
    sourcescraper = paramdict['source']
else:
    sourcescraper = 'postliste-ballangen'

scraperwiki.sqlite.attach(sourcescraper)

def htc(m):
    return chr(int(m.group(1),16))

def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url)

def table_saksbehandler():
    data = scraperwiki.sqlite.select(           
        '''saksbehandler,count(*) as antall from swdata group by saksbehandler order by antall desc'''
    )
    # print data

    print "<table>"           
    print "<tr><th>Saksbehandler</th><th>Saker</th>"
    for d in data:
        print "<tr>"
        print "<td>", d["saksbehandler"], "</td>"
        print "<td>", d["antall"], "</td>"
        print "</tr>"
    print "</table>"

# {'datert': datetime.date(2012, 1, 6), 'arkivsaksref': u'12/00008 - 008 U', 'tittel': u'INNKALLING TIL DR\xd8FTELSESM\xd8TE - 13.01.12', 'sakstittel': u'BEMANNINGSSITUASJON ETTER BUDSJETTVEDTAK 2012', 'laapenr': u'000183/12', 'kommune': 'Ballangen kommune', 'saksbehandler': u'Svenn Ole Wiik\n (R\xc5D/)', 'listdate': datetime.date(2012, 1, 6), 'gradering': '', 'fratil': u'Anne J\xf8rgensen'}

sql = "select * from swdata"
where = ""
args = []
if "caseid" in paramdict:
    where = where + ' caseid = ?'
    args.append(paramdict["caseid"])
if "agency" in paramdict:
    where = where + ' agency = ?'
    args.append(urldecode(paramdict["agency"]))
if "saksansvarlig" in paramdict:
    where = where + ' saksansvarlig = ?'
    saksansvarlig = urldecode(paramdict["saksansvarlig"])
    print "S: '" + saksansvarlig + "'"
    args.append(urldecode(paramdict["saksansvarlig"]))
if "fratil" in paramdict:
    where = where + ' sender = ? or recipient = ?'
    fratil = urldecode(paramdict["fratil"])
    args.extend([fratil, fratil])
if "q" in paramdict:
    q = urldecode(paramdict["q"])
    qlike = '%' + q + '%'
    where = where + ' docdesc like ? or casedesc like ? or sender like ? or recipient like ?'
    args.extend([qlike, qlike, qlike, qlike])
if where:
    sql = sql + ' where ' + where
sql = sql + " order by recorddate desc, casedocseq limit 200"
#print sql
data = scraperwiki.sqlite.execute(sql, args)
#print data
print "<head>"
print '<meta name="robots" content="noindex,nofollow">'
print "</head>"
print "<p>Søk i tittel, sakstittel, fra/til.</p>"
print "<p><form>Enter search term: "
print "<input name='q' length='60'>"
print "<input name='source' type='hidden' value='" + sourcescraper + "'>"
print "<INPUT type=\"submit\" value=\"Search\"> <INPUT type=\"reset\">"
print "</form></p>"
print "<table>"

#print data

i = 0
key = {}
print "<tr>"
while i < len(data['keys']):
    colname = data['keys'][i]
    key[colname] = i
    if colname in ["scrapedurl", "caseid", "scrapestamputc"]:
        True # Skip, see below
    else:
        print "<th>" + colname + "</th>"
    i = i + 1
print "</tr>"

#print data
for d in data['data']:
    print "<tr>"
    i = 0
    while i < len(data['keys']):
        colname = data['keys'][i]
        value = d[key[colname]]
        if value is None:
            value = ""
        if "docdesc" == colname:
            if 'scrapedurl' in key:
                scrapedurl = d[key['scrapedurl']]
                print "<td><a href='" + scrapedurl + "'>", value, "</a></td>"
            else:
                print "<td>", value, "</td>"
        elif "saksansvarlig" == colname:
            saksansvarlig = d[key['saksansvarlig']]
            print "<td><a href='?saksansvarlig=" + saksansvarlig + "'>", value, "</a></td>"
        elif "casedesc" == colname:
            caseid = d[key['caseid']]
            print "<td><a href='?caseid=" + caseid + "&source=" + sourcescraper + "'>", value, "</a></td>"
        elif "sender" == colname or "recipient" == colname:
            if "" != value:
                print "<td><a href='?fratil=" + value + "&source=" + sourcescraper + "'>", value, "</a></td>"
            else:
                print "<td></td>"
        elif colname in ["scrapedurl", "caseid", "scrapestamputc"]:
            True # Skip these, as they are included as links
        else:
            print "<td>", value, "</td>"
        i = i + 1
    print "</tr>"
print "</table>"
import scraperwiki
import cgi, os
import re

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
#print paramdict

if 'source' in paramdict:
    sourcescraper = paramdict['source']
else:
    sourcescraper = 'postliste-ballangen'

scraperwiki.sqlite.attach(sourcescraper)

def htc(m):
    return chr(int(m.group(1),16))

def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url)

def table_saksbehandler():
    data = scraperwiki.sqlite.select(           
        '''saksbehandler,count(*) as antall from swdata group by saksbehandler order by antall desc'''
    )
    # print data

    print "<table>"           
    print "<tr><th>Saksbehandler</th><th>Saker</th>"
    for d in data:
        print "<tr>"
        print "<td>", d["saksbehandler"], "</td>"
        print "<td>", d["antall"], "</td>"
        print "</tr>"
    print "</table>"

# {'datert': datetime.date(2012, 1, 6), 'arkivsaksref': u'12/00008 - 008 U', 'tittel': u'INNKALLING TIL DR\xd8FTELSESM\xd8TE - 13.01.12', 'sakstittel': u'BEMANNINGSSITUASJON ETTER BUDSJETTVEDTAK 2012', 'laapenr': u'000183/12', 'kommune': 'Ballangen kommune', 'saksbehandler': u'Svenn Ole Wiik\n (R\xc5D/)', 'listdate': datetime.date(2012, 1, 6), 'gradering': '', 'fratil': u'Anne J\xf8rgensen'}

sql = "select * from swdata"
where = ""
args = []
if "caseid" in paramdict:
    where = where + ' caseid = ?'
    args.append(paramdict["caseid"])
if "agency" in paramdict:
    where = where + ' agency = ?'
    args.append(urldecode(paramdict["agency"]))
if "saksansvarlig" in paramdict:
    where = where + ' saksansvarlig = ?'
    saksansvarlig = urldecode(paramdict["saksansvarlig"])
    print "S: '" + saksansvarlig + "'"
    args.append(urldecode(paramdict["saksansvarlig"]))
if "fratil" in paramdict:
    where = where + ' sender = ? or recipient = ?'
    fratil = urldecode(paramdict["fratil"])
    args.extend([fratil, fratil])
if "q" in paramdict:
    q = urldecode(paramdict["q"])
    qlike = '%' + q + '%'
    where = where + ' docdesc like ? or casedesc like ? or sender like ? or recipient like ?'
    args.extend([qlike, qlike, qlike, qlike])
if where:
    sql = sql + ' where ' + where
sql = sql + " order by recorddate desc, casedocseq limit 200"
#print sql
data = scraperwiki.sqlite.execute(sql, args)
#print data
print "<head>"
print '<meta name="robots" content="noindex,nofollow">'
print "</head>"
print "<p>Søk i tittel, sakstittel, fra/til.</p>"
print "<p><form>Enter search term: "
print "<input name='q' length='60'>"
print "<input name='source' type='hidden' value='" + sourcescraper + "'>"
print "<INPUT type=\"submit\" value=\"Search\"> <INPUT type=\"reset\">"
print "</form></p>"
print "<table>"

#print data

i = 0
key = {}
print "<tr>"
while i < len(data['keys']):
    colname = data['keys'][i]
    key[colname] = i
    if colname in ["scrapedurl", "caseid", "scrapestamputc"]:
        True # Skip, see below
    else:
        print "<th>" + colname + "</th>"
    i = i + 1
print "</tr>"

#print data
for d in data['data']:
    print "<tr>"
    i = 0
    while i < len(data['keys']):
        colname = data['keys'][i]
        value = d[key[colname]]
        if value is None:
            value = ""
        if "docdesc" == colname:
            if 'scrapedurl' in key:
                scrapedurl = d[key['scrapedurl']]
                print "<td><a href='" + scrapedurl + "'>", value, "</a></td>"
            else:
                print "<td>", value, "</td>"
        elif "saksansvarlig" == colname:
            saksansvarlig = d[key['saksansvarlig']]
            print "<td><a href='?saksansvarlig=" + saksansvarlig + "'>", value, "</a></td>"
        elif "casedesc" == colname:
            caseid = d[key['caseid']]
            print "<td><a href='?caseid=" + caseid + "&source=" + sourcescraper + "'>", value, "</a></td>"
        elif "sender" == colname or "recipient" == colname:
            if "" != value:
                print "<td><a href='?fratil=" + value + "&source=" + sourcescraper + "'>", value, "</a></td>"
            else:
                print "<td></td>"
        elif colname in ["scrapedurl", "caseid", "scrapestamputc"]:
            True # Skip these, as they are included as links
        else:
            print "<td>", value, "</td>"
        i = i + 1
    print "</tr>"
print "</table>"
