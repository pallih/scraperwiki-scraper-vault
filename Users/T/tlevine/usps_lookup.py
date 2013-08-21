'''
Send a query string 

'''
import os
from urllib2 import urlopen, URLError
from urllib import urlencode
from urlparse import parse_qs
from lxml.html import fromstring
from json import dumps

ADDRESS_LOOKUP_URL = 'https://tools.usps.com/go/ZipLookupResultsAction!input.action?'
EXPECTED_KEYS = {'address1', 'address2', 'city', 'state', 'zip'}

def check_and_format(address):
    '''
    `address` is a dictionary of the querystring paramaters.
    Validated it, then add the paramaters that are necessary for
    the call to the USPS page.
    '''

    # Dunno why they come as lists
    for k, v in address.items():
        address[k] = v[0]

    if set(address.keys()) == {'address1', 'city', 'state', 'zip'}:
        address['address2'] = ''

    if set(address.keys()) == EXPECTED_KEYS:
        address.update({
            "resultMode": 0,
            "companyName": "",
            "urbanCode": "",
            "postalCode": "",
        })
    else:
        raise ValueError(
            'Your request has these extra keys: %s. '
            'Your request is missing these keys: %s' % (
                set(address.keys()).difference(EXPECTED_KEYS),
                EXPECTED_KEYS.difference(set(address.keys()))
            )
        )
    return address

def do_request(address):
    '''
    `address` is a dictionary of paramaters for the USPS request.
    Make the request, parse the output and return the json that
    will be printed.
    '''
    url = ADDRESS_LOOKUP_URL + urlencode(address)
    output = {'url': url, 'addresses': []}
    while True:
        try:
            handle = urlopen(url)
        except URLError:
            randomsleep()
        else:
            text = handle.read()
            break

    if '''<li class="error">Unfortunately, this address wasn't found.</li>''' in text and \
        '''<li class="error">Please double-check it and try again.</li>''' in text:
        output['status'] = 'no match'
    else:
        output['status'] = 'okay'
        resultstart = '<div id="results-content" class="cap-middle">'
        text = resultstart + text.split(resultstart)[1].split('<div id="result-bottom" class="result-bottom">')[0].replace('&trade;', '')
        html = fromstring(text)
        for std_address in html.cssselect('#result-list p.std-address'):
            spans = std_address.xpath('span[@class != "address1 range" and @class != "hyphen"]')
            outaddress = {span.attrib['class'].replace(' range', ''): span.text for span in spans}

            addresses1 = std_address.xpath('span[@class="address1 range"]')
            outaddress['address1'] = addresses1[-1].text
            if len(addresses1) == 2:
                outaddress['name'] = addresses1[0].text

            if outaddress['zip4'] == 'None':
                outaddress['zip4'] = None
            output['addresses'].append(outaddress)

    return dumps(output)

DOCS = '''
<h1>USPS Address Lookup API</h1>
<p>This is a frontend to the <a href="https://tools.usps.com/go/ZipLookupAction!input.action">USPS zipcode lookup tool</a>.</p>

<p>
  Pass a query string with the keys "address1", "city", "state", "zip" and, optionally, "address2".
  The result is a JSON-encoded dictionary with a "status" field, a "url" field and an "addresses" field.
  the "addresses" field is a list of different matches, broken out into components, and
  The "url" field is the query to the USPS zipcode lookup tool.
</p>

<h2>Test</h2>
<a href="https://views.scraperwiki.com/run/usps_lookup/?address1=1600%20Pennsylvania%20Avenue%20NW&city=Washington&state=DC&zip=20500">This query</a>
should return JSON equivalent to the following JSON.
<pre>
{
  "url": "https://tools.usps.com/go/ZipLookupResultsAction!input.action?city=Washington&zip=20500&companyName=&address1=1600+Pennsylvania+Avenue+NW&address2=&postalCode=&state=DC&resultMode=0&urbanCode=",
  "status": "okay",
  "addresses": [
    {"city": "WASHINGTON ", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0003"},
    {"city": "WASHINGTON ", "name": "PRESIDENT", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0001"},
    {"city": "WASHINGTON ", "name": "FIRST LADY", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0002"},
    {"city": "WASHINGTON ", "name": "THE WHITE HOUSE", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0004"},
    {"city": "WASHINGTON ", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0005"},
    {"city": "WASHINGTON ", "name": "GREETINGS OFFICE", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0039"},
    {"city": "WASHINGTON ", "name": "WHITE HOUSE STATION", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0049"},
    {"city": "WASHINGTON ", "name": "AMER FUND FOR AFGHAN CHILD", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "1600"}
  ]
}
</pre>
'''

address = parse_qs(os.environ.get('QUERY_STRING', ''))
if address == {}:
    print DOCS
else:
    try:
        from scraperwiki.utils import httpresponseheader
    except ImportError:
        print "Content-Type: application/json"
        print
    else:
        httpresponseheader('Content-Type', 'application/json')

    try:
        address = check_and_format(address)
    except ValueError, msg:
        print dumps({"status": str(msg)})
    else:
        print do_request(address)