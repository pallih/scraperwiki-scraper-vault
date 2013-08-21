import scraperwiki
import lxml.html

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

cols = ['name','address','postcode','phonenumber','lat','lng']

def scrape(base_url):
    for i in range(1,11):
        page_url = base_url + str(i)
        lst = []
        root = fetch_html(page_url)
    
        # cycle over list of hospitals 
        for hospital in root.find_class('results')[1].xpath('li'):
            print hospital.xpath('ul')[0].xpath('li')[1].text_content().strip()
            lng, lat = None, None
            address =  hospital.xpath('ul')[0].xpath('li')[3].text_content().strip()
            postcode = scraperwiki.geo.extract_gb_postcode(address)
            try:
                lat, lng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
            except:
                print "Failed to get map coordinates for " + hospital.xpath('ul')[0].xpath('li')[1].text_content()

            try:
                phone = hospital.xpath('ul')[0].xpath('li')[4].text_content().replace('Tel: ', '')
            except:
                phone = ''

            row = [hospital.xpath('ul')[0].xpath('li')[1].text_content().strip(),
                   address,
                   postcode,
                   phone,
                   lat,
                   lng
                  ]
            lst.append( dict(zip(cols,row)) )
            scraperwiki.sqlite.save(['name', 'address'], lst, table_name='hospitals_with_ae')

# get the north hospitals
#print "Starting North"
#scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=LN4&Coords=3591,5124&ServiceType=AandE&JScript=1&PageCount=10&PageNumber=")

# get the south west ones:
print "Starting South West"
scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=DT1&Coords=900%20,3682&ServiceType=AandE&JScript=1&PageCount=10&PageNumber=")

# get north west ones:
print "Starting North West"
scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=L7&Coords=3902,3369&ServiceType=AandE&JScript=1&PageCount=10&PageNumber=")

# get london ones:
print "Starting London"
scrape("http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=NW10&Coords=1843,5212&ServiceType=AandE&JScript=1&PageCount=10&PageNumber=")