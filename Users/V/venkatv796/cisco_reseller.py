import mechanize
import scraperwiki
import cookielib
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.etree import tostring
import json
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Comment
import re
import cgi
import urllib
from pprint import pprint


EMPTY_VALUES = (None, '', [], (), {},'None')

KEYMAP = {
            "Company": "name",
            "url": "url",
            "Phone Number":"primary_phone"
         }

COMPANY_PROPERTIES_KEYS = ["Certifications","Cloud Partner","Cloud and Managed Services","Cloud Services","Managed Services",
                            "Services Reseller","Cisco Powered Services","Cisco Services","Other Authorizations",
                            "Cisco Authorized Partners","Cisco Partners","Specializations","Specialization",
                            "Industry Solutions Partners","Industry Solutions","Additional Partner Programs",
                            "Partner Programs","Authorized Technology Providers","Authorized Technology Provider",
                            "Technology Providers","Technology Provider","Learning Partners","Learning Partner",
                            "Partner since","profile_url"]

RELATIONSHIP_TYPE_MAP = {
                          "Services Reseller": "Reseller",
                          "Industry Solutions Partners": "Solution Provider",
                          "Authorized Technology Providers": "Technology Provider",
                          "Authorized Technology Provider": "Technology Provider",
                          "Technology Providers": "Technology Provider",
                          "Technology Provider": "Technology Provider",
                          "Learning Partners": "Learning Partner",
                          "Learning Partner": "Learning Partner",
                        }
                          

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



def parse_google_address_components(data):
    json_data = json.loads(data)
    return_dict = {
                    "state_code":"",
                    "pincode":"",
                    "address_formatted": ""
                   }
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
    return return_dict

def parse_company_profile(data):
    document = html.fromstring(data)
    table = document.xpath("//table[contains(@style,'word-wrap:break-word')]")[0]
    table_string = tostring(table)
    tree = BeautifulSoup(table_string)
    table_string = tree.prettify()
    table_string = remove_comments(table_string)
    table = html.fromstring(table_string)
    children = table.getchildren()
    company_profile = {}
    for child in children:
        td = child.getchildren()
        if len(td) >= 2:
            key = td[0].text
            value = td[1]
            key = strip_tags(key).strip().replace("\n","").replace("\t","").replace(' ,',',').replace(', ',',')
            if key in ['Site Address','HQ Address']:
                continue
            if "URL" in key:
                alink = td[1].getchildren()[0]
                value = alink.text
                value = value.lower().strip()
                if 'http' not in value:
                    value = 'http://'+value
                if not value.endswith('/'):
                    value = value+'/'
                key = 'url'
            else:
                value = tostring(value)
                value = re.sub('<br\s*/?>',',',value)
                value = strip_tags(value).strip().replace("\n","").replace("\t","").replace(' ,',',').replace(', ',',')
                value = value.replace("&#160;","").replace("&amp;","&")
                value = re.sub('\s+', ' ', value)
                value = re.sub('\s+,', ',', value)
                value = re.sub(',\s+', ',', value)
                value_elements = value.split(',')
                if len(value_elements) > 0:
                    tmp = []
                    for v in value_elements:
                        if v.startswith('-'):
                            v = v.replace('-','')
                        tmp.append(v)
                    value = ",".join(tmp)
                value = value.replace("\n","").replace("\r","").strip()
            if value not in EMPTY_VALUES:
                company_profile[key] = value
    return company_profile    

def process_base_page(response):
    document = html.fromstring(response)
    table = document.xpath("//table[contains(@width,'340px')]")[0]
    table_string = tostring(table)
    tree = BeautifulSoup(table_string)
    table = tree.prettify()
    table_document = html.fromstring(table)
    children = table_document.getchildren()[1:]
    companies = []
    for child in children:
        table_string = tostring(child)
        tree = BeautifulSoup(table_string)
        table_child = tree.prettify()
        document = html.fromstring(table_child)
        second_child = document.getchildren()[0].getchildren()[0]
        table_string = tostring(second_child)
        tree = BeautifulSoup(table_string)
        third_child = tree.prettify()
        document = html.fromstring(third_child)
        fourth_children = document.getchildren() ## list of all elements
        if len(fourth_children) > 0:
            ## get company names
            tr = fourth_children[0]
            name = tr.xpath("//span[contains(@class,'companyText')]")[0]
            name = name.text.strip() ## name
            alink = tr.xpath("//a[contains(@href,'partnerDetail.do')]")[0]
            partnerUrl = 'http://tools.cisco.com/WWChannels/LOCATR/'+alink.attrib['href']
            ## company address
            tr = fourth_children[1]
            addressSpan = tr.xpath("//span[contains(@class,'addresstext')]")[0]
            text = strip_tags(tostring(addressSpan)).strip().replace("\n","").replace("\t","").replace(' ,',',').replace(', ',',')
            hq_address = re.sub('\s+', ' ', text)
            phoneSpan = tr.xpath("//span[contains(@class,'contacttext')]")[0]
            text = strip_tags(tostring(phoneSpan)).strip().replace("\n","").replace("\t","").replace(' ,',',').replace(', ',',')
            text = re.sub('\s+', ' ', text)
            phone = text.replace('Phone:','').strip()
            tmp_dict = {
                    "name": name,
                    "profile_url": partnerUrl,
                    "hq_address": hq_address,
                    "phone": phone
                    }
            companies.append(tmp_dict)
    return companies


def process_secondary_pages(response):
    document = html.fromstring(response)
    table = document.xpath("//table[contains(@width,'340px')]")[0]
    table_string = tostring(table)
    table_string = table_string.replace('<div id="partnerInfoPopUp" style="display:none">','').replace('</div>','')
    table = html.fromstring(table_string)
    children = table.getchildren()
    count = 0
    companies = []
    for child in children:
            try:
                nameText = 'beGeoName%s' %(count)
                addressText = 'address%s' %(count)
                phoneText = 'contact%s' %(count)
                nameNode = child.xpath('//span[contains(@id,"%s")]' %(nameText))[0]
                name = nameNode.text.strip()
                alink = child.xpath("//a[contains(@href,'partnerDetail.do')]")[count]
                partnerUrl = 'http://tools.cisco.com/WWChannels/LOCATR/'+alink.attrib['href']
                addressSpan = child.xpath('//span[contains(@id,"%s")]' %(addressText))[0]
                text = strip_tags(tostring(addressSpan)).strip().replace("\n","").replace("\t","").replace(' ,',',').replace(', ',',')
                hq_address = re.sub('\s+', ' ', text)
                phoneSpan = child.xpath('//span[contains(@id,"%s")]' %(phoneText))[0]
                text = strip_tags(tostring(phoneSpan)).strip().replace("\n","").replace("\t","").replace(' ,',',').replace(', ',',')
                text = re.sub('\s+', ' ', text)
                phone = text.replace('Phone:','').strip()
                count += 1
                tmp_dict = {
                    "name": name,
                    "profile_url": partnerUrl,
                    "hq_address": hq_address,
                    "phone": phone
                    }
                companies.append(tmp_dict)
            except Exception,e:
                pass
    return companies

def process_company_list(companies):
    global KEYMAP, COMPANY_PROPERTIES_KEYS
    processed_companies = []
    existing_keys = KEYMAP.keys()
    relationship_map_keys = RELATIONSHIP_TYPE_MAP.keys()
    for company in companies:
        partner_link = company['profile_url']
        try:
            r = br.open(partner_link)
            data = r.read()
            tree = BeautifulSoup(data)
            html_string = tree.prettify()
            details = parse_company_profile(html_string)
            for key,value in details.items():
                company[key] = value
            ## do the key mappings from this to the standard json structure
            tmp_dict = {}
            company_properties = {}
            for old_key,value in company.items():
                if str(old_key) in existing_keys:
                    new_key = KEYMAP[str(old_key)]
                    tmp_dict[new_key] = value
                else:
                    if old_key in relationship_map_keys:
                        tmp_dict['relationship_type'] = RELATIONSHIP_TYPE_MAP[old_key]
                    elif old_key in COMPANY_PROPERTIES_KEYS:
                        company_properties[old_key] = value
                    else:
                        tmp_dict[old_key] = value

            if 'relationship_type' not in tmp_dict:
                tmp_dict['relationship_type']= 'Reseller'
            tmp_dict['relationship_properties'] = company_properties
            if 'hq_address' in tmp_dict:
                hq_address = tmp_dict['hq_address']
                elements = hq_address.split(',')
                state = elements[-2].strip()
                pincode = elements[-1].replace('USA','').replace('US','').strip()
                tmp_dict['address'] = {'state': state,'pincode': pincode,'address_formatted': hq_address}
                del tmp_dict['hq_address']
            if 'primary_phone' not in tmp_dict:
                tmp_dict['primary_phone'] = tmp_dict.get('phone','')
            if 'phone' in tmp_dict:
                del tmp_dict['phone']
            
            company_properties = {
                                    'federal_authorized':False,
                                    'state_authorized': False,
                                    'local_authorized': False,
                                     'edu_authorized': False
                                  }
            if 'Fax' in tmp_dict:
                company_properties['fax'] = tmp_dict['Fax']
                del tmp_dict['Fax']    
            tmp_dict['company_properties'] = company_properties
            processed_companies.append(tmp_dict)
        except Exception,e:
            print "Exception processing partner link:%s, %s" %(partner_link,e)
    return processed_companies


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
                #item['primary_phone'] = details.get('phone',None)
                item['industries'] = details.get('industry',None)
                #item['address'] = details.get('address',None)
            else:
                item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = None
        except:
            item['company_overview'] = item['revenue'] = item['employees'] = item['industries'] = None
        companies[index] = item
    return companies

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Open some site, let's pick a random one, the first that pops in mind:
r = br.open('http://tools.cisco.com/WWChannels/LOCATR/openBasicSearch.do')
#html = r.read()

# Show the source
#print html
# or
#print br.response().read()

# Show the html title
#print br.title()

# Show the response headers
#print r.info()
# or
#print br.response().info()

# Show the available forms
#for f in br.forms():
#    print f

# Select the first (index zero) form
br.select_form(nr=1)

#print br.form
# Let's search
print repr(br.form.__dict__)
br.form['country']=['US',]
br.submit()
response = br.response().read()
print "Processing Primary Page...."
#companies = process_base_page(response)
#processed_companies = process_company_list(companies)
#processed_companies = process_jigsaw_data(processed_companies)
processed_companies = []
print "Finished"
print "Processing secondary...."
pageno = 200
while pageno < 400:
    print "processing page:%s" %(pageno)
    pgdict = {'pageno' : '%s' %(pageno) }
    response = br.open("http://tools.cisco.com/WWChannels/LOCATR/paginateAjaxSearch.do",urllib.urlencode(pgdict))
    response = response.read()
    companies = process_secondary_pages(response)
    processed = process_company_list(companies)
    processed = process_jigsaw_data(processed)
    processed_companies.extend(processed)
    pageno += 1

print "Finished"

url_added = []
for company in processed_companies:
    url = company['url']
    if url not in url_added:
        scraperwiki.sqlite.save(unique_keys=[], data=company, table_name="cisco_reseller", verbose=2)
        url_added.append(url)

pprint(processed_companies)


"""
## To get to the next page, change the pageno param here

print response.read()
response = br.open("http://tools.cisco.com/WWChannels/LOCATR/paginateAjaxSearch.do",urllib.urlencode({'pageno' : '3'}))
response = response.read()

"""


"""
data_dict = {
                       'name':name,
                       'url': url,
                       'site_description': desc,
                       'relationship_type': 'reseller',
                       'company_properties':
                                     {
                                       'reseller_level': resellerLevel,
                                       'certifications': certifications,
                                       'solutions': reseller_solutions,
                                      },
                       'authorizations':
                                        {
                                         'federal': federal_auth,
                                         'state': localAndEduAuth,
                                         'local': localAndEduAuth,
                                         'edu': localAndEduAuth
                                        }

"""

## add relationship type: reseller
## get site information like revenue, number of employees etc from jigsaw
## create a company properties map out of the following keys:
# "Certifications","Cisco Powered Services","Cloud and Managed Services",
# "Other Authorizations","Partner since","Specializations","profile_url",
## get formatted address from google maps using the field "hq_address"

            
