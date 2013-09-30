import scraperwiki
import lxml.html

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

try:
    scraperwiki.sqlite.execute("drop table walkin_centres")
except:
    pass

scraperwiki.sqlite.execute("create table walkin_centres (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

for page_num in range(1,13):

    url = "http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=LN4&Coords=3591%2c5124&ServiceType=WalkInCentre&JScript=1&PageCount=13&PageNumber=" + str(page_num)
    print url

    root = fetch_html(url)

    for result in root.find_class('results'):
        for line in result.xpath('ul/li/ul'):
            title = link = address = phonenumber = lng = lat = postcode = ''
            for l in line.xpath('li'):
            
                if l.xpath('h3/a'):
                    title = l.xpath('h3/a')[0].text
                    for i in l.iterlinks():
                        link = "http://www.nhs.uk" + i[2]
                if l.text and not l.text.startswith('(') and not l.text.startswith('Tel:') :
                    address = l.text
                    try:
                        postcode = scraperwiki.geo.extract_gb_postcode(address)
                        lng, lat = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                    except:
                        pass
                if l.text and l.text.startswith('Tel:'):
                    tel, phonenumber = l.text.split(':')
                    

            scraperwiki.sqlite.execute('insert into walkin_centres values (?, ?, ?, ?, ?, ?, ?)', (title, link, address, phonenumber, lng, lat, postcode))
            scraperwiki.sqlite.commit()import scraperwiki
import lxml.html

def fetch_html(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

try:
    scraperwiki.sqlite.execute("drop table walkin_centres")
except:
    pass

scraperwiki.sqlite.execute("create table walkin_centres (title string, link string, address string, phonenumber string, lng int, lat int, postcode string)")

for page_num in range(1,13):

    url = "http://www.nhs.uk/ServiceDirectories/Pages/ServiceResults.aspx?Postcode=LN4&Coords=3591%2c5124&ServiceType=WalkInCentre&JScript=1&PageCount=13&PageNumber=" + str(page_num)
    print url

    root = fetch_html(url)

    for result in root.find_class('results'):
        for line in result.xpath('ul/li/ul'):
            title = link = address = phonenumber = lng = lat = postcode = ''
            for l in line.xpath('li'):
            
                if l.xpath('h3/a'):
                    title = l.xpath('h3/a')[0].text
                    for i in l.iterlinks():
                        link = "http://www.nhs.uk" + i[2]
                if l.text and not l.text.startswith('(') and not l.text.startswith('Tel:') :
                    address = l.text
                    try:
                        postcode = scraperwiki.geo.extract_gb_postcode(address)
                        lng, lat = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                    except:
                        pass
                if l.text and l.text.startswith('Tel:'):
                    tel, phonenumber = l.text.split(':')
                    

            scraperwiki.sqlite.execute('insert into walkin_centres values (?, ?, ?, ?, ?, ?, ?)', (title, link, address, phonenumber, lng, lat, postcode))
            scraperwiki.sqlite.commit()