import scraperwiki
import lxml.html
import xlrd
import json
import re
import urllib
import repr as reprlib

def valid_url(url):
    return re.compile(r'\w*about/policies\.html$').search(url)

def get_policy(url, rnum):       
    pet_allowed = 'NA',
    policy = 'NA',
    address = 'NA',
    location = 'Could not find URL'
    pet_table = 0
    if (url):      
        html = scraperwiki.scrape(url)    
        root = lxml.html.fromstring(html)
        print root
        for table in root.cssselect('table.property_policy_table'):
            for title in table.cssselect('th.table_block_head'):
                if (title.text_content().strip().lower() == 'Pets'.lower()):
                    pet_table = table
                    break
        if pet_table is not None:
            print pet_table.text_content()
            #for c in pet_table.cssselect('tbody tr:nth-child(1) td'):
            for c in pet_table.cssselect('tbody tr td'):
                pet_allowed = c.text_content().strip()
                print pet_allowed
                break
            if (pet_allowed  == 'Yes'):
                for p in root.cssselect('tbody tr:nth-child(1) + tr'):
                    policy = p.text_content().strip()                            
                    print policy
            else:
                policy = 'Pets Not Allowed'
                pet_allowed == 'No'
            for p in root.cssselect('span.address'):
                address = p.text_content().strip()
                break
            location = url
    pet = {
        'pets' : pet_allowed,
        'policy' : policy,
        'address' : address,
        'url' : location,
        'rnum' : int(rnum)
    }
    print scraperwiki.sqlite.save(unique_keys=['rnum'], data=pet)

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        q = rows[1]
        url = scrape_url(q)
        get_policy(url, rownum)

#START

def scrape_url(q):
    parm = {
        'cx' : '014212376427772793791:vitaxk4rzv8',
        'key' : 'AIzaSyBYiMH_P-KgXkBRdrqbKxIjU9_fEzW1U6s',#'AIzaSyDs4M61ATYhVhJO2S2KOs9c9bjBu4Vm45w',#'AIzaSyAWrKNUN3jbSEjttQV6QfjLhfUP24pBl3g',
        'num' : 3,
        'q' : q
    }
    data = scraperwiki.scrape('https://www.googleapis.com/customsearch/v1?' + urllib.urlencode(parm))
    res = parse_results(json.loads(data))
    if (res):
        return res
    else:
        return 0
    
def parse_results(data):
    if 'items' in data:
        for res in data['items']:
            url = res['link']
            if valid_url(url):
                return url
                break
            else:
                return 0
    else:
        url = "Couldn't find URL"
        return 0    


#Data source
src = "http://sanspace.in/pet/hilton.xls"
#get_source(src)
#go = 'http://doubletree3.hilton.com/en/hotels/maine/doubletree-by-hilton-hotel-portland-me-PWMMMDT/about/policies.html'

go = 'http://homewoodsuites3.hilton.com/en/hotels/maryland/homewood-suites-by-hilton-baltimore-arundel-mills-BALARHW/about/policies.html'
get_policy( go, 223)

