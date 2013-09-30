sourcescraper = 'mcso_inmate_booking_data_parse'
import scraperwiki
import os
import json
import sys
import urllib
import datetime
from pygooglechart import PieChart3D,PieChart2D

scraperwiki.sqlite.attach("mcso_inmate_booking_data_parse", "src")
base_url = "http://www.mcso.us/PAID/"

booked = 0

end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(7)

result = scraperwiki.sqlite.select("count(booking_id) FROM booking_detail WHERE booking_date <= ? AND booking_date >= ?",
    (end_date.strftime("%s"),start_date.strftime("%s")))
booked = result[0]["count(booking_id)"]

eyes = scraperwiki.sqlite.select("p.eyes as k,count(p.eyes) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))
gender = scraperwiki.sqlite.select("p.gender as k,count(p.gender) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))
race = scraperwiki.sqlite.select("p.race as k,count(p.race) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))
hair = scraperwiki.sqlite.select("p.hair as k,count(p.hair) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))

arresting_agency = scraperwiki.sqlite.select("d.arresting_agency as k,count(d.arresting_agency) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))

charges = scraperwiki.sqlite.select("c.charge as k,count(c.charge) as v FROM charge c" \
    " LEFT JOIN 'case' ON 'case'.id = c.case_id" \
    " LEFT JOIN booking_detail d ON 'case'.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))

def piechart(d):
    #medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    keys = []
    values = []
    vcount = sum(e.get("v") for e in d)
    for i in range(min(5, len(d))):
        keys.append("%s (%s%%)" % (d[i]["k"],d[i]["v"]*100/vcount ))
        values.append(d[i]["v"])
    if len(d) > 5:
        val = sum(e.get("v") for e in d[5:])
        values.append(val)
        keys.append("All Other (%s%%)" % (val*100/vcount))
    chart = PieChart2D(380, 180)
    chart.add_data(values)
    chart.set_legend(keys)
    return chart.get_url()


print '''
<style>
#stats {text-align: center;}
#stats table {border-collapse: collapse; width: 850px; margin: 0px auto;}
#stats td { border: 1px solid black; }
#stats td {text-align: center;}
</style>
'''
print '<div id="stats">'
print "<h2>Booking & Arrest Statistics for Multnomah County Sheriff's Office<br/>%s through %s</h2>" % (start_date.date(),end_date.date())
print '<table width="100%">'
print '<tr><td colspan="2">Total People Booked:%s</td></tr>' % (booked,)
print '<tr><td><h3>Arresting Agencies</h3><img src="%s"/></td><td><h3>Charges</h3><img src="%s"/></td></tr>' % (piechart(arresting_agency),piechart(charges))
print '<tr><td><h3>Gender</h3><img src="%s"/></td><td><h3>Race</h3><img src="%s"/></td>' % (piechart(gender),piechart(race))
print '<tr><td><h3>Eye Color</h3><img src="%s"/></td><td><h3>Hair Color</h3><img src="%s"/></td>' % (piechart(eyes),piechart(hair))
print '</table>'
print '</div>'sourcescraper = 'mcso_inmate_booking_data_parse'
import scraperwiki
import os
import json
import sys
import urllib
import datetime
from pygooglechart import PieChart3D,PieChart2D

scraperwiki.sqlite.attach("mcso_inmate_booking_data_parse", "src")
base_url = "http://www.mcso.us/PAID/"

booked = 0

end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(7)

result = scraperwiki.sqlite.select("count(booking_id) FROM booking_detail WHERE booking_date <= ? AND booking_date >= ?",
    (end_date.strftime("%s"),start_date.strftime("%s")))
booked = result[0]["count(booking_id)"]

eyes = scraperwiki.sqlite.select("p.eyes as k,count(p.eyes) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))
gender = scraperwiki.sqlite.select("p.gender as k,count(p.gender) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))
race = scraperwiki.sqlite.select("p.race as k,count(p.race) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))
hair = scraperwiki.sqlite.select("p.hair as k,count(p.hair) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))

arresting_agency = scraperwiki.sqlite.select("d.arresting_agency as k,count(d.arresting_agency) as v FROM person p" \
    " LEFT JOIN booking_detail d ON p.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))

charges = scraperwiki.sqlite.select("c.charge as k,count(c.charge) as v FROM charge c" \
    " LEFT JOIN 'case' ON 'case'.id = c.case_id" \
    " LEFT JOIN booking_detail d ON 'case'.booking_id = d.booking_id" \
    " WHERE d.booking_date <= ? AND d.booking_date >= ? GROUP BY k ORDER BY v DESC"
    ,(end_date.strftime("%s"),start_date.strftime("%s")))

def piechart(d):
    #medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    keys = []
    values = []
    vcount = sum(e.get("v") for e in d)
    for i in range(min(5, len(d))):
        keys.append("%s (%s%%)" % (d[i]["k"],d[i]["v"]*100/vcount ))
        values.append(d[i]["v"])
    if len(d) > 5:
        val = sum(e.get("v") for e in d[5:])
        values.append(val)
        keys.append("All Other (%s%%)" % (val*100/vcount))
    chart = PieChart2D(380, 180)
    chart.add_data(values)
    chart.set_legend(keys)
    return chart.get_url()


print '''
<style>
#stats {text-align: center;}
#stats table {border-collapse: collapse; width: 850px; margin: 0px auto;}
#stats td { border: 1px solid black; }
#stats td {text-align: center;}
</style>
'''
print '<div id="stats">'
print "<h2>Booking & Arrest Statistics for Multnomah County Sheriff's Office<br/>%s through %s</h2>" % (start_date.date(),end_date.date())
print '<table width="100%">'
print '<tr><td colspan="2">Total People Booked:%s</td></tr>' % (booked,)
print '<tr><td><h3>Arresting Agencies</h3><img src="%s"/></td><td><h3>Charges</h3><img src="%s"/></td></tr>' % (piechart(arresting_agency),piechart(charges))
print '<tr><td><h3>Gender</h3><img src="%s"/></td><td><h3>Race</h3><img src="%s"/></td>' % (piechart(gender),piechart(race))
print '<tr><td><h3>Eye Color</h3><img src="%s"/></td><td><h3>Hair Color</h3><img src="%s"/></td>' % (piechart(eyes),piechart(hair))
print '</table>'
print '</div>'