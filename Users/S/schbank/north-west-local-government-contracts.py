## North West Local Government Contracts ##

import scraperwiki
import mechanize
import re
from scraperwiki import datastore

def extra(contract):
    contract = contract.read()
    ##### Dates #####
    dates = re.findall('(?si)<!-- START OF DATE DETAILS -->(.*?)<!-- END OF DATE DETAILS SECTION -->', contract)
    review_date = re.findall('(?si)<dt>Review Date:</dt>\s<dd class="toRead">(.*?)</dd>', dates[0])
    if review_date == []:
        review_date = "Empty"
    else:
        review_date = review_date[0]
    ##### Contract Value #####
    contract_value = re.findall('(?si)<!-- START OF CONTRACT VALUE DETAILS -->(.*?)<!-- END OF CONTRACT VALUE SECTION -->', contract)
    annual_value = re.findall('(?si)<dt>Estimated Annual Value:</dt>\s<dd class="toRead">(.*?)\s*</dd>', contract_value[0])
    if annual_value == []:
        annual_value = "Empty"
    else:
        annual_value = annual_value[0]
    ##### Contact #####
    contact = re.findall('(?si)<!-- START OF CONTACT  DETAILS -->(.*?)<!-- END OF COUNCIL CONTACT SECTION -->', contract)
    name = re.findall('(?si)<dt>Name:</dt>\s<dd class="toRead">(.*?)</dd>', contact[0])
    if name == []:
        name = "Empty"
    else:
        name = re.sub('\xa0', '', name[0])
    phone = re.findall('(?si)<dt>Telephone Number:</dt>\s<dd class="toRead">(.*?)</dd>', contact[0])
    if phone == []:
        phone = "Empty"
    else:
        phone = phone[0]
    email = re.findall('(?si)<dt>Email:</dt>\s<dd class="toRead"><a .*>(.*?)</a></dd>', contact[0])
    if email == []:
        email = "Empty"
    else:
        email = email[0]
    department = re.findall('(?si)<dt>Department:</dt>\s<dd class="toRead">(.*?)</dd>', contact[0])
    if department == []:
        department = "Empty"
    else:
        department = department[0]
    owner = re.findall('(?si)<dt>Owner:</dt>\s<dd class="toRead">(.*?)</dd>', contact[0])
    if owner == []:
        owner = "Empty"
    else:
        owner = owner[0]
    ##### Record Details #####
    record = re.findall('(?si)<!-- START OF RECORD DETAILS  DETAILS -->(.*?)<!-- END OF RECORD DETAILS SECTION -->', contract)
    contract_created = re.findall('(?si)<dt>Contract Created:</dt>\s<dd class="toRead">(.*?)</dd>', record[0])
    if contract_created == []:
        contract_created = "Empty"
    else:
        contract_created = contract_created[0]
    expiry_date = re.findall('(?si)<dt>Record Expiry Date:</dt>\s<dd class="toRead">(.*?)</dd>', record[0])
    if expiry_date == ['']:
        expiry_date = "Empty"
    else:
        expiry_date = expiry_date[0]
    modified = re.findall('(?si)<dt>Modified:</dt>\s<dd class="toRead">(.*?)</dd>', record[0])
    if modified == []:
        modified = "Empty"
    else:
        modified = modified[0]
    data2 = { 'review date' : review_date, 'annual value' : annual_value, 'name' : name, 'phone' : phone, 'email' : email, 'department' : department, 'owner' : owner, 'contract created' : contract_created, 'expiry date' : expiry_date, 'modified' : modified }
    return data2

# Source
url = "http://thevault.nwce.gov.uk/procontract/portal.nsf/vLiveDocs/SD-DNWB-6VZHL3?OpenDocument&contentid=1.002"

br = mechanize.Browser()
br.set_handle_robots(False)
base = br.open(url)

# Follow link
link = br.follow_link(text_regex='Contracts')
n = 0
for x in range(1, 98):
    print "------------------------------------------------------------------------------------------"
    print "## PAGE: ", x, " ##"
    page = link.read()
    # Find the table
    table = re.findall('(?si)<tbody>(.*?)</tbody>', page)
    # Find the rows
    rows = re.findall('(?si)<tr>(.*?)</tr>', table[0])
    for row in rows:
        print "-----------------------------------------------------------------------------------------"
        print "-----------------------------------------------------------------------------------------"
        n += 1
        print "RECORD: ", n
        print "-----------------------------------------------------------------------------------------"        
        cells = re.findall('(?si)<td.*?>(.*?)</td>', row)
        council = re.findall('(?si)<a.*>(.*?)</a>', cells[0])
        contract_link = re.findall('(?si)<a href="(.*?)".*>.*</a>', cells[0])
        contract_link = ''.join(["http://thevault.nwce.gov.uk", contract_link[0]])
        id = re.findall('(?si)<a href=".*" title="View contract ref:(.*?)">.*</a>', cells[0])
        contract = br.follow_link(url_regex=id[0])
        #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        data2 = extra(contract)
        br.back()
        #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        title = cells[1]
        if title == '':
            title = "Empty"
        category = cells[2]
        if category == '':
            category = "Empty"
        else:
            category = re.sub('\xa0', '', category)
        start_date = cells[3]
        if start_date == '':
            start_date = "Empty"
        end_date = cells[4]
        if end_date == '':
            end_date = "Empty"
        total_value = cells[5]
        if total_value == '':
            total_value = "Empty"
        files = re.findall('(?si)<span.*>(.*?)</span>', cells[6])
        data = { 'council' : council[0], 'link' : contract_link, 'id' : id[0], 'title' : title, 'category' : category, 'start date' : start_date, 'end date' : end_date, 'total value' : total_value, 'files' : files[0] }
        data.update(data2)
        print "DATA: ", data
        datastore.save(unique_keys=['id'], data=data)
        
    link = br.follow_link(text_regex='Next.*')
        






