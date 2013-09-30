import scraperwiki

# Blank Python

import string
import lxml.html

def parsexml( root ):
    #<abbr title="January 7, 1905">07</abbr>
    for tr in root.cssselect('tbody tr'):
        tds = tr.cssselect('td')
        if len(tds)==13:
            elms = tds[0].getchildren()
          #  print "%-10s %3s" % (elms[0].tag, elms[0].get("title", "0"))
            date = string.split(elms[0].get("title", "0"))
            data = {
                'Month'   : date[0],
                'Year'    : date[2],
                'Date'    : elms[0].get("title", "0"),
                'maxTemp' : tds[1].text_content(),
                'minTemp' : tds[2].text_content()
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['Month','Year','Date'], data=data)

    count = 1
    for tr in root.cssselect('tfoot tr'):
        tds = tr.cssselect('td')
        if len(tds)==13:
            if count == 2:
                totals = {
                    'Month'   : date[0],
                    'Year'    : date[2],
                    'Date'    : "Averages",
                    'maxTemp' : tds[1].text_content(),
                    'minTemp' : tds[2].text_content(),
                    'meaTemp' : tds[3].text_content()
                }
                print totals
                scraperwiki.sqlite.save(unique_keys=['Month','Year','Date'], data=totals)
            elif count == 3:
                totals = {
                    'Month'   : date[0],
                    'Year'    : date[2],
                    'Date'    : "Extremes",
                    'maxTemp' : tds[1].text_content(),
                    'minTemp' : tds[2].text_content()
                }
                print totals
                scraperwiki.sqlite.save(unique_keys=['Month','Year','Date'], data=totals)

        count += 1

    return


years = ['2012']
for year in years:
    for month in range(1,12):
        html = scraperwiki.scrape("http://www.climate.weatheroffice.gc.ca/climateData/" + \
        "dailydata_e.html?timeframe=2&Prov=SASK&StationID=3328&dlyRange=1992-03-01|" + \
        "2012-02-30&Year="+str(year)+"&Month="+str(month)+"&Day=1")
    
        print html

        root = lxml.html.fromstring(html)
        parsexml(root)import scraperwiki

# Blank Python

import string
import lxml.html

def parsexml( root ):
    #<abbr title="January 7, 1905">07</abbr>
    for tr in root.cssselect('tbody tr'):
        tds = tr.cssselect('td')
        if len(tds)==13:
            elms = tds[0].getchildren()
          #  print "%-10s %3s" % (elms[0].tag, elms[0].get("title", "0"))
            date = string.split(elms[0].get("title", "0"))
            data = {
                'Month'   : date[0],
                'Year'    : date[2],
                'Date'    : elms[0].get("title", "0"),
                'maxTemp' : tds[1].text_content(),
                'minTemp' : tds[2].text_content()
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['Month','Year','Date'], data=data)

    count = 1
    for tr in root.cssselect('tfoot tr'):
        tds = tr.cssselect('td')
        if len(tds)==13:
            if count == 2:
                totals = {
                    'Month'   : date[0],
                    'Year'    : date[2],
                    'Date'    : "Averages",
                    'maxTemp' : tds[1].text_content(),
                    'minTemp' : tds[2].text_content(),
                    'meaTemp' : tds[3].text_content()
                }
                print totals
                scraperwiki.sqlite.save(unique_keys=['Month','Year','Date'], data=totals)
            elif count == 3:
                totals = {
                    'Month'   : date[0],
                    'Year'    : date[2],
                    'Date'    : "Extremes",
                    'maxTemp' : tds[1].text_content(),
                    'minTemp' : tds[2].text_content()
                }
                print totals
                scraperwiki.sqlite.save(unique_keys=['Month','Year','Date'], data=totals)

        count += 1

    return


years = ['2012']
for year in years:
    for month in range(1,12):
        html = scraperwiki.scrape("http://www.climate.weatheroffice.gc.ca/climateData/" + \
        "dailydata_e.html?timeframe=2&Prov=SASK&StationID=3328&dlyRange=1992-03-01|" + \
        "2012-02-30&Year="+str(year)+"&Month="+str(month)+"&Day=1")
    
        print html

        root = lxml.html.fromstring(html)
        parsexml(root)