import scraperwiki, re, time

# initializes counters
add_count = 8189 
max_page = 150 # all listing max page = "28646" (delay of 7 seconds makes it almost to 250)
page_count=1
rest = ''

def get_phone(input):
    match = re.search('Phone:\s([0-9-]*)', input)
    phone = ""
    if match:
        phone = match.group(1)
    return phone

def get_fax(input):
    match = re.search('Fax:\s([0-9-]*)', input)
    fax = ""
    if match:
        fax = match.group(1)
    return fax

def get_addr3(input):
    input = re.sub('&nbsp;', ' ', input)
    split_data = input.split('<br>')
    addr3 = ""
    for j in split_data:
        match = re.search('([[A-Z].*?,\s[A-Z][A-Z]\s+[0-9]{5})', j, re.I|re.S)
        if match:
            addr3 = j
    return addr3    

while page_count <= max_page:
    time.sleep(7)
    print page_count

    url_root = "http://www.nahcagencylocator.com/"
    if page_count == 1:
        # this next line sets the initial url to be scraped
        url_base = "http://www.nahcagencylocator.com/Listing.asp?Show=All&PID={FA0402E3-DF61-4920-88DF-4EA9825AEA23}&PRC=28679&page=8189"
    else:
        url_base = url_root + rest
    
    # this line acquires the html source code.
    html_page = scraperwiki.scrape(url_base)
    
    # this section acquires the url corresponding to the next button on each listing page.
    next_link = re.search('align="right"><a href="(.*?)"\sstyle=', html_page, re.S|re.I)
    print next_link
    if next_link:
        rest = next_link.group(1)
    else:
        print "The initial url needs to be reset."
    
    # this hones in on exact listing section.
    card = re.search('<td><strong>(.*?)</td>', html_page, re.I|re.S)
    data = card.group(1) if card else ""

    phone = get_phone(data)  # acquire phone number

    fax = get_fax(data)  # acquire fax number

    addr3 = get_addr3(data)  # acquire address line 3 using addr3 function
    
    # the following acquires the name
    last_list = data.split('<br>')
    name = last_list[0].split('</strong>')[0]
    
    # the following two lines acquire the agency type
    get_agency = re.search('Agency Type:\s+<i>(.*?)</i>', data, re.I|re.S)
    agency_type = get_agency.group(1) if get_agency else ""
    
    # the following acquires the email address
    spot = re.search("HREF='mailto:(.*?)\?Subject", html_page, re.I|re.S)
    email = spot.group(1) if spot else ""

    # commit data to datastore row: 'add_count'
    scraperwiki.sqlite.save(unique_keys=["agency"], data={"agency": add_count, "name": name, "address_3": addr3, "phone": phone, "fax": fax, "email": email, "agency_type": agency_type})
    
    # increment counters
    add_count+=1
    page_count+=1

print "END OF SCRAPE"


import scraperwiki, re, time

# initializes counters
add_count = 8189 
max_page = 150 # all listing max page = "28646" (delay of 7 seconds makes it almost to 250)
page_count=1
rest = ''

def get_phone(input):
    match = re.search('Phone:\s([0-9-]*)', input)
    phone = ""
    if match:
        phone = match.group(1)
    return phone

def get_fax(input):
    match = re.search('Fax:\s([0-9-]*)', input)
    fax = ""
    if match:
        fax = match.group(1)
    return fax

def get_addr3(input):
    input = re.sub('&nbsp;', ' ', input)
    split_data = input.split('<br>')
    addr3 = ""
    for j in split_data:
        match = re.search('([[A-Z].*?,\s[A-Z][A-Z]\s+[0-9]{5})', j, re.I|re.S)
        if match:
            addr3 = j
    return addr3    

while page_count <= max_page:
    time.sleep(7)
    print page_count

    url_root = "http://www.nahcagencylocator.com/"
    if page_count == 1:
        # this next line sets the initial url to be scraped
        url_base = "http://www.nahcagencylocator.com/Listing.asp?Show=All&PID={FA0402E3-DF61-4920-88DF-4EA9825AEA23}&PRC=28679&page=8189"
    else:
        url_base = url_root + rest
    
    # this line acquires the html source code.
    html_page = scraperwiki.scrape(url_base)
    
    # this section acquires the url corresponding to the next button on each listing page.
    next_link = re.search('align="right"><a href="(.*?)"\sstyle=', html_page, re.S|re.I)
    print next_link
    if next_link:
        rest = next_link.group(1)
    else:
        print "The initial url needs to be reset."
    
    # this hones in on exact listing section.
    card = re.search('<td><strong>(.*?)</td>', html_page, re.I|re.S)
    data = card.group(1) if card else ""

    phone = get_phone(data)  # acquire phone number

    fax = get_fax(data)  # acquire fax number

    addr3 = get_addr3(data)  # acquire address line 3 using addr3 function
    
    # the following acquires the name
    last_list = data.split('<br>')
    name = last_list[0].split('</strong>')[0]
    
    # the following two lines acquire the agency type
    get_agency = re.search('Agency Type:\s+<i>(.*?)</i>', data, re.I|re.S)
    agency_type = get_agency.group(1) if get_agency else ""
    
    # the following acquires the email address
    spot = re.search("HREF='mailto:(.*?)\?Subject", html_page, re.I|re.S)
    email = spot.group(1) if spot else ""

    # commit data to datastore row: 'add_count'
    scraperwiki.sqlite.save(unique_keys=["agency"], data={"agency": add_count, "name": name, "address_3": addr3, "phone": phone, "fax": fax, "email": email, "agency_type": agency_type})
    
    # increment counters
    add_count+=1
    page_count+=1

print "END OF SCRAPE"


