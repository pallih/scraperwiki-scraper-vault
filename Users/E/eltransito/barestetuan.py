import scraperwiki
import lxml.html

def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 
    

print "Starting!"

try:
    scraperwiki.sqlite.execute("drop table dentists")
except:
    pass

scraperwiki.sqlite.execute("create table dentists (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

for page_num in range(1,788):

    url = "http://11870.com/konsulto?q=bares+tetuan="+ str(page_num)
    print url

    root = fetch_html(url)
    if root:
        try:
            for result in root.find_class('organisation-wrapper'):
                title = link = address = phonenumber = lng = lat = postcode = ''
                title = result.find_class('notranslate')[0].xpath('a')[0].text.strip()
                link = "http://11870.com/" + result.find_class('notranslate')[0].xpath('a')[0].attrib['href']
                address = result.xpath('div/ul/li')[0]
                phonenumber = result.xpath('div/ul/li')[1]
                postcode = scraperwiki.geo.extract_gb_postcode(address.text)
                lng, lat = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                scraperwiki.sqlite.execute('insert into dentists values (?, ?, ?, ?, ?, ?, ?)', (title, link, address.text, phonenumber.text, lng, lat, postcode))
                scraperwiki.sqlite.commit()
        except:
            print "Failed on: " + title
    
