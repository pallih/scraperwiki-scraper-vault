import scraperwiki
import lxml.html

url = "http://www.atsb.gov.au/publications/safety-investigation-reports.aspx"

#all reports
#queryString = "s=1&mode=Aviation&sort=OccurrenceReleaseDate&sortAscending=descending&printAll=true&occurrenceClass=&typeOfOperation=&initialTab="

#newest 20 reports
queryString = "s=1&mode=Aviation&sort=OccurrenceDate&sortAscending=descending&investigationStatus=&occurrenceClass=&typeOfOperation=&initialTab="

html = scraperwiki.scrape(url + "?" + queryString)

root = lxml.html.fromstring(html)
for tr in root.cssselect("table[class='selectable_grid'] tr"):
    tds = tr.cssselect("td")
    if len(tds) == 5:
        data = { 
            'details_link' : "http://www.atsb.gov.au" + tds[0].cssselect("a")[0].attrib['href'],
            'investigation_number' : tds[0].text_content(),
            'description' : tds[1].text_content(),
            'occurence_date' : tds[2].text_content(),
            'report_status' : tds[3].text_content(),
            'release_date' : tds[4].text_content()
        }
        scraperwiki.sqlite.save(unique_keys = ['investigation_number'], data = data)

