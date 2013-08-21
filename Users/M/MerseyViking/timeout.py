import scraperwiki
import requests
import lxml.html
import re
from datetime import datetime


# A dictionary of addresses with incorrect postcodes, and their correct postcodes, or one that is near by.
duff_places = {
    "Saatchi Gallery Duke of York's HQ, King's Rd, SW3 4SQ": 'SW3 4RY',
    # Interestingly, 45 Davies Street doesn't appear on the Post Office's database, 43, 44, and 46 do though.
    "Belmacz Gallery 45 Davies Street, W1K 4LX": 'W1K 4LU',
    "Aldgate Underground Station Aldgate High St, England, E1": 'EC3N 1AH',
    "Hauser & Wirth 196a Piccadilly, W1J 9DY": 'W1J 9EY'
    }


# We have to relax our regex because zeroes can be stored as O's and 1's as I's.
postcode_regex = '\\b([A-Z]{1,2})([0-9RIO])([0-9A-Z]? ?)([0-9IO])([A-Z]{2})\\b'


def get_address(address_string):
    try:
        if address_string in duff_places:
            postcode = duff_places[address_string]
        else:
            # Because of our relaxed postcode regex, we can match some of words. So we'll assume the postcode is the
            # last match if there is more than one.
            match = None
            for match in re.finditer(postcode_regex, address_string, flags=re.IGNORECASE):
                pass

            if match is None:
                raise Exception

            postcode = match.group(1)
            # Do some basic fix-up.
            if match.group(2).lower() == 'i' or match.group(2).lower() == 'l':
                postcode += '1'
            elif match.group(2).lower() == 'o':
                postcode += '0'
            else:
                postcode += match.group(2)

            postcode += match.group(3)

            if match.group(4).lower() == 'i' or match.group(4).lower() == 'l':
                postcode += '1'
            elif match.group(4).lower() == 'o':
                postcode += '0'
            else:
                postcode += match.group(4)

            postcode += match.group(5)

        try:
            pos = scraperwiki.sqlite.select("lat, lon FROM postcodes WHERE postcode = ?", [postcode])[0]
            return (pos['lat'], pos['lon'])
        except:
            lat, lon = scraperwiki.geo.gb_postcode_to_latlng(postcode)
            if lat > 51.23 and lat < 51.74 and lon > -0.60 and lon < 0.32:
                scraperwiki.sqlite.execute('INSERT INTO postcodes VALUES(?, ?, ?)', [postcode, lat, lon])
                scraperwiki.sqlite.commit()
                return (lat, lon)
            else:
                print('Location {0}, {1} is not within the M25, giving up.'.format(lat, lon))
                return (None, None)
    except:
        print('Unable to geolocate "{0}", giving up.'.format(address_string))
        return (None, None)


def parse_page(page_dom):
    # Could also use vcard-Content-Venue to search for just venues.
    for event_dom in page_dom.xpath('//div[starts-with(@id, "vcard-Content-Event")]'):
        event_id = int(re.search('\d+$', event_dom.get('id')).group(0))

        # Check if we already have this event id, and skip this it if we do.
        events = scraperwiki.sqlite.select('* from swdata where guid = {0}'.format(event_id))
        if len(events) > 0:
            yield events[0]
            continue

        address_line = event_dom.xpath('.//address')[0].text_content()

        location = get_address(address_line)

        if location[0] is not None and location[1] is not None:
            event = {}

            information = event_dom.xpath('div[@class="information"]')[0]
            title = information.xpath('h2/a')[0]

            event['guid'] = event_id
            event['title'] = title.text_content()
            description_element = information.xpath('p[@class="overview"]')

            if len(description_element) > 0:
                event['description'] = description_element[0].text_content()

            event['link'] = title.get('href')
            event['categories'] = ','.join([s.strip().lower() for s in information.xpath('p')[0].text_content().split(',')])
            event['address'] = address_line
            event['lat'] = location[0]
            event['lon'] = location[1]
            event['pubDate'] = datetime.now()

            try:
                start_date = event_dom.cssselect('span.dtstart b')[0].get('title')
                event['start'] = datetime.strptime(start_date, '%Y-%m-%d')
            except:
                print('Unable to find a start date')

            try:
                end_date = event_dom.cssselect('b.dtend b')[0].get('title')
                event['end'] = datetime.strptime(end_date, '%Y-%m-%d')
            except:
                print('Unable to find an end date')

            try:
                image_url = event_dom.xpath('div[@class="additionalInformation"]/a/img')[0].get('src')
                image_id = re.search('images/([0-9]+)/', image_url).group(1)

                event['image_url'] = 'http://media.timeout.com/images/resizeBestFit/{0}/660/370/image.jpg'.format(image_id)
            except:
                pass

            yield event


def scrape():
    num_pages = 1

    while params['page'] <= num_pages:
        page = requests.get(URL, params=params).text

        page_dom = lxml.html.fromstring(page)

        if params['page'] == 1:
            summary = page_dom.xpath('//*[@id="mainContent"]/p')[0]
            count = int(re.search('(\d+) (match|matches) found', summary.text_content(), re.MULTILINE).group(1))
            print('TimeOut reports {0} records found'.format(count))

            if count == 0:
                break

            num_pages = int((count + params['page_size'] - 1) / params['page_size'])

        print('page {0} of {1}'.format(params['page'], num_pages))

        events = [event for event in parse_page(page_dom)]

        scraperwiki.sqlite.save(unique_keys=['guid'], data=events)
        params['page'] += 1


URL = 'http://www.timeout.com/london/search'

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `swdata` (`end` text, `description` text, `pubDate` text, `title` text, `lon` real, `start` text, `link` text, `address` text, `lat` real, `image_url` text, `guid` integer, `categories` text)')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS postcodes (`postcode` text PRIMARY KEY, `lat` real, `lon` real)')

# The postcodes are valid, but they don't appear in the database.
# "Paradise Row 74a Newman St, W1T 3DB"
# "Blain Southern 4 Hanover Square, W1S 1BP"
scraperwiki.sqlite.execute("INSERT OR REPLACE INTO postcodes VALUES('W1T 3DB', 51.51759280, -0.13602650)")
scraperwiki.sqlite.execute("INSERT OR REPLACE INTO postcodes VALUES('W1S 1BP', 51.51388850, -0.14331840)")

date_now = datetime.utcnow()

params = {
    "section": "art",
    "_source": "global",
    "profile": "london",
    "_dd": "",
    "keyword": "",
    "on": "",
    "t": "",
    "xarea": "",
    "order": "default",
    "s_date": "1900-01-01", # date_now.strftime('%Y-%m-%d'),
    "e_date": "9999-12-31", # datetime(date_now.year + 100, *date_now.timetuple()[1:-2]).strftime('%Y-%m-%d'),
    "page_size": 100,
    "page": 1
}

scrape()
#scraperwiki.sqlite.execute('delete FROM `swdata` WHERE guid = 186413')
#scraperwiki.sqlite.execute('delete FROM `swdata` WHERE guid = 359831')
#scraperwiki.sqlite.execute('delete FROM `swdata` WHERE guid = 439709')
#scraperwiki.sqlite.execute('delete FROM `swdata` WHERE guid = 495979')

