import scraperwiki
import lxml.html
import re



# Get root node from url
def scrape_content(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

def get_barnumber(el):
    return el.cssselect('tr:first-child td:nth-child(2)')[0].text_content()

def get_address(el):
    return el.cssselect('tr + tr > td + td span')[0].text_content().replace('\n','').replace('\t','').replace('Map it', '').replace('\r','')

def get_phone(el):
    return el.cssselect('tr + tr > td:last-child')[0].text_content()

def get_fax(el):
    return el.cssselect('tr:nth-child(3) td:last-child')[0].text_content()

def get_county(el):
    return el.cssselect('tr:nth-child(5) td:nth-child(2)')[0].text_content()

def get_ugschool(el):
    return el.cssselect('tr:nth-child(5) td:last-child')[0].text_content().replace('\n','').replace('\t','').replace('\r','')

def get_district(el):
    return el.cssselect('tr:nth-child(6) td:nth-child(2)')[0].text_content()

def get_sections(el):
    return el.cssselect('tr:nth-child(7) td:nth-child(2)')[0].text_content().replace('\n','').replace('\t','').replace('\r','')

def get_lawschool(el):
    return el.cssselect('tr:nth-child(7) td:last-child')[0].text_content().replace('\n','').replace('\t','').replace('\r','')

def decrypt_email(root):
    string = root.cssselect('style')[0].text_content()
    print string
    pos = string.find('{display:inl')
    return string[pos-3:pos].lstrip('#')


def get_email(el, root):
    #return el.cssselect(decrypt_email(root))[0].text_content()
    temp = 'span#' + decrypt_email(root)
    print temp
    print el.cssselect(temp)[0].text_content()
    for span in el.cssselect('tr:nth-child(4) td:nth-child(2) > span#' + decrypt_email(root) + ' a'):
        print '[' + span.text_content() + ']'

def parse_attorney(el, root):
    global id
    data = dict()
    data['id'] = id
    data['Bar Number'] = get_barnumber(el)
    data['Phone'] = get_phone(el)
    data['Address'] = get_address(el)
    data['Fax Number'] = get_fax(el)
    data['County'] = get_county(el)
    data['Undergraduate School'] = get_ugschool(el)
    data['District'] = get_district(el)
    data['Sections'] = get_sections(el)
    data['Law School'] = get_lawschool(el)
    data['Email'] = get_email(el, root)
    print data
    id += 1 

def get_attorney(url):
    root = scrape_content(url)
    #parse_attorney(root.cssselect('table.tblMemberDetail')[0], root)
    return root.cssselect('table.tblMemberDetail')[0]

def scrape_page(src):
    global id
    root = scrape_content(src)
    for link in root.cssselect('tr.rowASRLodd td a'):
        get_attorney('http://members.calbar.ca.gov/' + link.attrib['href'])
        break



        
id = 1
#src = 'http://members.calbar.ca.gov/fal/MemberSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=morgan+hill&State=CA&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=&x=106&y=15'
#scrape_page(src)
src = 'http://members.calbar.ca.gov/fal/Member/Detail/98703'

print get_email(get_attorney(src), scrape_content(src))



