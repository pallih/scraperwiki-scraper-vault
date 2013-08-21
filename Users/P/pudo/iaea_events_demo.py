import scraperwiki
from lxml import html

url = "http://www-news.iaea.org/EventList.aspx"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text) 

for row in doc.cssselect("#tblEvents tr"):
    #print row.cssselect("h4 a")
    link_in_header = row.cssselect("h4 a")
    print link_in_header
    link_in_header = link_in_header[0]
    print link_in_header
    event_title = link_in_header.text
    print event_title

    event_link = link_in_header.get('href')
    #date_section = row.cssselect(".float-right-margin").pop()
    #event_place_and_date = date_section.text
    #place, date = event_place_and_date.split(', ', 1)
    #print place + " + " + date

