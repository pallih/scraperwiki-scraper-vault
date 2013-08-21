# Stations that are direct to London between 75 and 135 minutes
# arriving at 9am on a Monday
# Only includes stations that are smaller than Stroud
# Requires detached houses and views
# Updated 28/12/2012 with new criteria in new_stations:
# only stations between 65-135 minutes from London plus
# direct journeys of fewer than six stops.
from lxml import etree
from lxml.etree import tostring
from datetime import datetime
import scraperwiki
import StringIO
import gdata.spreadsheet  
import gdata.spreadsheet.service
import urllib


gd_client = gdata.spreadsheet.service.SpreadsheetsService() 
gd_client.ssl = False
#gd_client.email = ''
#gd_client.password = ''
#gd_client.source = 'LIST'
#gd_client.ProgrammaticLogin()

# Parameters for the scraper: stations, radius etc.
# TODO: replace with Google spreadsheet data. 
stations = [ {'Bearsted': 722}, 
{'Wadhurst': 9506}, 
{'Westbury': 9920}, 
{'Retford': 7667}, 
{'Nailsea & Backwell': 6464}, 
{'Downham Market': 2879}, 
{'Tiverton Parkway': 9218}, 
{'Yatton': 10376}, 
{'Uckfield': 9401}, 
{'Whittlesford': 10052}, 
{'Kemble': 5009}, 
{'Warminster': 9620}, 
{'Wivenhoe': 10196}, 
{'Hungerford': 4814}, 
{'Arundel': 344}, 
{'Waterbeach': 9653}, 
{'Robertsbridge': 7730}, 
{'Castle Cary': 1853}, 
{'Charlbury': 1952}, 
{'Liss': 5585}, 
{'Etchingham': 3305}, 
{'Higham': 4574}, 
{'Tisbury': 9215}, 
{'Evesham': 3323}, 
{'Grateley': 3920}, 
{'Berkswell': 15005}, 
{'Sherborne': 8171}, 
{'Long Buckby': 5816}, 
{'East Midlands Parkway': 15019}, 
{'Pewsey': 7211}, 
{'Moreton-In-Marsh': 6371}, 
{'Hinton Admiral': 4643}, 
{'Stonegate': 8786}, 
{'Buxted': 1640},  
{'Teynham': 9089}, 
{'Littleport': 5606}, 
{'Kingham': 5156}, 
{'Shelford': 8138}, 
{'Wye': 10346}, 
{'Lenham': 5495}, 
{'Botley': 1217}, 
{'Dovercourt': 2873}, 
{'Sandling': 7961}, 
{'Thorpe-le-Soken': 9173}, 
{'Shawford': 8120}, 
{'Corby': 15013}, 
{'Stonehouse': 8795}, 
{'Watlington': 9698}, 
{'Cooden Beach': 2309}, 
{'Hanborough': 4214}, 
{'Ford': 3575}, 
{'Templecombe': 9080}, 
{'Harwich International': 4307}, 
{'Great Chesterford': 3944}, 
{'Bedhampton': 779}, 
{'Pluckley': 7259}, 
{'Sway': 8957}, 
{'Bosham': 1205}, 
{"Rowland's Castle": 7814}, 
{'Ashurst New Forest': 389}, 
{'Swaythling': 8960}, 
{'Bedwyn': 788}, 
{'Shepreth': 8168}, 
{'Langley Mill': 5378}, 
{'Charing': 1949}, 
{'Howden': 4781}, 
{'Aylesham': 464}, 
{'Minster': 6278}, 
{'Foxton': 3611}, 
{'Great Bentley': 3938}, 
{'Harrietsham': 4265}, 
{'Hythe': 4859}, 
{'Berwick (Sussex)': 884}, 
{'Sturry': 8864}, 
{'Chartham': 1958}, 
{'Selling': 8060}, 
{'Fishbourne': 3524}, 
{'Glynde': 3821}, 
{'Nutbourne': 6842}, 
{'Pershore': 7184}, 
{'Alresford': 179}, 
{'Westenhanger': 9929}, 
{'Mistley': 6284}, 
{"Shepherd's Well": 8159}, 
{'Amberley': 212}, 
{'Bekesbourne': 797}, 
{'Adisham': 95}, 
{'Crowhurst': 2486}, 
{'Ockley': 6869}, 
{'Dumpton Park': 2957}, 
{'Hollingbourne': 4661}, 
{'Atherstone': 413}, 
{"King's Sutton": 5189}, 
{'Leigh (Kent)': 5477}, 
{'Chilham': 2048}, 
{'Hatton': 4343}, 
{'Kearsney': 4985}, 
{'Honeybourne': 4697}, 
{'Lapworth': 5402}, 
{'Warblington': 9605}, 
{'Martin Mill': 6080}, 
{'Bishopstone': 1022}, 
{'Weeley': 9728}, 
{'Wrabness': 10325}, 
{'Wilmcote': 10118}, 
{'Snowdown': 8357}, 
{'Normans Bay': 6698}, 
{'Southease': 8474}, 
{'Warnham': 9623}, 
{'Pevensey Bay': 7208}, 
{'Shipton': 8207}, 
{'Claverdon': 2177}, 
{'Bearley': 716} ]

new_stations = [
{'Westbury': 9920}, 
{'Stroud': 8858},
{'Hungerford': 4814}, 
{'Pewsey': 7211}, 
{'Chippenham': 2069},
{'Bath spa': 680},
{'Bristol parkway': 1385},
{'Westbury': 9920},
{'Warminster': 9620},  
{'Andover': 236},
{'Grateley': 3920}, 
{'Salisbury': 7922},
{'Tisbury': 9215}, 
{'Castle Cary': 1853}, 
{'Kemble': 5009}, 
{'Stonehouse': 8795},  
{'Shipton': 8207}, 
{'Kingham': 5156}, 
{'Taunton': 9056}
]

MIN_PRICE = 270000
MAX_PRICE = 340000
MIN_BEDROOMS = 3
RADIUS_MILES = 10.0
stop_phrases = [ "views over the garden",
"views over the rear garden", "views over the front garden",
"views over rear garden", "views over front garden",
"views across the gardens", "views onto the garden",
"in need of updating", "in need of modernisation",
"views over rear aspect", "views over front aspect",
"views over the rear aspect", "views over the front aspect",
"views over side aspect", "views over the side aspect",
"1970s",  "bungalow", "bunaglow",
"views to the front garden", "views to the rear garden" ]
# "semi detached", "semi-detached", "semidetached",
DOMAIN = 'http://www.rightmove.co.uk' 

def scrape_individual_house(house_url, town):
    HOUSE_URL = (DOMAIN + house_url).split('/svr/')[0]
    #print 'Scraping %s' % HOUSE_URL
    house_html = scraperwiki.scrape(HOUSE_URL)
    house_parser = etree.HTMLParser()
    house_tree = etree.parse(StringIO.StringIO(house_html), house_parser)
    house_text = house_tree.xpath('string(//div[@class="propertyDetailDescription"])')
    title = house_tree.xpath('string(//h1[@id="propertytype"])')
    house = {}
    # Store information about views.
    stopped_phrase = None
    if 'views' in house_text.lower() or 'elevated position' in house_text.lower():
        house['views'] = True
        # Check for stop phrases
        for sp in stop_phrases:
            if (sp in house_text.lower()):
                #print 'Ignoring %s because of stop phrase: %s' % (HOUSE_URL, sp)
                stopped_phrase = sp
            if (sp in title.lower()):
                stopped_phrase = sp
    else:
        house['views'] = False
    if stopped_phrase:
        house['stop'] = stopped_phrase
    else:
        house['stop'] = ''
        #if not any(d.get('link') == HOUSE_URL for d in house_items):
    image_url = tostring(house_tree.xpath('//img[@id="mainphoto"]')[0])
    price = house_tree.xpath('string(//div[@id="amount"])')
    nearby_stations = house_tree.xpath('string(//div[@id="nearbystations"]/div)')
    ns = nearby_stations.split("(")
    distance = ns[-1].replace(")","")
    distance = ' '.join(distance.split()).strip()
    map_img = house_tree.xpath('//a[@id="minimapwrapper"]/img')
    if map_img:
        map_img = tostring(house_tree.xpath('//a[@id="minimapwrapper"]/img')[0])
    else:
        map_img = ''
    house['title'] = "%s - %s, %s, %s from station" % (title, town, price, distance)
    #print 'HOUSE FOUND! %s, %s ' % (house['title'], HOUSE_URL)
    item_text = '<a href="' + HOUSE_URL + '">' + image_url + '</a>'
    #item_text += '<div style="position:relative;">'
    item_text += '<a href="' + HOUSE_URL + '">' + map_img + '</a>'
    #item_text += '<img id="googlemapicon" src="http://www.rightmove.co.uk/ps/images11074/maps/icons/rmpin.png"'
    #item_text += ' style="position:absolute;top:100px;left:100px;alt="Property location" /></div>'
    item_text += house_text
    item_text = item_text.replace("views","<span style='font-weight:bold;color:red;'>views</span>")
    house['description'] = item_text.replace("fireplace","<span style='font-weight:bold;color:red;'>fireplace</span>")
    house['distance_miles'] = float(distance.replace(" miles",""))
    print HOUSE_URL
    house['link'] = HOUSE_URL
    house['pubDate'] = datetime.now()
    scraperwiki.sqlite.save(['link'], house)

# Gather list of results for an individual station. 
def scrape_results_page(results_url, town, initial=False):
    results_url = DOMAIN + results_url
    print results_url
    html = scraperwiki.scrape(results_url)
    print html
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO.StringIO(html), parser)
    house_links = tree.xpath('//ol[@id="summaries"]//a[starts-with(text(), "More details")]/@href')
    for house_link in house_links:
        scrape_individual_house(house_link, town)
    if initial:
        results_links = tree.xpath('//ul[@class="items"]//a/@href')
        for r in results_links:
            scrape_results_page(r, town)

# Go through each station: scrape each set of results in turn. 
for station in new_stations:
    station_name = station.keys()[0].title()
    print 'Scraping %s' % station_name
    station_id = station.values()[0]
    url1 = '/property-for-sale/find.html?locationIdentifier=STATION%%5E%s&minPrice=%s&maxPrice=%s' % (station_id, MIN_PRICE, MAX_PRICE)
    url2 = '&minBedrooms=%s&oldDisplayPropertyType=houses&radius=%s' % (MIN_BEDROOMS, RADIUS_MILES)
    INITIAL_URL = url1 + url2
    scrape_results_page(INITIAL_URL, town=station_name, initial=True)