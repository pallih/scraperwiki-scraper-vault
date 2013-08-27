# 4International Colleges & Universities contains one of the most comprehensive list of world universities
# This scraper downloads their list and rankings from www.4icu.org/reviews/ for research purposes


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse

# Defines the get_domain function to use later on
def get_domain(url, tlds):
    url_elements = urlparse(url)[1].split('.')
    # url_elements = ["abcde","co","uk"]

    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds:
        if (exception_candidate in tlds):
            return ".".join(url_elements[i:])
        if (candidate in tlds or wildcard_candidate in tlds):
            return ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"

    return urlparse(url)[1]


# Loads the TLD List to be used later in the program
tld_file = scraperwiki.scrape('http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1')
tlds = tld_file.splitlines()
for index in range(len(tlds)):
    tlds[index] = tlds[index].strip()
    if tlds[index][0:2] == '//':
        tlds[index] = ''
tlds = filter(None, tlds)


# Crawl through World Rankings Getting and Storing University Data
base_url = "http://www.4icu.org/reviews/"
try:
    current_page = int(scraperwiki.sqlite.get_var('last_page'))
except:
    current_page = 1
end_page = 15000
if current_page >= end_page:
    current_page = 1

while current_page <= end_page:
    scraperwiki.sqlite.save_var('last_page', current_page)
    url = base_url + str(current_page) + ".htm"
    try:
        # 4ICU stores its ranking in a different web page so institutions can post it as a banner, so this scraper extracts from both
        html = scraperwiki.scrape(url)
        ranking_html = scraperwiki.scrape("http://www.4icu.org/reviews/rankings/university-ranking-" + str(current_page) + ".htm") 
    except Exception as inst:
        # If the URL does not exist, or another error occurs, skip to the next page
        print "Error on Page: " + str(current_page) + " " + str(inst)
        #scraperwiki.sqlite.save(unique_keys=['page'], data={'page' : current_page, 'error' : str(inst)}, table_name="errors")
        current_page = current_page + 1
        continue

    root = lxml.html.fromstring(html)
    ranking_root = lxml.html.fromstring(ranking_html) 

    all_content = root.cssselect("table tr td")  

    # Sets data that is consistent with every page
    try:
        data = {
            'id' : current_page,
            'university_name' : all_content[13].text_content(),
            'url' : str(all_content[13].xpath('a/@href'))[2:-2],
            'domain' : get_domain(str(all_content[13].xpath('a/@href'))[2:-2], tlds),
            'rank' : int(ranking_root.cssselect('td')[1].text_content()),
            'region' : all_content[4].cssselect('a')[1].text_content().strip(),
            'country' : all_content[4].cssselect('a')[2].text_content().strip(),
            }
    except Exception as inst:
        # If their was an error while trying to get the basic data skip to the next page
        print "Error on Page: " + str(current_page) + " " + str(inst)
        current_page = current_page + 1
        continue
    
    #Extracts Domain from Universitie's URL
    u_url = str(all_content[13].xpath('a/@href'))[2:-2]
    if not u_url.startswith('http'):
        u_url = 'http://'+url
    u_website = urlparse(u_url)[1]
    u_domain = ('.').join(u_website.split('.')[1:])
    data['domain'] = u_domain


    # Sets data that varies in location or existence

    # Makes a list of text content of fields from page to use to determine relative position of data
    all_content_text = range(len(all_content))
    for counter in range(len(all_content)):
        all_content_text[counter] = all_content[counter].text_content().strip()
        # If no text exists in the field, assume it is an image and use the alternate text for the image
        if not(all_content_text[counter]):
            all_content_text[counter] = str(all_content[counter].xpath('img/@alt'))

        # The following code prints all the data in tables on the page and is only here to help develop / debug the scraper
        #print str(counter) + all_content_text[counter]



    # Gets Data that is one position away from label

    # Create a dictionary of all potential text fields on the page that are one space away from a value we want
    # Note: Text labels often appear multiple times as 4ICU changes these randomly
    field = {
        'English Name' : 'english_name',
        'Name in English' : 'english_name',
        'Acronym' : 'acronym',
        'Address' : 'address',
        'Population range' : 'population_range',
        'Year of Foundation' : 'year_established',
        'Year of establishment' : 'year_established',
        'Founded in' : 'year_established',
        'Established in' : 'year_established',
        'Motto' : 'motto',
        'Colours' : 'colours',
        }

    # Generate Empty Data Dictionary to avoid future errors
    for label in field:
        data[field[label]] = None

    # Assign Data based upon Text Fields in Document defined in field dictionary
    for label in field:
        #The following line is for debugging
        #print "Label is " + label + ", and Field is "+ field[label]
        if label in all_content_text:
            data[field[label]] = all_content_text[all_content_text.index(label)+1]
        else:
            if not(data[field[label]]):
                data[field[label]] = None
        

    # Sets the ['Phone', 'Fax'] if they exist (4ICU is tricky and seems to randomize the label)
    if "['Phone', 'Fax']" in all_content_text:
        label = "['Phone', 'Fax']"
    elif "['Telephone', 'Fax']" in all_content_text:
        label = "['Telephone', 'Fax']"
    elif "['Tel', 'Fax']" in all_content_text:
        label = "['Tel', 'Fax']"
    else:
        label = None

    if label:
        data['phone'] = all_content[all_content_text.index(label)+1].cssselect('h5')[0].text_content()
        data['fax'] = all_content[all_content_text.index(label)+1].cssselect('h5')[1].text_content()
    else:
        data['phone'] = None
        data['fax'] = None


    # Get Data that is in the same location as its label

    field = {
        'Gender Admission' : 'gender_admission',
        'Admission Selection' : 'admission_selection',
        'Selection Percentage' : 'selection_percentage',
        'Total Enrollment' : 'total_enrollment',
        'Total Staff' : 'total_staff',
        'Control' : 'entity_control',
        'Entity Type' : 'entity_type',
        'Academic Calendar' : 'academic_calendar',
        'Campus Type' : 'campus_type',
        'Religious Affiliation' : 'religious_affiliation',
        'Recognition or Accreditation' : 'accreditation',
        'Other Specialised or Programmatic Accreditation' : 'programmatic_accreditation',
        }

    # Generate Empty Data Dictionary to avoid future errors
    for label in field:
        data[field[label]] = None

    # Assign Data based upon Text Fields in Document defined in field dictionary
    for full_text in all_content_text:
        for label in field:
            if label in full_text:
                data[field[label]] = full_text.replace(label, '').strip()
            else:
                if not(data[field[label]]):
                    data[field[label]] = None
                

    # Write to the Database
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    # Increment the While Loop to go the Next Page
    current_page = current_page + 1
# 4International Colleges & Universities contains one of the most comprehensive list of world universities
# This scraper downloads their list and rankings from www.4icu.org/reviews/ for research purposes


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse

# Defines the get_domain function to use later on
def get_domain(url, tlds):
    url_elements = urlparse(url)[1].split('.')
    # url_elements = ["abcde","co","uk"]

    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds:
        if (exception_candidate in tlds):
            return ".".join(url_elements[i:])
        if (candidate in tlds or wildcard_candidate in tlds):
            return ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"

    return urlparse(url)[1]


# Loads the TLD List to be used later in the program
tld_file = scraperwiki.scrape('http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1')
tlds = tld_file.splitlines()
for index in range(len(tlds)):
    tlds[index] = tlds[index].strip()
    if tlds[index][0:2] == '//':
        tlds[index] = ''
tlds = filter(None, tlds)


# Crawl through World Rankings Getting and Storing University Data
base_url = "http://www.4icu.org/reviews/"
try:
    current_page = int(scraperwiki.sqlite.get_var('last_page'))
except:
    current_page = 1
end_page = 15000
if current_page >= end_page:
    current_page = 1

while current_page <= end_page:
    scraperwiki.sqlite.save_var('last_page', current_page)
    url = base_url + str(current_page) + ".htm"
    try:
        # 4ICU stores its ranking in a different web page so institutions can post it as a banner, so this scraper extracts from both
        html = scraperwiki.scrape(url)
        ranking_html = scraperwiki.scrape("http://www.4icu.org/reviews/rankings/university-ranking-" + str(current_page) + ".htm") 
    except Exception as inst:
        # If the URL does not exist, or another error occurs, skip to the next page
        print "Error on Page: " + str(current_page) + " " + str(inst)
        #scraperwiki.sqlite.save(unique_keys=['page'], data={'page' : current_page, 'error' : str(inst)}, table_name="errors")
        current_page = current_page + 1
        continue

    root = lxml.html.fromstring(html)
    ranking_root = lxml.html.fromstring(ranking_html) 

    all_content = root.cssselect("table tr td")  

    # Sets data that is consistent with every page
    try:
        data = {
            'id' : current_page,
            'university_name' : all_content[13].text_content(),
            'url' : str(all_content[13].xpath('a/@href'))[2:-2],
            'domain' : get_domain(str(all_content[13].xpath('a/@href'))[2:-2], tlds),
            'rank' : int(ranking_root.cssselect('td')[1].text_content()),
            'region' : all_content[4].cssselect('a')[1].text_content().strip(),
            'country' : all_content[4].cssselect('a')[2].text_content().strip(),
            }
    except Exception as inst:
        # If their was an error while trying to get the basic data skip to the next page
        print "Error on Page: " + str(current_page) + " " + str(inst)
        current_page = current_page + 1
        continue
    
    #Extracts Domain from Universitie's URL
    u_url = str(all_content[13].xpath('a/@href'))[2:-2]
    if not u_url.startswith('http'):
        u_url = 'http://'+url
    u_website = urlparse(u_url)[1]
    u_domain = ('.').join(u_website.split('.')[1:])
    data['domain'] = u_domain


    # Sets data that varies in location or existence

    # Makes a list of text content of fields from page to use to determine relative position of data
    all_content_text = range(len(all_content))
    for counter in range(len(all_content)):
        all_content_text[counter] = all_content[counter].text_content().strip()
        # If no text exists in the field, assume it is an image and use the alternate text for the image
        if not(all_content_text[counter]):
            all_content_text[counter] = str(all_content[counter].xpath('img/@alt'))

        # The following code prints all the data in tables on the page and is only here to help develop / debug the scraper
        #print str(counter) + all_content_text[counter]



    # Gets Data that is one position away from label

    # Create a dictionary of all potential text fields on the page that are one space away from a value we want
    # Note: Text labels often appear multiple times as 4ICU changes these randomly
    field = {
        'English Name' : 'english_name',
        'Name in English' : 'english_name',
        'Acronym' : 'acronym',
        'Address' : 'address',
        'Population range' : 'population_range',
        'Year of Foundation' : 'year_established',
        'Year of establishment' : 'year_established',
        'Founded in' : 'year_established',
        'Established in' : 'year_established',
        'Motto' : 'motto',
        'Colours' : 'colours',
        }

    # Generate Empty Data Dictionary to avoid future errors
    for label in field:
        data[field[label]] = None

    # Assign Data based upon Text Fields in Document defined in field dictionary
    for label in field:
        #The following line is for debugging
        #print "Label is " + label + ", and Field is "+ field[label]
        if label in all_content_text:
            data[field[label]] = all_content_text[all_content_text.index(label)+1]
        else:
            if not(data[field[label]]):
                data[field[label]] = None
        

    # Sets the ['Phone', 'Fax'] if they exist (4ICU is tricky and seems to randomize the label)
    if "['Phone', 'Fax']" in all_content_text:
        label = "['Phone', 'Fax']"
    elif "['Telephone', 'Fax']" in all_content_text:
        label = "['Telephone', 'Fax']"
    elif "['Tel', 'Fax']" in all_content_text:
        label = "['Tel', 'Fax']"
    else:
        label = None

    if label:
        data['phone'] = all_content[all_content_text.index(label)+1].cssselect('h5')[0].text_content()
        data['fax'] = all_content[all_content_text.index(label)+1].cssselect('h5')[1].text_content()
    else:
        data['phone'] = None
        data['fax'] = None


    # Get Data that is in the same location as its label

    field = {
        'Gender Admission' : 'gender_admission',
        'Admission Selection' : 'admission_selection',
        'Selection Percentage' : 'selection_percentage',
        'Total Enrollment' : 'total_enrollment',
        'Total Staff' : 'total_staff',
        'Control' : 'entity_control',
        'Entity Type' : 'entity_type',
        'Academic Calendar' : 'academic_calendar',
        'Campus Type' : 'campus_type',
        'Religious Affiliation' : 'religious_affiliation',
        'Recognition or Accreditation' : 'accreditation',
        'Other Specialised or Programmatic Accreditation' : 'programmatic_accreditation',
        }

    # Generate Empty Data Dictionary to avoid future errors
    for label in field:
        data[field[label]] = None

    # Assign Data based upon Text Fields in Document defined in field dictionary
    for full_text in all_content_text:
        for label in field:
            if label in full_text:
                data[field[label]] = full_text.replace(label, '').strip()
            else:
                if not(data[field[label]]):
                    data[field[label]] = None
                

    # Write to the Database
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    # Increment the While Loop to go the Next Page
    current_page = current_page + 1
# 4International Colleges & Universities contains one of the most comprehensive list of world universities
# This scraper downloads their list and rankings from www.4icu.org/reviews/ for research purposes


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse

# Defines the get_domain function to use later on
def get_domain(url, tlds):
    url_elements = urlparse(url)[1].split('.')
    # url_elements = ["abcde","co","uk"]

    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds:
        if (exception_candidate in tlds):
            return ".".join(url_elements[i:])
        if (candidate in tlds or wildcard_candidate in tlds):
            return ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"

    return urlparse(url)[1]


# Loads the TLD List to be used later in the program
tld_file = scraperwiki.scrape('http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1')
tlds = tld_file.splitlines()
for index in range(len(tlds)):
    tlds[index] = tlds[index].strip()
    if tlds[index][0:2] == '//':
        tlds[index] = ''
tlds = filter(None, tlds)


# Crawl through World Rankings Getting and Storing University Data
base_url = "http://www.4icu.org/reviews/"
try:
    current_page = int(scraperwiki.sqlite.get_var('last_page'))
except:
    current_page = 1
end_page = 15000
if current_page >= end_page:
    current_page = 1

while current_page <= end_page:
    scraperwiki.sqlite.save_var('last_page', current_page)
    url = base_url + str(current_page) + ".htm"
    try:
        # 4ICU stores its ranking in a different web page so institutions can post it as a banner, so this scraper extracts from both
        html = scraperwiki.scrape(url)
        ranking_html = scraperwiki.scrape("http://www.4icu.org/reviews/rankings/university-ranking-" + str(current_page) + ".htm") 
    except Exception as inst:
        # If the URL does not exist, or another error occurs, skip to the next page
        print "Error on Page: " + str(current_page) + " " + str(inst)
        #scraperwiki.sqlite.save(unique_keys=['page'], data={'page' : current_page, 'error' : str(inst)}, table_name="errors")
        current_page = current_page + 1
        continue

    root = lxml.html.fromstring(html)
    ranking_root = lxml.html.fromstring(ranking_html) 

    all_content = root.cssselect("table tr td")  

    # Sets data that is consistent with every page
    try:
        data = {
            'id' : current_page,
            'university_name' : all_content[13].text_content(),
            'url' : str(all_content[13].xpath('a/@href'))[2:-2],
            'domain' : get_domain(str(all_content[13].xpath('a/@href'))[2:-2], tlds),
            'rank' : int(ranking_root.cssselect('td')[1].text_content()),
            'region' : all_content[4].cssselect('a')[1].text_content().strip(),
            'country' : all_content[4].cssselect('a')[2].text_content().strip(),
            }
    except Exception as inst:
        # If their was an error while trying to get the basic data skip to the next page
        print "Error on Page: " + str(current_page) + " " + str(inst)
        current_page = current_page + 1
        continue
    
    #Extracts Domain from Universitie's URL
    u_url = str(all_content[13].xpath('a/@href'))[2:-2]
    if not u_url.startswith('http'):
        u_url = 'http://'+url
    u_website = urlparse(u_url)[1]
    u_domain = ('.').join(u_website.split('.')[1:])
    data['domain'] = u_domain


    # Sets data that varies in location or existence

    # Makes a list of text content of fields from page to use to determine relative position of data
    all_content_text = range(len(all_content))
    for counter in range(len(all_content)):
        all_content_text[counter] = all_content[counter].text_content().strip()
        # If no text exists in the field, assume it is an image and use the alternate text for the image
        if not(all_content_text[counter]):
            all_content_text[counter] = str(all_content[counter].xpath('img/@alt'))

        # The following code prints all the data in tables on the page and is only here to help develop / debug the scraper
        #print str(counter) + all_content_text[counter]



    # Gets Data that is one position away from label

    # Create a dictionary of all potential text fields on the page that are one space away from a value we want
    # Note: Text labels often appear multiple times as 4ICU changes these randomly
    field = {
        'English Name' : 'english_name',
        'Name in English' : 'english_name',
        'Acronym' : 'acronym',
        'Address' : 'address',
        'Population range' : 'population_range',
        'Year of Foundation' : 'year_established',
        'Year of establishment' : 'year_established',
        'Founded in' : 'year_established',
        'Established in' : 'year_established',
        'Motto' : 'motto',
        'Colours' : 'colours',
        }

    # Generate Empty Data Dictionary to avoid future errors
    for label in field:
        data[field[label]] = None

    # Assign Data based upon Text Fields in Document defined in field dictionary
    for label in field:
        #The following line is for debugging
        #print "Label is " + label + ", and Field is "+ field[label]
        if label in all_content_text:
            data[field[label]] = all_content_text[all_content_text.index(label)+1]
        else:
            if not(data[field[label]]):
                data[field[label]] = None
        

    # Sets the ['Phone', 'Fax'] if they exist (4ICU is tricky and seems to randomize the label)
    if "['Phone', 'Fax']" in all_content_text:
        label = "['Phone', 'Fax']"
    elif "['Telephone', 'Fax']" in all_content_text:
        label = "['Telephone', 'Fax']"
    elif "['Tel', 'Fax']" in all_content_text:
        label = "['Tel', 'Fax']"
    else:
        label = None

    if label:
        data['phone'] = all_content[all_content_text.index(label)+1].cssselect('h5')[0].text_content()
        data['fax'] = all_content[all_content_text.index(label)+1].cssselect('h5')[1].text_content()
    else:
        data['phone'] = None
        data['fax'] = None


    # Get Data that is in the same location as its label

    field = {
        'Gender Admission' : 'gender_admission',
        'Admission Selection' : 'admission_selection',
        'Selection Percentage' : 'selection_percentage',
        'Total Enrollment' : 'total_enrollment',
        'Total Staff' : 'total_staff',
        'Control' : 'entity_control',
        'Entity Type' : 'entity_type',
        'Academic Calendar' : 'academic_calendar',
        'Campus Type' : 'campus_type',
        'Religious Affiliation' : 'religious_affiliation',
        'Recognition or Accreditation' : 'accreditation',
        'Other Specialised or Programmatic Accreditation' : 'programmatic_accreditation',
        }

    # Generate Empty Data Dictionary to avoid future errors
    for label in field:
        data[field[label]] = None

    # Assign Data based upon Text Fields in Document defined in field dictionary
    for full_text in all_content_text:
        for label in field:
            if label in full_text:
                data[field[label]] = full_text.replace(label, '').strip()
            else:
                if not(data[field[label]]):
                    data[field[label]] = None
                

    # Write to the Database
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    # Increment the While Loop to go the Next Page
    current_page = current_page + 1
