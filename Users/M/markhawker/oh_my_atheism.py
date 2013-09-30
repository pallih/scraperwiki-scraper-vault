import math
import scraperwiki
import lxml.html

stub = 'http://www.guardian.co.uk/commentisfree/commentisfree+world/atheism?page='

page = 1
rpp = 15

# Functions

def month_lookup(month):
  months = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
  }
  return months[month]

def parse(date, title, url):
  pieces = date.split(" ")
  day = pieces[0]
  month = month_lookup(pieces[1])
  year = pieces[2][:-1]
  data = {
    'day': day,
    'month': month,
    'year': year,
    'title': title,
    'url': url
  }
  return data

def save(data):
  scraperwiki.sqlite.save(unique_keys=['url'], data = data)

# Get total number of articles

try:
  url = stub + '1'
  html = scraperwiki.scrape(url)
  root = lxml.html.fromstring(html)
  for element in root.cssselect("p[class='explainer']"):
    string = element.text_content()
    pieces = string.split(" ")
    total = int(pieces[1])
except:
  total = 1000;

limit = math.ceil(total/rpp) + 1

# Process the articles

try:
  while page <= limit:
    url = stub + str(page)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    i = 0;
    for element in root.cssselect("div[id='content'] span[class='date']"):
      date = element.text_content()
      title = root.cssselect("ul[id='cif-auto-trail-block'] li h3")[i].text_content()
      url = root.cssselect("ul[id='cif-auto-trail-block'] li h3 a")[i].attrib["href"]
      data = parse(date, title, url)
      save(data)
      i += 1
    page += 1
except:   
  print "There was an error."
  exit;import math
import scraperwiki
import lxml.html

stub = 'http://www.guardian.co.uk/commentisfree/commentisfree+world/atheism?page='

page = 1
rpp = 15

# Functions

def month_lookup(month):
  months = {
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
  }
  return months[month]

def parse(date, title, url):
  pieces = date.split(" ")
  day = pieces[0]
  month = month_lookup(pieces[1])
  year = pieces[2][:-1]
  data = {
    'day': day,
    'month': month,
    'year': year,
    'title': title,
    'url': url
  }
  return data

def save(data):
  scraperwiki.sqlite.save(unique_keys=['url'], data = data)

# Get total number of articles

try:
  url = stub + '1'
  html = scraperwiki.scrape(url)
  root = lxml.html.fromstring(html)
  for element in root.cssselect("p[class='explainer']"):
    string = element.text_content()
    pieces = string.split(" ")
    total = int(pieces[1])
except:
  total = 1000;

limit = math.ceil(total/rpp) + 1

# Process the articles

try:
  while page <= limit:
    url = stub + str(page)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    i = 0;
    for element in root.cssselect("div[id='content'] span[class='date']"):
      date = element.text_content()
      title = root.cssselect("ul[id='cif-auto-trail-block'] li h3")[i].text_content()
      url = root.cssselect("ul[id='cif-auto-trail-block'] li h3 a")[i].attrib["href"]
      data = parse(date, title, url)
      save(data)
      i += 1
    page += 1
except:   
  print "There was an error."
  exit;