import scraperwiki
import lxml.html
import xlrd

def scrape_content( url, rownum ):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    policy = 'Not Applicable'
    pets_allowed = 'Not Applicable'
    hotel_name = 'Not Applicable'
    pet_table = 3
    
    title = root.cssselect('div.property_details_container h1')[0]
    hotel_name = title.text_content()

    table = root.cssselect('table.property_policy_table tbody')[pet_table]
    pets_allowed = table.cssselect('tr td')[1]
    pets_allowed = pets_allowed.text_content().strip()

    if (pets_allowed.lower() == 'yes'):
        policy = ''
        for d in table.cssselect('tr:nth-child(2) ~ tr'):
            policy += d.text_content().strip() + ' '

    pet = {
        'Allowed' : pets_allowed,
        'Policy' : policy,
        'Name' : hotel_name,
        'url' : url,
        'rnum' : int(rownum)
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
        url = rows[0]
        scrape_content(url, rownum)        

#START


#Data source
src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
#src = "http://hiltongardeninn3.hilton.com/en/hotels/florida/hilton-garden-inn-jacksonville-downtown-southbank-JAXSBGI/about/policies.html"

get_source(src)