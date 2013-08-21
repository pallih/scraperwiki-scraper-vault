import scraperwiki
import urllib2
import lxml.html

years = range(1950,2011)
baseurl = 'http://www.airdisaster.com/cgi-bin/view_year.cgi?year='
xpath ='//tr/td/table/tr/td/table/.'
for year in years:
    print year
    url = baseurl + str(year)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    root = lxml.html.fromstring(html)
    for tr in root.xpath(xpath)[1:]:
        record = {}
        record['date'] =  tr[0][0][0][0][0].text
        record['url'] =   'http://www.airdisaster.com/cgi-bin/' + tr[0][0][0][0][0].get('href')
        record['airline'] =   tr[0][1][0].text
        record['aircraft_type'] =   tr[0][2][0].text
        fatalities = tr[0][3][0].text
        record['fatalities_on_board'] =   fatalities.partition(':')[0]
        record['total_passengers'] =   fatalities.partition(':')[2]
        record['fatalities_on_ground'] =   fatalities.partition('+')[2]
        if fatalities.rfind('+') > 0:
            record['fatalities_on_ground'] =   fatalities.partition('+')[2]
            record['fatalities_on_board'] =   fatalities.partition(':')[0]
            record['total_passengers'] =   fatalities.partition(':')[2].partition('+')[0]
        record['location'] =   tr[1][1][0].text
        record['registration'] =   tr[1][2][0].text
        #print tr[1][3][0].text
        scraperwiki.sqlite.save(['date'], data=record, table_name='airdisasters')
