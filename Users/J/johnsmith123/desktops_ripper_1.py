import scraperwiki
import requests
from lxml import html
import datetime
import sys
from cStringIO import StringIO
import hashlib

EXISTS = ()

# Last Known Page
KNOWN_PAGE = 35

# URL of the page
URL_PREFIX = "http://simpledesktops.com"

# Quit after QUIT_THRESHOLD existing images are found
QUIT_THRESHOLD = 3

# XPath for finding the image containers on the browse page
PAGE_XPATH = "//div[contains(@class, 'edge') and @class!='edge browse-ad']/div/a/@href"

# XPATH for finding the images links on the detail pages
DETAIL_XPATH = "//div/div[@class='edge']/div[@class='desktop']"

def browse_url(page=0):
    "Get a pages browse url"
    return "/".join((URL_PREFIX, "browse", str(page)))+"/"

def find_last_page(known_page=0):
    "Find the last page of images"
    current_page = known_page
    response = requests.head(browse_url(current_page))
    while response.status_code == 200:
        current_page += 1
        response = requests.head(browse_url(current_page))
    return current_page-1

def hash(file_obj, block_size=128):
    "Hash a file-like object"
    h = hashlib.sha1()
    file_obj.seek(0,0)
    data = file_obj.read(block_size)
    while data:
        h.update(data)
        data = file_obj.read(block_size)
    file_obj.seek(0,0)
    return h.hexdigest()

def fetch(url, parse_page=True):
    "Download a url and parse it's contents"
    page = requests.get(url)
    if parse_page:
        return page, html.document_fromstring(page.text)
    else:
        return page

def hash_url(url):
    "Hash a file, given it's url"
    f = fetch(url, parse_page=False)
    image_file = StringIO(f.content)
    fhash = hash(image_file)
    # Null out file to save memory
    image_file = None # probably unecciary
    return fhash

def parse_page(page_num):
    "Parse a browse page for links to detail pages"
    page, parsed = fetch(browse_url(page_num))
    detail_links = parsed.xpath(PAGE_XPATH)
    print len(detail_links), "Images found..."
    exists_counter = 0
    for link in detail_links:
        if parse_detail_page(link) == EXISTS:
            exists_counter += 1
        if exists_counter >= QUIT_THRESHOLD:
            print "Quit threshold reached, exiting..."
            sys.exit(0)

def parse_detail_page(detail_link):
    "Parse a detail page for image files"
    detail_page, parsed = fetch("".join((URL_PREFIX, detail_link)))
    detail_container = parsed.xpath(DETAIL_XPATH)[0]
        
    down_link = "".join((URL_PREFIX, detail_container.xpath("./h2/a/@href")[0]))
    name = detail_container.xpath("./h2/a/text()")[0]
    author = detail_container.xpath("./span/a/text()")[0]
    accessed = datetime.datetime.now().isoformat()
    fhash = hash_url(down_link)
    print "Loading", unicode(name).encode('ascii', 'replace')
    
    # Check to see if the image is a duplicate
    matches = db.select("id FROM images WHERE hash=?", (fhash,))
    if not matches:
        db.execute("""
            INSERT INTO images
                (name, author, url, accessed, hash)
                values (?,?,?,?,?)
        """, (name, author, down_link, accessed, fhash))
        db.commit()
    else:
        print fhash, "Already exists"
        return EXISTS

page_range = (1, find_last_page(KNOWN_PAGE))
db = scraperwiki.sqlite

# Make suret the table is set up
db.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name text,
        hash text,
        author text,
        url text,
        accessed text
    )
""")

#db.execute("DROP TABLE images;")
#print "Scraping from", page_range[0], "to", page_range[1]
for n in xrange(min(page_range), max(page_range)+1):
    print "Parsing page", n
    parse_page(n)

print "Done"













