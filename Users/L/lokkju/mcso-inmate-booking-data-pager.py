#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import scraperwiki
import json
from datetime import datetime,timedelta
import os

sourcescraper = "mcso-inmate-booking-data-scraper"

limit = 200
offset = 0
key = os.getenv("URLQUERY")
perp = None
scraperwiki.sqlite.attach("mcso_inmate_booking_data_parse", "src")
base_url = "http://www.mcso.us/PAID/"
limit = 100
offset = 0

person_columns = ["p.name","p.age","p.gender","p.race","p.height","p.weight","p.eyes","p.hair"]
booking_columns = ["d.booking_id","d.swis_id","d.status","d.booking_date",
    "d.facility","d.arrest_date","d.arresting_agency","d.projected_release_date",
    "d.release_date"]
results = scraperwiki.sqlite.select("%s,%s,b.last_scrapedate FROM bookings b LEFT JOIN booking_detail d ON b.booking_id = d.booking_id" \
    " JOIN person p ON d.booking_id = p.booking_id WHERE d.booking_id=?" 
    % (",".join(person_columns),",".join(booking_columns)),(key,))
perp = results[0]

results = scraperwiki.sqlite.select("booking_id, MIN(booking_date) AS min_booking_date FROM booking_detail" \
    " WHERE booking_date > (SELECT booking_date FROM booking_detail WHERE booking_id = ?)" \
    " GROUP BY booking_date ORDER BY booking_date ASC LIMIT 1",(key,))
next_perp_id = results[0]["booking_id"] if results and results[0] else None
results = scraperwiki.sqlite.select("booking_id, MAX(booking_date) AS min_booking_date FROM booking_detail" \
    " WHERE booking_date < (SELECT booking_date FROM booking_detail WHERE booking_id = ?)" \
    " GROUP BY booking_date ORDER BY booking_date DESC LIMIT 1",(key,))
prev_perp_id = results[0]["booking_id"] if results and results[0] else None

def booking_dl():
    h = []
    h.append('<dl class="booking table-display">')
    h.append('    <dt>SWIS ID</dt><dd>%s&nbsp;</dd>' % perp.get('swis_id'))
    h.append('    <dt>Status</dt><dd>%s&nbsp;</dd>' % perp.get('status'))
    h.append('    <dt>Record Updated</dt><dd>%s&nbsp;</dd>' % perp.get('last_scrapedate'))
    h.append('    <dt>Booking Date<dt><dd>%s&nbsp;</dd>' % perp.get('booking_date'))
    h.append('    <dt>Facility<dt><dd>%s&nbsp;</dd>' % perp.get('facility'))
    h.append('    <dt>Arrest Date<dt><dd>%s&nbsp;</dd>' % perp.get('arrest_date'))
    h.append('    <dt>Arresting Agency<dt><dd>%s&nbsp;</dd>' % perp.get('arresting_agency'))
    h.append('    <dt>Projected Release Date<dt><dd>%s&nbsp;</dd>' % perp.get('projected_release_date'))
    h.append('    <dt>Actual Release Date<dt><dd>%s&nbsp;</dd>' % perp.get('release_date'))
    h.append('</dl>')
    return '\n'.join(h)

def person_dl():
    h = []
    h.append('<dl class="person">')
    h.append('    <dt>Name</dt><dd>%s&nbsp;</dd>' % person.get('name'))
    h.append('    <dt>Race</dt><dd>%s</dd>' % person.get('race'))
    h.append('    <dt>Gender</dt><dd>%s</dd>' % person.get('gender'))
    h.append('    <dt>Age</dt><dd>%s</dd>' % person.get('age'))
    h.append('    <dt>Height</dt><dd>%s</dd>' % person.get('height'))
    h.append('    <dt>Wieght</dt><dd>%s</dd>' % person.get('wieght'))
    h.append('    <dt>Eye Color</dt><dd>%s</dd>' % person.get('eyes'))
    h.append('    <dt>Hair Color</dt><dd>%s</dd>' % person.get('hair'))
    h.append('</dl>')
    return ''.join(h)

print """
<style>
dl.table-display{float: left;width: 620px;margin: 1em 0;padding: 0;border-bottom: 1px solid #999;}
.table-display dt{clear: left;float: left;width: 200px;margin: 0;padding: 5px;border-top: 1px solid #999;font-weight: bold;}
.table-display dd{float: left;width: 400px;margin: 0;padding: 5px;border-top: 1px solid #999;}
</style>
"""
print booking_dl()
#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import scraperwiki
import json
from datetime import datetime,timedelta
import os

sourcescraper = "mcso-inmate-booking-data-scraper"

limit = 200
offset = 0
key = os.getenv("URLQUERY")
perp = None
scraperwiki.sqlite.attach("mcso_inmate_booking_data_parse", "src")
base_url = "http://www.mcso.us/PAID/"
limit = 100
offset = 0

person_columns = ["p.name","p.age","p.gender","p.race","p.height","p.weight","p.eyes","p.hair"]
booking_columns = ["d.booking_id","d.swis_id","d.status","d.booking_date",
    "d.facility","d.arrest_date","d.arresting_agency","d.projected_release_date",
    "d.release_date"]
results = scraperwiki.sqlite.select("%s,%s,b.last_scrapedate FROM bookings b LEFT JOIN booking_detail d ON b.booking_id = d.booking_id" \
    " JOIN person p ON d.booking_id = p.booking_id WHERE d.booking_id=?" 
    % (",".join(person_columns),",".join(booking_columns)),(key,))
perp = results[0]

results = scraperwiki.sqlite.select("booking_id, MIN(booking_date) AS min_booking_date FROM booking_detail" \
    " WHERE booking_date > (SELECT booking_date FROM booking_detail WHERE booking_id = ?)" \
    " GROUP BY booking_date ORDER BY booking_date ASC LIMIT 1",(key,))
next_perp_id = results[0]["booking_id"] if results and results[0] else None
results = scraperwiki.sqlite.select("booking_id, MAX(booking_date) AS min_booking_date FROM booking_detail" \
    " WHERE booking_date < (SELECT booking_date FROM booking_detail WHERE booking_id = ?)" \
    " GROUP BY booking_date ORDER BY booking_date DESC LIMIT 1",(key,))
prev_perp_id = results[0]["booking_id"] if results and results[0] else None

def booking_dl():
    h = []
    h.append('<dl class="booking table-display">')
    h.append('    <dt>SWIS ID</dt><dd>%s&nbsp;</dd>' % perp.get('swis_id'))
    h.append('    <dt>Status</dt><dd>%s&nbsp;</dd>' % perp.get('status'))
    h.append('    <dt>Record Updated</dt><dd>%s&nbsp;</dd>' % perp.get('last_scrapedate'))
    h.append('    <dt>Booking Date<dt><dd>%s&nbsp;</dd>' % perp.get('booking_date'))
    h.append('    <dt>Facility<dt><dd>%s&nbsp;</dd>' % perp.get('facility'))
    h.append('    <dt>Arrest Date<dt><dd>%s&nbsp;</dd>' % perp.get('arrest_date'))
    h.append('    <dt>Arresting Agency<dt><dd>%s&nbsp;</dd>' % perp.get('arresting_agency'))
    h.append('    <dt>Projected Release Date<dt><dd>%s&nbsp;</dd>' % perp.get('projected_release_date'))
    h.append('    <dt>Actual Release Date<dt><dd>%s&nbsp;</dd>' % perp.get('release_date'))
    h.append('</dl>')
    return '\n'.join(h)

def person_dl():
    h = []
    h.append('<dl class="person">')
    h.append('    <dt>Name</dt><dd>%s&nbsp;</dd>' % person.get('name'))
    h.append('    <dt>Race</dt><dd>%s</dd>' % person.get('race'))
    h.append('    <dt>Gender</dt><dd>%s</dd>' % person.get('gender'))
    h.append('    <dt>Age</dt><dd>%s</dd>' % person.get('age'))
    h.append('    <dt>Height</dt><dd>%s</dd>' % person.get('height'))
    h.append('    <dt>Wieght</dt><dd>%s</dd>' % person.get('wieght'))
    h.append('    <dt>Eye Color</dt><dd>%s</dd>' % person.get('eyes'))
    h.append('    <dt>Hair Color</dt><dd>%s</dd>' % person.get('hair'))
    h.append('</dl>')
    return ''.join(h)

print """
<style>
dl.table-display{float: left;width: 620px;margin: 1em 0;padding: 0;border-bottom: 1px solid #999;}
.table-display dt{clear: left;float: left;width: 200px;margin: 0;padding: 5px;border-top: 1px solid #999;font-weight: bold;}
.table-display dd{float: left;width: 400px;margin: 0;padding: 5px;border-top: 1px solid #999;}
</style>
"""
print booking_dl()
