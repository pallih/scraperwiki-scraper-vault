import lxml.html
import scraperwiki
import string

url = "http://www2.seattle.gov/fire/realTime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des"

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

print lxml.html.tostring(root, pretty_print=True)

# Build Table Schema
headers = root.xpath("/html/body/table/tr[2]/td/text()")

header_string = ""
header_sep = ""

clean_headers = []

for idx, header in enumerate(headers):
    header = filter(lambda x: x in string.letters, header)
    clean_headers.append(header)

    header_string = header_string + header_sep + header
    header_sep = ", "

print header_string

# Add data
datas = root.xpath("/html/body/table/tr[3]/td/table/tr/td/table/tr")

for data in datas:
    row = data.xpath("td/text()")

    row_string = ""
    row_sep = ""

    for item in row:
        row_string = row_string + row_sep + item
        row_sep = ", "

    print row_string

    scraperwiki.sqlite.save([clean_headers[1]], {clean_headers[0]:row[0], clean_headers[1]:row[1], clean_headers[2]:row[2], clean_headers[3]:row[3], clean_headers[4]:row[4] + ", Seattle, WA", clean_headers[5]:row[5]})import lxml.html
import scraperwiki
import string

url = "http://www2.seattle.gov/fire/realTime911/getRecsForDatePub.asp?action=Today&incDate=&rad1=des"

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

print lxml.html.tostring(root, pretty_print=True)

# Build Table Schema
headers = root.xpath("/html/body/table/tr[2]/td/text()")

header_string = ""
header_sep = ""

clean_headers = []

for idx, header in enumerate(headers):
    header = filter(lambda x: x in string.letters, header)
    clean_headers.append(header)

    header_string = header_string + header_sep + header
    header_sep = ", "

print header_string

# Add data
datas = root.xpath("/html/body/table/tr[3]/td/table/tr/td/table/tr")

for data in datas:
    row = data.xpath("td/text()")

    row_string = ""
    row_sep = ""

    for item in row:
        row_string = row_string + row_sep + item
        row_sep = ", "

    print row_string

    scraperwiki.sqlite.save([clean_headers[1]], {clean_headers[0]:row[0], clean_headers[1]:row[1], clean_headers[2]:row[2], clean_headers[3]:row[3], clean_headers[4]:row[4] + ", Seattle, WA", clean_headers[5]:row[5]})