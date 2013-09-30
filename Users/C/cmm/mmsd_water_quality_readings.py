import datetime
import re
import scraperwiki
from lxml import etree
from dateutil.parser import parse

STANDARDS_URL = "http://v3.mmsd.com/H2OInfo/xml/Standards.xml"
WATER_QUALITY_URL = "http://v3.mmsd.com/H2OInfo/xml/WaterQuality.xml"

def normalize_element_keys(element_attributes):
    return dict([(normalize_element_key(k), convert_to_datetime(normalize_element_key(k), v)) for k, v in element_attributes.iteritems()])

def normalize_element_key(key):
    if key == 'lat':
        return 'latitude'
    elif key == 'lon' or key == 'lng':
        return 'longitude'
    elif key == 'upstamp':
        return 'updated_at'
    elif key == 'stamp':
        return 'created_at'
    else:
        return convert_camel_case_to_underscore(key)

def convert_to_datetime(key, value):
    if key == 'created_at' or key == 'updated_at':
        value = parse(value)
    return value

def convert_camel_case_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

xml = scraperwiki.scrape(STANDARDS_URL)
standards_xml = etree.XML(xml)

try:
    last_update_at = parse(scraperwiki.sqlite.select("MAX(updated_at) AS last_updated_at FROM standards")[0]['last_updated_at'])
except:
    last_update_at = datetime.datetime.fromtimestamp(0)

if last_update_at < parse(standards_xml.get('upstamp')):
    scraperwiki.sqlite.save(['updated_at'], normalize_element_keys(standards_xml.attrib), table_name='standards')

    site_standards = []
    for site in standards_xml.findall('site'):
        site_standards.append({
            'mmsd_id': site.get('MMSD_ID'),
            'conductivity_low': site.find('conductivity').get('low'),
            'conductivity_high': site.find('conductivity').get('high'),
            'dissolved_oxygen_low': site.find('dissolvedOxygen').get('low'),
            'dissolved_oxygen_high': site.find('dissolvedOxygen').get('high'),
            'turbidity_low': site.find('turbidity').get('low'),
            'turbidity_high': site.find('turbidity').get('high'),
            'stage_active': site.find('stage').get('active'),
            'stage_flood': site.find('stage').get('flood'),
            'stage_moderate': site.find('stage').get('moderate'),
            'stage_major': site.find('stage').get('major'),
            'water_temperature_low': site.find('waterTemperature').get('low'), #missing?
            'water_temperature_high': site.find('waterTemperature').get('high')
        })
    scraperwiki.sqlite.save(['mmsd_id'], site_standards, table_name='site_standards')

xml = scraperwiki.scrape(WATER_QUALITY_URL)
water_quality_xml = etree.XML(xml)

try:
    last_update_at = parse(scraperwiki.sqlite.select("MAX(updated_at) AS last_updated_at FROM water_qualities")[0]['last_updated_at'])
except:
    last_update_at = datetime.datetime.fromtimestamp(0)

if last_update_at < parse(water_quality_xml.get('upstamp')):
    scraperwiki.sqlite.save(['updated_at'], normalize_element_keys(water_quality_xml.attrib), table_name='water_qualities')

    for site in water_quality_xml.findall('site'):
        site_data = normalize_element_keys(site.attrib)
        scraperwiki.sqlite.save(['mmsd_id'], site_data, table_name='water_quality_sites')
        mmsd_id = site_data['mmsd_id']
        for dailyUpdate in site.findall('dailyUpdate'):
            row = dict(normalize_element_keys(dailyUpdate.attrib).items() + {'mmsd_id': mmsd_id}.items())
            scraperwiki.sqlite.save(['created_at', 'mmsd_id'], row, table_name='water_quality_readings')
            data = []
            for hourlyUpdate in dailyUpdate.findall('hourlyUpdate'):
                #hourlyUpdate is just the average of quarterly update, so we don't need it since we pull in quarterlyUpdate
                for quarterlyUpdate in hourlyUpdate.findall('quarterlyUpdate'):
                    #quarterly refers to the 00 15 30 45 times of the hour
                    row = dict(normalize_element_keys(quarterlyUpdate.attrib).items() + {'mmsd_id': mmsd_id}.items())
                    data.append(row)
            scraperwiki.sqlite.save(['created_at', 'mmsd_id'], data, table_name='water_quality_readings')import datetime
import re
import scraperwiki
from lxml import etree
from dateutil.parser import parse

STANDARDS_URL = "http://v3.mmsd.com/H2OInfo/xml/Standards.xml"
WATER_QUALITY_URL = "http://v3.mmsd.com/H2OInfo/xml/WaterQuality.xml"

def normalize_element_keys(element_attributes):
    return dict([(normalize_element_key(k), convert_to_datetime(normalize_element_key(k), v)) for k, v in element_attributes.iteritems()])

def normalize_element_key(key):
    if key == 'lat':
        return 'latitude'
    elif key == 'lon' or key == 'lng':
        return 'longitude'
    elif key == 'upstamp':
        return 'updated_at'
    elif key == 'stamp':
        return 'created_at'
    else:
        return convert_camel_case_to_underscore(key)

def convert_to_datetime(key, value):
    if key == 'created_at' or key == 'updated_at':
        value = parse(value)
    return value

def convert_camel_case_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

xml = scraperwiki.scrape(STANDARDS_URL)
standards_xml = etree.XML(xml)

try:
    last_update_at = parse(scraperwiki.sqlite.select("MAX(updated_at) AS last_updated_at FROM standards")[0]['last_updated_at'])
except:
    last_update_at = datetime.datetime.fromtimestamp(0)

if last_update_at < parse(standards_xml.get('upstamp')):
    scraperwiki.sqlite.save(['updated_at'], normalize_element_keys(standards_xml.attrib), table_name='standards')

    site_standards = []
    for site in standards_xml.findall('site'):
        site_standards.append({
            'mmsd_id': site.get('MMSD_ID'),
            'conductivity_low': site.find('conductivity').get('low'),
            'conductivity_high': site.find('conductivity').get('high'),
            'dissolved_oxygen_low': site.find('dissolvedOxygen').get('low'),
            'dissolved_oxygen_high': site.find('dissolvedOxygen').get('high'),
            'turbidity_low': site.find('turbidity').get('low'),
            'turbidity_high': site.find('turbidity').get('high'),
            'stage_active': site.find('stage').get('active'),
            'stage_flood': site.find('stage').get('flood'),
            'stage_moderate': site.find('stage').get('moderate'),
            'stage_major': site.find('stage').get('major'),
            'water_temperature_low': site.find('waterTemperature').get('low'), #missing?
            'water_temperature_high': site.find('waterTemperature').get('high')
        })
    scraperwiki.sqlite.save(['mmsd_id'], site_standards, table_name='site_standards')

xml = scraperwiki.scrape(WATER_QUALITY_URL)
water_quality_xml = etree.XML(xml)

try:
    last_update_at = parse(scraperwiki.sqlite.select("MAX(updated_at) AS last_updated_at FROM water_qualities")[0]['last_updated_at'])
except:
    last_update_at = datetime.datetime.fromtimestamp(0)

if last_update_at < parse(water_quality_xml.get('upstamp')):
    scraperwiki.sqlite.save(['updated_at'], normalize_element_keys(water_quality_xml.attrib), table_name='water_qualities')

    for site in water_quality_xml.findall('site'):
        site_data = normalize_element_keys(site.attrib)
        scraperwiki.sqlite.save(['mmsd_id'], site_data, table_name='water_quality_sites')
        mmsd_id = site_data['mmsd_id']
        for dailyUpdate in site.findall('dailyUpdate'):
            row = dict(normalize_element_keys(dailyUpdate.attrib).items() + {'mmsd_id': mmsd_id}.items())
            scraperwiki.sqlite.save(['created_at', 'mmsd_id'], row, table_name='water_quality_readings')
            data = []
            for hourlyUpdate in dailyUpdate.findall('hourlyUpdate'):
                #hourlyUpdate is just the average of quarterly update, so we don't need it since we pull in quarterlyUpdate
                for quarterlyUpdate in hourlyUpdate.findall('quarterlyUpdate'):
                    #quarterly refers to the 00 15 30 45 times of the hour
                    row = dict(normalize_element_keys(quarterlyUpdate.attrib).items() + {'mmsd_id': mmsd_id}.items())
                    data.append(row)
            scraperwiki.sqlite.save(['created_at', 'mmsd_id'], data, table_name='water_quality_readings')