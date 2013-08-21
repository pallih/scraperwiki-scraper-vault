import scraperwiki
import lxml.html

for sch in range(950,8000):
    html = scraperwiki.scrape("http://www.churchofengland.org/education/your-local-school/school-details.aspx?id=" + str(sch))
    
    root = lxml.html.fromstring(html)

    try:
        title = root.cssselect("div[id='schoolscontainer']")[0].cssselect("h2")[0].text_content().strip()
    
        data = {
            'id': sch,
            'title' : title,
        }
    
        content = root.cssselect(".schooldetails p")[0].text_content().split('\r\n')
        for x in content:
            y = x.split(':')
            if len(y) > 1:
                data[y[0].strip()] = y[1].strip()
    
        #print data
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

    except:
        print "School No. %d failed" % sch

    


