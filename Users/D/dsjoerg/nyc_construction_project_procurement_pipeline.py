import scraperwiki
import lxml.html

html = scraperwiki.scrape('http://www.nyc.gov/html/mocs/html/research/pipeline.shtml')
print html

root = lxml.html.fromstring(html)

for table in root.cssselect('table'):
    rows = table.cssselect('tr')
    if len(rows) > 0:
        cells_in_first_row = rows[0].cssselect('td')
        if len(cells_in_first_row) > 0 and cells_in_first_row[0].text_content() == "Estimated Bid Date":
            for row in rows:
                cells = row.cssselect('td')
                entries = [ cell.text_content() for cell in cells ]
                data = { "Estimated Bid Date" : entries[0],
                         "Agency" : entries[1],
                         "Trade" : entries[2],
                         "Project Description" : entries[3],
                         "Engineers Estimate" : entries[4],
                         "Subject to a PLA" : entries[5]
                       }
                scraperwiki.sqlite.save(["Estimated Bid Date", "Agency", "Trade", "Project Description"], data)

