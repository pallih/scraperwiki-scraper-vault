import scraperwiki
import lxml.html
import datetime
import re
import urllib
import demjson

# search for 4-5 bedroom houses in Athboy and Trim
url = 'http://www.daft.ie'
next_page = '/searchsale.daft?s[cc_id]=c2&s[a_id][]=2760&s[a_id][]=2776&s[route_id]=&s[a_id_transport]=0&s[address]=&s[txt]=&s[mnb]=4&s[mxb]=5&s[mnbt]=&s[mxbt]=&s[mnp]=&s[mxp]=&s[pt_id]=&s[house_type]=&s[sqmn]=&s[sqmx]=&s[mna]=&s[mxa]=&s[npt_id]=&s[days_old]=&s[new]=&s[agreed]=&search.x=33&search.y=10&more=&tab=&search=1&s[search_type]=sale&s[transport]=&s[advanced]=1&s[price_per_room]=&fr=default'




GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

def geocode(address, sensor = 'false', **geo_args):
    geo_args.update({
        'address': address,
        'sensor': sensor  
    })

    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = demjson.decode(urllib.urlopen(url).read())

    lat, lng = None, None
    if result['status'] == 'OK':
        try:
            lat = float(result['results'][0]['geometry']['location']['lat'])
            lng = float(result['results'][0]['geometry']['location']['lng'])
        except Exception as e:
            print 'failed to get coords when addres %s had result %r' % (address, result)

    return lat, lng


def drop_table():
        scraperwiki.sqlite.execute('''DROP TABLE `house_data`''')
#drop_table()


def create_table():
    scraperwiki.sqlite.execute('''CREATE TABLE `house_data` (`town` text, `price` text, `num_bedrooms` text, `address` text, `date_added` text, `price_per_room` integer, `type` text, `lat` real, `lng` real, CONSTRAINT unique_on_address_town_price UNIQUE (address, town, price))''')
#create_table()


def update_table(data_dict):
    scraperwiki.sqlite.execute('''INSERT OR IGNORE INTO house_data VALUES (:town, :price, :num_bedrooms, :address, :date_added, :price_per_room, :type, :lat, :lng)''',
    data_dict)
    scraperwiki.sqlite.commit()



def parse_page(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for box in root.cssselect('table#sr_content div.box'):
        title_a = box.cssselect('h2 > a')
        if title_a:
            description = title_a[0].text
            print title_a

            description_patterns = [r'(.*), (Athboy)', r'(.*), (Trim)']
            for pattern in description_patterns:
                m = re.compile(pattern).search(description)
                if m:
                    address = m.group(1).strip()
                    town = m.group(2).strip()
                    lookup_address = '%s, %s, Meath, Ireland' % (address, town)
                    lat, lng = geocode(lookup_address)                    
                    break


            def get_type(info_li):
                for item in info_li:
                    if 'semi' in item.text_content().lower():
                         return 'semi-detached'
                    if 'detached' in item.text_content().lower():
                         return 'detached'


            def get_num_rooms(info_li):
                for item in info_li:
                    num_rooms = None
                    #TODO
                    return house_type


            for house_type, num_bedrooms, _ in box.cssselect('.info li'):
                if 'semi' in info_li.text_content().lower():
                    type = 'semi-detached'
                else:
                    type = 'detached'
            print type


            price = box.cssselect('.price')[0].text_content()
            num_bedrooms = box.cssselect('.bedrooms')[0].text_content()
            try:
                euro = re.compile('([\d,]+).*').search(price).group(1)
                num_bedrooms = re.compile(r'(\d+) Bedrooms').search(num_bedrooms).group(1)
                price_per_room = int(euro.replace(',', ''))/int(num_bedrooms)
            except Exception as e:
                euro = price # probably says "Price on Application"
                price_per_room = None
            data = {
              #'date': datetime.date.today(),
              'date_added': str(datetime.date.today()),
              'type': type,
              'address' : address,
              'town': town,
              'price': euro,
              'price_per_room': price_per_room,
              'num_bedrooms': num_bedrooms,
              'lat': lat,
              'lng': lng,
            }
            #scraperwiki.sqlite.save(unique_keys=['address', 'price'], data=data)
            print address, town, euro
            update_table(data)

    try:
        next_page ,= root.cssselect('div.pagination div.next a')
    except ValueError as e:
        return None
    else:
        return next_page.attrib['href']


def main(url, next_page):
    while(True):
        print next_page
        next_page = parse_page(url + next_page)
        if not next_page:
            break
main(url, next_page)

def test():
    print scraperwiki.sqlite.show_tables() 


import scraperwiki
import lxml.html
import datetime
import re
import urllib
import demjson

# search for 4-5 bedroom houses in Athboy and Trim
url = 'http://www.daft.ie'
next_page = '/searchsale.daft?s[cc_id]=c2&s[a_id][]=2760&s[a_id][]=2776&s[route_id]=&s[a_id_transport]=0&s[address]=&s[txt]=&s[mnb]=4&s[mxb]=5&s[mnbt]=&s[mxbt]=&s[mnp]=&s[mxp]=&s[pt_id]=&s[house_type]=&s[sqmn]=&s[sqmx]=&s[mna]=&s[mxa]=&s[npt_id]=&s[days_old]=&s[new]=&s[agreed]=&search.x=33&search.y=10&more=&tab=&search=1&s[search_type]=sale&s[transport]=&s[advanced]=1&s[price_per_room]=&fr=default'




GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

def geocode(address, sensor = 'false', **geo_args):
    geo_args.update({
        'address': address,
        'sensor': sensor  
    })

    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    result = demjson.decode(urllib.urlopen(url).read())

    lat, lng = None, None
    if result['status'] == 'OK':
        try:
            lat = float(result['results'][0]['geometry']['location']['lat'])
            lng = float(result['results'][0]['geometry']['location']['lng'])
        except Exception as e:
            print 'failed to get coords when addres %s had result %r' % (address, result)

    return lat, lng


def drop_table():
        scraperwiki.sqlite.execute('''DROP TABLE `house_data`''')
#drop_table()


def create_table():
    scraperwiki.sqlite.execute('''CREATE TABLE `house_data` (`town` text, `price` text, `num_bedrooms` text, `address` text, `date_added` text, `price_per_room` integer, `type` text, `lat` real, `lng` real, CONSTRAINT unique_on_address_town_price UNIQUE (address, town, price))''')
#create_table()


def update_table(data_dict):
    scraperwiki.sqlite.execute('''INSERT OR IGNORE INTO house_data VALUES (:town, :price, :num_bedrooms, :address, :date_added, :price_per_room, :type, :lat, :lng)''',
    data_dict)
    scraperwiki.sqlite.commit()



def parse_page(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for box in root.cssselect('table#sr_content div.box'):
        title_a = box.cssselect('h2 > a')
        if title_a:
            description = title_a[0].text
            print title_a

            description_patterns = [r'(.*), (Athboy)', r'(.*), (Trim)']
            for pattern in description_patterns:
                m = re.compile(pattern).search(description)
                if m:
                    address = m.group(1).strip()
                    town = m.group(2).strip()
                    lookup_address = '%s, %s, Meath, Ireland' % (address, town)
                    lat, lng = geocode(lookup_address)                    
                    break


            def get_type(info_li):
                for item in info_li:
                    if 'semi' in item.text_content().lower():
                         return 'semi-detached'
                    if 'detached' in item.text_content().lower():
                         return 'detached'


            def get_num_rooms(info_li):
                for item in info_li:
                    num_rooms = None
                    #TODO
                    return house_type


            for house_type, num_bedrooms, _ in box.cssselect('.info li'):
                if 'semi' in info_li.text_content().lower():
                    type = 'semi-detached'
                else:
                    type = 'detached'
            print type


            price = box.cssselect('.price')[0].text_content()
            num_bedrooms = box.cssselect('.bedrooms')[0].text_content()
            try:
                euro = re.compile('([\d,]+).*').search(price).group(1)
                num_bedrooms = re.compile(r'(\d+) Bedrooms').search(num_bedrooms).group(1)
                price_per_room = int(euro.replace(',', ''))/int(num_bedrooms)
            except Exception as e:
                euro = price # probably says "Price on Application"
                price_per_room = None
            data = {
              #'date': datetime.date.today(),
              'date_added': str(datetime.date.today()),
              'type': type,
              'address' : address,
              'town': town,
              'price': euro,
              'price_per_room': price_per_room,
              'num_bedrooms': num_bedrooms,
              'lat': lat,
              'lng': lng,
            }
            #scraperwiki.sqlite.save(unique_keys=['address', 'price'], data=data)
            print address, town, euro
            update_table(data)

    try:
        next_page ,= root.cssselect('div.pagination div.next a')
    except ValueError as e:
        return None
    else:
        return next_page.attrib['href']


def main(url, next_page):
    while(True):
        print next_page
        next_page = parse_page(url + next_page)
        if not next_page:
            break
main(url, next_page)

def test():
    print scraperwiki.sqlite.show_tables() 


