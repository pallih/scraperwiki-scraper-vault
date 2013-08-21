import scraperwiki
import re

from BeautifulSoup import BeautifulSoup, Comment
from lxml import etree
from StringIO import StringIO

# Clear records before each run.
if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = "http://www.halifax.ca/Councillors/index.html"
soup = BeautifulSoup(scraperwiki.scrape(url))
links = soup.findAll("table", "side_links")[1].findAll("a")

def counc(i, url):
    contact = "http://www.halifax.ca/councillors/district" + str(i + 1).zfill(2) + "/contact.html"

    response = scraperwiki.scrape(contact)
    s = BeautifulSoup(response)

    match = re.search(r"District \d+\s*(.+)", ' '.join(h.text for h in s.findAll("h5")))
    if match is None:
        return
    else:
        district_name = match.group(1)

    # remove comments
    comments = s.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    record = {}
    record['source_url'] = url
    record['elected_office'] = 'Councillor'

    c = s.find("td", id="content_main")
    t = c.text

    name = ' '.join(t.split('District')[0].split(' ')[1:])
    name = re.sub(r'\s+', ' ', name)
    record['name'] = name.strip()

    record['district_id'] = i + 1
    record['district_name'] = district_name

    a = c.findAll('a')[0]
    record['email'] = a.text.replace('[at]', '@').lower()

    scraperwiki.sqlite.save(['name'], record)


for i in range(0, len(links)):
    counc(i, links[i]['href'])

# mayor

url = "http://www.halifax.ca/mayor/"
s = BeautifulSoup(scraperwiki.scrape(url))

# remove comments
comments = s.findAll(text=lambda text:isinstance(text, Comment))
[comment.extract() for comment in comments]



record = {}
record["elected_office"] = "Mayor"
record["name"] = s.find("section", {"class":"left_col"}).findAll("h1")[1].text.replace("Bio","").strip()
record["source_url"] = url
record["boundary_url"] = '/boundaries/census-subdivisions/1209034/'

url = "http://www.halifax.ca/mayor/Contact.php"
s = BeautifulSoup(scraperwiki.scrape(url))
td = s.findAll("p")[1]

record["email"] = td.find("a").text

scraperwiki.sqlite.save(['name'], record)