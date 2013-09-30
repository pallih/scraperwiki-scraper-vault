import logging, re, scraperwiki, time, urllib2

def scrape(url):
    # Escape non-ASCII characters
    url = re.sub(r"[^\0-\177]", lambda mo: "%%%2X" % ord(mo.group(0)), url)
    return scraperwiki.scrape(url)

# This page lists all the Lords, with links to the biography pages
list_page = scrape("http://www.parliament.uk/mps-lords-and-offices/lords/")

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

# For each Lord, fetch the biography and extract the contact information
for list_mo in re.finditer(r'<a href="(/biographies[^"]+)"', list_page):
    lord_url = "http://www.parliament.uk" + list_mo.group(1)
    try:
        lord_page = scrape(lord_url)
    except:
        logging.exception("Failed to fetch %s", lord_url)
        continue

    # Get the name of the Lord
    name_mo = re.search(r'<h1 id="ctl00_ctl00_SiteSpecificPlaceholder_.+_h1Item">(?:<!--(?:[^-]|-[^-])+-->|\s)+(.+?)(?:<!--(?:[^-]|-[^-])+-->|\s)+</h1>', lord_page, re.DOTALL)
    if not name_mo:
        logging.error("Could not find name for %s", lord_url)
        continue
    name = name_mo.group(1)
    name = re.sub(r'&#(\d+);', lambda mo: unichr(int(mo.group(1))), name)

    # Separate the title (Mr, Mrs, etc) from the name
    name_parts_mo = re.match(r'((?:Mr|Mrs|Miss|Ms|Dr|Prof|Sir|Rt Hon(?:\s+Sir)?))\s+(.+)', name)
    if name_parts_mo:
        title, name = name_parts_mo.group(1), name_parts_mo.group(2)
    else:
        title = None

    # Party
    party_mo = re.search(r'<h3[^>]*>Party</h3>\s+<p>([^<]+)</p>', lord_page, re.DOTALL)
    if not party_mo:
        logging.error("No party for %s", lord_url)
        party = None
    else:
        party = party_mo.group(1)

    # Political interests
    political_interests = re.search(r'<h4[^>]*>Political interests</h4>\s+<p>([^<]+)</p>', lord_page, re.DOTALL)
    if not political_interests:
        logging.error('Could not find "Political interests" for %s', lord_url)
        political_interests = None
    else:
        political_interests = political_interests.group(1)

    # How to address the Lord in question, e.g. "Lady Herman", "Mr Bercow", "Prime Minister"
    address_as_mo = re.search(r'<h3[^>]*>Address as</h3>\s+<p>([^<]+)</p>', lord_page, re.DOTALL)
    if not address_as_mo:
        logging.error('Could not find "Address as" for %s', lord_url)
        address_as = None
    else:
        address_as = address_as_mo.group(1)
    
    # Get Westminster contact details
    westminster_mo = re.search(r'<strong>Westminster</strong>\s*<p>((?:[^<]+|<[^/]|</[^p])*)</p>', lord_page)
    if not westminster_mo:
        logging.error("Could not find Westminster contact details for %s", lord_url)
        westminster_contact_details = {}
    else:
        westminster_contact_details = extract_contact_details(westminster_mo.group(1))
    
    values = {
        "parliament_biography_url": lord_url,
        
        "title": title,
        "name": name,
        "address_as": address_as,
        "party": party,
        "political_interests": political_interests,
        
        "westminster_address": westminster_contact_details.get("address"),
        "westminster_phone": westminster_contact_details.get("phone"),
        "westminster_fax": westminster_contact_details.get("fax"),
        "westminster_email": westminster_contact_details.get("email"),
        # They never have a Westminster web page, at least at the time of writing
    }
    
    scraperwiki.sqlite.save(["parliament_biography_url"], values)

import logging, re, scraperwiki, time, urllib2

def scrape(url):
    # Escape non-ASCII characters
    url = re.sub(r"[^\0-\177]", lambda mo: "%%%2X" % ord(mo.group(0)), url)
    return scraperwiki.scrape(url)

# This page lists all the Lords, with links to the biography pages
list_page = scrape("http://www.parliament.uk/mps-lords-and-offices/lords/")

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

# For each Lord, fetch the biography and extract the contact information
for list_mo in re.finditer(r'<a href="(/biographies[^"]+)"', list_page):
    lord_url = "http://www.parliament.uk" + list_mo.group(1)
    try:
        lord_page = scrape(lord_url)
    except:
        logging.exception("Failed to fetch %s", lord_url)
        continue

    # Get the name of the Lord
    name_mo = re.search(r'<h1 id="ctl00_ctl00_SiteSpecificPlaceholder_.+_h1Item">(?:<!--(?:[^-]|-[^-])+-->|\s)+(.+?)(?:<!--(?:[^-]|-[^-])+-->|\s)+</h1>', lord_page, re.DOTALL)
    if not name_mo:
        logging.error("Could not find name for %s", lord_url)
        continue
    name = name_mo.group(1)
    name = re.sub(r'&#(\d+);', lambda mo: unichr(int(mo.group(1))), name)

    # Separate the title (Mr, Mrs, etc) from the name
    name_parts_mo = re.match(r'((?:Mr|Mrs|Miss|Ms|Dr|Prof|Sir|Rt Hon(?:\s+Sir)?))\s+(.+)', name)
    if name_parts_mo:
        title, name = name_parts_mo.group(1), name_parts_mo.group(2)
    else:
        title = None

    # Party
    party_mo = re.search(r'<h3[^>]*>Party</h3>\s+<p>([^<]+)</p>', lord_page, re.DOTALL)
    if not party_mo:
        logging.error("No party for %s", lord_url)
        party = None
    else:
        party = party_mo.group(1)

    # Political interests
    political_interests = re.search(r'<h4[^>]*>Political interests</h4>\s+<p>([^<]+)</p>', lord_page, re.DOTALL)
    if not political_interests:
        logging.error('Could not find "Political interests" for %s', lord_url)
        political_interests = None
    else:
        political_interests = political_interests.group(1)

    # How to address the Lord in question, e.g. "Lady Herman", "Mr Bercow", "Prime Minister"
    address_as_mo = re.search(r'<h3[^>]*>Address as</h3>\s+<p>([^<]+)</p>', lord_page, re.DOTALL)
    if not address_as_mo:
        logging.error('Could not find "Address as" for %s', lord_url)
        address_as = None
    else:
        address_as = address_as_mo.group(1)
    
    # Get Westminster contact details
    westminster_mo = re.search(r'<strong>Westminster</strong>\s*<p>((?:[^<]+|<[^/]|</[^p])*)</p>', lord_page)
    if not westminster_mo:
        logging.error("Could not find Westminster contact details for %s", lord_url)
        westminster_contact_details = {}
    else:
        westminster_contact_details = extract_contact_details(westminster_mo.group(1))
    
    values = {
        "parliament_biography_url": lord_url,
        
        "title": title,
        "name": name,
        "address_as": address_as,
        "party": party,
        "political_interests": political_interests,
        
        "westminster_address": westminster_contact_details.get("address"),
        "westminster_phone": westminster_contact_details.get("phone"),
        "westminster_fax": westminster_contact_details.get("fax"),
        "westminster_email": westminster_contact_details.get("email"),
        # They never have a Westminster web page, at least at the time of writing
    }
    
    scraperwiki.sqlite.save(["parliament_biography_url"], values)

