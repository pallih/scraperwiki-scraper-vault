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
import ast

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



def load_initial():
    city_list = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Jacksonville', 'Indianapolis', 'Austin', 'San Francisco', 'Columbus', 'Fort Worth', 'Charlotte', 'Detroit', 'El Paso', 'Memphis', 'Boston', 'Seattle', 'Denver', 'Baltimore', 'Washington', 'Nashville', 'Louisville', 'Milwaukee', 'Portland', 'Oklahoma City', 'Las Vegas', 'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Long Beach', 'Kansas City', 'Mesa', 'Virginia Beach', 'Atlanta', 'Colorado Springs', 'Raleigh', 'Omaha', 'Miami', 'Tulsa', 'Oakland', 'Cleveland', 'Minneapolis', 'Wichita', 'Arlington', 'New Orleans', 'Bakersfield', 'Tampa', 'Anaheim', 'Honolulu', 'Aurora', 'Santa Ana', 'Saint Louis', 'Riverside', 'Corpus Christi', 'Pittsburgh', 'Lexington', 'Stockton', 'Cincinnati', 'Anchorage', 'Saint Paul', 'Toledo', 'Newark', 'Greensboro', 'Plano', 'Lincoln', 'Buffalo', 'Henderson', 'Fort Wayne', 'Jersey City', 'Chula Vista', 'Saint Petersburg', 'Orlando', 'Norfolk', 'Laredo', 'Chandler', 'Madison', 'Lubbock', 'Durham', 'Winston-Salem', 'Garland', 'Glendale', 'Baton Rouge', 'Hialeah', 'Reno', 'Chesapeake', 'Scottsdale', 'Irving', 'North Las Vegas', 'Fremont', 'Irvine', 'San Bernardino', 'Birmingham', 'Gilbert', 'Rochester', 'Boise', 'Spokane', 'Montgomery', 'Des Moines', 'Richmond', 'Fayetteville', 'Modesto', 'Shreveport', 'Tacoma', 'Oxnard', 'Aurora', 'Fontana', 'Akron', 'Moreno Valley', 'Yonkers', 'Augusta', 'Little Rock', 'Mobile', 'Columbus', 'Amarillo', 'Glendale', 'Huntington Beach', 'Salt Lake City', 'Grand Rapids', 'Tallahassee', 'Huntsville', 'Worcester', 'Knoxville', 'Newport News', 'Grand Prairie', 'Brownsville', 'Providence', 'Santa Clarita', 'Overland Park', 'Jackson', 'Garden Grove', 'Chattanooga', 'Oceanside', 'Santa Rosa', 'Fort Lauderdale', 'Rancho Cucamonga', 'Ontario', 'Port Saint Lucie', 'Vancouver', 'Tempe', 'Springfield', 'Lancaster', 'Pembroke Pines', 'Cape Coral', 'Eugene', 'Peoria', 'Sioux Falls', 'Salem', 'Corona', 'Elk Grove', 'Palmdale', 'Springfield', 'Salinas', 'Pasadena', 'Rockford', 'Pomona', 'Joliet', 'Fort Collins', 'Torrance', 'Kansas City', 'Paterson', 'Hayward', 'Escondido', 'Bridgeport', 'Syracuse', 'Lakewood', 'Alexandria', 'Hollywood', 'Naperville', 'Mesquite', 'Sunnyvale', 'Dayton', 'Cary', 'Savannah', 'Orange', 'Pasadena', 'Fullerton', 'Hampton', 'Clarksville', 'McKinney', 'Warren', 'McAllen', 'West Valley City', 'Columbia', 'Killeen', 'Sterling Heights', 'New Haven', 'Topeka', 'Thousand Oaks', 'Olathe', 'Cedar Rapids', 'Waco', 'Visalia', 'Elizabeth', 'Simi Valley', 'Gainesville', 'Hartford', 'Bellevue', 'Miramar', 'Concord', 'Stamford', 'Coral Springs', 'Charleston', 'Carrollton', 'Lafayette', 'Roseville', 'Thornton', 'Frisco', 'Kent', 'Surprise', 'Allentown', 'Beaumont', 'Santa Clara', 'Abilene', 'Evansville', 'Victorville', 'Independence', 'Denton', 'Springfield', 'Vallejo', 'Athens', 'Provo', 'Peoria', 'Ann Arbor', 'Lansing', 'El Monte', 'Midland', 'Berkeley', 'Norman', 'Downey', 'Costa Mesa', 'Murfreesboro', 'Inglewood', 'Columbia', 'Waterbury', 'Manchester', 'Miami Gardens', 'Elgin', 'Wilmington', 'Westminster', 'Rochester', 'Clearwater', 'Lowell', 'Pueblo', 'Arvada', 'Ventura', 'Gresham', 'Fargo', 'Carlsbad', 'West Covina', 'Norwalk', 'Fairfield', 'Cambridge', 'Murrieta', 'Green Bay', 'High Point', 'West Jordan', 'Billings', 'Richmond', 'Round Rock', 'Everett', 'Burbank', 'Antioch', 'Wichita Falls', 'Palm Bay', 'Centennial', 'Temecula', 'Daly City', 'Odessa', 'Erie', 'Richardson', 'Pompano Beach', 'Flint', 'South Bend', 'West Palm Beach', 'El Cajon', 'Davenport', 'Rialto', 'Santa Maria', 'Broken Arrow']

    partner_data = []
    session = requests.session()
    names_seen = []
    for city_name in city_list:
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
                    if company_name not in names_seen:
                        names_seen.append(company_name)
                    else:
                        continue
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
                            #scraperwiki.sqlite.save(unique_keys=[], data=data_dict, table_name="avaya_reseller_incomplete", verbose=2)
                            partner_data.append(data_dict)
                                    
        else:
            print "No results found for city "+city_name
    
    print len(partner_data)
    
    for data in partner_data:
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name="avaya_reseller_incomplete", verbose=2)


def process_jigsaw_data(companies):
    index = 0
    for item in companies:
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
                primary_phone = item['primary_phone']
                if primary_phone in EMPTY_VALUES:
                    item['primary_phone'] = details.get('phone',primary_phone)
                item['industries'] = details.get('industry',None)
                item['jigsaw_address'] = details.get('address',None)
            else:
                item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = item['jigsaw_address'] = None
        except Exception,e:
            print "Exception processing company:%s,%s" %(url,e)
            item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = item['jigsaw_address'] = None
        companies[index] = item
        index += 1
    return companies

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
        tmp_dict[key] = value
        counter += 1
    if to_add:
        partner_data.append(tmp_dict)

companies_with_urls = []
companies_without_urls = []
for data in partner_data:
    url = data.get('url',None)
    if url in EMPTY_VALUES:
        companies_without_urls.append(data)
    else:
        companies_with_urls.append(data)

print len(companies_with_urls)


print len(companies_without_urls)

"""
companies = process_jigsaw_data(companies_with_urls)
for company in companies:
    scraperwiki.sqlite.save(unique_keys=[], data=company, table_name="avaya_reseller_processed", verbose=2)    
print companies
"""

data_list = scraperwiki.sqlite.execute("select * from avaya_reseller_processed")
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
        tmp_dict[key] = value
        counter += 1
    if to_add:
        partner_data.append(tmp_dict)

for data in partner_data:
    index = 0
    address = data['address']
    address = ast.literal_eval(address)
    data['avaya_address_format'] = address
    tmp_address_dict = {}
    tmp_address_dict['pincode'] = address.get('zipPostalCode','')
    tmp_address_dict['state'] = address.get('state','')
    #tmp_address_dict['country'] = address.get('country','')
    tmp_address_dict['address_formatted'] = address.get('street')+' '+address.get('city')+','+address.get('state')+', '+address.get('zipPostalCode')+', '+address.get('country')
    data['address'] = tmp_address_dict
    partner_data[index] = data
    index +=1

print json.dumps(partner_data)
    








"""
COMPANY_NAME_MAPPINGS = {
                          "AT&T":"AT&T CORP. - LIFECYCLE",
                          "Comm-Works":"Comm-Works/harbor Solutions",
                          "Kelcom Telco":"Kelcom/windsor Telco"
                          "Strategic Products & Services":"Strategic Products & Services/Newton Group",
                          "Cable Link Solutions":"Cable Link Solutions dba Jamco Communications",
                          "Netversant Solutions":"Netversant Solutions Ii Llc",
                          "VIRGINIA INTEGRATED COMMUNICATION":"VIRGINIA INTEGRATED COMMUNICATION   DBA: VICOM"
                        }
company_names = []
for company in companies_without_urls:
    company_names.append(company['name'])

print company_names
"""



