import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime



search_url = "http://www.epa.ie/terminalfour/ippc/ippc-search.jsp?Submit=Browse&name="

# ideally cross reference with enforcement notices
#   http://www.epa.ie/downloads/pubs/other/corporate/oee/name,13031,en.html

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Main():
    # Use this one for testing
#    process_search_result_page('Am*')
    for letter in alphabet:
        process_search_result_page(letter + '*')

def add_data_from_detail_page(data):
    # get table from data['url']
    print 'Getting details for ' + data['regno']
    root = fetch_and_parse(data['url'])

    rows = root.cssselect('div#maincontent table tr')

    for row in rows:
        key = row[0].text
        value = row[1]
        if key == 'Reg No.':
            data['feed_url'] = value.cssselect('a')[0].get('href')
        elif key == 'Applicant Name:':
            data['applicant_name'] = value.text
        elif key == 'Location of Facility:':
            data['facility_location'] = value.text
            regex = re.compile('.*, ([^,]*)\.$')
            m = regex.match(value.text)
            if m:
                data['county'] = m.group(1)
        elif key == 'Principal Class of Activity:':
            data['activity_class_code'] = value.text.split(':')[0]
            data['activity_class_name'] = value.text.split(':')[1].strip()
        elif key == 'Description of Principal Class of Activity:':
            data['activity_class_description'] = value.text
        elif key.startswith('Other Classes of Activity'):
            if value.text != 'n/a':
                data['other_activity_classes'] = value.text
        elif key == 'Application Date:':
            data['application_date'] = parse_date(value.text)
        elif key == 'Licence Status:':
            data['status'] = inner_html(value)
        elif key == 'Latest licence for this facility:':
            data['latest_licence'] = parse_regno_reference(value)
        elif key == 'Under Review/Replaced By:':
            data['under_review_replaced_by'] = parse_regno_reference(value)
        elif key == 'Replaced Licence:':
            data['replaces'] = parse_regno_reference(value)
        elif key == 'Proposed Decision issued date:':
            data['proposed_decision_date'] = parse_date(value.text)
        elif key == 'Closing date for objections to Proposed Decision:':
            data['closing_date_for_objections'] = parse_date(value.text)
        elif key == 'Final Decision issued date:':
            data['final_decision_date'] = parse_date(value.text)
        else:
            raise Exception('Unexpected key "' + key + '" in table on detail page <' + data['url'] + '>')

def parse_regno_reference(element):
    # The value could look like this: 'Reg No. P0840-01', and the
    # code might be an HTML link.
    # Let's get just the regno code with a regular expression
    regno_regex = re.compile('P\d+-\d+')
    html = lxml.etree.tostring(element)
    return regno_regex.findall(html)[0]

def parse_date(s):
    if (s == 'N/A'):
        return None
    date_regex = re.compile('(\d\d?)/(\d\d?)/(\d\d\d\d)')
    m = date_regex.match(s.strip())
    if m:
        return datetime.datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    else:
        raise Exception('Not a date: "' + s + '"')

def process_search_result_page(search):
    print 'Searching for "' + search + '"'
    url = search_url + search
    root = fetch_and_parse(url)

    # place your cssselection case here and extract the values
    rows = root.cssselect('div#maincontent table tr')
    if len(rows) == 0:
        return
    headers = [ th.text  for th in rows[0].cssselect('th') ]
    assert headers == ['Reg No.', 'Name', 'Documents?']
    for row in rows[1:]:
        data = { }
        data['url'] = 'http://www.epa.ie/terminalfour/ippc/' + row[0][0].get('href')
        data['regno'] = row[0][0].text
        data['name'] = row[1].text
        add_data_from_detail_page(data)        

        scraperwiki.datastore.save(unique_keys=['regno'], data=data, date=data['application_date'])
    
def inner_html(el):
    r = [ el.text ]
    for v in el:
        r.append(lxml.etree.tostring(v))
        if v.tail:
            r.append(v.tail)
    return "".join(r)

def fetch_and_parse(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError:
            pass
            # just try again
    raise Exception('Failed to fetch ' + url)

Main()
