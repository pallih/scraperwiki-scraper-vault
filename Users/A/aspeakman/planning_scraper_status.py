import scraperwiki
import urllib, urllib2
import json
import cgi
import re
from datetime import timedelta
from datetime import date
from datetime import datetime
import time
import sys
import os

util = scraperwiki.utils.swimport("utility_library")
scraperwiki.sqlite.attach('planning_authority_lookup')

SW_SCRAPE_URL = "https://scraperwiki.com/scrapers/"
SW_DB_URL = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=%s&query=%s"
OL_SCRAPER_URL = "http://openlylocal.com/councils/%d/planning_applications"

current = date.today() - timedelta(days=60) # current application threshold
date_current = current.strftime('%Y-%m-%d')
recent = date.today() - timedelta(days=30) # recent application threshold
date_ok = recent.strftime('%Y-%m-%d')
#last2weeks = date.today() - timedelta(days=14) # last2weeks run threshold
#date_fine = last2weeks.strftime('%Y-%m-%d')
lastweek = date.today() - timedelta(days=7) # lastweek application threshold
date_good = lastweek.strftime('%Y-%m-%d')

main_order_options = [ 
    ("name asc", "Alphabetical"), 
    ("name desc", "Reverse Alphabetical"),
    ("ol_most_recent desc", "Most Up To Date On OpenlyLocal"),
    ("case when openlylocal_id is null then 1 else 0 end, ol_most_recent asc", "Least Up To Date On OpenlyLocal"),
    ("sw_most_recent desc", "Most Up To Date On ScraperWiki"),
    ("case when scraper is null then 1 else 0 end, sw_most_recent asc", "Least Up To Date On ScraperWiki"),
    ("checked_at desc", "Most Recently Checked"),
    ("case when scraper is null then 1 else 0 end, checked_at asc", "Least Recently Checked"),
]

table_order_options = [
    ("name asc", "Alphabetical"),
    ("name desc", "Reverse Alphabetical"),
    ("sw_most_recent desc", "Most Up To Date"),
    ("sw_most_recent asc", "Least Up To Date"),
]

db_order_options = [
    ("date_scraped desc", "Recent Scrape Dates First"),
    ("date_scraped asc", "Recent Scrape Date Last"),
    ("sdt desc", "Recent Application Dates First"),
    ("sdt asc", "Recent Application Dates Last"),
]

show_fields = [ 
    ('uid', 'Identifier'),
    ('date_scraped', 'Date Scraped'),
    ('sdt', 'Application Date'),
    ('address', 'Address'),
    ('description', 'Description'),
    ('rowid', 'Row No.')
]

standard_fields = [
'url',
'address',
'applicant_address',
'applicant_name',
'start_date',
'date_received',
'date_validated',
'date_scraped',
'description',
'uid',
'agent_address',
'agent_name',
'agent_tel',
'appeal_date',
'appeal_decision_date',
'appeal_result',
'appeal_status',
'application_type',
'application_expires_date',
'associated_application_uid',
'case_officer',
'comment_url',
'comment_date',
'consultation_end_date',
'consultation_start_date',
'decided_by',
'decision',
'decision_date',
'decision_issued_date',
'decision_published_date',
'development_type',
'district',
'easting',
'last_advertised_date',
'lat',
'latest_advertisement_expiry_date',
'lng',
'meeting_date',
'neighbour_consultation_end_date',
'neighbour_consultation_start_date',
'northing',
'os_grid_ref',
'parish',
'permission_expires_date',
'planning_portal_id',
'postcode',
'reference',
'site_notice_end_date',
'site_notice_start_date',
'status',
'target_decision_date',
'uprn',
'ward_name',
]

try:
    userquery = scraperwiki.utils.GET()
except:
    userquery = {}

if userquery.get('dbimg'):

    db_data = util.get_table_vals('status', 'name,date_plot', 
        "name = '%(dbimg)s' or sw_name like '%%%(dbimg)s%%' or ol_name like '%%%(dbimg)s%%' or snac_id = '%(dbimg)s' or authority_id = '%(dbimg)s'" % userquery)
    #print db_data

    if db_data and len(db_data) == 1 and db_data[0]['date_plot']:

        scraperwiki.utils.httpresponseheader("Content-Type", "image/png")
        scraperwiki.dumpMessage({"content":db_data[0]['date_plot'], "message_type":"console", "encoding":"base64"})

    elif not db_data or (len(db_data) == 1 and not db_data[0]['date_plot']):

        print "No date plot image found for '%(dbimg)s'" % userquery

    else:

        auth_list = util.get_list(db_data, 'name')
        print "More than 1 scraper found when searching for date plot '%(dbimg)s': " % userquery + ', '.join(auth_list)

    sys.exit()
    
header = """
<html><head>
<style type="text/css">%s</style>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
<script type="text/javascript">
function showImage(Id) {
        var idenc = encodeURIComponent(Id);
        var idnosp = Id.replace(/ /g, ''); // replace spaces globally, not just the first one
        $("#slnk-"+idnosp).hide();
        $("#slnk-"+idnosp).after('<img src="?dbimg='+idenc+'" width="100" height="75" id="img-'+idnosp+'" style="display: none;"> </img>');
        $("#img-"+idnosp).after('<img src="http://upload.wikimedia.org/wikipedia/commons/d/de/Ajax-loader.gif"> </img>');
        $("#img-"+idnosp).bind("load", function () { $(this).next().remove(); $(this).next().show(); $(this).fadeIn('slow'); });
        $("#img-"+idnosp).bind("error", function () { $(this).prev().show(); $(this).next().remove(); $(this).next().hide(); $(this).remove(); });
    }
function hideImage(Id) {
        var idenc = encodeURIComponent(Id);
        var idnosp = Id.replace(/ /g, ''); // replace spaces globally, not just the first one
        $("#img-"+idnosp).remove()
        $("#hlnk-"+idnosp).hide();
        $("#slnk-"+idnosp).show();
    }
</script>
</head><body>""" % util.base_css()

ordering = '<form method="get" name="form1"><strong>Ordered By:</strong>&nbsp;'

if userquery.get('db'):

    result = util.get_table_vals('status', '', 
        "name = '%(db)s' or sw_name like '%%%(db)s%%' or ol_name like '%%%(db)s%%' or snac_id = '%(db)s' or authority_id = '%(db)s'" % userquery)
    subs = result[0]
    if not subs or not subs.get('scraper'):
        print "No records found"
        sys.exit()
    if not subs.get('table_name'):
        subs['table_name'] = 'swdata'
    fields = subs['field_names'].split(', ')
    if 'start_date' in fields:
        subs['sdt'] = 'start_date'
    elif 'date_received' in fields:
        subs['sdt'] = 'date_received'
    elif 'date_validated' in fields:
        subs['sdt'] = 'date_validated'
    else:
        subs['sdt'] = 'start_date'
    order_options = db_order_options
    order = userquery.get('order')
    if not order: order = order_options[0][0]
    subs['order'] = order
    subs['current'] = date_current
    sql = """select *, rowid, %(sdt)s as sdt
        from %(table_name)s where date_scraped is not null and (sdt
        is null or sdt > '%(current)s') order by %(order)s""" % subs
    #print sql
    url = SW_DB_URL % (subs['scraper'], urllib.quote_plus(sql))
    db_data = json.load(urllib2.urlopen(url))
    #print db_data

    title = "<h1>%d Current Records from %s (id:%d)</h1>" % (len(db_data), subs['sw_name'], subs['authority_id'])
    subtitle = '<h3>i.e. where the application date is within the last 60 days (or is missing)</h3>'

    ordering += '<input type="hidden" name="db" value="%s">' % userquery['db']
    key = ""

    table_data = '<table><tr>'
    for f in show_fields:
        table_data += '<th>%s</th>' % f[1]
    table_data += '</tr>'
    for r in db_data:
        table_data += '<tr>'
        for f in show_fields:
            name = f[0]
            if not r.get(name):
                table_data += '<td>-</td>'
            elif name == 'uid' and r.get('url'):
                table_data += '<td><a href="%s">%s</a></td>' % (r['url'], r['uid'])
            elif name == 'description':
                descr = r[name] if len(r[name]) <= 40 else r[name][0:37]+' ...'
                table_data += '<td>%s</td>' % (descr)
            elif name == 'rowid':
                table_data += '<td>%d</td>' % r[name]
            else:
                table_data += '<td>%s</td>' % r[name]
        table_data += '</tr>'
    table_data += '</table>'

elif userquery.get('table'):

    order_options = table_order_options
    order = userquery.get('order')
    if not order: order = order_options[0][0]
    db_data = util.get_table_vals('status', '', 'scraper is not null', 'order by %s' % order)
    #print db_data

    title = "<h1>Status Table For %d Planning Scrapers On ScraperWiki</h1>" % len(db_data)
    subtitle = ""
    key = ""

    ordering += '<input type="hidden" name="table" value="%s">'

    table_data = """<table>
    <tr><th colspan="4">Scraper</th><th>ID Only Records</th><th colspan="13">Full Records</th></tr>
    <tr><th>Authority</th><th>Last Run</th><th>Run Time (mins)</th><th>Total Records</th><th>Total</th><th>Total</th><th>Current Full Records (last 60 days)</th><th>Current Records Scraped in Last 7 Days</th><th>Earliest Start Date</th><th>Date Distribution</th><th>Latest Start Date</th><th>Address (%Complete)</th><th>Description (%Complete)</th><th>URL (%Complete)</th><th>Start Date (%Complete)</th><th>Postcodes (%Supplied)</th><th>Date Fields With Non Standard Format</th><th>Fields with Non Standard Names</th></tr>
    """

    for r in db_data:
        non_standard_fields = []
        fields = r['field_names'].split(', ')
        for i in fields:
            if i not in standard_fields:
                f2 = i if len(i) <= 25 else i[0:25]+' ...'
                non_standard_fields.append(f2)
        r["last_run"] = r["last_run"][:10]
        if r["last_run"] < date_ok:
            r["last_run"] = '<span style="background-color:red;color:white;">%s</span>' %  r["last_run"]
        r["last_run_time"] = format(r["last_run_time"]/60.0, '.1f')
        if float(r["last_run_time"]) > 120.0 :
            r["last_run_time"] = '<span style="background-color:red;color:white;">%s</span>' %  r["last_run_time"]
        r["num_idonly"] = "%d (%.0f%%)" % (r["num_idonly"], 100.0 * r["num_idonly"] / r["num_recs"])
        num_full_recs = r["num_full_recs"]
        r["num_full_recs"] = "%d (%.0f%%)" % (r["num_full_recs"], 100.0 * num_full_recs / r["num_recs"])
        if not r.get("num_current"):
            r["num_recently_scraped"] = "-"
        else:
            percent_scraped = 100.0 * r["num_recently_scraped"] / r["num_current"]
            if percent_scraped > 50.0:
                r["num_recently_scraped"] = "%d (%.0f%%)" % (r["num_recently_scraped"], percent_scraped)
            else:
                r["num_recently_scraped"] = '%d (<span style="background-color:red;color:white;">%.0f%%</span>)' % (r["num_recently_scraped"], percent_scraped)
        if r["num_current"] <= 0:
            r["num_current"] = '<span style="background-color:red;color:white;">%d</span>' %  r["num_current"]
        if r["last_full_rec"] < date_ok:
            r["last_full_rec"] = '<span style="background-color:red;color:white;">%s</span>' %  r["last_full_rec"]
        address_percent = 100.0 * r["address_count"] / num_full_recs
        descr_percent = 100.0 * r["description_count"] / num_full_recs
        url_percent = 100.0 * r["url_count"] / num_full_recs
        sdate_percent = 100.0 * r["used_sdate_count"] / num_full_recs
        if address_percent < 25.0:
            r["address_count"] = '<span style="background-color:red;color:white;">%.0f%%</span>' %  address_percent
        else:
            r["address_count"] = '%.0f%%' %  address_percent
        if descr_percent < 25.0:
            r["description_count"] = '<span style="background-color:red;color:white;">%.0f%%</span>' %  descr_percent
        else:
            r["description_count"] = '%.0f%%' %  descr_percent
        if url_percent < 25.0:
            r["url_count"] = '<span style="background-color:red;color:white;">%.0f%%</span>' %  url_percent
        else:
            r["url_count"] = '%.0f%%' %  url_percent
        if sdate_percent < 25.0:
            r["used_sdate_count"] = '<span style="background-color:red;color:white;">%.0f%%</span>' %  sdate_percent
        else:
            r["used_sdate_count"] = '%.0f%%' %  sdate_percent
        if r["postcodes_percent"] < 25.0:
            r["postcodes_percent"] = '<span style="background-color:red;color:white;">%.0f%%</span>' %  r["postcodes_percent"]
        else:
            r["postcodes_percent"] = '%.0f%%' %  r["postcodes_percent"]
        table_data += """<tr><td><a name="xx%(authority_id)s"></a><a href="https://scraperwiki.com/scrapers/%(scraper)s">%(name)s</a></td>
           <td>%(last_run)s</td> <td>%(last_run_time)s</td> <td>%(num_recs)s</td>
           <td>%(num_idonly)s</td> <td>%(num_full_recs)s</td> <td><a href="?db=%(authority_id)d">%(num_current)s</a></td>
           <td>%(num_recently_scraped)s</td> <td>%(first_full_rec)s</td> 
           <td align="center"> <a href="javascript:showImage('%(authority_id)d')" id="slnk-%(authority_id)d">Show</a>
                <a href="javascript:hideImage('%(authority_id)d')" id="hlnk-%(authority_id)d" style="display:none;">Hide</a> </td> 
           <td>%(last_full_rec)s</td>
           <td>%(address_count)s</td> <td>%(description_count)s</td> 
           <td>%(url_count)s</td> <td>%(used_sdate_count)s</td> <td>%(postcodes_percent)s</td>
           <td>%(bad_date_fields)s</td> """ % r
        table_data += '<td>%s</td> </tr>' % ', '.join(non_standard_fields)
        
    table_data += '</table>'

else:

    order_options = main_order_options
    order = userquery.get('order')
    if not order: order = order_options[0][0]
    db_data = util.get_table_vals('status', '', '', 'order by %s' % order)
    #print db_data

    title = "<h1>Details of Scrapers for %d UK Planning Authorities</h1>" % len(db_data)
    subtitle = ""

    key = """<p><b>Key:</b>
        date of most recent planning application
        <span style="background-color:red;color:white;">more than 30 days old</span> <span style="background-color:green;color:white;">less than 7 days old</span>
        <br /></p>"""

    table_data = '<dl>'
    for r in db_data:
        #print r
        # (id: %(authority_id)d)
        table_data += '<dt>%(name)s <span style="font-size:x-small;">(last checked: %(checked_at)s)</span></dt><dd>' % r
        if r.get('openlylocal_id'):
            if not r.get("ol_most_recent") or r["ol_most_recent"] < date_ok:
                r["ol_most_recent"] = '<span style="background-color:red;color:white;">%s</span>' %  r["ol_most_recent"]
            if r.get("ol_most_recent") and r["ol_most_recent"] >= date_good:
                r["ol_most_recent"] = '<span style="background-color:green;color:white;">%s</span>' %  r["ol_most_recent"]
            table_data += 'On OpenlyLocal: <a href="http://openlylocal.com/councils/%(openlylocal_id)d/planning_applications">%(ol_name)s</a> %(ol_most_recent)s <br />' % r
        if r.get('scraper'):
            if not r.get("sw_most_recent") or r["sw_most_recent"] < date_ok:
                r["sw_most_recent"] = '<span style="background-color:red;color:white;">%s</span>' %  r["sw_most_recent"]
            if r.get("sw_most_recent") and r["sw_most_recent"] >= date_good:
                r["sw_most_recent"] = '<span style="background-color:green;color:white;">%s</span>' %  r["sw_most_recent"]
            table_data += """On ScraperWiki: <a href="https://scraperwiki.com/scrapers/%(scraper)s/">%(sw_name)s</a>
                 %(sw_most_recent)s <a href="?table=yes#xx%(authority_id)d">Details</a> <br />""" % r
        if not r.get('openlylocal_id') and not r.get('scraper'):
            table_data += 'No scraper on ScraperWiki or OpenlyLocal</dd>'
        else:
            table_data += '</dd>'
    table_data += '</dl>'

ordering += '<select name="order" id="order" onchange="this.form.submit()">'
sortorder = sorted(order_options, key=lambda opt: opt[1]) 
for item in sortorder:
    k, v = item
    if k == order:
        ordering += '<option selected="selected" value="%s">%s</option>' % (k, v)
    else:
        ordering += '<option value="%s">%s</option>' % (k, v)
ordering += '</select></form>'

footer = "</body></html>"

print header
print title
print subtitle
print ordering
print key
print table_data
print footer



