import scraperwiki 
import requests
import lxml.html
from datetime import datetime, date, timedelta

gc_project = 'ostinato'

#
# scrape and get today's cumulative download count
#
r = requests.get('http://code.google.com/p/' + gc_project + '/downloads/list?can=1&sort=uploaded&colspec=Filename+DownloadCount') 
doc = lxml.html.document_fromstring(r.text)
downloads = doc.xpath("//tr[@class='ifOpened']")
data = {'Date':date.today(), 'Timestamp':datetime.utcnow()}
for d in downloads:
    #print(lxml.html.tostring(d, pretty_print=True))
    filename = d[1].text_content().strip().replace('.', '_')
    count = d[2].text_content().strip()
    data[filename] = count
print data

#
# retrieve yesterday's cumulative download count and subtract from today's to get the day's download count
#
diff_data = {}
try:
    last_data_list = scraperwiki.sqlite.select("* from swdata where Date=(select max(Date) from swdata where Date < '" + date.today().isoformat() + "')")
    last_data = last_data_list[0]
    print last_data
    diff_data['Date'] = date.today()
    for k,v in data.iteritems():
        if (k == 'Date' or k == 'Timestamp'):
            continue;
        last_v = last_data.get(k, '0')
        diff_data[k] = int(v) - int(last_v)
    print diff_data
except scraperwiki.sqlite.SqliteError, e:
    print str(e) 

#
# save to datastore
#
scraperwiki.sqlite.save(unique_keys=['Date'], data=data) 
if (len(diff_data)):
    scraperwiki.sqlite.save(unique_keys=['Date'], data=diff_data, table_name='downloads')
