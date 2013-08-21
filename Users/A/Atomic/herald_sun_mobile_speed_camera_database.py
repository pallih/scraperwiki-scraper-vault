import scraperwiki
import urlparse
import lxml.html

url = "http://www.heraldsunonline.com.au/dbs/speed_cameras/search.php"

print "Retrieving web page. Please wait...",
html = scraperwiki.scrape(url)
print "Done"

print "Doing work. Please wait..."
root = lxml.html.fromstring(html)
rows = root.cssselect("div#results table>tr")

rd_sec_prefix = 'between '
rd_sec_sep = ' and '
for i in range(len(rows)):
    data = rows[i].cssselect("td")
    if data:
        rd_sec_tmp = data[2].text
        rd_sec_start = ''
        rd_sec_end = ''

        if rd_sec_tmp.startswith(rd_sec_prefix):
            rd_sec_tmp = rd_sec_tmp[len(rd_sec_prefix):]

        rd_sec_tmp = rd_sec_tmp.split(rd_sec_sep, 1)
        if len(rd_sec_tmp) > 1:
            rd_sec_start = rd_sec_tmp[0].strip()
            rd_sec_end = rd_sec_tmp[1].strip()
        
        record = {
            'id' : i,
            'suburb' : data[0].text,
            'street' : data[1].text,
            'section_text' : data[2].text,
            'section_start' : rd_sec_start,
            'section_end' : rd_sec_end
        }

        scraperwiki.datastore.save(['id'], record)
