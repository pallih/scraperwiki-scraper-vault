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
session = requests.session()

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


def populate_partner_data(document):
    resultset = document.xpath("//div[contains(@class,'resultSet')]")[0]
    children = resultset.getchildren()
    partner_list = []
    for item in children:
        children = item.getchildren()
        tmp_dict = {'relationship_type':'Reseller'}
        for child in children:
            className = child.attrib['class']
            if className == "title":
                titleChild = child.getchildren()[0]
                tmp_dict['profile_url'] = titleChild.attrib['href']
                tmp_dict['name'] = titleChild.text
            if className == 'description':
                descChild = child.getchildren()[0]
                tmp_dict['description'] = descChild.text
            if className == 'certifications':
                reseller_properties = {}
                certChildren = child.getchildren()
                certCompetencies = child.getchildren()[0]
                competencies = certCompetencies.getchildren()
                c_list = []
                for c in competencies:
                     text = c.getchildren()[0].getchildren()[1].text
                     c_list.append(text)
                reseller_properties['certifications'] = ",".join(c_list) 
                if len(certChildren) > 1:
                    certBadges = certChildren[1]
                    c_list = []
                    for child in certBadges.getchildren():
                        c_list.append(child.getchildren()[0].getchildren()[0].text)
                    reseller_properties['badges'] = ",".join(c_list)
                if reseller_properties not in EMPTY_VALUES:
                    tmp_dict['reseller_properties'] = reseller_properties
            if className == "hidden":
                hiddenChildren = child.getchildren()
                addrNode = telNoNode = None
                for node in hiddenChildren:
                    nodeClass = node.attrib.get('class',None)
                    if nodeClass not in ['adr','tel phone']:
                        continue
                    if nodeClass == 'adr':
                        addrNode = node
                    if nodeClass == 'tel phone':
                        telNoNode = node
                if addrNode is not None:
                    try:
                        addrChildren = addrNode.getchildren()
                        addr_list = [c.text for c in addrChildren if c.text not in EMPTY_VALUES]
                        #print "Addr List:%s" %(addr_list)
                        location = addr_list[-1]
                        #print "Location:%s" %(location)
                        city,state,pin = location.split(',')
                        tmp_dict['address'] = {'address_formatted': ",".join(addr_list),'state':state,'pincode':pin}  
                    except Exception,e:
                        #print "Exception:%s" %(e)
                        tmp_dict['address'] = None
               
                if telNoNode is not None:
                    tmp_dict['primary_phone'] = telNoNode.getchildren()[1].text
        partner_list.append(tmp_dict)
    return partner_list

def get_data(url):
    global session
    resp = session.get(url)
    document = html.fromstring(resp.text)    
    return document

def get_no_pages(document):
    resultCount = document.xpath('//h1[contains(@id,"ppt_searchResultCount")]')[0].text
    rElements = resultCount.split('of')[1].split('Results')[0].strip()
    no_results = int(str(rElements))
    no_pages = no_results/10
    if (no_results%10) != 0:
        no_pages += 1
    return no_pages


def process_profile_page(data):
    profile_url = data.get('profile_url')
    name = data.get('name')
    document = get_data(profile_url)
    try:
        summary = document.xpath("//div[contains(@class,'summary')]")[0]
        if len(summary) > 1:
            li = summary.getchildren()[1].getchildren()[1]
            url = li.getchildren()[1].getchildren()[0].text
            data['url'] = url
        else:
            print "no url found for company:%s" %(name)
    except:
        print "no url found for company:%s" %(name)

    companyAppsPrev = document.xpath('//div[contains(@class,"companyApps")]')
    if len(companyAppsPrev) > 0:
        companyApps = companyAppsPrev[0]
        products = []
        appsNodePrev = companyApps.getchildren()
        if len(appsNodePrev) > -0:
            appsNode = appsNodePrev[1].getchildren()
            for node in appsNode:
                alink = node.getchildren()[0]
                link = alink.attrib['href']
                name = alink.text
                products.append({'name': name,'url':link})
            data['products'] = products
    """
    certifications = document.xpath('//div[contains(@class,"certContainer")]')[0]
    certNodes = certifications.getchildren()[0].getchildren()[1:]
    certList = []
    for node in certNodes:
        try:
            nodeText = node.attrib['class'].title()
            applicationValue = node.text
            certList.append(nodeText+' '+applicationValue)
        except:
            pass
    print "CertList:%s" %(certList)
    if len(certList) > 0:
        certificates = ",".join(certList)
        data['reseller_properties']['certifications'] = certificates
    """
    return data
"""
competency_url = "http://pinpoint.microsoft.com/en-US/companies/search?fcrc=USA&fs=100227&q=Communications+Competency"
document = get_data(competency_url)
no_pages = get_no_pages(document)
current_page = 2
competency_urls = []

while current_page <= no_pages:
    competency_urls.append("http://pinpoint.microsoft.com/en-US/companies/search?fcrc=USA&fs=100227&page=%s&q=Communications+Competency" %(current_page)) 
    current_page += 1

partner_list = populate_partner_data(document)


for competency_url in competency_urls:
    document = get_data(competency_url)
    page_list = populate_partner_data(document)
    partner_list.extend(page_list)

for data in partner_list:
    new_data = process_profile_page(data)
    scraperwiki.sqlite.save(unique_keys=[], data=new_data, table_name="microsoft_reseller_incomplete", verbose=2)
    print new_data

"""
def process_address(data):
    address = data.get('jigsaw_address',None)
    return_dict = {
                    "state_code":"",
                    "pincode":"",
                    "address_formatted": ""
                   }
    if address not in EMPTY_VALUES:
        address_encoded = urllib.quote_plus(address)
        url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %(address_encoded)
        response = requests.get(url)
        json_data = json.loads(response.text)
        results = json_data.get('results',[])
        if len(results) > 0:
            results = results[0]
            address_components = results.get("address_components",[])
            for component in address_components:
                if 'administrative_area_level_1' in component.get('types',[]):
                    return_dict["state_code"] = component.get('short_name',"")
                if 'postal_code' in component.get('types',[]):
                    return_dict["pincode"] = component.get('short_name',"")
            if 'formatted_address' in results:
                return_dict['address_formatted'] = results.get('formatted_address','')
    data['address_formatted'] = return_dict
    return data
    
    


def process_jigsaw_data(item):
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
            #item['primary_phone'] = details.get('phone',None)
            item['industries'] = details.get('industry',None)
            if item['address'] is None:
                item['jigsaw_address'] = details.get('address',None)
        else:
            item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = None
    except:
        item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = None
    return item

NAME_URL_MAP = {
                'Atrion Networking': 'http://www.atrion.net/',
                'Carousel Industries of North America, Inc.':'http://www.carouselindustries.com/',
                'ExtraTeam, Inc.': 'http://www.extrateam.com/',
                'arvato systems NA': 'http://arvatosystems.com/',
                'C.C.S.I.':'http:/www.ccsi.org/',
                'Biz Technology Solutions, Inc.': 'http://biztechnologysolutions.com/'
                }
"""
data_list = scraperwiki.sqlite.execute("select * from microsoft_reseller_incomplete")
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

new_partner_data = []
for data in partner_data:
    name = data['name']
    if name in NAME_URL_MAP:
         data['url'] = NAME_URL_MAP[name]
    url = data['url']
    if url not in EMPTY_VALUES:
        print "Processing:%s" %(name)
        new_data = process_jigsaw_data(data)
        if new_data['address'] is None:
            new_data = process_address(data)
        
        new_data['company_properties'] = {
                                        'federal_authorized':False,
                                        'state_authorized': False,
                                        'local_authorized': False,
                                         'edu_authorized': False
                                     }
        scraperwiki.sqlite.save(unique_keys=[], data=new_data, table_name="microsoft_reseller_processed", verbose=2)
        new_partner_data.append(new_data)

print new_partner_data
"""

data_list = scraperwiki.sqlite.execute("select * from microsoft_reseller_processed")
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

print json.dumps(partner_data)