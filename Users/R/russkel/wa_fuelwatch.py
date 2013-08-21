import scraperwiki, urllib2, re, lxml.etree
from datetime import datetime


url = "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=%i&Region=%i&Day=%s"

# tomorrow's data is available after 14:30 WST (GMT+8) apparently

#Day:
#    today (this is the default)
#    tomorrow (only available after 2:30PM) 

products = {
    1: 'Unleaded Petrol',
    2: 'Premium Unleaded',
    4: 'Diesel',
    5: 'LPG',
    6: '98 RON',
    7: 'B20 diesel'
}

regions = {
  25: 'Metro : North of River',
  26: 'Metro : South of River',
  27: 'Metro : East/Hills',
  15: 'Albany',
  28: 'Augusta / Margaret River',
  30: 'Bridgetown / Greenbushes',
  1: 'Boulder',
  2: 'Broome',
  16: 'Bunbury',
  3: 'Busselton (Townsite)',
  29: 'Busselton (Shire)',
  19: 'Capel',
  4: 'Carnarvon',
  33: 'Cataby',
  5: 'Collie',
  34: 'Coolgardie',
  35: 'Cunderdin',
  31: 'Donnybrook / Balingup',
  36: 'Dalwallinu',
  6: 'Dampier',
  20: 'Dardanup',
  37: 'Denmark',
  38: 'Derby',
  39: 'Dongara',
  7: 'Esperance',
  40: 'Exmouth',
  41: 'Fitzroy Crossing',
  17: 'Geraldton',
  21: 'Greenough',
  22: 'Harvey',
  42: 'Jurien',
  8: 'Kalgoorlie',
  43: 'Kambalda',
  9: 'Karratha',
  44: 'Kellerberrin',
  45: 'Kojonup',
  10: 'Kununurra',
  18: 'Mandurah',
  32: 'Manjimup',
  46: 'Meekatharra',
  47: 'Moora',
  48: 'Mt Barker',
  23: 'Murray',
  11: 'Narrogin',
  49: 'Newman',
  50: 'Norseman',
  12: 'Northam',
  13: 'Port Hedland',
  51: 'Ravensthorpe',
  14: 'South Hedland',
  53: 'Tammin',
  24: 'Waroona',
  54: 'Williams',
  55: 'Wubin',
  56: 'York'
}

#cruft at the start
# <rss version="2.0"><channel><title>FuelWatch Prices For all metro regions</title><ttl>720</ttl><link>http://www.fuelwatch.wa.gov.au</link><description>10/12/2011 - all metro regions</description><language>en-us</language><copyright>Copyright 2005 FuelWatch. All Rights Reserved.</copyright><lastBuildDate>Sat Dec 10 17:33:45 WST 2011Sat Dec 10 17:33:45 WST 2011</lastBuildDate><image><url>/fuelwatch/art/fuelwatch-logo.gif</url><title>FuelWatch</title><link>http://www.fuelwatch.wa.gov.au</link></image>

#the actual meat and potatos
#<item> <title>131.1: Coles Express Clarkson</title> <description>Address: Cnr Marmion Ave &amp; Pensacola Tce, CLARKSON, Phone: (08) 9408 6690</description> <brand>Coles Express</brand> <date>2011-12-10</date> <price>131.1</price> <trading-name>Coles Express Clarkson</trading-name> <location>CLARKSON</location> <address>Cnr Marmion Ave &amp; Pensacola Tce</address> <phone>(08) 9408 6690</phone> <latitude>-31.691894</latitude><longitude>115.716118</longitude> <site-features>, </site-features></item>

#</channel></rss>

dates = ['today']
#dates = [
#'5/12/2011',
#'8/12/2011',
#'9/12/2011',
#]

for date in dates:
    for reg in regions.keys():
        for prod in products.keys():
            print "Fetching %s in %s for %s..." % (products[prod], regions[reg], date)
            tree = lxml.etree.parse(urllib2.urlopen(url % (prod, reg, date)))

            datalist = []
            for item in tree.xpath('/rss/channel/item'):
                #print lxml.etree.tostring(item)
                data = {
                    'trading-name': item.xpath('trading-name/text()')[0],
                    'brand': item.xpath('brand/text()')[0],
                    'address': item.xpath('address/text()')[0],
                    'suburb': item.xpath('location/text()')[0],
                    'phone': item.xpath('phone/text()'),
                    'latitude': item.xpath('latitude/text()'),
                    'longitude': item.xpath('longitude/text()'),
                    'date': datetime.strptime(item.xpath('date/text()')[0], "%Y-%m-%d"),
                    'price': item.xpath('price/text()')[0],
                    'product': products[prod],
                    'region': regions[reg]
                }

                for f in ['latitude', 'longitude', 'phone']:
                    if isinstance(data[f], list):
                        if len(data[f]) > 0:
                            data[f] = data[f][0]
                        else:
                            data[f] = None

                #print data
                datalist.append(data)

            scraperwiki.sqlite.save(unique_keys=['trading-name', 'date'], data=datalist)
