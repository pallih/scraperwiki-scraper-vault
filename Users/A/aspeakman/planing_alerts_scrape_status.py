import scraperwiki
import urllib, urllib2
import json
import cgi
from datetime import date

util = scraperwiki.utils.swimport("utility_library")

DBS = {
    'East England': "east_england_planning_applications",
    'East Midlands': "east_midlands_planning_applications",
    'London': "london_planning_applications",
    'Northern Ireland': "northern_ireland_planning_applications",
    'North East': "north_east_planning_applications",
    'North West': "north_west_planning_applications",
    'Scotland': "scotland_planning_applications",
    'South East': "south_east_planning_applications",
    'South West': "south_west_planning_applications",
    'Wales': "wales_planning_applications",
    'West Midlands': "west_midlands_planning_applications",
    'Yorkshire and Humber': "yorkshire_planning_applications"
    }

default_db = 'London'

query = scraperwiki.utils.GET()

dbase = query.get('db', default_db)

auth_get = query.get('auth', '')
cfg_get = query.get('cfg', '')

try:
    scraperwiki.sqlite.attach(DBS.get(dbase), 'db')
except:
    dbase = default_db
    scraperwiki.sqlite.attach(DBS.get(dbase), 'db')

scraperwiki.sqlite.attach("planning_authorities", 'cfg')

# get latest runtime information for this scraper
run_info = None
run_url = "https://api.scraperwiki.com/api/1.0/scraper/getruninfo?format=jsondict&name=" + DBS.get(dbase)
result = json.load(urllib2.urlopen(run_url, None, 10))  # 10 sec timeout
if result:
    run_info = result[0]

print "<html><head>"

print '<style type="text/css">'+util.base_css()+'</style>'

print """<script type="text/javascript">
function showhide(divId)
{
    if(document.getElementById(divId).style.display == 'none')
        {
        document.getElementById(divId).style.display = 'block';
        }
    else
        {
        document.getElementById(divId).style.display = 'none';
        }
}
</script>"""

print "</head><body>"

print '<h1><a href="?db='+dbase+'">UK Planning Applications</a></h1>'


if auth_get:
    auth_data = util.get_table_vals('db.authorities', 'long_name, scrape_date_type', "name = '"+auth_get+"'")
    name = auth_data[0]['long_name']
    date_type = auth_data[0]['scrape_date_type']
    order = 'order by received_date desc, reference asc'
    today = date.today().strftime(util.ISO8601_DATE)
    four_months_ago, st = util.inc_dt(today, util.ISO8601_DATE, -120)
    eight_months_ago, st = util.inc_dt(today, util.ISO8601_DATE, -240)
    #print '<p>', today, four_months_ago, eight_months_ago, '</p>'
    if date_type == 'validated':
        order = 'order by validated_date desc, reference asc'
    app_data1 = util.get_table_vals('applications', '', "authority='"+auth_get+"' and (lng is null or lat is null or (received_date is null and validated_date is null) or (received_date is not null and received_date not like '%-%') or (validated_date is not null and validated_date not like '%-%'))", order)
    app_data3 = util.get_table_vals('applications', '', "authority='"+auth_get+"'", order+' limit 10')
    app_data2 = util.get_table_vals('applications', '', "authority='"+auth_get+"' and ((validated_date is not null and validated_date < '"+four_months_ago+"') or (validated_date is null and received_date is not null and received_date < '"+eight_months_ago+"'))", order+' limit 10')
    for i in range(1,4):
        app = None
        if i == 1:
            if len(app_data1) == 0: continue
            print "<h2>"+name+" "+str(len(app_data1))+" Applications With Missing Location Data Or Bad Dates</h2>"
            app = app_data1
        elif i == 2:
            if len(app_data2) == 0: continue
            print "<h2>"+name+" "+str(len(app_data2))+" Expired Applications (validated before "+four_months_ago+" or received before "+eight_months_ago+")</h2>"
            app = app_data2
        else:
            print "<h2>"+name+" 10 Most Recent Applications</h2>"
            app = app_data3
        print '<table>'
        print "<tr><th>Authority</th><th>Received</th><th>Validated</th><th>Reference</th><th>Address</th><th>Description</th><th>Postcode</th><th>Lat</th><th>Lng</th></tr>"
        for d in app:
            print "<tr>"
            print "<td>", d["authority"], "</td>"
            if d["received_date"]:
                print "<td>", d["received_date"], "</td>"
            else:
                print "<td>Null/Empty</td>"
            if d["validated_date"]:
                print "<td>", d["validated_date"], "</td>"
            else:
                print "<td>Null/Empty</td>"
            print '<td><a href="'+d["info_url"]+'">', d["reference"], "</a></td>" 
            print "<td>", d["address"], "</td>" 
            print "<td>", d["description"], "</td>"
            print "<td>", d["postcode"], "</td>" 
            print "<td>", d["lat"], "</td>" 
            print "<td>", d["lng"], "</td>" 
            print "</tr>"
        print "</table>" 

elif cfg_get:
    auth_list = util.get_table_vals('cfg.authorities', 'name, long_name, region', "config = '"+cfg_get+"'", 'order by name')
    config_list = util.get_table_vals('cfg.configurations', '', '', 'order by name')
    config_map = util.get_map(config_list, 'name')
    cfg_key = config_map['_Key']
    cfg_data = config_map[cfg_get]
    parent = ''
    cfg_parent = {}
    if cfg_data.get('parent'):
        parent = ' - ' + cfg_data['parent']
        cfg_parent = util.dict_inherited(config_map, cfg_data['parent'])
    cfg_plus = util.dict_inherited(config_map, cfg_get)
    del cfg_plus['name']
    print "<h2>Configuration Settings</h2>"
    print '<form method="get" name="form2"><strong>Configuration:</strong>&nbsp;<select name="cfg" id="cfg" onchange="this.form.submit()">'
    for i in config_list:
        if i['name'] != '_Key':
            sel = ''
            if i['name'] == cfg_get: sel = 'selected="selected" '
            print '<option '+sel+'value="'+i['name']+'">'+i['name']+'</option>'
    print '</select></form>'
    print '<h4>List of authorities using this configuration:</h4><p>'
    for i in auth_list:
        print i['name'], ' (' , i['region'], '), '
    print "</p><table>" 
    print '<tr><th>Config</th><th>Key</th><th>Local Settings - '+cfg_get+'</th><th>Inherited Settings'+parent+'</th></tr>'
    if cfg_plus:
        cfgkeys = cfg_plus.keys()
        cfgkeys.sort()
        for j in cfgkeys:
            if cfg_plus.get(j):
                if not cfg_parent.get(j):
                    parent_val = ''
                else:
                    parent_val = cfg_parent.get(j)
                if not cfg_data.get(j):
                    local_val = ''
                else:
                    local_val = cfg_data.get(j)
                print "<tr><td>", j, "</td>"
                print "<td><small>"+cfg_key.get(j)+"</small></td>"
                print "<td><pre>"+cgi.escape(local_val)+"</pre></td>"
                if local_val and parent_val:
                    print "<td><del><pre>"+cgi.escape(parent_val)+"</pre></del></td></tr>"
                else:
                    print "<td><pre>"+cgi.escape(parent_val)+"</pre></td></tr>"
    print "</table>" 

else:
    today = date.today().strftime(util.ISO8601_DATE)
    two_weeks_ago, st = util.inc_dt(today, util.ISO8601_DATE, -14)
    four_weeks_ago, st = util.inc_dt(today, util.ISO8601_DATE, -28)
    app_data = scraperwiki.sqlite.select("authority, count(*) as records, min(received_date) as rmin, max(received_date) as rmax , min(validated_date) as vmin, max(validated_date) as vmax from db.applications group by authority order by authority")
    apps = {}
    num_applics = 0
    for d in app_data:
        apps[d['authority']] = d
        num_applics += d['records']
    #print apps
    auth_data = util.get_table_vals('db.authorities', '', '', 'order by name')
    print "<h2>Authorities Scraper Status</h2>"
    print '<form method="get" name="form1"><strong>Region:</strong>&nbsp;<select name="db" id="db" onchange="this.form.submit()">'
    sortdbs = DBS.keys()
    sortdbs.sort()
    for i in sortdbs: 
        sel = ''
        if i == dbase: sel = 'selected="selected" '
        print '<option '+sel+'value="'+i+'">'+i+'</option>'
    #print '</select>&nbsp;<input type="submit" value="Change" /></form>'
    print '</select></form>'
    print "<h3>Totals: "+str(len(auth_data))+" authorities, "+str(num_applics)+" applications</h3>"
    if run_info:
        started = run_info.get('run_ended')
        cvt_date = util.convert_dt(started, "%Y-%m-%dT%H:%M:%S", "%A, %d %B %Y at %H:%M:%S")
        print """<h4>Last run on <a href="javascript:showhide('runinfo')">"""+cvt_date+"</a></h4>"
        print '<pre id="runinfo" style="display: none;">'+run_info.get('output')+"</pre>"
    print '<table>'
    print '<tr><th colspan="2">Planning Authority</th><th colspan="4">Scraping Sequence</th><th colspan="5">Stored Applications</th><th colspan="5">Last Scrape</th></tr>'
    print "<tr><th>Name</th><th>Config</th><th>Type</th><th>Started</th><th>Reached</th><th>Total</th><th>Earliest Received</th><th>Latest Received</th><th>Earliest Validated</th><th>Latest Validated</th><th>Records Count</th><th>Date</th><th>Status</th><th>Count</th><th>Match Count</th><th>Message</th></tr>"
    for d in auth_data: 
        auth = d["name"]
        if d.get('search_url'): # show the user friendly version by default
            auth_url = d["search_url"]
        elif d.get('scrape_url'): # otherwise use the working version 
            auth_url = d["scrape_url"]
        elif d.get('base_url'):
            auth_url = d["base_url"]
        else:
            auth_url = d["start_url"]
        print "<tr>" 
        print '<td><a href="'+auth_url+'">', auth, "</a>"
        if d.get('scraper'):
            print ' <a href="https://scraperwiki.com/views/'+d['scraper']+'">*</a></td>'
        else:
            print '</td>'
        # print "<td>", d["region"], "</td>" 
        #print "<td>", d["config"], "</td>" 
        print '<td><a href="?cfg='+urllib.quote_plus(d["config"])+'">', d["config"], "</a></td>"
        if d.get("scrape_date_type"):
            print "<td>", d["scrape_date_type"].capitalize(), "</td>" 
        else:
            print "<td></td>"
        started = util.convert_dt(d["start_date"], util.ISO8601_DATE, util.DATE_FORMAT)
        reached = util.convert_dt(d["last_date"], util.ISO8601_DATE, util.DATE_FORMAT)
        print "<td>", started, "</td>"
        if d["last_date"] < four_weeks_ago:
            print '<td style="background-color:red;">', reached, "</td>" 
        elif d["last_date"] < two_weeks_ago:
            print '<td style="background-color:yellow;">', reached, "</td>" 
        else:
            print '<td style="background-color:green;">', reached, "</td>" 
        print "<td>", d.get("total", "0"), "</td>"
        if auth in apps:
            rmin = apps[auth]["rmin"]
            if rmin:
                dmin = util.convert_dt(rmin, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmin == rmin: dmin = dmin+'*'
            else:
                dmin = 'Null/Empty'
            rmax = apps[auth]["rmax"]
            if rmax:
                dmax = util.convert_dt(rmax, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmax == rmax: dmax = dmax+'*'
            else:
                dmax = 'Null/Empty'
            print "<td>", dmin, "</td>"
            print "<td>", dmax, "</td>"
            vmin = apps[auth]["vmin"]
            if vmin:
                dmin = util.convert_dt(vmin, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmin == vmin: dmin = dmin+'*'
            else:
                dmin = 'Null/Empty'
            vmax = apps[auth]["vmax"]
            if vmax:
                dmax = util.convert_dt(vmax, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmax == vmax: dmax = dmax+'*'
            else:
                dmax = 'Null/Empty'
            print "<td>", dmin, "</td>"
            print "<td>", dmax, "</td>"
            print "<td>", apps[auth]["records"], "</td>"
        else:
            print '<td colspan="5" />'
        dscrape = util.convert_dt(d["last_scrape"], util.ISO8601_DATE, util.DATE_FORMAT)
        print "<td>", dscrape, "</td>" 
        print '<td><a href="?auth='+urllib.quote_plus(auth)+'&db='+urllib.quote_plus(dbase)+'">', d["last_status"], "</a></td>"
        print "<td>", d["last_count"], "</td>"
        print "<td>", d["last_match_count"], "</td>"
        print "<td>", cgi.escape(d["last_msg"]), "</td>"
        print "</tr>" 
    print "</table>" 

print "</body></html>"

import scraperwiki
import urllib, urllib2
import json
import cgi
from datetime import date

util = scraperwiki.utils.swimport("utility_library")

DBS = {
    'East England': "east_england_planning_applications",
    'East Midlands': "east_midlands_planning_applications",
    'London': "london_planning_applications",
    'Northern Ireland': "northern_ireland_planning_applications",
    'North East': "north_east_planning_applications",
    'North West': "north_west_planning_applications",
    'Scotland': "scotland_planning_applications",
    'South East': "south_east_planning_applications",
    'South West': "south_west_planning_applications",
    'Wales': "wales_planning_applications",
    'West Midlands': "west_midlands_planning_applications",
    'Yorkshire and Humber': "yorkshire_planning_applications"
    }

default_db = 'London'

query = scraperwiki.utils.GET()

dbase = query.get('db', default_db)

auth_get = query.get('auth', '')
cfg_get = query.get('cfg', '')

try:
    scraperwiki.sqlite.attach(DBS.get(dbase), 'db')
except:
    dbase = default_db
    scraperwiki.sqlite.attach(DBS.get(dbase), 'db')

scraperwiki.sqlite.attach("planning_authorities", 'cfg')

# get latest runtime information for this scraper
run_info = None
run_url = "https://api.scraperwiki.com/api/1.0/scraper/getruninfo?format=jsondict&name=" + DBS.get(dbase)
result = json.load(urllib2.urlopen(run_url, None, 10))  # 10 sec timeout
if result:
    run_info = result[0]

print "<html><head>"

print '<style type="text/css">'+util.base_css()+'</style>'

print """<script type="text/javascript">
function showhide(divId)
{
    if(document.getElementById(divId).style.display == 'none')
        {
        document.getElementById(divId).style.display = 'block';
        }
    else
        {
        document.getElementById(divId).style.display = 'none';
        }
}
</script>"""

print "</head><body>"

print '<h1><a href="?db='+dbase+'">UK Planning Applications</a></h1>'


if auth_get:
    auth_data = util.get_table_vals('db.authorities', 'long_name, scrape_date_type', "name = '"+auth_get+"'")
    name = auth_data[0]['long_name']
    date_type = auth_data[0]['scrape_date_type']
    order = 'order by received_date desc, reference asc'
    today = date.today().strftime(util.ISO8601_DATE)
    four_months_ago, st = util.inc_dt(today, util.ISO8601_DATE, -120)
    eight_months_ago, st = util.inc_dt(today, util.ISO8601_DATE, -240)
    #print '<p>', today, four_months_ago, eight_months_ago, '</p>'
    if date_type == 'validated':
        order = 'order by validated_date desc, reference asc'
    app_data1 = util.get_table_vals('applications', '', "authority='"+auth_get+"' and (lng is null or lat is null or (received_date is null and validated_date is null) or (received_date is not null and received_date not like '%-%') or (validated_date is not null and validated_date not like '%-%'))", order)
    app_data3 = util.get_table_vals('applications', '', "authority='"+auth_get+"'", order+' limit 10')
    app_data2 = util.get_table_vals('applications', '', "authority='"+auth_get+"' and ((validated_date is not null and validated_date < '"+four_months_ago+"') or (validated_date is null and received_date is not null and received_date < '"+eight_months_ago+"'))", order+' limit 10')
    for i in range(1,4):
        app = None
        if i == 1:
            if len(app_data1) == 0: continue
            print "<h2>"+name+" "+str(len(app_data1))+" Applications With Missing Location Data Or Bad Dates</h2>"
            app = app_data1
        elif i == 2:
            if len(app_data2) == 0: continue
            print "<h2>"+name+" "+str(len(app_data2))+" Expired Applications (validated before "+four_months_ago+" or received before "+eight_months_ago+")</h2>"
            app = app_data2
        else:
            print "<h2>"+name+" 10 Most Recent Applications</h2>"
            app = app_data3
        print '<table>'
        print "<tr><th>Authority</th><th>Received</th><th>Validated</th><th>Reference</th><th>Address</th><th>Description</th><th>Postcode</th><th>Lat</th><th>Lng</th></tr>"
        for d in app:
            print "<tr>"
            print "<td>", d["authority"], "</td>"
            if d["received_date"]:
                print "<td>", d["received_date"], "</td>"
            else:
                print "<td>Null/Empty</td>"
            if d["validated_date"]:
                print "<td>", d["validated_date"], "</td>"
            else:
                print "<td>Null/Empty</td>"
            print '<td><a href="'+d["info_url"]+'">', d["reference"], "</a></td>" 
            print "<td>", d["address"], "</td>" 
            print "<td>", d["description"], "</td>"
            print "<td>", d["postcode"], "</td>" 
            print "<td>", d["lat"], "</td>" 
            print "<td>", d["lng"], "</td>" 
            print "</tr>"
        print "</table>" 

elif cfg_get:
    auth_list = util.get_table_vals('cfg.authorities', 'name, long_name, region', "config = '"+cfg_get+"'", 'order by name')
    config_list = util.get_table_vals('cfg.configurations', '', '', 'order by name')
    config_map = util.get_map(config_list, 'name')
    cfg_key = config_map['_Key']
    cfg_data = config_map[cfg_get]
    parent = ''
    cfg_parent = {}
    if cfg_data.get('parent'):
        parent = ' - ' + cfg_data['parent']
        cfg_parent = util.dict_inherited(config_map, cfg_data['parent'])
    cfg_plus = util.dict_inherited(config_map, cfg_get)
    del cfg_plus['name']
    print "<h2>Configuration Settings</h2>"
    print '<form method="get" name="form2"><strong>Configuration:</strong>&nbsp;<select name="cfg" id="cfg" onchange="this.form.submit()">'
    for i in config_list:
        if i['name'] != '_Key':
            sel = ''
            if i['name'] == cfg_get: sel = 'selected="selected" '
            print '<option '+sel+'value="'+i['name']+'">'+i['name']+'</option>'
    print '</select></form>'
    print '<h4>List of authorities using this configuration:</h4><p>'
    for i in auth_list:
        print i['name'], ' (' , i['region'], '), '
    print "</p><table>" 
    print '<tr><th>Config</th><th>Key</th><th>Local Settings - '+cfg_get+'</th><th>Inherited Settings'+parent+'</th></tr>'
    if cfg_plus:
        cfgkeys = cfg_plus.keys()
        cfgkeys.sort()
        for j in cfgkeys:
            if cfg_plus.get(j):
                if not cfg_parent.get(j):
                    parent_val = ''
                else:
                    parent_val = cfg_parent.get(j)
                if not cfg_data.get(j):
                    local_val = ''
                else:
                    local_val = cfg_data.get(j)
                print "<tr><td>", j, "</td>"
                print "<td><small>"+cfg_key.get(j)+"</small></td>"
                print "<td><pre>"+cgi.escape(local_val)+"</pre></td>"
                if local_val and parent_val:
                    print "<td><del><pre>"+cgi.escape(parent_val)+"</pre></del></td></tr>"
                else:
                    print "<td><pre>"+cgi.escape(parent_val)+"</pre></td></tr>"
    print "</table>" 

else:
    today = date.today().strftime(util.ISO8601_DATE)
    two_weeks_ago, st = util.inc_dt(today, util.ISO8601_DATE, -14)
    four_weeks_ago, st = util.inc_dt(today, util.ISO8601_DATE, -28)
    app_data = scraperwiki.sqlite.select("authority, count(*) as records, min(received_date) as rmin, max(received_date) as rmax , min(validated_date) as vmin, max(validated_date) as vmax from db.applications group by authority order by authority")
    apps = {}
    num_applics = 0
    for d in app_data:
        apps[d['authority']] = d
        num_applics += d['records']
    #print apps
    auth_data = util.get_table_vals('db.authorities', '', '', 'order by name')
    print "<h2>Authorities Scraper Status</h2>"
    print '<form method="get" name="form1"><strong>Region:</strong>&nbsp;<select name="db" id="db" onchange="this.form.submit()">'
    sortdbs = DBS.keys()
    sortdbs.sort()
    for i in sortdbs: 
        sel = ''
        if i == dbase: sel = 'selected="selected" '
        print '<option '+sel+'value="'+i+'">'+i+'</option>'
    #print '</select>&nbsp;<input type="submit" value="Change" /></form>'
    print '</select></form>'
    print "<h3>Totals: "+str(len(auth_data))+" authorities, "+str(num_applics)+" applications</h3>"
    if run_info:
        started = run_info.get('run_ended')
        cvt_date = util.convert_dt(started, "%Y-%m-%dT%H:%M:%S", "%A, %d %B %Y at %H:%M:%S")
        print """<h4>Last run on <a href="javascript:showhide('runinfo')">"""+cvt_date+"</a></h4>"
        print '<pre id="runinfo" style="display: none;">'+run_info.get('output')+"</pre>"
    print '<table>'
    print '<tr><th colspan="2">Planning Authority</th><th colspan="4">Scraping Sequence</th><th colspan="5">Stored Applications</th><th colspan="5">Last Scrape</th></tr>'
    print "<tr><th>Name</th><th>Config</th><th>Type</th><th>Started</th><th>Reached</th><th>Total</th><th>Earliest Received</th><th>Latest Received</th><th>Earliest Validated</th><th>Latest Validated</th><th>Records Count</th><th>Date</th><th>Status</th><th>Count</th><th>Match Count</th><th>Message</th></tr>"
    for d in auth_data: 
        auth = d["name"]
        if d.get('search_url'): # show the user friendly version by default
            auth_url = d["search_url"]
        elif d.get('scrape_url'): # otherwise use the working version 
            auth_url = d["scrape_url"]
        elif d.get('base_url'):
            auth_url = d["base_url"]
        else:
            auth_url = d["start_url"]
        print "<tr>" 
        print '<td><a href="'+auth_url+'">', auth, "</a>"
        if d.get('scraper'):
            print ' <a href="https://scraperwiki.com/views/'+d['scraper']+'">*</a></td>'
        else:
            print '</td>'
        # print "<td>", d["region"], "</td>" 
        #print "<td>", d["config"], "</td>" 
        print '<td><a href="?cfg='+urllib.quote_plus(d["config"])+'">', d["config"], "</a></td>"
        if d.get("scrape_date_type"):
            print "<td>", d["scrape_date_type"].capitalize(), "</td>" 
        else:
            print "<td></td>"
        started = util.convert_dt(d["start_date"], util.ISO8601_DATE, util.DATE_FORMAT)
        reached = util.convert_dt(d["last_date"], util.ISO8601_DATE, util.DATE_FORMAT)
        print "<td>", started, "</td>"
        if d["last_date"] < four_weeks_ago:
            print '<td style="background-color:red;">', reached, "</td>" 
        elif d["last_date"] < two_weeks_ago:
            print '<td style="background-color:yellow;">', reached, "</td>" 
        else:
            print '<td style="background-color:green;">', reached, "</td>" 
        print "<td>", d.get("total", "0"), "</td>"
        if auth in apps:
            rmin = apps[auth]["rmin"]
            if rmin:
                dmin = util.convert_dt(rmin, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmin == rmin: dmin = dmin+'*'
            else:
                dmin = 'Null/Empty'
            rmax = apps[auth]["rmax"]
            if rmax:
                dmax = util.convert_dt(rmax, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmax == rmax: dmax = dmax+'*'
            else:
                dmax = 'Null/Empty'
            print "<td>", dmin, "</td>"
            print "<td>", dmax, "</td>"
            vmin = apps[auth]["vmin"]
            if vmin:
                dmin = util.convert_dt(vmin, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmin == vmin: dmin = dmin+'*'
            else:
                dmin = 'Null/Empty'
            vmax = apps[auth]["vmax"]
            if vmax:
                dmax = util.convert_dt(vmax, util.ISO8601_DATE, util.DATE_FORMAT)
                if dmax == vmax: dmax = dmax+'*'
            else:
                dmax = 'Null/Empty'
            print "<td>", dmin, "</td>"
            print "<td>", dmax, "</td>"
            print "<td>", apps[auth]["records"], "</td>"
        else:
            print '<td colspan="5" />'
        dscrape = util.convert_dt(d["last_scrape"], util.ISO8601_DATE, util.DATE_FORMAT)
        print "<td>", dscrape, "</td>" 
        print '<td><a href="?auth='+urllib.quote_plus(auth)+'&db='+urllib.quote_plus(dbase)+'">', d["last_status"], "</a></td>"
        print "<td>", d["last_count"], "</td>"
        print "<td>", d["last_match_count"], "</td>"
        print "<td>", cgi.escape(d["last_msg"]), "</td>"
        print "</tr>" 
    print "</table>" 

print "</body></html>"

