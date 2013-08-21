import mechanize 
import lxml.html
import string, random
import scraperwiki  
import base64
import urlparse
import copy
import re
import time


get_contact_from_lead411 = False
get_company_from_lead411 = False

counter = 0
total = 0
percentage = 0
start_time = time.time()
br = mechanize.Browser()

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


### lead411 section START
lead411_base_url = "http://www.lead411.com/"

lead411_signup_url = "freetrial.taf"
lead411_company_search_url_name_next = "cosearch.taf?_function=list&CoSearchText="

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

### lead411 section END

### socal section START
socal_intel_base_url = "http://www.socaltech.com/intelligence/"

socal_founding_url_params = "?filter=&year=-1&round=-1&action=recentdeals&companyarea=2&industry=6"
socal_edit_company_url_id_next = "?action=editcompanyuser&id="
socal_edit_contact_url_id_next = "?action=editpersonbyuser&id="

def socal_login():
    response = br.open("https://www.socaltech.com/socaltech/login.php")

    br.select_form(name="loginform")
    
    br.form["log"] = base64.b64decode("bWdhcmxhbmRAdGllbXBvZGV2ZWxvcG1lbnQuY29t")
    br.form["pwd"] = base64.b64decode("dGllbXBvMjAxMw==")
    
    response = br.submit()

### socal section END

socal_login()


root = get_root_from_url(socal_intel_base_url + socal_founding_url_params)
odd_table_rows = root.cssselect("table[class='deals'] tr[class='deals']")

headers = odd_table_rows.pop(0)

pair_table_rows = root.cssselect("table[class='deals'] tr[class='dealsalt']")

table_rows = [None]*(len(odd_table_rows)+len(pair_table_rows))
table_rows[::2] = odd_table_rows
table_rows[1::2] = pair_table_rows
total = len(table_rows)
print "table rows: ", total


for tr in table_rows:
    tds = tr.cssselect("td")
    socal_founding_url = socal_intel_base_url + tds[1].cssselect("a")[0].attrib.get('href')

    socal_founding_url_params = urlparse.parse_qs(urlparse.urlparse( socal_founding_url ).query)
    socal_founding_id = socal_founding_url_params['id'][0]
    

    founding_deal = {
        'socal_id': socal_founding_id,
        'date'    : dateutil.parser.parse(tds[0].text_content()).date(),
        'company' : tds[1].text_content(),
        'round'   : tds[2].text_content(),
        'city'    : tds[3].text_content(),
        'amount'  : tds[4].text_content()
    }
    
    print socal_founding_url
    root =  get_root_from_url(socal_founding_url)
    details_table_rows = root.cssselect("table[width='500'] tr")

    founding_details_list_details = [{'label_to_search': "Details",   'type_of_getter': "html_content"},
                                     {'label_to_search': "Investors", 'type_of_getter': "html_content"}]
    
    get_details_from_table(founding_deal, details_table_rows, founding_details_list_details )

    
    #Geting info from company
    company_url = socal_intel_base_url + details_table_rows[0].cssselect("a")[0].attrib.get('href')
    company_url_params = urlparse.parse_qs(urlparse.urlparse( company_url ).query)

    company_id = company_url_params['id'][0]
    
    founding_deal['company_socal_id'] = company_id
    scraperwiki.sqlite.save(unique_keys=['socal_id'], data=founding_deal , table_name='founding_deal')
    counter += 1
    progress = counter / float(total)
    update_progress(progress, company_id)
    #print  counter, " - company_id: ", company_id, 
    
    company_edit_url = socal_intel_base_url + socal_edit_company_url_id_next + company_id

    root =  get_root_from_url(company_edit_url)
    edit_company_table_rows = root.cssselect("table[width='500'] tr")
    
    company = {
        'socal_id': company_id 
    }
    
    company_list_details = [{'label_to_search': "Name",        'type_of_getter': "input_value"},
                            {'label_to_search': "Industry",    'type_of_getter': "select_value"},
                            {'label_to_search': "Status",      'type_of_getter': "select_value"},    
                            {'label_to_search': "Stage",       'type_of_getter': "select_value"},    
                            {'label_to_search': "Description", 'type_of_getter': "textarea_value"},    
                            {'label_to_search': "Address",     'type_of_getter': "input_value"},    
                            {'label_to_search': "City",        'type_of_getter': "input_value"},    
                            {'label_to_search': "State",       'type_of_getter': "input_value"},    
                            {'label_to_search': "Country",     'type_of_getter': "input_value"},    
                            {'label_to_search': "Zip",         'type_of_getter': "input_value"},    
                            {'label_to_search': "Phone",       'type_of_getter': "input_value"},    
                            {'label_to_search': "Fax",         'type_of_getter': "input_value"},    
                            {'label_to_search': "URL",         'type_of_getter': "input_value"}]

    get_details_from_table(company, edit_company_table_rows , company_list_details)

    scraperwiki.sqlite.save(unique_keys=['socal_id'], data=company , table_name='company')

    root =  get_root_from_url(company_url)
    company_profile_table_rows = root.cssselect("table[width='500'] tr")
    
    company_contacts_by_departments = { }

    company_contacts_company_profile_list_details = [{'label_to_search': "Board",      'type_of_getter': "html_content"},
                                                     {'label_to_search': "Executives", 'type_of_getter': "html_content"}
                                                     #,{'label_to_search': "Former Relationships", 'type_of_getter': "html_content"}
                                                    ]
    
    get_details_from_table(company_contacts_by_departments, company_profile_table_rows, company_contacts_company_profile_list_details)
    
    
    departments = company_contacts_by_departments.keys()
    
    regex = '^.*action=.*?id=(?P<socal_id>\d+)\"\>(?P<last_name>.+?), (?P<first_name>.+?) (?P<middle>.*?)\s?\<\/a\>, (?P<title>.+?) \<'
    separator = "<br>"

    for department in departments:    
        contacts_template = {'company_socal_id' : company_id,
                             'department'       : key_to_label(department)
                            }
        html_content = company_contacts_by_departments[label_to_key(department)]
        html_content_fixed = s_remove_tr(html_content)    
    
        contacts = fields_from_split_html(contacts_template, html_content_fixed, separator, regex)

        for contact in contacts:
            contact_edit_url = socal_intel_base_url + socal_edit_contact_url_id_next + contact["socal_id"]
            root = get_root_from_url(contact_edit_url)
            
            edit_contact_table_rows = root.cssselect("table[width='500'] tr")
            contact_edit_details = [{'label_to_search': "First Name", 'type_of_getter': "input_value"},
                                    {'label_to_search': "Middle",     'type_of_getter': "input_value"},    
                                    {'label_to_search': "Last Name",  'type_of_getter': "input_value"},    
                                    {'label_to_search': "Email",      'type_of_getter': "input_value"},  
                                    {'label_to_search': "Biography",  'type_of_getter': "textarea_value"}]
            
            get_details_from_table(contact, edit_contact_table_rows, contact_edit_details)
            
            
            scraperwiki.sqlite.save(unique_keys=['socal_id'], data=contact, table_name='contact')



"""
    if get_company_from_lead411:

        lead411_login()
        response = get_response_forwarded_from_url(lead411_base_url + lead411_company_search_url_name_next + company['name'])
        url = response.geturl()
        root = get_root_from_response(response)
        

        if "cosearch.taf" in url:
            #redirected to company list, get first company
            var = ""


        if "company.taf" in url:
            #redirected to company page
            #GET COMPANY DATA
            
            lead411_id = ""
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
            
            
            company_url = url

            m = re.match('^.*(?P<lead411_id>\d+)+\.?h?tm?l?$', url)
            if hasattr(m, 'groupdict'): 
                lead411_id = m.groupdict()['lead411_id']
            
            for tr in root.cssselect("tr[valign='TOP' align='LEFT']"):
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
            
            for tr in root.cssselect("table[width='550' class='normal'] tr"):
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
            
            sector_links = root.cssselect("font[face='arial' size='2']")
            for link in sector_links:
                link_text = link.text_content()
                if "Industries" in link_text:
                    #Do nothing
                    var = ""
                else:
                    sector = sector + " " + link_text
            
            
            source = '<a href="' + company_url  + '">Lead411.com</a>'
            
            
            company_lead411 = {
                    'lead411_id'             : lead411_id,
                    'socal_id'               : company['socal_id'],
                    'name'                   : company,  
                    'industry'               : sector,
                    'status'                 : company['status'],
                    'stage'                  : "",
                    'description'            : about,
                    'address'                : address1 + address2,
                    'city'                   : city,
                    'state'                  : state,
                    'country'                : country,
                    'zip'                    : zip,
                    'phone'                  : phone,
                    'fax'                    : company['fax'],
                    'url'                    : website,
                    'source'                 : company_url,
                    'Yearly Revenue'         : yearly_rev,
                    'Number of employees'    : num_employees,
                    'Available Jobs'         : available_jobs}
                    
                
            scraperwiki.sqlite.save(unique_keys=['lead411_id'], data=company_lead411, table_name='company_lead411')
            
            
            if get_contact_from_lead411:
                
                fname2 = ""
                lname2 = ""
                title2 = ""
                email2 = ""
                pfname2 = ""
                plname2 = ""
                ptitle2 = ""
                pemail2 = ""
                
                lead411_contacts_counter = 0
                for tr in rootc.cssselect("tr[class='data2']"):
                    lead411_contacts_counter += 1
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
    
    
                    vcardlink = 'http://www.lead411.com/vcard/'+ fname[0:1]+lname + '.vcf'
                    contact_lead411= {
                        'lead411_id'             : lead411_id,
                        'Venture Company Source' : source,
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
                        'FName Contact'          : fname,
                        'LName Contact'          : lname,
                        'Title'                  : title,
                        'Email'                  : email,
                        'Notes/What they do'     : about,
                        'Yearly Revenue'         : yearly_rev,
                        'Number of employees'    : num_employees,
                        'Available Jobs'         : available_jobs,
                        'Contact Link'           : clink,
                        'Vcard (not verified)'   : vcardlink}
                        
        
                    scraperwiki.sqlite.save(unique_keys=['Contact Link'], data=data, table_name='contact_lead411')
                    
                    if contact_counter == 1:
                        pfname2 = fname
                        plname2 = lname
                        ptitle2 = title
                        pemail2 = email
    
                    if contact_counter == 2:
                        fname2 = fname
                        lname2 = lname
                        title2 = title
                        email2 = email
    
                        venture_sheet = {
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
                            'FName Contact1'         : pfname2,
                            'LName Contact 1'        : plname2,
                            'Title'                  : ptitle2,
                            'Email 1'                : pemail2,
                            'FName Contact2'         : fname2,
                            'LName Contact 2'        : lname2,
                            'Title'                  : title2,
                            'Email2'                 : email2,
                            'Notes/What they do'     : about,
                            'Yearly Revenue'         : yearly_rev,
                            'Number of employees'    : num_employees,
                            'Available Jobs'         : available_jobs,
                            'Plataform'              : ""}
                        
                        scraperwiki.sqlite.save(unique_keys=['Venture Company Source'], data=venture_sheet, table_name='venture_sheet')

"""