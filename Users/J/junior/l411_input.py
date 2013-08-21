import mechanize 
import lxml.html
import string, random
import scraperwiki  
import base64
import urlparse
import copy
import re
import time

counter = 0
total = 0
percentage = 0
br = mechanize.Browser()
start_time = time.time()

###############################################
###############################################



def update_progress(progress, id):
    barLength = 40 # Modify this to change the length of the progress bar
    status = ""
    elapsed_time = time.time() - start_time
    eta = elapsed_time / progress
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    if id: 
        id_string = " - id: " + id 
    else: 
        id_string = ""
    print "%0.1f%s - "  % (progress*100, "%"), time.strftime('%H:%M:%S', time.gmtime(elapsed_time)), "[ ","#"*block + '\\'*(barLength-block)," ] ETA: ", time.strftime('%H:%M:%S', time.gmtime(eta)),status,id_string


def label_to_key(label):
    return label.strip().lower().replace(" ", "_")

def key_to_label(key): 
    return key.replace("_", " ").title()

def s_remove_tr(broken_html):
    result = broken_html.split("<tr", 1)[0]
    return result

def get_root_from_url(url):
    response = br.open(url)
    html = response.read()
    root = lxml.html.fromstring(html)
    return root

def get_response_forwarded_from_url(url):
    return br.open(url)
    
def get_root_from_response(response):
    html = response.read()
    root = lxml.html.fromstring(html)
    return root


def innerHTML(node):
    return (node.text or '') + ''.join([lxml.html.tostring(child) for child in node]) 


def fields_from_split_html(template, html, separator, regex_with_groups_named_as_keys):
    list_to_ret = []
    lines = html.split(separator)
    for line in lines: 
        m = re.match(regex_with_groups_named_as_keys, line)
        if hasattr(m, 'groupdict'): 
            dict_to_ret = dict(template.items() + m.groupdict().items())
            list_to_ret.append(dict_to_ret)
    
    return list_to_ret
        

def get_details_from_table(data_dict, list_elements, list_details, element_tag = "td", label_id = 0, value_id = 1):
    for element in list_elements:
        data_element = element.cssselect(element_tag)
        for details in list_details:
            value = ""
            data = ""
            if data_element[label_id].text_content().strip() == details['label_to_search'].strip():
                if 'type_of_getter' in details:
                    type_of_getter = details['type_of_getter']
    
                    if   type_of_getter == "text_content" :
                        value = data_element[value_id].text_content()
                    elif type_of_getter == "html_content":
                        value = innerHTML(data_element[value_id]) 
                    elif type_of_getter == "input_value":
                        inputs = data_element[value_id].cssselect("input") 
                        value = inputs[0].attrib.get('value')
                    elif type_of_getter == "select_value":
                        selects = data_element[value_id].cssselect("select") 
                        option_id = selects[0].value
                        options = selects[0].cssselect("option")
                        for option in options:
                            if option.get('value') == option_id:
                                value = option.text
                    elif type_of_getter == "textarea_value":
                        inputs = data_element[value_id].cssselect("textarea") 
                        value = inputs[0].attrib.get('value')
                else:
                    value = data_element[value_id].text_content()
            if value != "":
                if 'key_name' in details:
                    key_name = details['key_name'] 
                else:
                    key_name = label_to_key(details['label_to_search'])
    
                data_dict[key_name] = value
               




###############################################
###############################################


lead411_base_url = "http://www.lead411.com/"

lead411_signup_url = "freetrial.taf"
lead411_company_search_url_name_next = "cosearch.taf?_function=list&CoSearchText="

lead411_newslatter_url = "newsletter.taf"


def lead411_login():
    response = br.open(lead411_base_url + lead411_signup_url)
    

    l = string.lowercase
    d = string.digits
    email     = ''.join(random.sample(l+d,5)) + "@mailinator.com"
    password  = ''.join(random.sample(l+d,10))
    
    br.select_form(nr=1)
    br.form["firstname"]  = ''.join(random.sample(l,10))
    br.form["lastname"]   = ''.join(random.sample(l,7))
    br.form["Company"]    = ''.join(random.sample(l,6))
    br.form["Title"]      = ''.join(random.sample(l,5))
    br.form["email"]      = email
    br.form["Password"]   = password
    br.form["phone"]      = ''.join(random.sample(d,10))
    br.form["terms"]      = ['on']
    
    response = br.submit()
    
    print "email: " + email + " password: " + password


## Start Navigation

lead411_login()

get_root_from_url("http://www.lead411.com/leadhound.taf?" + "_function=search" + "&PressID=1" + "&industry=Software" + "&State=CA" + "&MaxResults=200" + "&sort=9+DESC" + "&range=range" + "&beg_month=1" + "&beg_day=1" + "&beg_year=2013" + "&end_month=7" + "&end_day=28" + "&end_year=2013" + "&Submit=Fetch+it%212")




"""


prev_company = "no comp$$"
company      = ""
website      = ""
sector       = ""
address1     = ""
address2     = ""
city         = ""
state        = ""
zipcode      = ""
country      = ""
cphone       = ""

num_employees = ""
yearly_rev   = ""
available_jobs = ""

about        = ""

while(next100):
    
    html = response.read()
    root = lxml.html.fromstring(html)
    
    for tr in root.cssselect("tr[bgcolor='EEEEEE']"):
        tds = tr.cssselect("td")
        #print root.cssselect("td[align='left' class='normal']")
        
        
        company = tds[1].text_content()
        if company != prev_company:
            
            website = ""
            sector  = ""
            address1 = ""
            address2 = ""
            city    = ""
            state   = ""
            zipcode = ""
            country = ""
            cphone  = ""

            num_employees = ""
            yearly_rev   = ""
            available_jobs = ""

            about        = ""

            
            links = tds[1].cssselect("a")
            company_url = 'http://www.lead411.com/' + links[0].attrib['href']
            print company_url
            response=br.open(company_url)
            htmlc = response.read()
            rootc = lxml.html.fromstring(htmlc)

            for tr in rootc.cssselect("tr[valign='TOP' align='LEFT']"):
                tds = tr.csselect("td")
                text = tds[0].text_content()
                
                if "Headquarters" in text:
                    #do nothing
                    var = ""
                elif "USA" in text:
                    #Pleasanton, CA USA 94588
                    city = text[:text.find(",")]
                    state = text[text.find(",")+2:text.find("USA")]
                    country = "USA"
                    zip = text[text.find("USA") + 4:]
                elif "Phone:" in text:
                    cphone = text.strip()
                elif "Fax:" in text:
                    if cphone != text.strip():
                        cphone = cphone , ", " , text.strip()
                elif address1 == "":
                    address1 = text
                else:
                    address2 = text
            
            for tr in rootc.cssselect("table[width='550' class='normal'] tr"):
                tds = tr.csselect("td")
                label = tds[0].text_content()
                
                if "Number of Employees:" in text:
                    num_employees = tds[1].text_content()
                elif "Yearly Revenues:" in text:
                    yearly_rev   = tds[1].text_content()
                elif "Available Jobs" in text:
                    available_jobs = tds[1].text_content() 
                                                                                                                                                                                             
            tds = rootc.cssselect("table[border='0' cellspacing='1' width='742' class='normal'] tbody tr td")
            if tds != "":
                about = tds[0].text_content()
            
            sector_links = rootc.cssselect("font[face='arial' size='2']")
            for link in sector_links:
                link_text = link.text_content()
                if "Industries" in link_text:
                    #Do nothing
                    var = ""
                else:
                    sector = sector + " " + link_text
            
            
            for tr in rootc.cssselect("tr[class='data2']"):
                tds = tr.cssselect("td")
                
                name = ""
                fname = ""
                lname = ""
                phone = ""    
                email = ""
                title = ""
                clink = ""


                title   = tds[2].text_content()

        
                name = tds[1].text_content().split
                fname = name[:1]
                lname = name[1:]

                clink = tds[1].cssselect("a")[0].attrib.get('href')
        

                if (tds[3].cssselect("a")):
                    email = tds[3].cssselect("a")[0].text_content()
                    phone = tds[3].text_content().replace(email,'')
                else:
                    email = ""
                    phone = tds[3].text_content().replace('Not Available', ' ').replace(' ','').trim()
                    
                if ( phone == " "):
                    phone = cphone           


                source = '<a href="' + company_url  + '">Lead411.com</a>'
                vcardlink = 'http://www.lead411.com/vcard/'+ fname[0:1]+lname + '.vcf'

                data = {
                    "Venture Company Source" : source,
                    'CompanyName'            : company,  
                    'Sector'                 : sector,
                    'Address1'               : address1,
                    'Address2'               : address2,
                    'City'                   : city,
                    'State'                  : state,
                    'Zip'                    : zip,
                    'Country'                : country,
                    'Phone'                  : phone,
                    'Website'                : website,
                    'FName Contact1'         : fname,
                    'LName Contact 1'        : lname,
                    'Title'                  : title,
                    'Email 1'                : email,
                    'FName Contact2'         : "",
                    'LName Contact 2'        : "",
                    'Title'                  : "",
                    'Email2'                 : "",
                    'Notes/What they do'     : about,
                    'Yearly Revenue'         : yearly_rev,
                    'Number of employees'    : num_employees,
                    'Available Jobs'         : available_jobs,
                    'Contact Link'           : clink,
                    'Vcard (not verified)'   : vcardlink}
                    
    
                scraperwiki.sqlite.save(unique_keys=['Contact Link'], data=data, table_name='l411')
                #print data
            
        prev_company = company

        br.back()


        


        
        
        
        
    next100 = False
    for form in br.forms():
        if (form.name == "NEXT"):
            next100 = True
            br.select_form("NEXT")
            response = br.submit()



"""