import lxml.html          
import scraperwiki 
import dateutil.parser 
import unicodedata as ud

# download one page 

html = scraperwiki.scrape( "http://spring96.org/persecution/?DateFrom=2000-01-01&DateTo=2014-12-31&print=all" )
root = lxml.html.fromstring(html.decode("UTF-8"))

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) > 2:
        data = {
            'Number' : int(tds[0].text_content()),
            'Name' : tds[1].text_content().strip(),
            'Comment' : tds[len(tds)-1].text_content().strip()
        }
        for entry in tds[2].cssselect("tr"):
            detail = entry.cssselect("td")
            key = '';
            if detail[0].text_content().strip() == 'Суд'.decode("UTF-8"):
                key = 'Court'
            if detail[0].text_content().strip() == 'Дата затрыманьня'.decode("UTF-8"):
                key = 'Date_Arrest'
            if detail[0].text_content().strip() == 'Дата суда'.decode("UTF-8"):
                key = 'Date_Court'
            if detail[0].text_content().strip() == 'Арышт (сут.)'.decode("UTF-8"):
                key = 'Days_Arrest'
            if detail[0].text_content().strip() == 'Судзьдзя'.decode("UTF-8"):
                key = 'Judge'
            if detail[0].text_content().strip() == 'Штраф (б.в.)'.decode("UTF-8"):
                key = 'Fine_Units'
            if detail[0].text_content().strip() == 'Штраф (руб.)'.decode("UTF-8"):
                key = 'Fine_Roubles'
            if key != '':
                data[key] = detail[1].text_content().strip()
        scraperwiki.sqlite.save(unique_keys=['Number'], data=data)





