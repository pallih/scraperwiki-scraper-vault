import scraperwiki
import lxml.html

#TO DO
#Run through archive
#Daily scrape of daily page probably not useful?
#instead, do a daily scrape of the top archive item?
def dailyScraper(url='http://www.syfire.gov.uk/1684.asp'):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    tables=root.findall('.//table')
    print tables

    rows = tables[0].findall('.//tr')
    day=rows[0].find('th').text
    day=day.replace('DAILY SUMMARY ','')
    print day
    
    for row in rows[1:]:
        data={'day':day}
        txt=[]
        cells= row.findall('td')
        data['type']=cells[0].text
        data['count']=cells[1].text
        print data
        #scraperwiki.sqlite.save(table_name='dailySummary', data=data)
    rows = tables[1].findall('tbody/tr')
    for row in rows[1:]:
        txt=[]
        cells= row.findall('td')
        data={'day':day}
        data['number']=cells[0].text
        data['time']=cells[1].text
        data['addr']=cells[2].text
        data['desc']=cells[3].text
        for srow in cells[4].findall('.//tr'):
            data2=data
            scells=srow.findall('td')
            data2['appliance']=scells[0].text
            data2['endtime']=scells[1].text
            print data2
            #scraperwiki.sqlite.save(table_name='dailyEvents', data=data2)

        


dailyScraper()