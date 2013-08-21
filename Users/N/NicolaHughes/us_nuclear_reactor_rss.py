import scraperwiki
import uuid

scraperwiki.sqlite.attach('us_nuclear_power_reactor_status_reports')

old_datastore = scraperwiki.sqlite.execute("select 'http://www.nrc.gov/reading-rm/doc-collections/event-status/reactor-status/' as link, `unit` as 'title', `reason or comment` as 'reason', `date` as 'date', Power from us_nuclear_power_reactor_status_reports.swdata where `Reason or Comment` like '%#%' order by date desc limit 20")



old_datastore['keys'].append('description')
old_datastore['keys'].append('guid')

for item in old_datastore['data']:

    item.append('On %s, %s reactor had power output of %s because %s' % (item[3], item[1], item[4], item[2]))
    guid = str( uuid.uuid4() )
    item.append(guid)
    row = dict(zip(old_datastore['keys'], item))

    scraperwiki.sqlite.save(["date", "title"], row)

#print old_datastore