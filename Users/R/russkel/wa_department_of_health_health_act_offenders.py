import scraperwiki, lxml.html, urllib2, re
from datetime import datetime

#html = scraperwiki.scrape("http://www.public.health.wa.gov.au/2/1035/2/publication_of_names_of_offenders_list.pm")
doc = lxml.html.parse(urllib2.urlopen("http://www.public.health.wa.gov.au/2/1035/2/publication_of_names_of_offenders_list.pm"))
root = doc.getroot()

#select the table that contains the offenders, ignoring the first one that contains the header row
for tr in root.xpath("//div[@id='verdiSection10']/div/div/table/tbody/tr")[1:]:
    data = {
        'conviction_date': datetime.strptime(
            re.match("(\d+/\d+/\d+)", tr[0].text_content().strip()).group(1),
            "%d/%m/%Y"), #sometimes they include two dates in the entry, so we'll have to grab the first (damnit)
        'business_name': tr[1].text_content().strip(),
        'business_address': tr[2].text_content().strip(),
        'convicted_name': tr[3].text_content().strip(),
        'agency': tr[4].text_content().strip(),
        'pdf': tr[5].xpath(".//a")[0].get("href")
    }
    
    scraperwiki.sqlite.save(unique_keys=['pdf'], data=data)
import scraperwiki, lxml.html, urllib2, re
from datetime import datetime

#html = scraperwiki.scrape("http://www.public.health.wa.gov.au/2/1035/2/publication_of_names_of_offenders_list.pm")
doc = lxml.html.parse(urllib2.urlopen("http://www.public.health.wa.gov.au/2/1035/2/publication_of_names_of_offenders_list.pm"))
root = doc.getroot()

#select the table that contains the offenders, ignoring the first one that contains the header row
for tr in root.xpath("//div[@id='verdiSection10']/div/div/table/tbody/tr")[1:]:
    data = {
        'conviction_date': datetime.strptime(
            re.match("(\d+/\d+/\d+)", tr[0].text_content().strip()).group(1),
            "%d/%m/%Y"), #sometimes they include two dates in the entry, so we'll have to grab the first (damnit)
        'business_name': tr[1].text_content().strip(),
        'business_address': tr[2].text_content().strip(),
        'convicted_name': tr[3].text_content().strip(),
        'agency': tr[4].text_content().strip(),
        'pdf': tr[5].xpath(".//a")[0].get("href")
    }
    
    scraperwiki.sqlite.save(unique_keys=['pdf'], data=data)
