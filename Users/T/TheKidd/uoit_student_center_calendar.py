import scraperwiki
import lxml.html

scraperwiki.sqlite.save_var("pos", 1)
i= scraperwiki.sqlite.get_var("pos", 0)
try:
    while True:
        html = scraperwiki.scrape("http://www.your-sa.ca/events/calendar.htm?action=displayGlobalEventDetails&eventId=" + str(i))
        root = lxml.html.fromstring(html)
        lines = root.cssselect("div.twoThirdsBox div.row div")

        data = {'id': i}
        data['name'] = lines[0].text_content().encode('latin-1','ignore').replace("’","'").strip("\t\r\n ")
        data['from'] = lines[1].text_content().split("to")[0].strip("\t\r\n ")
        data['to'] = lines[1].text_content().split("to")[1].strip("\t\r\n ")
        data['location'] = lines[2].text_content().strip("\t\r\n ")
        print data
        
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        i+=1
except Exception as inst:
    print inst
finally:
    scraperwiki.sqlite.save_var("pos", i)