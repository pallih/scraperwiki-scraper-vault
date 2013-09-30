from requests import session
from lxml.html import fromstring

s = session()

honoree = {
    'gift_amount': '0.01',
    'designation': '22',
    'designation2': 'Cornell University 001004',
    'designation_other': '',
    'iho_imo': 'iho',
    'h_type': 'person',
    'honoree': 'Raskolnikov',
    'notify_name': 'Raskolnikov',
    'notify_address': '122 Risley Hall',
    'notify_address2': '',
    'notify_city': 'Ithaca',
    'notify_state': 'NY',
    'notify_zip': '14853',
    'notify_country': 'US',
    'notify_comments': '',
    'gift_type': 'gift1',
    'end_year': '2013',
    'step': '1',
}

personal = {
    'title': 'Mr',
    'fname': 'Thomas',
    'mname': 'Kai',
    'lname': 'Levine',
    'name_oncard': 'Thomas Levine',
    'empid': '',
    'classyear': '1337',
    'spousename': 'Thomas Levine',
    'spouseyear': '31337',
    'matchcomp': 'Industrial Peanut Butterer Parts & Supplies and Bagels Company',
    'address': '54 Walworth Avenue',
    'address2': '',
    'city': 'Scarsdale',
    'state': 'NY',
    'province': 'NY',
    'postal_code': '10583-1423',
    'country': 'US',
    'email': '',
    'email_type': 'personal',
    'phone': '607-699-1866',
    'phone_type': 'personal',
    'step': '2',
}

# Go to the first page
r = s.get('http://www.alumni.cornell.edu/seniorclass/give/')

# Choose credit card
r = s.post('http://www.alumni.cornell.edu/seniorclass/give/cfxcgi/redirect.cfm', {'type': 'giving_cc'})
r = s.get(r.headers['location'], verify = False)

# Step 1
r = s.post('https://www.giving.cornell.edu/give/index.cfm', honoree, verify = False)

# Step 2
r = s.post('https://www.giving.cornell.edu/give/index.cfm', {'continue': 'true', 'step': '1'}, verify = False)
r = s.post('https://www.giving.cornell.edu/give/index.cfm', personal, verify = False)

# Pay
r = s.get('https://www.giving.cornell.edu/give/' + fromstring(r.text).xpath('//iframe/@src')[0], verify = False)
html = fromstring(r.text)
params = {input.attrib['name']: input.attrib['value'] for input in html.xpath('//form/input')}
r = s.post(html.xpath('//form/@action')[0], params, verify = False)

print r.textfrom requests import session
from lxml.html import fromstring

s = session()

honoree = {
    'gift_amount': '0.01',
    'designation': '22',
    'designation2': 'Cornell University 001004',
    'designation_other': '',
    'iho_imo': 'iho',
    'h_type': 'person',
    'honoree': 'Raskolnikov',
    'notify_name': 'Raskolnikov',
    'notify_address': '122 Risley Hall',
    'notify_address2': '',
    'notify_city': 'Ithaca',
    'notify_state': 'NY',
    'notify_zip': '14853',
    'notify_country': 'US',
    'notify_comments': '',
    'gift_type': 'gift1',
    'end_year': '2013',
    'step': '1',
}

personal = {
    'title': 'Mr',
    'fname': 'Thomas',
    'mname': 'Kai',
    'lname': 'Levine',
    'name_oncard': 'Thomas Levine',
    'empid': '',
    'classyear': '1337',
    'spousename': 'Thomas Levine',
    'spouseyear': '31337',
    'matchcomp': 'Industrial Peanut Butterer Parts & Supplies and Bagels Company',
    'address': '54 Walworth Avenue',
    'address2': '',
    'city': 'Scarsdale',
    'state': 'NY',
    'province': 'NY',
    'postal_code': '10583-1423',
    'country': 'US',
    'email': '',
    'email_type': 'personal',
    'phone': '607-699-1866',
    'phone_type': 'personal',
    'step': '2',
}

# Go to the first page
r = s.get('http://www.alumni.cornell.edu/seniorclass/give/')

# Choose credit card
r = s.post('http://www.alumni.cornell.edu/seniorclass/give/cfxcgi/redirect.cfm', {'type': 'giving_cc'})
r = s.get(r.headers['location'], verify = False)

# Step 1
r = s.post('https://www.giving.cornell.edu/give/index.cfm', honoree, verify = False)

# Step 2
r = s.post('https://www.giving.cornell.edu/give/index.cfm', {'continue': 'true', 'step': '1'}, verify = False)
r = s.post('https://www.giving.cornell.edu/give/index.cfm', personal, verify = False)

# Pay
r = s.get('https://www.giving.cornell.edu/give/' + fromstring(r.text).xpath('//iframe/@src')[0], verify = False)
html = fromstring(r.text)
params = {input.attrib['name']: input.attrib['value'] for input in html.xpath('//form/input')}
r = s.post(html.xpath('//form/@action')[0], params, verify = False)

print r.text