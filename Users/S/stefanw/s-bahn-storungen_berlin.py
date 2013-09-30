import lxml.html
from datetime import datetime
import re

import scraperwiki

prefix = "http://www.s-bahn-berlin.de/fahrplanundnetz/"
url = prefix + "mobilitaetsstoerungen.php"

root = lxml.html.parse(url).getroot()

types = ['elevator', 'escalator']

dates = []

count = 0
# Date is always the date/time of webpage retrival, argh
# store away anyhow.
for date in root.xpath('//table//table//tr/td[2]'):
    date = date.text.strip().split("Stand:")[1].strip()
    dates.append(datetime.strptime(date, "%d.%m.%Y %H:%M:%S"))


for i, table in enumerate(root.cssselect('table#Tabelle')):
    rows = table.cssselect("tr#Row")
    for row in rows:
        problem = {"type": types[i], "last_update": dates[i]}
        link = row.xpath("td[1]//a")
        if link:
            problem['name'] = link[0].text
            problem['href'] = prefix + link[0].attrib['href'] if 'href' in link[0].attrib else None
        location = row.xpath("td[2]")
        if location:
            problem['location'] = location[0].text.strip()
        extra = row.xpath("td[3]")
        if extra:
            problem['extra'] = extra[0].text
            if problem['extra']:
                problem['extra']= problem['extra'].strip()
            if not problem['extra']:
                problem['extra'] = None
        connecting_lines = row.xpath("td[4]//a")
        connecting = []
        for line in connecting_lines:
            connecting.append({"href": prefix + line.attrib.get('href') if 'href' in line.attrib else None,
                    "connecting": line.attrib.get('title'),
                    "line": line.text})
        other_lines = row.xpath("td[4]//img")
        for line in other_lines:
            connecting.append({"type": line.attrib.get('src', '').split('/')[-1].split('.')[0]})
        problem['lines'] = connecting
        scraperwiki.sqlite.save(unique_keys=['name', 'type'], data=problem)

bvg_url = "http://www.bvg.de/index.php/de/9466/name/Aufzugsmeldungen.html"
html = scraperwiki.scrape(bvg_url).decode('utf-8')
root = lxml.html.fromstring(html)

re_comment = re.compile(r'href="([^"]+)">(.*?)</a>')

trs = root.xpath('//table[@class="col2_tbl elevator_overview"]/tbody/tr')
for tr in trs:
    problem = {"type": "elevator"}
    tds = tr.xpath('td')
    if len(tds) > 0:
        problem["lines"] = [{"line": tds[0].xpath("span")[0].text, "href": None, "connecting": None}]
    if len(tds) > 1:
        problem["name"] = tds[1].text
    for c in tds[2]:
        match = re_comment.search(unicode(c))
        if match is not None:
            problem['href'] = match.group(1)
            problem["location"] = match.group(2)
    scraperwiki.sqlite.save(unique_keys=['name', 'type'], data=problem)
import lxml.html
from datetime import datetime
import re

import scraperwiki

prefix = "http://www.s-bahn-berlin.de/fahrplanundnetz/"
url = prefix + "mobilitaetsstoerungen.php"

root = lxml.html.parse(url).getroot()

types = ['elevator', 'escalator']

dates = []

count = 0
# Date is always the date/time of webpage retrival, argh
# store away anyhow.
for date in root.xpath('//table//table//tr/td[2]'):
    date = date.text.strip().split("Stand:")[1].strip()
    dates.append(datetime.strptime(date, "%d.%m.%Y %H:%M:%S"))


for i, table in enumerate(root.cssselect('table#Tabelle')):
    rows = table.cssselect("tr#Row")
    for row in rows:
        problem = {"type": types[i], "last_update": dates[i]}
        link = row.xpath("td[1]//a")
        if link:
            problem['name'] = link[0].text
            problem['href'] = prefix + link[0].attrib['href'] if 'href' in link[0].attrib else None
        location = row.xpath("td[2]")
        if location:
            problem['location'] = location[0].text.strip()
        extra = row.xpath("td[3]")
        if extra:
            problem['extra'] = extra[0].text
            if problem['extra']:
                problem['extra']= problem['extra'].strip()
            if not problem['extra']:
                problem['extra'] = None
        connecting_lines = row.xpath("td[4]//a")
        connecting = []
        for line in connecting_lines:
            connecting.append({"href": prefix + line.attrib.get('href') if 'href' in line.attrib else None,
                    "connecting": line.attrib.get('title'),
                    "line": line.text})
        other_lines = row.xpath("td[4]//img")
        for line in other_lines:
            connecting.append({"type": line.attrib.get('src', '').split('/')[-1].split('.')[0]})
        problem['lines'] = connecting
        scraperwiki.sqlite.save(unique_keys=['name', 'type'], data=problem)

bvg_url = "http://www.bvg.de/index.php/de/9466/name/Aufzugsmeldungen.html"
html = scraperwiki.scrape(bvg_url).decode('utf-8')
root = lxml.html.fromstring(html)

re_comment = re.compile(r'href="([^"]+)">(.*?)</a>')

trs = root.xpath('//table[@class="col2_tbl elevator_overview"]/tbody/tr')
for tr in trs:
    problem = {"type": "elevator"}
    tds = tr.xpath('td')
    if len(tds) > 0:
        problem["lines"] = [{"line": tds[0].xpath("span")[0].text, "href": None, "connecting": None}]
    if len(tds) > 1:
        problem["name"] = tds[1].text
    for c in tds[2]:
        match = re_comment.search(unicode(c))
        if match is not None:
            problem['href'] = match.group(1)
            problem["location"] = match.group(2)
    scraperwiki.sqlite.save(unique_keys=['name', 'type'], data=problem)
