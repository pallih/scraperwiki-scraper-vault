# UK MEPs #

import scraperwiki
import mechanize
import re
from scraperwiki import datastore

# Source
#url = "http://www.europarl.org.uk/section/your-meps/your-meps"  //Original page has been changed  and laid out over multiple pages.
url = "http://www.europarl.org.uk/view/en/your_MEPs/List-MEPs-by-region/London.html"

br = mechanize.Browser()
br.set_handle_robots(False)
base = br.open(url)

# Select the form
br.select_form(nr=1)
# Select input
br["filter0"] = ["**ALL**"]
# Submit the form
response = br.submit()
# Read the page
page = response.read()

# Get MEPs
details = re.findall('(?si)<li>(.*?)</li>', page)

x = 0
# Loop through meps
for mep in details:
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    x += 1
    print "MEP No.: ", x
    print "-----------------------------------------------------------------------------------------"
    # Get name
    name = re.findall('(?si)<div class="view-field view-data-title">\s\s\s\s<h2>(.*?)\s\s</h2>\s\s</div>', mep)
    
    ## GET ADDRESS & BIO ##
    details = re.findall('(?si)<div class="view-field view-data-field-address-value">(.*?)</div>', mep)
    # Get address
    address = re.findall('(?si)\s*(.*?)<a href=".*" title=".*">.*</a>', details[0])
    if address != []:
        address = re.sub('<p>|</p>|&nbsp;|\n|\xc2|\xa0', '', address[0])
        address = re.sub('<br />|  ', ' ', address)
        address = re.sub('  ', ' ', address)
    else:
        address = "None"
    # Get biograhical details link
    bio_link = re.findall('(?si)<a href="(.*?)".*?>.*?</a>', details[0])
    
    ## GET Contact Details ##
    contact = re.findall('(?si)<div class="view-field view-data-field-email-value">(.*?)</div>', mep)
    # Get telephone
    phone = re.findall('(?si)<strong>Telephone:</strong>\s*(.*?)\D*\s*<br/>', contact[0])
    if phone == ['']:
        phone = "None"
    else:
        phone = re.sub(' |\D*', '', phone[0])
        phone = re.findall('(?si).{11}', phone)
        phone = phone[0]
    # Get fax
    fax = re.findall('(?si)<strong>Fax:</strong>\s*(.*?)\D*\s*<br/>', contact[0])
    if fax == ['']:
        fax = "None"
    else:
        fax = re.sub('\+', '0', fax[0])
        fax = re.sub(' |\D*', '', fax)
        fax = re.findall('(?si).{10,12}', fax)
        fax = fax[0]
    # Get e-mail
    email = []
    mail = re.findall('(?si)"mailto:(.*?)"', contact[0])
    for i in mail:
        if i != "":
            email.append(i)
        else:
            None
            
    ## Get Party Details ##
    # Get electoral area
    area = re.findall('(?si)<div class="view-field view-data-field-national-party-value">\r\n<strong>Electoral Area: </strong>(.*?)\s<br/>\s\s\s<strong>National Political Party: </strong>.*?<br/>\s\s\s<strong>European Group: </strong>.*?</div>', mep)
    #area = area[0]
    # Get national political party
    party = re.findall('(?si)<div class="view-field view-data-field-national-party-value">\r\n<strong>Electoral Area: </strong>.*?\s<br/>\s\s\s<strong>National Political Party: </strong>(.*?)<br/>\s\s\s<strong>European Group: </strong>.*?</div>', mep)
    #party = party[0]
    # Get european group
    eu_group = re.findall('(?si)<div class="view-field view-data-field-national-party-value">\r\n<strong>Electoral Area: </strong>.*?\s<br/>\s\s\s<strong>National Political Party: </strong>.*?<br/>\s\s\s<strong>European Group: </strong>(.*?)</div>', mep)
    #eu_group = eu_group[0]
    
    ## Committees & Delegations ##
    a = re.findall('(?si)<div class="view-field view-data-field-committees-value">(.*?)</div>', mep)
    # Get committees
    comms = []
    b = re.findall('(?si)<p class="padThisText"><span class="bulletThisText">.</span>(.*?)</p>', a[0])
    for i in b:
        comms.append(i)
    # Get delegations
    delegs = []
    c = re.findall('(?si)<p class="padThisText"><span class="bulletThisText">.</span>(.*?)</p>', a[1])
    if c == []:
        delegs = "None"
    else:
        for i in c:
            delegs.append(i)
            
    # The data
    data = { 'name' : name[0], 'address' : address, 'biography_link' : bio_link[0], 'telephone' : phone, 'fax' : fax, 'email' : email, 'electoral_area' : area[0], 'political_party' : party[0], 'european_group' : eu_group[0], 'committees' : comms, 'delegations' : delegs }
    print data
    datastore.save(unique_keys=['name', 'electoral_area'], data=data)


