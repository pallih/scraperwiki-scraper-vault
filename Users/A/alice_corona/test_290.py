import scraperwiki
import requests
import lxml.html
import mechanize
url = 'http://www.interpol.int/Wanted-Persons/(wanted_id)/2013-19960'
html = requests.get(url).text
br = mechanize.Browser()
br.set_handle_robots(False)
root = lxml.html.fromstring(html)
info = []

for tr in root.cssselect("td[class='col2 strong']"):
       info.append(tr.text_content())
data = {
    'Surname' : info[0],
    'Name' : info[1],
    'Sex' : info[2],
    'Date of Birth': info[3],
    'Place of Birth': info[4],
    'Language(s) Spoken' : info [5],
    'Nationality' : info [6],
    'Charges' :info [-1],
    'Link' : url
        }
scraperwiki.sqlite.save(unique_keys = ['Link'], data=data)

print data
print len(info)
