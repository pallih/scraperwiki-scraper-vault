# encoding: utf-8

"""
Quick experiment based on code written for OpenBlock"""

import scraperwiki

from datetime import datetime
import feedparser

URL = 'http://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php'

# 'address': u'1600 BROADWAY E-CO',
#  'agencies': u'Boone Hospital Center Ambulance',
#  'calldatetime': u'12/8/2010 12:19:35 PM',
#  'extnaturedisplayname': u'Long Distance Transport',
#  'fdids': u'19054',
#  'geo_lat': u'38.94981118',
#  'geo_long': u'-92.31585499',
#  'innum': u'201022877',
#  'latitude': u'38.94981118',
#  'longitude': u'-92.31585499',
#  'summary': u'12/8/2010 12:19:35 PM : 1600 BROADWAY E-CO : Boone Hospital Center Ambulance',
#  'summary_detail': {'base': 'http://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php',
#                     'language': None,
#                     'type': 'text/html',
#                     'value': u'12/8/2010 12:19:35 PM : 1600 BROADWAY E-CO : Boone Hospital Center Ambulance'},
#  'timestamp': u'1291832375',
#  'title': u'Long Distance Transport',
#  'title_detail': {'base': 'http://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php',
#                   'language': None,
#                   'type': 'text/plain',
#                   'value': u'Long Distance Transport'},
#  'trucks': u'M151',
#  'updated': u'Wed, 08 Dec 2010 12:19:35 CST',
#  'updated_parsed': time.struct_time(tm_year=2010, tm_mon=12, tm_mday=8, tm_hour=18, tm_min=19, tm_sec=35, tm_wday=2, tm_yday=342, tm_isdst=0)}

def get_element(entry, name, namespace="calldata"):
    """Workaround for horrible feedparser behavior where you sometimes
    get the xml namespace as part of the property name, and sometimes don't.
    """
    return getattr(entry, '%s_%s' % (namespace, name), None) or getattr(entry, name)


def update(url):
    f = feedparser.parse(url)
    for entry in f.entries:
        item = dict(
            title = entry.title,
            description = entry.summary,
            pub_date = datetime(*entry.updated_parsed[:6]),
            lat = float(entry.geo_lat),
            lon=float(entry.geo_long),
            location_name=get_element(entry, 'address'),
        )
        # parse call time
        ct = datetime.strptime(get_element(entry, 'calldatetime'),
                               r"%m/%d/%Y %I:%M:%S %p")
        item['item_date'] = ct

        # extra attributes
        item['calldatetime'] = ct
        try:
            item['innum'] = int(get_element(entry, 'innum'))
        except:
            print "Missing incident number"
            continue

        for key in ['trucks', 'fdids', 'agencies', 'address']: 
            try:
                item[key]  = get_element(entry, entry[key])
            except: 
                pass

        # this one will be a Lookup on the openblock side.
        # a category that is available in the data.
        item['incident_type'] = entry.title
        yield item

for item in update(URL):
    print scraperwiki.sqlite.save(unique_keys=["innum"], data=item)


# encoding: utf-8

"""
Quick experiment based on code written for OpenBlock"""

import scraperwiki

from datetime import datetime
import feedparser

URL = 'http://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php'

# 'address': u'1600 BROADWAY E-CO',
#  'agencies': u'Boone Hospital Center Ambulance',
#  'calldatetime': u'12/8/2010 12:19:35 PM',
#  'extnaturedisplayname': u'Long Distance Transport',
#  'fdids': u'19054',
#  'geo_lat': u'38.94981118',
#  'geo_long': u'-92.31585499',
#  'innum': u'201022877',
#  'latitude': u'38.94981118',
#  'longitude': u'-92.31585499',
#  'summary': u'12/8/2010 12:19:35 PM : 1600 BROADWAY E-CO : Boone Hospital Center Ambulance',
#  'summary_detail': {'base': 'http://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php',
#                     'language': None,
#                     'type': 'text/html',
#                     'value': u'12/8/2010 12:19:35 PM : 1600 BROADWAY E-CO : Boone Hospital Center Ambulance'},
#  'timestamp': u'1291832375',
#  'title': u'Long Distance Transport',
#  'title_detail': {'base': 'http://www.gocolumbiamo.com/PSJC/Services/911/911dispatch/fire_georss.php',
#                   'language': None,
#                   'type': 'text/plain',
#                   'value': u'Long Distance Transport'},
#  'trucks': u'M151',
#  'updated': u'Wed, 08 Dec 2010 12:19:35 CST',
#  'updated_parsed': time.struct_time(tm_year=2010, tm_mon=12, tm_mday=8, tm_hour=18, tm_min=19, tm_sec=35, tm_wday=2, tm_yday=342, tm_isdst=0)}

def get_element(entry, name, namespace="calldata"):
    """Workaround for horrible feedparser behavior where you sometimes
    get the xml namespace as part of the property name, and sometimes don't.
    """
    return getattr(entry, '%s_%s' % (namespace, name), None) or getattr(entry, name)


def update(url):
    f = feedparser.parse(url)
    for entry in f.entries:
        item = dict(
            title = entry.title,
            description = entry.summary,
            pub_date = datetime(*entry.updated_parsed[:6]),
            lat = float(entry.geo_lat),
            lon=float(entry.geo_long),
            location_name=get_element(entry, 'address'),
        )
        # parse call time
        ct = datetime.strptime(get_element(entry, 'calldatetime'),
                               r"%m/%d/%Y %I:%M:%S %p")
        item['item_date'] = ct

        # extra attributes
        item['calldatetime'] = ct
        try:
            item['innum'] = int(get_element(entry, 'innum'))
        except:
            print "Missing incident number"
            continue

        for key in ['trucks', 'fdids', 'agencies', 'address']: 
            try:
                item[key]  = get_element(entry, entry[key])
            except: 
                pass

        # this one will be a Lookup on the openblock side.
        # a category that is available in the data.
        item['incident_type'] = entry.title
        yield item

for item in update(URL):
    print scraperwiki.sqlite.save(unique_keys=["innum"], data=item)


