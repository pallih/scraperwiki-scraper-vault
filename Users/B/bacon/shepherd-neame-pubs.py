import scraperwiki
import mechanize
import re
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Name', 'Address', 'Geocode', 'Telephone', 'Description', 'Image', 'ListingPage', 'Website', 'OpenHours', 'Live Sky Sports', 'Food', 'Accommodation', 'Outdoor Area', 'Historic Building', 'Real Fire', 'Function Room', 'Live Music'])

commentregex = re.compile( '<!--[^-->]*-->')

pub_urls = []

def scrape_links(soup):
    buttons = soup.findAll("a", { "class" : "link-full-details" })
    for button in buttons:
        pub_urls.append(button.get("href"))

def scrape_and_look_for_next_link(soup):
    scrape_links(soup)
    print len(pub_urls)
    next_link = soup.find("a", { "id" : "ctl00_mainContent_linkNextPage" })
    if next_link:
        br.select_form(name='aspnetForm')
        br.form.set_all_readonly(False)
        br.form.find_control('ctl00$mainContent$btnSearchExtended').disabled=True
        br['__EVENTTARGET'] = 'ctl00$mainContent$linkNextPage'
        br['__EVENTARGUMENT'] = ''
        br.submit()
        soup = BeautifulSoup(br.response().read())
        scrape_and_look_for_next_link(soup)

def scrape_pub(pub_url):
    record = {}
    record['Live Sky Sports'] = False
    record['Food'] = False
    record['Accommodation'] = False
    record['Outdoor Area'] = False
    record['Historic Building'] = False
    record['Real Fire'] = False
    record['Function Room'] = False
    record['Live Music'] = False
    record['ListingPage'] = base_url + pub_url
    html = scraperwiki.scrape(base_url + pub_url)
    soup = BeautifulSoup(html)
    title = soup.find("h1", { "class" : "navigation-header" })
    if title:
        record['Name'] = title.text
    adr = soup.find("span", { "class" : "adr" })
    if adr:
        address = adr.find("span", { "class" : "street-address" }).text + " "
        address = address + adr.find("span", { "class" : "locality" }).text + " "
        address = address + adr.find("span", { "class" : "region" }).text + " "
        postcode = adr.find("span", { "class" : "postal-code" }).text
        address = address + postcode
        record['Address'] = address
        record['Geocode'] = scraperwiki.geo.gb_postcode_to_latlng(postcode)
    telephone = soup.find("span", { "class" : "tel" })
    if telephone:
        record['Telephone'] = telephone.text
    descr_parent = soup.find("div", { "class" : "pub-description" })
    if descr_parent:
        descr_parts = descr_parent.findAll("p")
        descr = "";
        for descr_part in descr_parts:
            descr = descr + commentregex.sub( '', descr_part.text) + "\n"
        record['Description'] = descr
    image = soup.find("img", { "id" : "ctl00_mainContent_imgPubHeroImage" })
    if image:
        if image.get("src").startswith("http://"):
            record['Image'] = image.get("src")
        else:
            record['Image'] = "http://www.shepherdneame.co.uk" + image.get("src")
    website = soup.find("a", { "id" : "ctl00_mainContent_linkPubWebsite" })
    if website:
        record['Website'] = website.get("href")
    openhours = soup.find("div", { "id" : "pub-opening" })
    if openhours:
        record['OpenHours'] = openhours.find("dl").renderContents()
    facilities = soup.find("div", { "id" : "pub-facilities" }).findAll("li")
    for facility in facilities:
        record[facility.text] = 'True'
    scraperwiki.datastore.save(["Name"], record)


# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_url = 'http://www.shepherdneame.co.uk'
starting_url = base_url + '/pub-search.aspx'
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
soup = BeautifulSoup(br.response().read())
search_button = soup.find("input", { "id" : "ctl00_mainContent_btnSearchExtended" })
if search_button:
    br.select_form(name='aspnetForm')
    br.submit()
    soup = BeautifulSoup(br.response().read())
    scrape_and_look_for_next_link(soup)
    print "Found ",
    print len(pub_urls),
    print " pubs"
    for pub_url in pub_urls:
        scrape_pub(pub_url)
else:
    print "could not submit search form"





