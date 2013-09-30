import scraperwiki
import json
from lxml import html
from lxml.etree import tostring
import urllib
import requests
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import re
import cgi
import urllib

# Blank Python

EMPTY_VALUES = (None, '', [], (), {},'None')

def strip_tags(document):
    return ''.join(BeautifulSoup(document).findAll(text=True))

def remove_comments(page):
    soup = BeautifulSoup(page)
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup.prettify()

def processoverview(value):
    value_text = tostring(value)
    value_text = strip_tags(value_text)
    value_text = value_text.replace("&#13;","")
    value_text = value_text.replace('view more and edit','')
    value_text = value_text.replace('&#160;',' ')
    value_text = value_text.replace('if company wiki -','')
    value_text = value_text.strip('\n').strip('\r')
    value_text = value_text.strip()
    return value_text


def processhq(value):
    text = []
    children = value.getchildren()
    for c in children:
        value_text = tostring(c)
        value_text = value_text.replace("&#13;","")
        value_text = value_text.replace("&#160;map","")
        value_text = value_text.replace("&#160;","")
        value_text = value_text.replace("&#8217;","'")
        value_text = value_text.strip()
        if value_text not in EMPTY_VALUES:
            text.append(value_text)
    text = list(set(text))
    text = " ".join(text)
    text = strip_tags(text)
    text = text.replace("map","")
    pattern = re.compile(r'\s+')
    text = re.sub(pattern,' ',text)
    text = text.strip('\n').strip('\r').strip()
    return text

def processIndustries(value):
    text = []
    children = value.getchildren()
    for c in children:
        value_text = tostring(c)
        value_text = strip_tags(value_text)
        value_text = value_text.replace("&#13;","")
        value_text = value_text.replace('amp;','')
        if value_text not in EMPTY_VALUES:
            text.append(value_text)
    text = list(set(text))
    text = ",".join(text)
    pattern = re.compile(r'\s+')
    text = re.sub(pattern,' ',text)
    escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
    text = str(escaped)
    text = text.replace('amp;','')
    text = text.strip('\n').strip('\r').strip()
    return text

def processText(value):
    text = ''
    children = value.getchildren()
    if len(children) > 0:
        text = []
        for c in children:
            value_text = tostring(c)
            value_text = strip_tags(value_text)
            value_text = value_text.replace("&#13;","")
            value_text = value_text.replace('&gt;',">")
            value_text = value_text.replace("&lt;","<")
            if value_text not in EMPTY_VALUES:
                text.append(value_text)
        text = list(set(text))
        text = " ".join(text)
        pattern = re.compile(r'\s+')
        escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
        text = str(escaped)
        text = re.sub(pattern,' ',text)
    else:
        value_text = tostring(value)
        value_text = strip_tags(value_text)
        value_text = value_text.replace("&#13;","")
        value_text = value_text.replace('&gt;',">")
        value_text = value_text.replace("&lt;","<")
        text = value_text
        pattern = re.compile(r'\s+')
        text = re.sub(pattern,' ',text)
        escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
        text = str(escaped)
    return text


def get_units(value):
    units = None
    value = str(value)
    if 'M' in value or 'm' in value:
        units = 'M'
    if 'K' in value or 'k' in value:
        units = 'K'
    if 'b' in value or 'B' in value:
        units = 'B'
    return units

def processValue(value,units):
    value = value.strip()
    regex = re.compile(r'[^\d.]+')
    actual = regex.sub('',value)
    actual = float(str(actual))
    if units == 'K':
        actual = actual*float(1000)
    elif units == 'M':
        actual = actual * float(1000000)
    elif units == 'B':
        actual = actual * float(1000000000)
    return actual


def processRanges(ranges,ptype,is_range):
    start = ranges[0]
    end = ranges[1]
    start_units = get_units(start)
    end_units = get_units(end)
    if not start_units:
        start_units = end_units
    startValue = processValue(start, start_units)
    endValue = processValue(end, end_units)
    if ptype == "EMPLOYEES" and start_units is not None and end_units is not None:
        startValue = startValue * 1000 ## because processValue reduces everything by 1000 in case of units available
        endValue = endValue * 1000
    if is_range:
        return [startValue,endValue]
    else:
        actual = int((startValue+endValue)/2)
        return actual

def pre_process_value(value):
    items = []
    if value not in EMPTY_VALUES:
        escaped = cgi.escape(value).encode('ascii','xmlcharrefreplace')
        value = str(value)
        value = value.replace("<","").replace(">","").replace('$','')
        items = value.split('-')
    return items


def revenue_actual(revenue):
    revenue_items = pre_process_value(revenue)
    units = get_units(revenue)
    if len(revenue_items) == 0:
        return None
    if len(revenue_items) > 1:
        actual_revenue = processRanges(revenue_items,"REVENUE",False)
    else:
        actual_revenue = processValue(revenue, units)
    return actual_revenue

def processRevenue(value):
    text = processText(value)
    text = text.replace('&gt;',"")
    text = text.replace("&lt;","")
    escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
    text = str(escaped).strip()
    actual_revenue = revenue_actual(text)
    return actual_revenue


def employees_actual(employees):
    employee_items = pre_process_value(employees)
    if len(employee_items) == 0:
        return None
    if len(employee_items) > 1:
        actual_employees = processRanges(employee_items,"EMPLOYEES",False)
    else:
        units = get_units(employees)
        actual_employees = processValue(employees,units)
    return actual_employees

def processEmployees(value):
    text = processText(value)
    text = text.replace('&gt;',"")
    text = text.replace("&lt;","")
    escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
    text = text.replace(',','')
    text = str(escaped).strip()
    actual_employees = employees_actual(text)
    return actual_employees



def __processSingleCompanyDetails(document):
    ## just a single company, get the company email domain maybe
    website_elements = {}
    titles = document.xpath("//p[contains(@id,'pageTitle')]")
    if len(titles) > 0:
        website_elements['name'] = titles[0].text
    divelements = document.xpath("//div[contains(@class,'fLeft borderRightCD')]")
    
    if len(divelements) > 0:
        divelement = divelements[0]
        table = divelement.find("table")
        children = table.getchildren()
        for tr in children:
            tds = tr.getchildren()
            label = tds[0]
            value = tds[1]
            label_text = label.find("label").text
            """
            if label_text == "Website":
                link = processwebsite(value)
                #content = "%s-%s"%(label_text,link) 
                website_elements['url'] = link
            """
            if label_text == "Overview":
                text = processoverview(value)
                #content = "%s - %s"%(label_text,text)
                website_elements['overview'] = text 
            if label_text == "Headquarters":
                text = processhq(value)
                #content = "%s - %s"%(label_text,text) 
                website_elements['address'] = text 
            if label_text == "Phone":
                #content = "%s -%s" %(label_text,value.text)
                website_elements['phone'] = value.text
            if label_text == "Industries":
                text = processIndustries(value)
                #content =  "%s - %s"%(label_text,text)
                website_elements['industry'] = text
            if label_text == "Employees":
                text = processEmployees(value)
                website_elements['employees'] = text
            if label_text == "Revenue":
                text = processRevenue(value)
                website_elements['revenue'] = text
        return website_elements


city_list = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Jacksonville', 'Indianapolis', 'Austin', 'San Francisco', 'Columbus', 'Fort Worth', 'Charlotte', 'Detroit', 'El Paso', 'Memphis', 'Boston', 'Seattle', 'Denver', 'Baltimore', 'Washington', 'Nashville', 'Louisville', 'Milwaukee', 'Portland', 'Oklahoma City', 'Las Vegas', 'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Long Beach', 'Kansas City', 'Mesa', 'Virginia Beach', 'Atlanta', 'Colorado Springs', 'Raleigh', 'Omaha', 'Miami', 'Tulsa', 'Oakland', 'Cleveland', 'Minneapolis', 'Wichita', 'Arlington', 'New Orleans', 'Bakersfield', 'Tampa', 'Anaheim', 'Honolulu', 'Aurora', 'Santa Ana', 'Saint Louis', 'Riverside', 'Corpus Christi', 'Pittsburgh', 'Lexington', 'Stockton', 'Cincinnati', 'Anchorage', 'Saint Paul', 'Toledo', 'Newark', 'Greensboro', 'Plano', 'Lincoln', 'Buffalo', 'Henderson', 'Fort Wayne', 'Jersey City', 'Chula Vista', 'Saint Petersburg', 'Orlando', 'Norfolk', 'Laredo', 'Chandler', 'Madison', 'Lubbock', 'Durham', 'Winston-Salem', 'Garland', 'Glendale', 'Baton Rouge', 'Hialeah', 'Reno', 'Chesapeake', 'Scottsdale', 'Irving', 'North Las Vegas', 'Fremont', 'Irvine', 'San Bernardino', 'Birmingham', 'Gilbert', 'Rochester', 'Boise', 'Spokane', 'Montgomery', 'Des Moines', 'Richmond', 'Fayetteville', 'Modesto', 'Shreveport', 'Tacoma', 'Oxnard', 'Aurora', 'Fontana', 'Akron', 'Moreno Valley', 'Yonkers', 'Augusta', 'Little Rock', 'Mobile', 'Columbus', 'Amarillo', 'Glendale', 'Huntington Beach', 'Salt Lake City', 'Grand Rapids', 'Tallahassee', 'Huntsville', 'Worcester', 'Knoxville', 'Newport News', 'Grand Prairie', 'Brownsville', 'Providence', 'Santa Clarita', 'Overland Park', 'Jackson', 'Garden Grove', 'Chattanooga', 'Oceanside', 'Santa Rosa', 'Fort Lauderdale', 'Rancho Cucamonga', 'Ontario', 'Port Saint Lucie', 'Vancouver', 'Tempe', 'Springfield', 'Lancaster', 'Pembroke Pines', 'Cape Coral', 'Eugene', 'Peoria', 'Sioux Falls', 'Salem', 'Corona', 'Elk Grove', 'Palmdale', 'Springfield', 'Salinas', 'Pasadena', 'Rockford', 'Pomona', 'Joliet', 'Fort Collins', 'Torrance', 'Kansas City', 'Paterson', 'Hayward', 'Escondido', 'Bridgeport', 'Syracuse', 'Lakewood', 'Alexandria', 'Hollywood', 'Naperville', 'Mesquite', 'Sunnyvale', 'Dayton', 'Cary', 'Savannah', 'Orange', 'Pasadena', 'Fullerton', 'Hampton', 'Clarksville', 'McKinney', 'Warren', 'McAllen', 'West Valley City', 'Columbia', 'Killeen', 'Sterling Heights', 'New Haven', 'Topeka', 'Thousand Oaks', 'Olathe', 'Cedar Rapids', 'Waco', 'Visalia', 'Elizabeth', 'Simi Valley', 'Gainesville', 'Hartford', 'Bellevue', 'Miramar', 'Concord', 'Stamford', 'Coral Springs', 'Charleston', 'Carrollton', 'Lafayette', 'Roseville', 'Thornton', 'Frisco', 'Kent', 'Surprise', 'Allentown', 'Beaumont', 'Santa Clara', 'Abilene', 'Evansville', 'Victorville', 'Independence', 'Denton', 'Springfield', 'Vallejo', 'Athens', 'Provo', 'Peoria', 'Ann Arbor', 'Lansing', 'El Monte', 'Midland', 'Berkeley', 'Norman', 'Downey', 'Costa Mesa', 'Murfreesboro', 'Inglewood', 'Columbia', 'Waterbury', 'Manchester', 'Miami Gardens', 'Elgin', 'Wilmington', 'Westminster', 'Rochester', 'Clearwater', 'Lowell', 'Pueblo', 'Arvada', 'Ventura', 'Gresham', 'Fargo', 'Carlsbad', 'West Covina', 'Norwalk', 'Fairfield', 'Cambridge', 'Murrieta', 'Green Bay', 'High Point', 'West Jordan', 'Billings', 'Richmond', 'Round Rock', 'Everett', 'Burbank', 'Antioch', 'Wichita Falls', 'Palm Bay', 'Centennial', 'Temecula', 'Daly City', 'Odessa', 'Erie', 'Richardson', 'Pompano Beach', 'Flint', 'South Bend', 'West Palm Beach', 'El Cajon', 'Davenport', 'Rialto', 'Santa Maria', 'Broken Arrow']

"""
partner_data = []
session = requests.session()
for city_name in city_list[1:]:
    params = {'id':'0','method':"GetPartnerList",'params':'[{"partnername":"","city":"%s","state":"","zip":"","country":"United States","product":"","size":"","area":"","distance":"","sortby":"certificationlevel"}]'%(city_name)}
    json_request_data = json.dumps(params)
    print "posting to "+city_name
    resp = session.post("http://www.avaya.com/usa/PartnerLocator.ashx",data = json_request_data)
    json_data = json.loads(resp.text)
    if 'result' in json_data:
        result = json_data['result']
        if 'partners' in result:
            partners = result['partners']
            partners_json = json.dumps(partners)
            for partner in partners:
                company_id = partner.get("id")
                company_name = partner.get("name")
                contact = partner.get("contact",{})
                notes = partner.get('notes','')
                awards = partner.get('awards',{})
                if contact not in EMPTY_VALUES:
                    website = contact.get("website",None)
                    primary_phone = contact.get('phone','')
                    if notes not in EMPTY_VALUES:
                        data_dict = {
                           'name':company_name,
                           'url': website,
                           'relationship_type': 'Reseller',
                           'company_properties':{
                                    'federal_authorized':False,
                                    'state_authorized': False,
                                    'local_authorized': False,
                                     'edu_authorized': False
                           },
                           'primary_phone': primary_phone

                        }
                        notes = notes.split(',')
                        if len(notes) > 0:
                            
                            relationship_properties = {'reseller_level': notes[0]}
                            if len(notes) > 1:
                                specializations = ",".join(notes[1:])
                                relationship_properties['specialization'] = specializations
                            if awards not in EMPTY_VALUES:
                                awards_list = []
                                for key,value in awards.items():
                                    awards_list.append('%s:%s' %(key,value))
                                    awards = ",".join(awards)
                                relationship_properties['awards'] = awards
                            data_dict['relationship_properties'] = relationship_properties
                        data_dict['address'] = partner.get('address',{})
                        scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_incomplete", verbose=2)
                        partner_data.append(data_dict)
                                
    else:
        print "No results found for city "+city_name

print partner_data
"""

"""
## only get unique company names from the above list
data_list = scraperwiki.sqlite.execute("select * from avaya_reseller_incomplete")
keys = data_list.get('keys')
data = data_list.get('data')
partner_data = []
names_seen = []
for item in data:
    tmp_dict = {}
    counter = 0
    to_add = True
    for value in item:
        key = keys[counter]
        if key == "name":
            if value not in names_seen:
                names_seen.append(value)
            else:
                to_add = False
                break
        tmp_dict[key] = value
        counter += 1
    if to_add:
        partner_data.append(tmp_dict)

for data in partner_data:
    if data not in EMPTY_VALUES:
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name="avaya_reseller_incomplete_v2", verbose=2)
## end of unique companies
"""



### after getting all the items
URL_NOT_FOUND_COMPANIES = []
MULTIPLE_COMPANIES = []

def process_partner_data_without_url(data):
    company_name = data.get('name')
    if '/' in company_name:
         company_name = company_name.split('/')[1]
    elif ':' in company_name:
        company_name = company_name.split(':')[1]
    company_name_encoded = urllib.quote_plus(company_name)
    company_search_url = "http://www.jigsaw.com/SearchCompany.xhtml?opCode=search&orderby=0&order=0&nextURL=&mode=0&countryvalue=&statevalue=&metrovalue=&indvalue=&subindvalue=&companyIds=&showAdvancedSearch=true&name=%s&cnArea1=&cnZip=&fortune=0&screenNameType=0&screenName=&omitScreenNameType=0&omitScreenName=" %(company_name_encoded)
    jigsaw_data = scraperwiki.scrape(company_search_url)
    document = html.fromstring(jigsaw_data)
    sortedTable = document.xpath("//table[contains(@id,'sortableTable')]")
    if len(sortedTable) > 0:
        mult = {'name': company_name,'url': company_search_url}
        MULTIPLE_COMPANIES.append(data)
    elif "did not match any results" in data:
        #print "Company URL not found:%s,%s" %(company_name,company_search_url)
        URL_NOT_FOUND_COMPANIES.append(data)
    else:
        jigsaw_url = company_search_url
        jigsaw_data = scraperwiki.scrape(jigsaw_url)
        document = html.fromstring(jigsaw_data)
        details = __processSingleCompanyDetails(document)
        if details is not None:
            data['overview'] = details.get('overview',None)
            data['revenue'] = details.get('revenue',None)
            data['employees'] = details.get('employees',None)
            orig_phone = data.get('primary_phone')
            data['primary_phone'] = details.get('phone',orig_phone)
            data['industries'] = details.get('industry',None)
            data['jigsaw_address'] = details.get('address',None)
        else:
            data['company_overview'] = data['revenue'] = data['employees'] = data['industries'] = data['jigsaw_address'] = None
        print "Single company returned:%s" %(company_search_url)
        return data,True
    return data,False

def process_partner_data_with_url(item):
    url = item['url']
    elements = urlparse(url)
    try:
        jigsaw_url = "http://www.jigsaw.com/FreeTextSearch.xhtml?opCode=search&autoSuggested=true&freeText=%s" %(elements.netloc)
        data = scraperwiki.scrape(jigsaw_url)
        document = html.fromstring(data)
        details = __processSingleCompanyDetails(document)
        if details is not None:
            item['overview'] = details.get('overview',None)
            item['revenue'] = details.get('revenue',None)
            item['employees'] = details.get('employees',None)
            orig_phone = data.get('primary_phone')
            if orig_phone in EMPTY_VALUES:
                item['primary_phone'] = details.get('phone',None)
            item['industries'] = details.get('industry',None)
            item['jigsaw_address'] = details.get('address',None)
        else:
            item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = data['jigsaw_address'] = None
    except:
        item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = data['jigsaw_address'] = None
    return item

data_list = scraperwiki.sqlite.execute("select * from avaya_reseller_incomplete_v2")
keys = data_list.get('keys')
data = data_list.get('data')
partner_data = []
for item in data:
    tmp_dict = {}
    counter = 0
    for value in item:
        key = keys[counter]
        tmp_dict[key] = value
        counter += 1
    partner_data.append(tmp_dict)

for data in partner_data:
    url = data.get('ur',None)
    if url in EMPTY_VALUES:
        data_dict,processed = process_partner_data_without_url(data)
        if processed:
            scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_processed", verbose=2)
    else:
        data_dict = process_partner_data_with_url(data)
        if data_dict not in EMPTY_VALUES:
            scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_processed", verbose=2)
        
print "URL NOT FOUND:%s" %(URL_NOT_FOUND_COMPANIES)
print "MULTIPLE COMPANIES_FOUND:%s" %(MULTIPLE_COMPANIES)


"""
multiple_companies = [{u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'(646) 348-6464', u'url': u'www.consultedge.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert,Services Expert'}", u'address': u"{u'distance': 2.8, u'zipPostalCode': u'10018', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'501 7TH AVE, STE 520', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'2128857600', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 3, u'zipPostalCode': u'10017', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'18 East 41st Street, FLOOR 2', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'BLACK BOX NETWORK SERVICES', u'primary_phone': u'(877) 500-4778', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 3.2, u'zipPostalCode': u'10177-0399', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'250 Park Ave, Floor 3', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 3.4, u'zipPostalCode': u'10036-5000', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'546 5th Ave, Fl 10', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'9738087000', u'url': u'www.spscom.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 19.6, u'zipPostalCode': u'07004', u'city': u'Fairfield', u'country': u'United States', u'state': u'New Jersey', u'street': u'15 Gardner Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 20.2, u'zipPostalCode': u'08837-2226', u'city': u'Edison', u'country': u'United States', u'state': u'New Jersey', u'street': u'379 Thornall St, Ste 12', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 21.8, u'zipPostalCode': u'07932-1212', u'city': u'Florham Park', u'country': u'United States', u'state': u'New Jersey', u'street': u'325 Columbia Tpke, Ste 102', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'9738841400', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 22.4, u'zipPostalCode': u'07981', u'city': u'Whippany', u'country': u'United States', u'state': u'New Jersey', u'street': u'9 Whippany Road, B2-7', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 26.3, u'zipPostalCode': u'11791', u'city': u'Syosset', u'country': u'United States', u'state': u'New York', u'street': u'6800 Jericho Turnpike', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Verizon Business', u'primary_phone': u'(877) 297-7816', u'url': u'www.verizonbusiness.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert,Services Expert'}", u'address': u"{u'distance': 27.7, u'zipPostalCode': u'07920', u'city': u'Basking Ridge', u'country': u'United States', u'state': u'New Jersey', u'street': u'One Verizon Way', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 33.8, u'zipPostalCode': u'06902-3734', u'city': u'Stamford', u'country': u'United States', u'state': u'Connecticut', u'street': u'9 West Broad St, Ste 2', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'88877772805321', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 37, u'zipPostalCode': u'06820', u'city': u'Darien', u'country': u'United States', u'state': u'Connecticut', u'street': u'3 Throndal Circle', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'9738525247', u'url': u'.spscom.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 70.1, u'zipPostalCode': u'19103', u'city': u'Horsham', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'113 Gibraltar Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'(800) 626-2515', u'url': u'www.consultedge.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 76.6, u'zipPostalCode': u'19446', u'city': u'Lansdale', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'621 Garfield Ave.', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Black Box Network Services', u'primary_phone': u'215-654-9226', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum'}", u'address': u"{u'distance': 78.3, u'zipPostalCode': u'19422', u'city': u'Blue Bell', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'540 Township Line Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'BLACK BOX NETWORK SERVICES', u'primary_phone': u'(877) 500-4778', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 78.3, u'zipPostalCode': u'19422', u'city': u'Blue Bell', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'540 Township Line Rd', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 79.1, u'zipPostalCode': u'19123', u'city': u'Philadelphia', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'520 N Delaware Avenue', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Johnston Communications', u'primary_phone': u'212-860-6633', u'url': '', u'relationship_properties': u"{'reseller_level': u'Gold', 'awards': u'outstanding_satisfaction', 'specialization': u'Services Expert'}", u'address': u"{u'distance': 2.8, u'zipPostalCode': u'10018', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'1375 Broadway, 3rd Floor', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CONSOLIDATED TECHNOLOGIES, INC.', u'primary_phone': u'9149356000', u'url': u'www.consoltech.com', u'relationship_properties': u"{'reseller_level': u'Gold', 'specialization': u'SME Expert,Services Expert'}", u'address': u"{u'distance': 26.4, u'zipPostalCode': u'10573', u'city': u'Port Chester', u'country': u'United States', u'state': u'New York', u'street': u'10 Midland Avenue', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CONSOLIDATED TECHNOLOGIES, INC.', u'primary_phone': u'8566264800', u'url': '', u'relationship_properties': u"{'reseller_level': u'Gold', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 43.2, u'zipPostalCode': u'08540', u'city': u'Princeton', u'country': u'United States', u'state': u'New Jersey', u'street': u'13 Roszel Road, Suite C 201', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'DJJ TECHNOLOGIES', u'primary_phone': u'(212) 481-2044', u'url': '', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 2.3, u'zipPostalCode': u'10016', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'233 Fifth Avenue, SUITE 5A', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CASS INC.', u'primary_phone': u'2128567220', u'url': '', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction'}", u'address': u"{u'distance': 3.2, u'zipPostalCode': u'10017', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'555 5th Avenue, 17th Floor', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CASS INC.', u'primary_phone': u'5162477100', u'url': u'www.cassbts.com', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction'}", u'address': u"{u'distance': 18.1, u'zipPostalCode': u'11050', u'city': u'Port Washington', u'country': u'United States', u'state': u'New York', u'street': u'17 Smull Place', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'OFFICE SOLUTIONS, INC.', u'primary_phone': u'7323560200', u'url': u'www.osidirect.com', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction'}", u'address': u"{u'distance': 26.6, u'zipPostalCode': u'07059', u'city': u'Warren', u'country': u'United States', u'state': u'New Jersey', u'street': u'217 Mount Horeb Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'DJJ TECHNOLOGIES', u'primary_phone': u'(800) 355-2952', u'url': u'www.djjtechnologies.com', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 49, u'zipPostalCode': u'11749', u'city': u'Islandia', u'country': u'United States', u'state': u'New York', u'street': u'3116 Expressway Drive South', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Digitel Corporation', u'primary_phone': u'610-522-1111', u'url': '', u'relationship_properties': u"{'reseller_level': u'Silver', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 89, u'zipPostalCode': u'19074', u'city': u'Norwood', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'510 Chester Pike', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Camelot Communications', u'primary_phone': u'(212) 635-2685', u'url': u'www.camelotgrp.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 0.8, u'zipPostalCode': u'10004', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'2 Washington Street', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Connect Communications Inc', u'primary_phone': u'212-244-5100', u'url': u'http://www.connectcomminc.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 2.6, u'zipPostalCode': u'10001-3011', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'1 W 34th St, Suite 903', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'212-448-9633', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 2.7, u'zipPostalCode': u'10016', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'200 Madison Avenue', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Versatech Inc.', u'primary_phone': u'212-501-4900', u'url': u'http://www.VersaTechSolutions.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 2.9, u'zipPostalCode': u'10018-4307', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'545 8th Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Telequest Communication', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 3, u'zipPostalCode': u'10036', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'11 West 42nd Street, Suite 1201', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CTVI DBA: EAGLE CONSULTANTS', u'primary_phone': u'7182528075', u'url': u'www.ctvi.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 6.6, u'zipPostalCode': u'11210', u'city': u'Brooklyn', u'country': u'United States', u'state': u'New York', u'street': u'2814 Avenue I', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'American Computer Consultants', u'primary_phone': u'(718) 740-0442', u'url': u'www.acc99.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 13.7, u'zipPostalCode': u'11428', u'city': u'Queens Village', u'country': u'United States', u'state': u'New York', u'street': u'212-55 Jamaica Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Com/peripherals Inc', u'primary_phone': u'516-487-0690', u'url': u'http://www.comper.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 14.8, u'zipPostalCode': u'11021', u'city': u'Great Neck', u'country': u'United States', u'state': u'New York', u'street': u'11 Northern Boulevard, Suite C-1', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Data Access Inc', u'primary_phone': u'(201) 843-5468', u'url': u'www.data-access.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 15.2, u'zipPostalCode': u'07430', u'city': u'Paramus', u'country': u'United States', u'state': u'New Jersey', u'street': u'40 Eisenhower Dr', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'DIRECT BUSINESS SERVICES INTERNATIONAL, LLC.  DBA: DBSI', u'primary_phone': u'(800) 400-4901', u'url': u'www.DBSI.net', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 18.2, u'zipPostalCode': u'07004', u'city': u'Fairfield', u'country': u'United States', u'state': u'New Jersey', u'street': u'40 Pier Lane West, PO Box 11145', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'201-890-5414', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 19.3, u'zipPostalCode': u'07936-3149', u'city': u'East Hanover', u'country': u'United States', u'state': u'New Jersey', u'street': u'100 Eagle Rock Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'201-887-1000', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 20.5, u'zipPostalCode': u'07058', u'city': u'Pine Brook', u'country': u'United States', u'state': u'New Jersey', u'street': u'10 Old Bloomfield Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Corporate Computer Solutions', u'primary_phone': u'914-835-1105', u'url': u'http://www. corporatecomputersol.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 22.8, u'zipPostalCode': u'10528-4116', u'city': u'Harrison', u'country': u'United States', u'state': u'New York', u'street': u'55 Halstead Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'908-346-0260', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 22.9, u'zipPostalCode': u'08818', u'city': u'Edison', u'country': u'United States', u'state': u'New Jersey', u'street': u'344 Raritan Pkwy', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'ENTEL SYSTEMS', u'primary_phone': u'2014472000', u'url': u'www.entelsystems.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 24.3, u'zipPostalCode': u'07444', u'city': u'Pompton Plains', u'country': u'United States', u'state': u'New Jersey', u'street': u'230 W. Parkway', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Computer Sciences Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 30.4, u'zipPostalCode': u'07724-2200', u'city': u'Eatontown', u'country': u'United States', u'state': u'New Jersey', u'street': u'442 State Route 35 South', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Vicom Computer Services Inc', u'primary_phone': u'631-694-3900', u'url': u'http://WWW.VICOMNET.COM', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 30.8, u'zipPostalCode': u'11735-1525', u'city': u'Farmingdale', u'country': u'United States', u'state': u'New York', u'street': u'60 Carolyn Blvd', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Kehley Construction LLC DBA: Northeastern Communications', u'primary_phone': u'(732) 333-5934', u'url': u'www.necommnyc.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 33.5, u'zipPostalCode': u'07726', u'city': u'Manalapan', u'country': u'United States', u'state': u'New Jersey', u'street': u'124 Park Avenue (Tech Park) rt33', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'203-356-1920', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 34.3, u'zipPostalCode': u'06905-4310', u'city': u'Stamford', u'country': u'United States', u'state': u'Connecticut', u'street': u'2777 Summer St', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Comnet Communications Llc', u'primary_phone': u'904-464-0114', u'url': u'http://www.comnetcomm.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 53.2, u'zipPostalCode': u'06810-5100', u'city': u'Danbury', u'country': u'United States', u'state': u'Connecticut', u'street': u'39 Old Ridgebury Rd, Ste 3', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'215-428-3820', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 53.6, u'zipPostalCode': u'19067-6649', u'city': u'Morrisville', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'325 Harper Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 55.2, u'zipPostalCode': u'08721-1379', u'city': u'Bayville', u'country': u'United States', u'state': u'New Jersey', u'street': u'30 Sunnydale Dr', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'TRICOM SYSTEMS, INC.', u'primary_phone': u'2038768500', u'url': u'http://tricom-systems.net', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 63.5, u'zipPostalCode': u'06460', u'city': u'Milford', u'country': u'United States', u'state': u'Connecticut', u'street': u'233 Research Drive, Unit 10', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'GLOBAL LINK COMMUNICATIONS, INC', u'primary_phone': u'2156330300', u'url': u'http://www.glinkcomm.net', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 65, u'zipPostalCode': u'19020', u'city': u'Bensalem', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'3448 Progress Drive, Suite A', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'T3 Technologies, LLC', u'primary_phone': u'(484) 357-0190', u'url': u'www.t3-tek.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 78.4, u'zipPostalCode': u'18052', u'city': u'Whitehall', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'P.O. Box 289', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'HENKELS & MCCOY, INC.', u'primary_phone': u'(484) 344-2161', u'url': u'www.henkelsnetworks.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 80, u'zipPostalCode': u'19462', u'city': u'Plymouth Meeting', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'450 Davis Drive', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}]

for data_dict in multiple_companies:
    scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_multiple_companies", verbose=2)
"""import scraperwiki
import json
from lxml import html
from lxml.etree import tostring
import urllib
import requests
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import re
import cgi
import urllib

# Blank Python

EMPTY_VALUES = (None, '', [], (), {},'None')

def strip_tags(document):
    return ''.join(BeautifulSoup(document).findAll(text=True))

def remove_comments(page):
    soup = BeautifulSoup(page)
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    return soup.prettify()

def processoverview(value):
    value_text = tostring(value)
    value_text = strip_tags(value_text)
    value_text = value_text.replace("&#13;","")
    value_text = value_text.replace('view more and edit','')
    value_text = value_text.replace('&#160;',' ')
    value_text = value_text.replace('if company wiki -','')
    value_text = value_text.strip('\n').strip('\r')
    value_text = value_text.strip()
    return value_text


def processhq(value):
    text = []
    children = value.getchildren()
    for c in children:
        value_text = tostring(c)
        value_text = value_text.replace("&#13;","")
        value_text = value_text.replace("&#160;map","")
        value_text = value_text.replace("&#160;","")
        value_text = value_text.replace("&#8217;","'")
        value_text = value_text.strip()
        if value_text not in EMPTY_VALUES:
            text.append(value_text)
    text = list(set(text))
    text = " ".join(text)
    text = strip_tags(text)
    text = text.replace("map","")
    pattern = re.compile(r'\s+')
    text = re.sub(pattern,' ',text)
    text = text.strip('\n').strip('\r').strip()
    return text

def processIndustries(value):
    text = []
    children = value.getchildren()
    for c in children:
        value_text = tostring(c)
        value_text = strip_tags(value_text)
        value_text = value_text.replace("&#13;","")
        value_text = value_text.replace('amp;','')
        if value_text not in EMPTY_VALUES:
            text.append(value_text)
    text = list(set(text))
    text = ",".join(text)
    pattern = re.compile(r'\s+')
    text = re.sub(pattern,' ',text)
    escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
    text = str(escaped)
    text = text.replace('amp;','')
    text = text.strip('\n').strip('\r').strip()
    return text

def processText(value):
    text = ''
    children = value.getchildren()
    if len(children) > 0:
        text = []
        for c in children:
            value_text = tostring(c)
            value_text = strip_tags(value_text)
            value_text = value_text.replace("&#13;","")
            value_text = value_text.replace('&gt;',">")
            value_text = value_text.replace("&lt;","<")
            if value_text not in EMPTY_VALUES:
                text.append(value_text)
        text = list(set(text))
        text = " ".join(text)
        pattern = re.compile(r'\s+')
        escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
        text = str(escaped)
        text = re.sub(pattern,' ',text)
    else:
        value_text = tostring(value)
        value_text = strip_tags(value_text)
        value_text = value_text.replace("&#13;","")
        value_text = value_text.replace('&gt;',">")
        value_text = value_text.replace("&lt;","<")
        text = value_text
        pattern = re.compile(r'\s+')
        text = re.sub(pattern,' ',text)
        escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
        text = str(escaped)
    return text


def get_units(value):
    units = None
    value = str(value)
    if 'M' in value or 'm' in value:
        units = 'M'
    if 'K' in value or 'k' in value:
        units = 'K'
    if 'b' in value or 'B' in value:
        units = 'B'
    return units

def processValue(value,units):
    value = value.strip()
    regex = re.compile(r'[^\d.]+')
    actual = regex.sub('',value)
    actual = float(str(actual))
    if units == 'K':
        actual = actual*float(1000)
    elif units == 'M':
        actual = actual * float(1000000)
    elif units == 'B':
        actual = actual * float(1000000000)
    return actual


def processRanges(ranges,ptype,is_range):
    start = ranges[0]
    end = ranges[1]
    start_units = get_units(start)
    end_units = get_units(end)
    if not start_units:
        start_units = end_units
    startValue = processValue(start, start_units)
    endValue = processValue(end, end_units)
    if ptype == "EMPLOYEES" and start_units is not None and end_units is not None:
        startValue = startValue * 1000 ## because processValue reduces everything by 1000 in case of units available
        endValue = endValue * 1000
    if is_range:
        return [startValue,endValue]
    else:
        actual = int((startValue+endValue)/2)
        return actual

def pre_process_value(value):
    items = []
    if value not in EMPTY_VALUES:
        escaped = cgi.escape(value).encode('ascii','xmlcharrefreplace')
        value = str(value)
        value = value.replace("<","").replace(">","").replace('$','')
        items = value.split('-')
    return items


def revenue_actual(revenue):
    revenue_items = pre_process_value(revenue)
    units = get_units(revenue)
    if len(revenue_items) == 0:
        return None
    if len(revenue_items) > 1:
        actual_revenue = processRanges(revenue_items,"REVENUE",False)
    else:
        actual_revenue = processValue(revenue, units)
    return actual_revenue

def processRevenue(value):
    text = processText(value)
    text = text.replace('&gt;',"")
    text = text.replace("&lt;","")
    escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
    text = str(escaped).strip()
    actual_revenue = revenue_actual(text)
    return actual_revenue


def employees_actual(employees):
    employee_items = pre_process_value(employees)
    if len(employee_items) == 0:
        return None
    if len(employee_items) > 1:
        actual_employees = processRanges(employee_items,"EMPLOYEES",False)
    else:
        units = get_units(employees)
        actual_employees = processValue(employees,units)
    return actual_employees

def processEmployees(value):
    text = processText(value)
    text = text.replace('&gt;',"")
    text = text.replace("&lt;","")
    escaped = cgi.escape(text).encode('ascii','xmlcharrefreplace')
    text = text.replace(',','')
    text = str(escaped).strip()
    actual_employees = employees_actual(text)
    return actual_employees



def __processSingleCompanyDetails(document):
    ## just a single company, get the company email domain maybe
    website_elements = {}
    titles = document.xpath("//p[contains(@id,'pageTitle')]")
    if len(titles) > 0:
        website_elements['name'] = titles[0].text
    divelements = document.xpath("//div[contains(@class,'fLeft borderRightCD')]")
    
    if len(divelements) > 0:
        divelement = divelements[0]
        table = divelement.find("table")
        children = table.getchildren()
        for tr in children:
            tds = tr.getchildren()
            label = tds[0]
            value = tds[1]
            label_text = label.find("label").text
            """
            if label_text == "Website":
                link = processwebsite(value)
                #content = "%s-%s"%(label_text,link) 
                website_elements['url'] = link
            """
            if label_text == "Overview":
                text = processoverview(value)
                #content = "%s - %s"%(label_text,text)
                website_elements['overview'] = text 
            if label_text == "Headquarters":
                text = processhq(value)
                #content = "%s - %s"%(label_text,text) 
                website_elements['address'] = text 
            if label_text == "Phone":
                #content = "%s -%s" %(label_text,value.text)
                website_elements['phone'] = value.text
            if label_text == "Industries":
                text = processIndustries(value)
                #content =  "%s - %s"%(label_text,text)
                website_elements['industry'] = text
            if label_text == "Employees":
                text = processEmployees(value)
                website_elements['employees'] = text
            if label_text == "Revenue":
                text = processRevenue(value)
                website_elements['revenue'] = text
        return website_elements


city_list = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Jacksonville', 'Indianapolis', 'Austin', 'San Francisco', 'Columbus', 'Fort Worth', 'Charlotte', 'Detroit', 'El Paso', 'Memphis', 'Boston', 'Seattle', 'Denver', 'Baltimore', 'Washington', 'Nashville', 'Louisville', 'Milwaukee', 'Portland', 'Oklahoma City', 'Las Vegas', 'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Long Beach', 'Kansas City', 'Mesa', 'Virginia Beach', 'Atlanta', 'Colorado Springs', 'Raleigh', 'Omaha', 'Miami', 'Tulsa', 'Oakland', 'Cleveland', 'Minneapolis', 'Wichita', 'Arlington', 'New Orleans', 'Bakersfield', 'Tampa', 'Anaheim', 'Honolulu', 'Aurora', 'Santa Ana', 'Saint Louis', 'Riverside', 'Corpus Christi', 'Pittsburgh', 'Lexington', 'Stockton', 'Cincinnati', 'Anchorage', 'Saint Paul', 'Toledo', 'Newark', 'Greensboro', 'Plano', 'Lincoln', 'Buffalo', 'Henderson', 'Fort Wayne', 'Jersey City', 'Chula Vista', 'Saint Petersburg', 'Orlando', 'Norfolk', 'Laredo', 'Chandler', 'Madison', 'Lubbock', 'Durham', 'Winston-Salem', 'Garland', 'Glendale', 'Baton Rouge', 'Hialeah', 'Reno', 'Chesapeake', 'Scottsdale', 'Irving', 'North Las Vegas', 'Fremont', 'Irvine', 'San Bernardino', 'Birmingham', 'Gilbert', 'Rochester', 'Boise', 'Spokane', 'Montgomery', 'Des Moines', 'Richmond', 'Fayetteville', 'Modesto', 'Shreveport', 'Tacoma', 'Oxnard', 'Aurora', 'Fontana', 'Akron', 'Moreno Valley', 'Yonkers', 'Augusta', 'Little Rock', 'Mobile', 'Columbus', 'Amarillo', 'Glendale', 'Huntington Beach', 'Salt Lake City', 'Grand Rapids', 'Tallahassee', 'Huntsville', 'Worcester', 'Knoxville', 'Newport News', 'Grand Prairie', 'Brownsville', 'Providence', 'Santa Clarita', 'Overland Park', 'Jackson', 'Garden Grove', 'Chattanooga', 'Oceanside', 'Santa Rosa', 'Fort Lauderdale', 'Rancho Cucamonga', 'Ontario', 'Port Saint Lucie', 'Vancouver', 'Tempe', 'Springfield', 'Lancaster', 'Pembroke Pines', 'Cape Coral', 'Eugene', 'Peoria', 'Sioux Falls', 'Salem', 'Corona', 'Elk Grove', 'Palmdale', 'Springfield', 'Salinas', 'Pasadena', 'Rockford', 'Pomona', 'Joliet', 'Fort Collins', 'Torrance', 'Kansas City', 'Paterson', 'Hayward', 'Escondido', 'Bridgeport', 'Syracuse', 'Lakewood', 'Alexandria', 'Hollywood', 'Naperville', 'Mesquite', 'Sunnyvale', 'Dayton', 'Cary', 'Savannah', 'Orange', 'Pasadena', 'Fullerton', 'Hampton', 'Clarksville', 'McKinney', 'Warren', 'McAllen', 'West Valley City', 'Columbia', 'Killeen', 'Sterling Heights', 'New Haven', 'Topeka', 'Thousand Oaks', 'Olathe', 'Cedar Rapids', 'Waco', 'Visalia', 'Elizabeth', 'Simi Valley', 'Gainesville', 'Hartford', 'Bellevue', 'Miramar', 'Concord', 'Stamford', 'Coral Springs', 'Charleston', 'Carrollton', 'Lafayette', 'Roseville', 'Thornton', 'Frisco', 'Kent', 'Surprise', 'Allentown', 'Beaumont', 'Santa Clara', 'Abilene', 'Evansville', 'Victorville', 'Independence', 'Denton', 'Springfield', 'Vallejo', 'Athens', 'Provo', 'Peoria', 'Ann Arbor', 'Lansing', 'El Monte', 'Midland', 'Berkeley', 'Norman', 'Downey', 'Costa Mesa', 'Murfreesboro', 'Inglewood', 'Columbia', 'Waterbury', 'Manchester', 'Miami Gardens', 'Elgin', 'Wilmington', 'Westminster', 'Rochester', 'Clearwater', 'Lowell', 'Pueblo', 'Arvada', 'Ventura', 'Gresham', 'Fargo', 'Carlsbad', 'West Covina', 'Norwalk', 'Fairfield', 'Cambridge', 'Murrieta', 'Green Bay', 'High Point', 'West Jordan', 'Billings', 'Richmond', 'Round Rock', 'Everett', 'Burbank', 'Antioch', 'Wichita Falls', 'Palm Bay', 'Centennial', 'Temecula', 'Daly City', 'Odessa', 'Erie', 'Richardson', 'Pompano Beach', 'Flint', 'South Bend', 'West Palm Beach', 'El Cajon', 'Davenport', 'Rialto', 'Santa Maria', 'Broken Arrow']

"""
partner_data = []
session = requests.session()
for city_name in city_list[1:]:
    params = {'id':'0','method':"GetPartnerList",'params':'[{"partnername":"","city":"%s","state":"","zip":"","country":"United States","product":"","size":"","area":"","distance":"","sortby":"certificationlevel"}]'%(city_name)}
    json_request_data = json.dumps(params)
    print "posting to "+city_name
    resp = session.post("http://www.avaya.com/usa/PartnerLocator.ashx",data = json_request_data)
    json_data = json.loads(resp.text)
    if 'result' in json_data:
        result = json_data['result']
        if 'partners' in result:
            partners = result['partners']
            partners_json = json.dumps(partners)
            for partner in partners:
                company_id = partner.get("id")
                company_name = partner.get("name")
                contact = partner.get("contact",{})
                notes = partner.get('notes','')
                awards = partner.get('awards',{})
                if contact not in EMPTY_VALUES:
                    website = contact.get("website",None)
                    primary_phone = contact.get('phone','')
                    if notes not in EMPTY_VALUES:
                        data_dict = {
                           'name':company_name,
                           'url': website,
                           'relationship_type': 'Reseller',
                           'company_properties':{
                                    'federal_authorized':False,
                                    'state_authorized': False,
                                    'local_authorized': False,
                                     'edu_authorized': False
                           },
                           'primary_phone': primary_phone

                        }
                        notes = notes.split(',')
                        if len(notes) > 0:
                            
                            relationship_properties = {'reseller_level': notes[0]}
                            if len(notes) > 1:
                                specializations = ",".join(notes[1:])
                                relationship_properties['specialization'] = specializations
                            if awards not in EMPTY_VALUES:
                                awards_list = []
                                for key,value in awards.items():
                                    awards_list.append('%s:%s' %(key,value))
                                    awards = ",".join(awards)
                                relationship_properties['awards'] = awards
                            data_dict['relationship_properties'] = relationship_properties
                        data_dict['address'] = partner.get('address',{})
                        scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_incomplete", verbose=2)
                        partner_data.append(data_dict)
                                
    else:
        print "No results found for city "+city_name

print partner_data
"""

"""
## only get unique company names from the above list
data_list = scraperwiki.sqlite.execute("select * from avaya_reseller_incomplete")
keys = data_list.get('keys')
data = data_list.get('data')
partner_data = []
names_seen = []
for item in data:
    tmp_dict = {}
    counter = 0
    to_add = True
    for value in item:
        key = keys[counter]
        if key == "name":
            if value not in names_seen:
                names_seen.append(value)
            else:
                to_add = False
                break
        tmp_dict[key] = value
        counter += 1
    if to_add:
        partner_data.append(tmp_dict)

for data in partner_data:
    if data not in EMPTY_VALUES:
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name="avaya_reseller_incomplete_v2", verbose=2)
## end of unique companies
"""



### after getting all the items
URL_NOT_FOUND_COMPANIES = []
MULTIPLE_COMPANIES = []

def process_partner_data_without_url(data):
    company_name = data.get('name')
    if '/' in company_name:
         company_name = company_name.split('/')[1]
    elif ':' in company_name:
        company_name = company_name.split(':')[1]
    company_name_encoded = urllib.quote_plus(company_name)
    company_search_url = "http://www.jigsaw.com/SearchCompany.xhtml?opCode=search&orderby=0&order=0&nextURL=&mode=0&countryvalue=&statevalue=&metrovalue=&indvalue=&subindvalue=&companyIds=&showAdvancedSearch=true&name=%s&cnArea1=&cnZip=&fortune=0&screenNameType=0&screenName=&omitScreenNameType=0&omitScreenName=" %(company_name_encoded)
    jigsaw_data = scraperwiki.scrape(company_search_url)
    document = html.fromstring(jigsaw_data)
    sortedTable = document.xpath("//table[contains(@id,'sortableTable')]")
    if len(sortedTable) > 0:
        mult = {'name': company_name,'url': company_search_url}
        MULTIPLE_COMPANIES.append(data)
    elif "did not match any results" in data:
        #print "Company URL not found:%s,%s" %(company_name,company_search_url)
        URL_NOT_FOUND_COMPANIES.append(data)
    else:
        jigsaw_url = company_search_url
        jigsaw_data = scraperwiki.scrape(jigsaw_url)
        document = html.fromstring(jigsaw_data)
        details = __processSingleCompanyDetails(document)
        if details is not None:
            data['overview'] = details.get('overview',None)
            data['revenue'] = details.get('revenue',None)
            data['employees'] = details.get('employees',None)
            orig_phone = data.get('primary_phone')
            data['primary_phone'] = details.get('phone',orig_phone)
            data['industries'] = details.get('industry',None)
            data['jigsaw_address'] = details.get('address',None)
        else:
            data['company_overview'] = data['revenue'] = data['employees'] = data['industries'] = data['jigsaw_address'] = None
        print "Single company returned:%s" %(company_search_url)
        return data,True
    return data,False

def process_partner_data_with_url(item):
    url = item['url']
    elements = urlparse(url)
    try:
        jigsaw_url = "http://www.jigsaw.com/FreeTextSearch.xhtml?opCode=search&autoSuggested=true&freeText=%s" %(elements.netloc)
        data = scraperwiki.scrape(jigsaw_url)
        document = html.fromstring(data)
        details = __processSingleCompanyDetails(document)
        if details is not None:
            item['overview'] = details.get('overview',None)
            item['revenue'] = details.get('revenue',None)
            item['employees'] = details.get('employees',None)
            orig_phone = data.get('primary_phone')
            if orig_phone in EMPTY_VALUES:
                item['primary_phone'] = details.get('phone',None)
            item['industries'] = details.get('industry',None)
            item['jigsaw_address'] = details.get('address',None)
        else:
            item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = data['jigsaw_address'] = None
    except:
        item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = data['jigsaw_address'] = None
    return item

data_list = scraperwiki.sqlite.execute("select * from avaya_reseller_incomplete_v2")
keys = data_list.get('keys')
data = data_list.get('data')
partner_data = []
for item in data:
    tmp_dict = {}
    counter = 0
    for value in item:
        key = keys[counter]
        tmp_dict[key] = value
        counter += 1
    partner_data.append(tmp_dict)

for data in partner_data:
    url = data.get('ur',None)
    if url in EMPTY_VALUES:
        data_dict,processed = process_partner_data_without_url(data)
        if processed:
            scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_processed", verbose=2)
    else:
        data_dict = process_partner_data_with_url(data)
        if data_dict not in EMPTY_VALUES:
            scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_processed", verbose=2)
        
print "URL NOT FOUND:%s" %(URL_NOT_FOUND_COMPANIES)
print "MULTIPLE COMPANIES_FOUND:%s" %(MULTIPLE_COMPANIES)


"""
multiple_companies = [{u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'(646) 348-6464', u'url': u'www.consultedge.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert,Services Expert'}", u'address': u"{u'distance': 2.8, u'zipPostalCode': u'10018', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'501 7TH AVE, STE 520', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'2128857600', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 3, u'zipPostalCode': u'10017', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'18 East 41st Street, FLOOR 2', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'BLACK BOX NETWORK SERVICES', u'primary_phone': u'(877) 500-4778', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 3.2, u'zipPostalCode': u'10177-0399', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'250 Park Ave, Floor 3', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 3.4, u'zipPostalCode': u'10036-5000', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'546 5th Ave, Fl 10', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'9738087000', u'url': u'www.spscom.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 19.6, u'zipPostalCode': u'07004', u'city': u'Fairfield', u'country': u'United States', u'state': u'New Jersey', u'street': u'15 Gardner Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 20.2, u'zipPostalCode': u'08837-2226', u'city': u'Edison', u'country': u'United States', u'state': u'New Jersey', u'street': u'379 Thornall St, Ste 12', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 21.8, u'zipPostalCode': u'07932-1212', u'city': u'Florham Park', u'country': u'United States', u'state': u'New Jersey', u'street': u'325 Columbia Tpke, Ste 102', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'9738841400', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 22.4, u'zipPostalCode': u'07981', u'city': u'Whippany', u'country': u'United States', u'state': u'New Jersey', u'street': u'9 Whippany Road, B2-7', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 26.3, u'zipPostalCode': u'11791', u'city': u'Syosset', u'country': u'United States', u'state': u'New York', u'street': u'6800 Jericho Turnpike', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Verizon Business', u'primary_phone': u'(877) 297-7816', u'url': u'www.verizonbusiness.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert,Services Expert'}", u'address': u"{u'distance': 27.7, u'zipPostalCode': u'07920', u'city': u'Basking Ridge', u'country': u'United States', u'state': u'New Jersey', u'street': u'One Verizon Way', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 33.8, u'zipPostalCode': u'06902-3734', u'city': u'Stamford', u'country': u'United States', u'state': u'Connecticut', u'street': u'9 West Broad St, Ste 2', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'88877772805321', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 37, u'zipPostalCode': u'06820', u'city': u'Darien', u'country': u'United States', u'state': u'Connecticut', u'street': u'3 Throndal Circle', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'9738525247', u'url': u'.spscom.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 70.1, u'zipPostalCode': u'19103', u'city': u'Horsham', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'113 Gibraltar Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'STRATEGIC PRODUCTS & SERVICES/NEWTON GROUP', u'primary_phone': u'(800) 626-2515', u'url': u'www.consultedge.com', u'relationship_properties': u"{'reseller_level': u'Platinum', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 76.6, u'zipPostalCode': u'19446', u'city': u'Lansdale', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'621 Garfield Ave.', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Black Box Network Services', u'primary_phone': u'215-654-9226', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum'}", u'address': u"{u'distance': 78.3, u'zipPostalCode': u'19422', u'city': u'Blue Bell', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'540 Township Line Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'BLACK BOX NETWORK SERVICES', u'primary_phone': u'(877) 500-4778', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 78.3, u'zipPostalCode': u'19422', u'city': u'Blue Bell', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'540 Township Line Rd', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Qwest Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Platinum', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 79.1, u'zipPostalCode': u'19123', u'city': u'Philadelphia', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'520 N Delaware Avenue', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Johnston Communications', u'primary_phone': u'212-860-6633', u'url': '', u'relationship_properties': u"{'reseller_level': u'Gold', 'awards': u'outstanding_satisfaction', 'specialization': u'Services Expert'}", u'address': u"{u'distance': 2.8, u'zipPostalCode': u'10018', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'1375 Broadway, 3rd Floor', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CONSOLIDATED TECHNOLOGIES, INC.', u'primary_phone': u'9149356000', u'url': u'www.consoltech.com', u'relationship_properties': u"{'reseller_level': u'Gold', 'specialization': u'SME Expert,Services Expert'}", u'address': u"{u'distance': 26.4, u'zipPostalCode': u'10573', u'city': u'Port Chester', u'country': u'United States', u'state': u'New York', u'street': u'10 Midland Avenue', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CONSOLIDATED TECHNOLOGIES, INC.', u'primary_phone': u'8566264800', u'url': '', u'relationship_properties': u"{'reseller_level': u'Gold', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 43.2, u'zipPostalCode': u'08540', u'city': u'Princeton', u'country': u'United States', u'state': u'New Jersey', u'street': u'13 Roszel Road, Suite C 201', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'DJJ TECHNOLOGIES', u'primary_phone': u'(212) 481-2044', u'url': '', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 2.3, u'zipPostalCode': u'10016', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'233 Fifth Avenue, SUITE 5A', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CASS INC.', u'primary_phone': u'2128567220', u'url': '', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction'}", u'address': u"{u'distance': 3.2, u'zipPostalCode': u'10017', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'555 5th Avenue, 17th Floor', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CASS INC.', u'primary_phone': u'5162477100', u'url': u'www.cassbts.com', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction'}", u'address': u"{u'distance': 18.1, u'zipPostalCode': u'11050', u'city': u'Port Washington', u'country': u'United States', u'state': u'New York', u'street': u'17 Smull Place', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'OFFICE SOLUTIONS, INC.', u'primary_phone': u'7323560200', u'url': u'www.osidirect.com', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction'}", u'address': u"{u'distance': 26.6, u'zipPostalCode': u'07059', u'city': u'Warren', u'country': u'United States', u'state': u'New Jersey', u'street': u'217 Mount Horeb Road', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'DJJ TECHNOLOGIES', u'primary_phone': u'(800) 355-2952', u'url': u'www.djjtechnologies.com', u'relationship_properties': u"{'reseller_level': u'Silver', 'awards': u'outstanding_satisfaction', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 49, u'zipPostalCode': u'11749', u'city': u'Islandia', u'country': u'United States', u'state': u'New York', u'street': u'3116 Expressway Drive South', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Digitel Corporation', u'primary_phone': u'610-522-1111', u'url': '', u'relationship_properties': u"{'reseller_level': u'Silver', 'specialization': u'SME Expert'}", u'address': u"{u'distance': 89, u'zipPostalCode': u'19074', u'city': u'Norwood', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'510 Chester Pike', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Camelot Communications', u'primary_phone': u'(212) 635-2685', u'url': u'www.camelotgrp.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 0.8, u'zipPostalCode': u'10004', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'2 Washington Street', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Connect Communications Inc', u'primary_phone': u'212-244-5100', u'url': u'http://www.connectcomminc.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 2.6, u'zipPostalCode': u'10001-3011', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'1 W 34th St, Suite 903', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'212-448-9633', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 2.7, u'zipPostalCode': u'10016', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'200 Madison Avenue', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Versatech Inc.', u'primary_phone': u'212-501-4900', u'url': u'http://www.VersaTechSolutions.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 2.9, u'zipPostalCode': u'10018-4307', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'545 8th Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Telequest Communication', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 3, u'zipPostalCode': u'10036', u'city': u'New York', u'country': u'United States', u'state': u'New York', u'street': u'11 West 42nd Street, Suite 1201', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'CTVI DBA: EAGLE CONSULTANTS', u'primary_phone': u'7182528075', u'url': u'www.ctvi.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 6.6, u'zipPostalCode': u'11210', u'city': u'Brooklyn', u'country': u'United States', u'state': u'New York', u'street': u'2814 Avenue I', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'American Computer Consultants', u'primary_phone': u'(718) 740-0442', u'url': u'www.acc99.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 13.7, u'zipPostalCode': u'11428', u'city': u'Queens Village', u'country': u'United States', u'state': u'New York', u'street': u'212-55 Jamaica Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Com/peripherals Inc', u'primary_phone': u'516-487-0690', u'url': u'http://www.comper.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 14.8, u'zipPostalCode': u'11021', u'city': u'Great Neck', u'country': u'United States', u'state': u'New York', u'street': u'11 Northern Boulevard, Suite C-1', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Data Access Inc', u'primary_phone': u'(201) 843-5468', u'url': u'www.data-access.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 15.2, u'zipPostalCode': u'07430', u'city': u'Paramus', u'country': u'United States', u'state': u'New Jersey', u'street': u'40 Eisenhower Dr', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'DIRECT BUSINESS SERVICES INTERNATIONAL, LLC.  DBA: DBSI', u'primary_phone': u'(800) 400-4901', u'url': u'www.DBSI.net', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 18.2, u'zipPostalCode': u'07004', u'city': u'Fairfield', u'country': u'United States', u'state': u'New Jersey', u'street': u'40 Pier Lane West, PO Box 11145', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'201-890-5414', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 19.3, u'zipPostalCode': u'07936-3149', u'city': u'East Hanover', u'country': u'United States', u'state': u'New Jersey', u'street': u'100 Eagle Rock Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'201-887-1000', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 20.5, u'zipPostalCode': u'07058', u'city': u'Pine Brook', u'country': u'United States', u'state': u'New Jersey', u'street': u'10 Old Bloomfield Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Corporate Computer Solutions', u'primary_phone': u'914-835-1105', u'url': u'http://www. corporatecomputersol.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 22.8, u'zipPostalCode': u'10528-4116', u'city': u'Harrison', u'country': u'United States', u'state': u'New York', u'street': u'55 Halstead Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'908-346-0260', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 22.9, u'zipPostalCode': u'08818', u'city': u'Edison', u'country': u'United States', u'state': u'New Jersey', u'street': u'344 Raritan Pkwy', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'ENTEL SYSTEMS', u'primary_phone': u'2014472000', u'url': u'www.entelsystems.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 24.3, u'zipPostalCode': u'07444', u'city': u'Pompton Plains', u'country': u'United States', u'state': u'New Jersey', u'street': u'230 W. Parkway', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Computer Sciences Corporation', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 30.4, u'zipPostalCode': u'07724-2200', u'city': u'Eatontown', u'country': u'United States', u'state': u'New Jersey', u'street': u'442 State Route 35 South', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Vicom Computer Services Inc', u'primary_phone': u'631-694-3900', u'url': u'http://WWW.VICOMNET.COM', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 30.8, u'zipPostalCode': u'11735-1525', u'city': u'Farmingdale', u'country': u'United States', u'state': u'New York', u'street': u'60 Carolyn Blvd', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Kehley Construction LLC DBA: Northeastern Communications', u'primary_phone': u'(732) 333-5934', u'url': u'www.necommnyc.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 33.5, u'zipPostalCode': u'07726', u'city': u'Manalapan', u'country': u'United States', u'state': u'New Jersey', u'street': u'124 Park Avenue (Tech Park) rt33', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'203-356-1920', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 34.3, u'zipPostalCode': u'06905-4310', u'city': u'Stamford', u'country': u'United States', u'state': u'Connecticut', u'street': u'2777 Summer St', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Comnet Communications Llc', u'primary_phone': u'904-464-0114', u'url': u'http://www.comnetcomm.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 53.2, u'zipPostalCode': u'06810-5100', u'city': u'Danbury', u'country': u'United States', u'state': u'Connecticut', u'street': u'39 Old Ridgebury Rd, Ste 3', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': u'215-428-3820', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 53.6, u'zipPostalCode': u'19067-6649', u'city': u'Morrisville', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'325 Harper Ave', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'Compucom Systems Inc', u'primary_phone': '', u'url': '', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 55.2, u'zipPostalCode': u'08721-1379', u'city': u'Bayville', u'country': u'United States', u'state': u'New Jersey', u'street': u'30 Sunnydale Dr', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'TRICOM SYSTEMS, INC.', u'primary_phone': u'2038768500', u'url': u'http://tricom-systems.net', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 63.5, u'zipPostalCode': u'06460', u'city': u'Milford', u'country': u'United States', u'state': u'Connecticut', u'street': u'233 Research Drive, Unit 10', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'GLOBAL LINK COMMUNICATIONS, INC', u'primary_phone': u'2156330300', u'url': u'http://www.glinkcomm.net', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 65, u'zipPostalCode': u'19020', u'city': u'Bensalem', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'3448 Progress Drive, Suite A', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'T3 Technologies, LLC', u'primary_phone': u'(484) 357-0190', u'url': u'www.t3-tek.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 78.4, u'zipPostalCode': u'18052', u'city': u'Whitehall', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'P.O. Box 289', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}, {u'name': u'HENKELS & MCCOY, INC.', u'primary_phone': u'(484) 344-2161', u'url': u'www.henkelsnetworks.com', u'relationship_properties': u"{'reseller_level': u'Authorized'}", u'address': u"{u'distance': 80, u'zipPostalCode': u'19462', u'city': u'Plymouth Meeting', u'country': u'United States', u'state': u'Pennsylvania', u'street': u'450 Davis Drive', u'id': 0}", u'relationship_type': u'Reseller', u'company_properties': u"{'local_authorized': False, 'state_authorized': False, 'edu_authorized': False, 'federal_authorized': False}"}]

for data_dict in multiple_companies:
    scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_multiple_companies", verbose=2)
"""