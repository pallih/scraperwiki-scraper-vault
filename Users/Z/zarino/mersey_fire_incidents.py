import scraperwiki
import requests
import lxml.html
from datetime import datetime

debug = True

def log(message):
    if debug:
        print message

def save():
    global incidents
    log('saving %s incidents: %s' % (len(incidents), incidents))
    scraperwiki.sqlite.save(['id'], incidents, 'incidents')
    incidents = []

incidents = []
errors_in_a_row = 0

# trick the ScraperWiki screenshooter into giving us a pretty screenshot
requests.get('http://www.merseyfire.gov.uk/aspx/pages/Incidents/IncidentDetailsList.aspx')

try:
    # pick up where the last run left off
    i = scraperwiki.sqlite.select('id from incidents order by id desc limit 1')[0]['id'] + 1
except scraperwiki.sqlite.SqliteError:
    # start from scratch
    i = 1

# allow for 20 non-existent incidents in a row
while errors_in_a_row < 20:
    log('scraping incident %s' % i)
    html = requests.get('http://www.merseyfire.gov.uk/aspx/pages/Incidents/IncidentDetail.aspx?id=%s' % i).text
    dom = lxml.html.fromstring(html)
    if dom.cssselect('#ctl00_ContentPlaceHolderMain_FormView1_IncTitleLabel'):
        errors_in_a_row = 0
        incidents.append({
            'id': i,
            'title': dom.cssselect('#ctl00_ContentPlaceHolderMain_FormView1_IncTitleLabel')[0].text,
            'date': dom.cssselect('#ctl00_ContentPlaceHolderMain_FormView1_IncDateLabel')[0].text,
            'location': dom.cssselect('#ctl00_ContentPlaceHolderMain_FormView1_IncLocationLabel')[0].text,
            'description': dom.cssselect('#ctl00_ContentPlaceHolderMain_FormView1_IncTextLabel')[0].text,
            'date_scraped': datetime.now()
        })
    else:
        log('-- incident %s does not exist' % i)
        errors_in_a_row += 1

    i += 1

    # save to the datastore once we've got 10 rows
    if len(incidents) == 10:
        save()

# any incidents left? save them.
if len(incidents):
    save()

log('done')

