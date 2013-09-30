import scraperwiki
# Blank Python
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.etree import tostring
import json
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import re
import cgi

EMPTY_VALUES = (None, '', [], (), {})


"""

def strip_tags(document):
    return ''.join(BeautifulSoup(document).findAll(text=True))

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


data = scraperwiki.scrape("http://www.netapp.com/us/how-to-buy/resellers-new/")
document = html.fromstring(data)
trs = document.xpath("//tr[contains(@class,'tr_commonRow')]")
count = 1
data_list = []
for tr in trs:
    tds = tr.getchildren()
    name = url = desc = resellerLevel = certifications = reseller_solutions = None
    federal_auth = localAndEduAuth = False
    countrycode = tds[2].getchildren()[0].text
    if countrycode.strip() == "US":
        resellerLevel = str(tds[3].getchildren()[0].text).strip()
        linkIdName = 'partlink%s' %(count)
        alink = tr.xpath("//a[contains(@id,'%s')]" %(linkIdName))
        if len(alink) > 0:
            alink = alink[0]
            name = alink.text
            url = alink.attrib['href']
        popupcontentName = 'partcontent%s' %(count)
        popupcontentdiv = tr.xpath("//div[contains(@id,'%s')]" %(popupcontentName))
        if len(popupcontentdiv) > 0:
            desc = popupcontentdiv[0].getchildren()[0].getchildren()[0].getchildren()[0].text
        ## certifications
        cnode = tds[4].getchildren()
        if len(cnode) > 0:
            cnode = cnode[0].getchildren()
            certifications = [node.text for node in cnode]
            certifications = ",".join(certifications)
        ## reseller solutions
        rnode = tds[6].getchildren()
        if len(rnode) > 0:
            rnode = rnode[0].getchildren()
            reseller_solutions = [node.text for node in rnode]
            reseller_solutions = ",".join(reseller_solutions)
        ## authorizations
        fedauthNode = tds[7].getchildren()[0].getchildren()
        if len(fedauthNode) > 0:
            federal_auth = True
        localauthNode = tds[8].getchildren()[0].getchildren()
        if len(localauthNode) > 0:
            localAndEduAuth = True
        data_dict = {
                       'name':name,
                       'url': url,
                       'level': resellerLevel,
                       'description': desc,
                       'certifications': certifications,
                       'solutions': reseller_solutions,
                       'authorizations':
                                        {
                                         'federal': federal_auth,
                                         'state': localAndEduAuth,
                                         'local': localAndEduAuth,
                                         'edu': localAndEduAuth
                                        }
                    }
        data_list.append(data_dict)
        #print "name:%s,url:%s,resellerLevel:%s,desc:%s" %(name,url,resellerLevel,desc)
        #print "%s,%s,%s,%s,%s" %(name,certifications,reseller_solutions,federal_auth,localAndEduAuth)
    count += 1


index = 0
print len(data_list)
for item in data_list:
    url = item['url']
    elements = urlparse(url)
    jigsaw_url = "http://www.jigsaw.com/FreeTextSearch.xhtml?opCode=search&autoSuggested=true&freeText=%s" %(elements.netloc)
    data = scraperwiki.scrape(jigsaw_url)
    document = html.fromstring(data)
    details = __processSingleCompanyDetails(document)
    if details is not None:
        item['overview'] = details.get('overview',None)
        item['revenue'] = details.get('revenue',None)
        item['employees'] = details.get('employees',None)
        item['primary_phone'] = details.get('phone',None)
        item['industries'] = details.get('industry',None)
        item['address'] = details.get('address',None)
    else:
        item['overview'] = item['revenue'] = item['employees'] = item['primary_phone'] = item['industries'] = item['address'] = None
    data_list[index] = item
    index += 1

"""

data_list = scraperwiki.sqlite.execute("select * from napp_reseller")
keys = data_list.keys()
data = data_list.values()
data_list_formatted = []

key_list = data[0]
value_list = data[1]
for item_list in value_list:
    counter = 0
    tmp_dict = {}
    while counter < len(item_list):
        value = item_list[counter]
        key = key_list[counter]
        tmp_dict[key] = value
        counter += 1
    
    data_list_formatted.append(tmp_dict)

data_list = data_list_formatted
json_data = json.dumps(data_list)
#scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print json_data
import scraperwiki
# Blank Python
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.etree import tostring
import json
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import re
import cgi

EMPTY_VALUES = (None, '', [], (), {})


"""

def strip_tags(document):
    return ''.join(BeautifulSoup(document).findAll(text=True))

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


data = scraperwiki.scrape("http://www.netapp.com/us/how-to-buy/resellers-new/")
document = html.fromstring(data)
trs = document.xpath("//tr[contains(@class,'tr_commonRow')]")
count = 1
data_list = []
for tr in trs:
    tds = tr.getchildren()
    name = url = desc = resellerLevel = certifications = reseller_solutions = None
    federal_auth = localAndEduAuth = False
    countrycode = tds[2].getchildren()[0].text
    if countrycode.strip() == "US":
        resellerLevel = str(tds[3].getchildren()[0].text).strip()
        linkIdName = 'partlink%s' %(count)
        alink = tr.xpath("//a[contains(@id,'%s')]" %(linkIdName))
        if len(alink) > 0:
            alink = alink[0]
            name = alink.text
            url = alink.attrib['href']
        popupcontentName = 'partcontent%s' %(count)
        popupcontentdiv = tr.xpath("//div[contains(@id,'%s')]" %(popupcontentName))
        if len(popupcontentdiv) > 0:
            desc = popupcontentdiv[0].getchildren()[0].getchildren()[0].getchildren()[0].text
        ## certifications
        cnode = tds[4].getchildren()
        if len(cnode) > 0:
            cnode = cnode[0].getchildren()
            certifications = [node.text for node in cnode]
            certifications = ",".join(certifications)
        ## reseller solutions
        rnode = tds[6].getchildren()
        if len(rnode) > 0:
            rnode = rnode[0].getchildren()
            reseller_solutions = [node.text for node in rnode]
            reseller_solutions = ",".join(reseller_solutions)
        ## authorizations
        fedauthNode = tds[7].getchildren()[0].getchildren()
        if len(fedauthNode) > 0:
            federal_auth = True
        localauthNode = tds[8].getchildren()[0].getchildren()
        if len(localauthNode) > 0:
            localAndEduAuth = True
        data_dict = {
                       'name':name,
                       'url': url,
                       'level': resellerLevel,
                       'description': desc,
                       'certifications': certifications,
                       'solutions': reseller_solutions,
                       'authorizations':
                                        {
                                         'federal': federal_auth,
                                         'state': localAndEduAuth,
                                         'local': localAndEduAuth,
                                         'edu': localAndEduAuth
                                        }
                    }
        data_list.append(data_dict)
        #print "name:%s,url:%s,resellerLevel:%s,desc:%s" %(name,url,resellerLevel,desc)
        #print "%s,%s,%s,%s,%s" %(name,certifications,reseller_solutions,federal_auth,localAndEduAuth)
    count += 1


index = 0
print len(data_list)
for item in data_list:
    url = item['url']
    elements = urlparse(url)
    jigsaw_url = "http://www.jigsaw.com/FreeTextSearch.xhtml?opCode=search&autoSuggested=true&freeText=%s" %(elements.netloc)
    data = scraperwiki.scrape(jigsaw_url)
    document = html.fromstring(data)
    details = __processSingleCompanyDetails(document)
    if details is not None:
        item['overview'] = details.get('overview',None)
        item['revenue'] = details.get('revenue',None)
        item['employees'] = details.get('employees',None)
        item['primary_phone'] = details.get('phone',None)
        item['industries'] = details.get('industry',None)
        item['address'] = details.get('address',None)
    else:
        item['overview'] = item['revenue'] = item['employees'] = item['primary_phone'] = item['industries'] = item['address'] = None
    data_list[index] = item
    index += 1

"""

data_list = scraperwiki.sqlite.execute("select * from napp_reseller")
keys = data_list.keys()
data = data_list.values()
data_list_formatted = []

key_list = data[0]
value_list = data[1]
for item_list in value_list:
    counter = 0
    tmp_dict = {}
    while counter < len(item_list):
        value = item_list[counter]
        key = key_list[counter]
        tmp_dict[key] = value
        counter += 1
    
    data_list_formatted.append(tmp_dict)

data_list = data_list_formatted
json_data = json.dumps(data_list)
#scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print json_data
