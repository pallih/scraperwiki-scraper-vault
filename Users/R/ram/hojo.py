import scraperwiki
import lxml.html
import xlrd

def scrape_content( url, rownum ):
    hotel_name = 'Empty Hotel Name'
    policy = 'Empty Policy'
    try:
        html = scraperwiki.scrape(url)

        root = lxml.html.fromstring(html)
        hotel_name = root.cssselect('div.prop_header address h1')[0].text_content()
        policy = 'Empty'
        
        policy = root.cssselect('ul.regulations li span.pets')[0].text_content() 
    except IndexError, e:
        policy = root.cssselect('ul.regulations li span.no_pets')[0].text_content()
        #policy = e#+' might be no pet policy'
    except:
        policy = 'Unexpected Error: mostly 404'

    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : hotel_name if hotel_name is not None else 'Empty Hotel Name',
        'policy' : policy if policy is not 'Empty' else 'No Pet Policy'
    }

    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)
    #print data

def get_source( src ): #open excel and get the sheet
    print 'hello'
    xlbin = scraperwiki.scrape(src)
    print 'hello'
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
#src = 'http://ramanathan.weebly.com/uploads/1/1/0/3/1103525/set1.xls'
src = 'http://sanspace.in/test/set1.xls'
get_source(src)

#url = 'http://www.hojo.com/hotels/texas/austin/howard-johnson-inn-austin-i-35/hotel-overview'
#scrape_content( url, 25)
#url = 'http://www.hojo.com/hotels/arkansas/eureka-springs/howard-johnson-express-inn-eureka-springs/hotel-overview'
#scrape_content( url, 27)
#url = 'http://www.super8.com/hotels/kentucky/bowling-green/super-8-bowling-green-south/hotel-overview'
scrape_content( url, 23)

#url = 'http://www.super8.com/hotels/oklahoma/big-cabin-vinita/super-8-big-cabin-vinita-area/hotel-overview'
scrape_content( url, 24)
