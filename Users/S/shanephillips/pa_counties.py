import scraperwiki
import lxml.html
        
html = scraperwiki.scrape("http://sites.state.pa.us/govlocal.html")
         
root = lxml.html.fromstring(html)
for a in root.xpath("//td//li/a"):

        municipality = a.xpath("normalize-space(.)")
        link = a.xpath("@href")[0]
        status = ""
        county = a.xpath("normalize-space(./..)") # get the parent LI text
        county = county.replace(municipality, "") # remove the muni name (it gets captured with the <A> text
        county = county.replace(",", "").strip()  # replace the first comma and trim whitespace

        data = {
            "municipality" : municipality, 
            "county" : county,
            "link" : link, 
            "status" : status 
        }

        try:
            #sub_html = scraperwiki.scrape(data['href'])
            data['status'] = 'OK'
        except:
            data['status'] = 'DEAD'
            print 'DEAD: ' + data['href'] 

        scraperwiki.sqlite.save(unique_keys=["municipality"], data=data, table_name="pa_municipalities", verbose=2) 
        print data

import scraperwiki
import lxml.html
        
html = scraperwiki.scrape("http://sites.state.pa.us/govlocal.html")
         
root = lxml.html.fromstring(html)
for a in root.xpath("//td//li/a"):

        municipality = a.xpath("normalize-space(.)")
        link = a.xpath("@href")[0]
        status = ""
        county = a.xpath("normalize-space(./..)") # get the parent LI text
        county = county.replace(municipality, "") # remove the muni name (it gets captured with the <A> text
        county = county.replace(",", "").strip()  # replace the first comma and trim whitespace

        data = {
            "municipality" : municipality, 
            "county" : county,
            "link" : link, 
            "status" : status 
        }

        try:
            #sub_html = scraperwiki.scrape(data['href'])
            data['status'] = 'OK'
        except:
            data['status'] = 'DEAD'
            print 'DEAD: ' + data['href'] 

        scraperwiki.sqlite.save(unique_keys=["municipality"], data=data, table_name="pa_municipalities", verbose=2) 
        print data

