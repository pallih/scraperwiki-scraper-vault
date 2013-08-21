import math
import scraperwiki
import lxml.html

keyword = 'health'
stub = 'http://www.crunchbase.com/search?query=' + keyword + '&page='

page = 1
rpp = 7

# Functions

def parse_company(url):
  html = scraperwiki.scrape(url)
  root = lxml.html.fromstring(html)
  name = get_name(root)
  funding = get_funding(root)
  data = parse(url, name, funding)
  save(data)

def get_name(root):
  return root.cssselect("h1[class='h1_first']")[0].text_content()[:-5] # [:-5] is due to "edit" being appended to the name

def get_funding(root):
  has_funding = "No"
  for element in root.cssselect("h2"):
    if "Funding" in element.text_content():
      has_funding = "Yes"
  return has_funding

def parse(url, name, funding):
  data = {
    'url': url,
    'name': name,
    'funding': funding
  }
  return data

def save(data):
  scraperwiki.sqlite.save(unique_keys=['url'], data = data)

# Get total number of pages

try:
  url = stub + '1'
  html = scraperwiki.scrape(url)
  root = lxml.html.fromstring(html)
  for element in root.cssselect("div[class='pagination'] a"):
    if not "Next" in element.text_content():
      total = element.text_content()
except:
  total = 1

limit = math.ceil(int(total)/rpp) + 1

# Process the companies

try:
  while page <= limit:
    url = stub + str(page)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for element in root.cssselect("div[class='search_result_name'] a"):
      url = "http://www.crunchbase.com" + element.attrib["href"]
      parse_company(url)
    page += 1
except:   
  print "There was an error."
  exit