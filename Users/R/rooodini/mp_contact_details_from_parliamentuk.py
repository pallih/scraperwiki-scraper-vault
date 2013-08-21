import logging, re, scraperwiki, time, urllib2

MAX_RETRIES = 5


def latlng_from_postcode(postcode):
    retries = 0
    delay_seconds = 1
    while True:
        try:
            return scraperwiki.geo.gb_postcode_to_latlng(postcode)
        except:
            if retries >= MAX_RETRIES:
                raise
            retries += 1
            logging.info("Failed to retrieve valid JSON from geo.gb_postcode_to_latlng")
            time.sleep(delay_seconds)
            delay_seconds *=2

def extract_contact_details(para):
    """Extract contact details from the paragraph.
    """
    r = {}
    
    address_mo = re.match(r'^\s+([^<]+)', para, re.DOTALL)
    r["address"] = address_mo.group(1)
    
    tel_mo = re.search(r'Tel: ([\d\s-]+)', para)
    if tel_mo:
        r["phone"] = tel_mo.group(1).replace("-", " ")
    
    fax_mo = re.search(r'Fax: ([\d\s-]+)', para)
    if fax_mo:
        r["fax"] = fax_mo.group(1).replace("-", " ")
    
    email_mo = re.search(r'mailto:([^"]+)', para)
    if email_mo:
        r["email"] = email_mo.group(1)
    
    url_mo = re.search(r'(https?:[^"]+)', para)
    if url_mo:
        r["url"] = url_mo.group(1)
    
    return r

def scrape(url):
    """The scraperwiki.scrape function sometimes raises an HTTPError,
    apparently at random, with no further information. This function
    retries a limited number of times in such cases, with exponential
    back-off.
    """
    
    # Escape non-ASCII characters
    # url = re.sub(r"[^\0-\177]", lambda mo: "%%%2X" % ord(mo.group(0)), url)
    
    retries = 0
    delay_seconds = 1
    while True:
        try:
            return scraperwiki.scrape(url)
        except urllib2.HTTPError:
            if retries >= MAX_RETRIES:
                raise
            retries += 1
            logging.info("Failed to fetch %s on attempt %d", url, retries)
            time.sleep(delay_seconds)
            delay_seconds *= 2

# This page lists all the MPs, with links to the biography pages
list_page = scrape("http://www.parliament.uk/mps-lords-and-offices/mps/")

# For each MP, fetch the biography and extract the contact information
found = False
for list_mo in re.finditer(r'href="(.*?/biographies[^"]+)"', list_page):
    found = True
    mp_url = list_mo.group(1).replace('&#39;', '')
    try:
        mp_page = scrape(mp_url)
    except:
        logging.exception("Failed to fetch %s", mp_url)
        continue
    
    # Get the name of the MP
    name_mo = re.search(r'<h1>(?:<!--(?:[^-]|-[^-])+-->|\s)*(.+?)(?:<!--(?:[^-]|-[^-])+-->|\s)*</h1>', mp_page, re.DOTALL)
    if not name_mo:
        logging.error("Could not find name for %s", mp_url)
        continue
    name = name_mo.group(1)
    name = re.sub(r'&#(\d+);', lambda mo: unichr(int(mo.group(1))), name)
    
    # Separate the title (Mr, Mrs, etc) from the name
    name_parts_mo = re.match(r'((?:Mr|Mrs|Miss|Ms|Dr|Prof|Sir|Rt Hon(?:\s+Sir)?))\s+(.+)', name)
    if name_parts_mo:
        title, name = name_parts_mo.group(1), name_parts_mo.group(2)
    else:
        title = None
    
    # Constituency
    constituency_mo = re.search(r'<h3 class[^>]*>Constituency</h3>\s+<p>([^<]+)</p>', mp_page, re.DOTALL)
    if not constituency_mo:
        logging.error("Could not find constituency for %s", mp_url)
        continue
    constituency = constituency_mo.group(1)
    
    # Party
    party_mo = re.search(r'<h3[^>]*>Party</h3>\s+<p>([^<]+)</p>', mp_page, re.DOTALL)
    if not party_mo:
        logging.error("Could not find party for %s", mp_url)
        continue
    party = party_mo.group(1)
    
    # How to address the MP in question, e.g. "Lady Herman", "Mr Bercow", "Prime Minister"
    address_as_mo = re.search(r'<h3[^>]*>Address as</h3>\s+<p>([^<]+)</p>', mp_page, re.DOTALL)
    if not address_as_mo:
        logging.warn('Could not find "Address as" for %s', mp_url)
        address_as = None
    else:
        address_as = address_as_mo.group(1)
    
    # Get Westminster contact details
    westminster_mo = re.search(r'<h3 id[^>]*>Parliamentary</h3>\s+<p>((?:[^<]+|<[^/]|</[^p])*)</p>', mp_page)
    if not westminster_mo:
        logging.warn("Could not find Westminster contact details for %s", mp_url)
        westminster_contact_details = {}
    else:
        westminster_contact_details = extract_contact_details(westminster_mo.group(1))
    
    # Get constituency contact details
    constituency_mo = re.search(r'<h3 id[^>]*>Constituency</h3>\s+<p>((?:[^<]+|<[^/]|</[^p])*)</p>', mp_page)
    if not constituency_mo:
        # Quite a few MPs have no constituency contact details shown, so this is a non-fatal error
        logging.warn("Could not find constituency contact details for %s", mp_url)
        constituency_contact_details = {}
        constituency_latlong = None
    else:
        constituency_contact_details = extract_contact_details(constituency_mo.group(1))
        constituency_postcode = scraperwiki.geo.extract_gb_postcode(constituency_contact_details.get("address"))
        if constituency_postcode:
            constituency_latlong = latlng_from_postcode(constituency_postcode)
        else: 
            constituency_latlong = None
    
    values = {
        "parliament_biography_url": mp_url,
        
        "title": title,
        "name": name,
        "address_as": address_as,
        "constituency": constituency,
        "party": party,
        
        "westminster_address": westminster_contact_details.get("address"),
        "westminster_phone": westminster_contact_details.get("phone"),
        "westminster_fax": westminster_contact_details.get("fax"),
        "westminster_email": westminster_contact_details.get("email"),
        # They never have a Westminster web page, at least at the time of writing
        
        "constituency_address": constituency_contact_details.get("address"),
        "constituency_phone": constituency_contact_details.get("phone"),
        "constituency_fax": constituency_contact_details.get("fax"),
        "constituency_email": constituency_contact_details.get("email"),
        "constituency_url": constituency_contact_details.get("url"),
        "constituency_latlong": constituency_latlong,
        "latlng": constituency_latlong,
    }

    scraperwiki.sqlite.save(["parliament_biography_url"], values)

if not found:
    logging.error("Did not find any MPs on the list page!")

