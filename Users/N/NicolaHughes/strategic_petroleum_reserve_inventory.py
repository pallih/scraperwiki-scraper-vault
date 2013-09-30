import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.spr.doe.gov/dir/dir.html")
root = lxml.html.fromstring(html)
#CELLSPACING="0" BORDER="0" CELLPADDING="2"   DIR="LTR"

datecell = root.cssselect('table tr')[2].cssselect('td')[1]
datetext = datecell.text_content().strip()[len('INVENTORY AS OF '):]


for tr in root.cssselect('table[width="707"] tr')[4:]:
    tds = tr.cssselect("td")
    #print len(tds), tds
    #for i,t in enumerate(tds):
        #print 'Position', i, ' is ', t.text_content()

    if len(tds) >= 7 and tds[6].text_content() != '':
        data = {'Date' :datetext,'Sweet' : tds[1].text_content().strip(), 'Sour' : tds[2].text_content().strip(), 'Total' : tds[6].text_content().strip()}
        print data
        scraperwiki.sqlite.save(unique_keys=['Date'], data=data)import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.spr.doe.gov/dir/dir.html")
root = lxml.html.fromstring(html)
#CELLSPACING="0" BORDER="0" CELLPADDING="2"   DIR="LTR"

datecell = root.cssselect('table tr')[2].cssselect('td')[1]
datetext = datecell.text_content().strip()[len('INVENTORY AS OF '):]


for tr in root.cssselect('table[width="707"] tr')[4:]:
    tds = tr.cssselect("td")
    #print len(tds), tds
    #for i,t in enumerate(tds):
        #print 'Position', i, ' is ', t.text_content()

    if len(tds) >= 7 and tds[6].text_content() != '':
        data = {'Date' :datetext,'Sweet' : tds[1].text_content().strip(), 'Sour' : tds[2].text_content().strip(), 'Total' : tds[6].text_content().strip()}
        print data
        scraperwiki.sqlite.save(unique_keys=['Date'], data=data)