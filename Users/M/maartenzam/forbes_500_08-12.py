import scraperwiki
import lxml.html 

rooturl = "http://money.cnn.com/magazines/fortune/global500/"

for year in range(2005, 2013):
    print year
    for urlrank in range(0, 5):
        
        if (urlrank == 0 and year > 2005):
            urltoscrape = rooturl + str(year) + '/full_list/' + 'index.html'
        elif (urlrank == 0 and year < 2006):
            urltoscrape = rooturl + str(year) + '/index.html'
        elif (urlrank > 0 and year < 2006):
            start = urlrank*100 + 1
            end = urlrank*100 + 100
            urltoscrape = rooturl + str(year) + '/' + str(start) + '_' + str(end) + '.html'
        else:
            start = urlrank*100 + 1
            end = urlrank*100 + 100
            urltoscrape = rooturl + str(year) + '/full_list/' + str(start) + '_' + str(end) + '.html'
        
        print urltoscrape
        
        html = scraperwiki.scrape(urltoscrape)
          
        root = lxml.html.fromstring(html)
    
        if year == 2008:
            selector = 'table.with220inset tr'
        elif year == 2005:
            selector = 'table.f500table tr'
        elif (year == 2006 or year == 2007):
            selector = 'table.maglisttable tr'
        else:
            selector = 'table.cnnwith220inset tr'
        
        for tr in root.cssselect(selector):
            tds = tr.cssselect("td")
            if tds:
                key = str(year)+"," + tds[1].text_content()
                data = {
                  'Key' : key,
                  'Year' : year,
                  'Rank' : tds[0].text_content(),
                  'Revenue': tds[2].text_content().replace(",", ""),
                  'Profits': tds[3].text_content().replace(",", "")
                }
                scraperwiki.sqlite.save(unique_keys=['Key'], data=data)