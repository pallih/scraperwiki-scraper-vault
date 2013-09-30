# Extracts the non-copyright material from the NZ Historic Places Register
# TODO
#    bios http://www.historic.org.nz/corporate/registersearch/ProfessionalBio/Professional.aspx?ID=43


import os
import sys
from datetime import datetime
#from multiprocessing import Pool, Process, JoinableQueue
from threading import Thread
from urlparse import urlsplit

from dateutil import parser as dateparser
from scraperwiki import sqlite as store
from scrapemark import scrape


def finddate(datestr):
    default = datetime(year=1, month=1, day=1, hour=0, minute=0)
    return str(dateparser.parse(datestr, default=default))

def threading_is_okay():
    try:
        print 'module name:', __name__
        print 'parent process:', os.getppid()
        print 'process id:', os.getpid()
    except Exception, e:
        print 'UNTHREADED'
        return False
    return True

BASICS ="""
<div class="pageTitle">
    <h1>{{ title }}</h1>
   {* <span>{{ subtitle }}</span> *}
</div>

<h2>{{ address }}</h2>

<div class="sListingImages">
    {*            
    <tr>
        <td>
            <a href="{{ [images].large_link|abs }}"  title='::{{ [images].title }}' >
            </a>
            <div style="ImageCaption">{{ [images].caption }} </div>          
        </td>
    </tr>
     *}
</div>

<div class="dsListingDetails">{{ details|html }}</div>
"""

def extract_register_id(details):
    pattern = """<h6>Register Number</h6>{{ register_id|int }}"""
    return 'register_number', scrape(pattern, html=details)['register_id']

def extract_registration_type(details):
    pattern = """<h6>Registration Type</h6>{{ register_type }}
                <span>{{ register_category }}</span>    
    """
    return 'registration_details', scrape(pattern, html=details)

def extract_region(details):
    pattern= "<h6>Region</h6>{{  }}"
    return 'region', scrape(pattern, html=details)

def extract_date_registered(details):
    pattern = "<h6>Date Registered</h6>{{  }}"
    return 'date_registered', scrape(pattern, html=details)

def extract_councils(details):
    pattern = "<h6>City/District Council</h6>{* <li> {{ [councils] }} </li> *}"
    return 'councils', scrape(pattern, details)['councils']

def extract_legal_desc(details):
    pattern = "<h6>Legal Description</h6>{{ }}"
    return 'legal_description', scrape(pattern, html=details)

def extract_other_names(details):
    pattern = "<h6>Other Names</h6>{* <li>{{ [other_names] }}</li> *}"
    return 'other_names', scrape(pattern, html=details)['other_names']


def extract_status_explaination(details):
    pattern = """<h6>Status Explanation</h6>{{ }}"""
    return 'status_explanation', scrape(pattern, html=details)

def extract_current_uses(details):
    pattern = """<h6>Current Use</h6>{* <li>{{ [current_uses] }}</li> *}
    """
    return 'current_uses', scrape(pattern, html=details)['current_uses']

def extract_construction_dates(details):
    pattern = "<h6>Construction Dates</h6> {* <li>{{ [cdates].desc }}:{{ [cdates].dates }}</li> *}"
    return 'cdates', scrape(pattern, html=details)['cdates']

def extract_construction_profs(details):
    blanket = "<h6>Construction Professionals</h6>{{ pros|html }}"""
    targetted = """<h6>Construction Professionals</h6>{* <a href="javascript:viewBio('{{ [pros.id] }}');">{{ [pros].name }} </a> *}"""
    pros = scrape(targetted, html=details)['pros']
    if not pros:
        pros = scrape(blanket, html=details)['pros']
    return 'pros', pros

def extract_construction_details(details):
    pattern = "<h6>Construction Details</h6>{{ }}" 
    return 'construction_details', scrape(pattern, details)

def extract_gps_references(details):
    pattern = "<h6>GPS References</h6>{* <li>Easting:{{ [gps_references].x|int }}, Northing:{{ [gps_references].y|int }}</li> *}"
    return 'gps', scrape(pattern, html=details)['gps_references']

def extract_aasn(details):
    pattern = "<h6>NZ Archaeological Association Site Number</h6>{* <li>P05/True Easting:{{ [aasn].x|int}}, Northing: {{ [aasn].y|int}}</li> *}"
    return 'aasn', scrape(pattern, html=details)['aasn']

def extract_other_info(details):
    pattern = "<h6>Other Information</h6>{{ }}"
    return 'other_information', scrape(pattern, html=details)

def extract_entry_by(details):
    pattern ="<h6>Entry Written By </h6>{{ }}"
    return 'written_by', scrape(pattern, html=details)

def extract_entry_date(details):
    pattern = "<h6>Entry Date</h6>{{ }}"
    return 'entry_date', scrape(pattern, html=details)

def extract_info_sources(details):
    pattern = "{* <li>{{ [info_sources] }}</li> *}"
    return 'info_sources', scrape(pattern, html=details)['info_sources']

def extract_doc_managed(details):
    pattern = "<h6>DOC Managed</h6>{{ }}"
    return 'doc_managed', scrape(pattern, html=details)

def extract_associated_listings(details):
    pattern = """
    {* <A HREF='/TheRegister/RegisterSearch/RegisterResults.aspx?RID={{ [associated].assoc_id|int }}'>{{ [associated].title }}</A> *}
    """
    return 'associated', scrape(pattern, html=details)['associated']

def extract_former_uses(details):
    pattern = "<h6>Former</h6>{* <li>{{ [former_uses] }}</li> *} </div>"
    return 'former_uses', scrape(pattern, html=details)['former_uses']

def extract_s23_assessment(details):
    pattern = "<h6>Further Assessment under Section 23</h6>{{ }}"
    return 's23_assessment', scrape(pattern, html=details)

def extract_links(details):
    pattern = """{* <a href="{{ [links].href|abs }}">{{ [links].title }}</a> *}"""
    return 'links', scrape(pattern, html=details)['links']

def extract_notable_features(details):
    pattern = '<h6>Notable Features</h6>{{ }}'
    return 'notable_features', scrape(pattern, html=details)

def extract_location_description(details):
    pattern = '<h6>Location Description</h6>{{ }}'
    return 'location_description', scrape(pattern, html=details)

def extract_heritage_covenant(details):
    pattern = '<h6>Heritage</h6>{{ }}'
    return 'heritage_covenant', scrape(pattern, html=details)

def extract_area_description(details):
    pattern = '<h6></h6>{{ }}'
    return 'area_description', scrape(pattern, html=details)

FIND_SECTION_PATTERN = """
{* <div id="ctl12_ctl02_PropertyRPT_ctl00_tr{{ [sections].key }}">{{ [sections].contents|html }}</div> *}

"""
test_refs = [3267, 3268, 2, 232, 5200, 12, 45, 6998] #3267 doesn't exist
test_urls = ["http://www.historic.org.nz/TheRegister/RegisterSearch/RegisterResults.aspx?RID=%s&m=advanced" % ref for ref in test_refs]

extract = {
u'AssociatedListings': extract_associated_listings,
u'RegisterID': extract_register_id, 
u'RegistrationType': extract_registration_type,
u'Region': extract_region,
u'DateRegistered': extract_date_registered,
u'Council': extract_councils,
u'LocationDescription': extract_location_description,
u'LegalDescription': extract_legal_desc,
u'OtherNames': extract_other_names,
u'StatusExplanation': extract_status_explaination,
u'BriefDescription': lambda x: ('brief_description', None),
u'CurrentUse': extract_current_uses,
u'Former': extract_former_uses,
u'ConstructionDates': extract_construction_dates, 
u'ConstructionProfessional': extract_construction_profs,
u'PhysicalDescription': lambda x: ('physical_description', None),
u'ConstructionDetails': extract_construction_details,
u'CulturalSignificance':  lambda x: ('cultural_significance', None),
u'HistoricalNarrative': lambda x: ('historical_narrative', None),
u'HistoricalSignificance': lambda x: ('historical_significance', None), 
u'PhysicalSignificance': lambda x: ('pyhsical_significance', None), 
u'DetailSection23': lambda x: ('detail_section_23', None), 
u'OtherInformation': extract_other_info, 
u'EntryBy': extract_entry_by, 
u'EntryDate': extract_entry_date, 
u'InformationSources': extract_info_sources,
u'Links': extract_links,
u'NotableFeatures': extract_notable_features,
u'GPSReferences': extract_gps_references,
u'rsNZMS260': extract_aasn,
u'HeritageCovenant': extract_heritage_covenant,
u'AreaDescription': extract_area_description
}

available_keys = set(extract.keys())

def extract_sections(html):
    return scrape(FIND_SECTION_PATTERN, html=html)['sections']

def extract_basics(url):
    return scrape(BASICS, url=url)

def do_place(ref):
    url = "http://www.historic.org.nz/TheRegister/RegisterSearch/RegisterResults.aspx?RID=%d&m=advanced" % ref    
    basics = extract_basics(url)
    if not basics:
        print >>sys.stderr, "Skipping: %d doesn't exist" % ref
        store.save(['place_id'],
                    data=dict(place_id=ref, exists=0, accessed_at=str(datetime.now())), 
                    table_name='_places_accessed')
    else:
        print 'Processing: ', ref
        place = {}
        place['place_id'] = ref
        place['images'] = '|'.join(img['large_link'] for img in basics['images'])
        place['title'] = basics['title']
        place['subtitle'] = basics['subtitle']
        place['address'] = basics['address']

        for image in basics['images']:
            details = [d.strip() for d in image['caption'].split('. ')]
            for d in details :
                if d.startswith('Copyright'): 
                    image['copyright'] = d.strip('Copyright ')
                elif d.startswith('Photographed by'):
                    image['photographer'] = d.strip('Photographed by ')
                    taken_at = ''
                    try:
                        orig = d.split()[-1][:-1]
                        taken_at = finddate(orig)
                    except ValueError, e:
                        print 'DEBUG: %s: Could not parse date of photo : %s (%s)' % (ref, d, e)
                        pass
                    if taken_at:
                        store.save(['place_id','dates'],
                            data=dict(place_id=ref, dates=taken_at, date_orig=orig, description=details[0], type='photo_taken'),
                            table_name='events')
                        image['taken_at'] = taken_at
                elif d.startswith('From'):
                    image['source'] = d.strip('From: ')[:1]
                    store.save(['link', 'place_id'], data=dict(place_id=ref, link=image['source'], domain=urlsplit(image['source'])[1], title=details[0]), table_name='links')

                    
            image['place_id'] = ref
            
        store.save(['place_id', 'large_link'], data=basics['images'], table_name='images') 

        sections = extract_sections(basics['details'])
        for s in sections:
            try:
                res = extract[s['key']](s['contents'])
                place[res[0]] = res[1]
            except KeyError:
                troublemaker = s['key']
                if troublemaker.endswith('b') or troublemaker.endswith('2') or u'Linksbr' in troublemaker:
                    pass
                else:
                    print >>sys.stderr, "TODO: %s: %s is not being handled properly." % (ref, s['key'])
            except IndexError, e:
                print "Response: ", res
                print e
                raise

        if 'associated' in place:
            for assoc in place['associated']:
                store.save(['place_id','assoc_id'], data=dict(place_id=ref, assoc_id=assoc['assoc_id']), table_name='associated_places')
            place['associated_ids'] = '|'.join(p['assoc_id'] for p in place['associated'])
            place['associated_titles'] = '|'.join(p['assoc_title'] for p in place['associated'])
            del place['associated']

        if 'cdates' in place:
            cdates = place['cdates']
            for date in cdates:
                date['approx'] = 0
                dates = []
                for datestr in date['dates'].split():
                    if datestr.isdigit():
                        dates.append(finddate(datestr))
                    elif 'c' in datestr.lower():
                        date['approx'] = 1
                if len(dates) > 1:
                    store.save(['place_id','dates'],
                            data=dict(place_id=ref, dates=dates[0], date_range_start=dates[0], date_range_end=dates[1], is_range=1, description=date['desc'], type='construction', date_orig=date['dates'], approx=date['approx']),
                            table_name='events')
                else:
                    store.save(['place_id','dates'], data=dict(place_id=ref, dates=' '.join(dates), date_orig=date['dates'], description=date['desc'], type='construction'), table_name='events')
            place['construction_dates'] = '|'.join('%s:%s' % (d['desc'], d['dates']) for d in cdates)
            del place['cdates']

        if 'councils' in place:
            place['councils'] = '|'.join(place['councils'])

        if 'current_uses' in place:
            uses = place['current_uses']
            for use in uses:
                store.save(['place_id', 'use'], data=dict(place_id=ref, use=use, type='current'), table_name='uses')
            place['current_uses'] = u'|'.join(uses)

        if 'links' in place:
            links = place['links']
            for l in links:
                link = dict(
                    place_id=ref,
                    link = l['href'],
                    domain = urlsplit(l['href'])[1],
                    title = l['title'])
                store.save(['link', 'place_id'], data=link, table_name='links')
            place['links'] = '|'.join(l['href'] for l in links)

        if 'info_sources' in place:
            sources = place['info_sources']
            for source in sources:
                store.save(['place_id', 'source'], data=dict(place_id=ref, source=source, author_last_name=source.split(',')[0]), table_name='sources')
                orig=[d for d in source.replace(',',' ').split() if d.isdigit()]
                if orig:
                    try:
                        dates = finddate(orig[-1])
                        store.save(['place_id','dates'], data=dict(place_id=ref, dates=dates, date_orig=orig, description=source, type='publication_written'),
                            table_name='events')
                    except ValueError:
                        print >>sys.stderr, 'DEBUG : %d : Cant parse string as date (%s)' % (ref, orig)
            place['info_sources'] = u'|'.join(sources)

        if 'former_uses' in place:
            uses = place['former_uses']
            for use in uses:
                store.save(['place_id', 'use'], data=dict(place_id=ref, use=use, type='former'), table_name='uses')
            place['former_uses'] = u'|'.join(uses)

        locations = []
        if 'gps' in place:
            for coords in place['gps']:
                locations.append(dict(place_id=ref, x=coords['x'], y=coords['y'], type='gps'))

        if 'aasn' in place:
            for coords in place['aasn']:
                locations.append(dict(place_id=ref, x=coords['x'], y=coords['y'], type='aasn'))
        
        if locations:
            place['locations'] = '|'.join('%s,%s' % (l['x'], l['y']) for l in locations)
            for l in locations:
                l['map_series'] = 'NZMS 260'
                l['gps_proj'] = "NZMG (EPSG:27200)"
            store.save(['place_id', 'x', 'y', 'type'], data=locations, table_name='locations')

        if 'other_names' in place:
            place['other_names'] = '|'.join(place['other_names'])

        if 'registration_details' in place and place['registration_details'] is not None:
            details = place['registration_details']
            place['registration_type'] = details['register_type']
            place['registration_category'] = details['register_category'].split()[-1]
            del place['registration_details']

        if 'pros' in place:
            pros = place['pros']
            if isinstance(pros, list):
                for pro in pros:
                    store.save(['prof_id', 'place_id'], data=dict(place_id=ref, prof_id=pro['id'], name=pro['name']), table_name='construction_professionals')
                place['construction_professionals_name'] = '|'.join(p['name'] for p in pros)
                place['construction_professionals_id'] = '|'.join(p['id'] for p in pros)
            else:
                store.save(['place_id'],
                            data=dict(place_id=ref, details=pros), 
                            table_name='construction_professionals_unsorted')
                place['construction_professionals_name'] = pros
        store.save(['place_id'], data=place, table_name='places')
        store.save(['place_id'], data=dict(place_id=ref, exists=1, accessed_at=str(datetime.now())), table_name='_places_accessed')
        print 'Done'


def main(mode="initial"):
    end = 10000 # seems like most recent from http://www.historic.org.nz/en/TheRegister/RecentReg.aspx
    if mode == "initial":
        accessed = [p['place_id'] for p in store.select("place_id FROM _places_accessed")]
        #start = max(accessed)        
        for ref in xrange(end):
            if ref not in accessed:
                print ref
                do_place(ref)

    elif mode == "crawl":
        start = 0
        for ref in xrange(start, end):
            do_place(ref)
main()
# Extracts the non-copyright material from the NZ Historic Places Register
# TODO
#    bios http://www.historic.org.nz/corporate/registersearch/ProfessionalBio/Professional.aspx?ID=43


import os
import sys
from datetime import datetime
#from multiprocessing import Pool, Process, JoinableQueue
from threading import Thread
from urlparse import urlsplit

from dateutil import parser as dateparser
from scraperwiki import sqlite as store
from scrapemark import scrape


def finddate(datestr):
    default = datetime(year=1, month=1, day=1, hour=0, minute=0)
    return str(dateparser.parse(datestr, default=default))

def threading_is_okay():
    try:
        print 'module name:', __name__
        print 'parent process:', os.getppid()
        print 'process id:', os.getpid()
    except Exception, e:
        print 'UNTHREADED'
        return False
    return True

BASICS ="""
<div class="pageTitle">
    <h1>{{ title }}</h1>
   {* <span>{{ subtitle }}</span> *}
</div>

<h2>{{ address }}</h2>

<div class="sListingImages">
    {*            
    <tr>
        <td>
            <a href="{{ [images].large_link|abs }}"  title='::{{ [images].title }}' >
            </a>
            <div style="ImageCaption">{{ [images].caption }} </div>          
        </td>
    </tr>
     *}
</div>

<div class="dsListingDetails">{{ details|html }}</div>
"""

def extract_register_id(details):
    pattern = """<h6>Register Number</h6>{{ register_id|int }}"""
    return 'register_number', scrape(pattern, html=details)['register_id']

def extract_registration_type(details):
    pattern = """<h6>Registration Type</h6>{{ register_type }}
                <span>{{ register_category }}</span>    
    """
    return 'registration_details', scrape(pattern, html=details)

def extract_region(details):
    pattern= "<h6>Region</h6>{{  }}"
    return 'region', scrape(pattern, html=details)

def extract_date_registered(details):
    pattern = "<h6>Date Registered</h6>{{  }}"
    return 'date_registered', scrape(pattern, html=details)

def extract_councils(details):
    pattern = "<h6>City/District Council</h6>{* <li> {{ [councils] }} </li> *}"
    return 'councils', scrape(pattern, details)['councils']

def extract_legal_desc(details):
    pattern = "<h6>Legal Description</h6>{{ }}"
    return 'legal_description', scrape(pattern, html=details)

def extract_other_names(details):
    pattern = "<h6>Other Names</h6>{* <li>{{ [other_names] }}</li> *}"
    return 'other_names', scrape(pattern, html=details)['other_names']


def extract_status_explaination(details):
    pattern = """<h6>Status Explanation</h6>{{ }}"""
    return 'status_explanation', scrape(pattern, html=details)

def extract_current_uses(details):
    pattern = """<h6>Current Use</h6>{* <li>{{ [current_uses] }}</li> *}
    """
    return 'current_uses', scrape(pattern, html=details)['current_uses']

def extract_construction_dates(details):
    pattern = "<h6>Construction Dates</h6> {* <li>{{ [cdates].desc }}:{{ [cdates].dates }}</li> *}"
    return 'cdates', scrape(pattern, html=details)['cdates']

def extract_construction_profs(details):
    blanket = "<h6>Construction Professionals</h6>{{ pros|html }}"""
    targetted = """<h6>Construction Professionals</h6>{* <a href="javascript:viewBio('{{ [pros.id] }}');">{{ [pros].name }} </a> *}"""
    pros = scrape(targetted, html=details)['pros']
    if not pros:
        pros = scrape(blanket, html=details)['pros']
    return 'pros', pros

def extract_construction_details(details):
    pattern = "<h6>Construction Details</h6>{{ }}" 
    return 'construction_details', scrape(pattern, details)

def extract_gps_references(details):
    pattern = "<h6>GPS References</h6>{* <li>Easting:{{ [gps_references].x|int }}, Northing:{{ [gps_references].y|int }}</li> *}"
    return 'gps', scrape(pattern, html=details)['gps_references']

def extract_aasn(details):
    pattern = "<h6>NZ Archaeological Association Site Number</h6>{* <li>P05/True Easting:{{ [aasn].x|int}}, Northing: {{ [aasn].y|int}}</li> *}"
    return 'aasn', scrape(pattern, html=details)['aasn']

def extract_other_info(details):
    pattern = "<h6>Other Information</h6>{{ }}"
    return 'other_information', scrape(pattern, html=details)

def extract_entry_by(details):
    pattern ="<h6>Entry Written By </h6>{{ }}"
    return 'written_by', scrape(pattern, html=details)

def extract_entry_date(details):
    pattern = "<h6>Entry Date</h6>{{ }}"
    return 'entry_date', scrape(pattern, html=details)

def extract_info_sources(details):
    pattern = "{* <li>{{ [info_sources] }}</li> *}"
    return 'info_sources', scrape(pattern, html=details)['info_sources']

def extract_doc_managed(details):
    pattern = "<h6>DOC Managed</h6>{{ }}"
    return 'doc_managed', scrape(pattern, html=details)

def extract_associated_listings(details):
    pattern = """
    {* <A HREF='/TheRegister/RegisterSearch/RegisterResults.aspx?RID={{ [associated].assoc_id|int }}'>{{ [associated].title }}</A> *}
    """
    return 'associated', scrape(pattern, html=details)['associated']

def extract_former_uses(details):
    pattern = "<h6>Former</h6>{* <li>{{ [former_uses] }}</li> *} </div>"
    return 'former_uses', scrape(pattern, html=details)['former_uses']

def extract_s23_assessment(details):
    pattern = "<h6>Further Assessment under Section 23</h6>{{ }}"
    return 's23_assessment', scrape(pattern, html=details)

def extract_links(details):
    pattern = """{* <a href="{{ [links].href|abs }}">{{ [links].title }}</a> *}"""
    return 'links', scrape(pattern, html=details)['links']

def extract_notable_features(details):
    pattern = '<h6>Notable Features</h6>{{ }}'
    return 'notable_features', scrape(pattern, html=details)

def extract_location_description(details):
    pattern = '<h6>Location Description</h6>{{ }}'
    return 'location_description', scrape(pattern, html=details)

def extract_heritage_covenant(details):
    pattern = '<h6>Heritage</h6>{{ }}'
    return 'heritage_covenant', scrape(pattern, html=details)

def extract_area_description(details):
    pattern = '<h6></h6>{{ }}'
    return 'area_description', scrape(pattern, html=details)

FIND_SECTION_PATTERN = """
{* <div id="ctl12_ctl02_PropertyRPT_ctl00_tr{{ [sections].key }}">{{ [sections].contents|html }}</div> *}

"""
test_refs = [3267, 3268, 2, 232, 5200, 12, 45, 6998] #3267 doesn't exist
test_urls = ["http://www.historic.org.nz/TheRegister/RegisterSearch/RegisterResults.aspx?RID=%s&m=advanced" % ref for ref in test_refs]

extract = {
u'AssociatedListings': extract_associated_listings,
u'RegisterID': extract_register_id, 
u'RegistrationType': extract_registration_type,
u'Region': extract_region,
u'DateRegistered': extract_date_registered,
u'Council': extract_councils,
u'LocationDescription': extract_location_description,
u'LegalDescription': extract_legal_desc,
u'OtherNames': extract_other_names,
u'StatusExplanation': extract_status_explaination,
u'BriefDescription': lambda x: ('brief_description', None),
u'CurrentUse': extract_current_uses,
u'Former': extract_former_uses,
u'ConstructionDates': extract_construction_dates, 
u'ConstructionProfessional': extract_construction_profs,
u'PhysicalDescription': lambda x: ('physical_description', None),
u'ConstructionDetails': extract_construction_details,
u'CulturalSignificance':  lambda x: ('cultural_significance', None),
u'HistoricalNarrative': lambda x: ('historical_narrative', None),
u'HistoricalSignificance': lambda x: ('historical_significance', None), 
u'PhysicalSignificance': lambda x: ('pyhsical_significance', None), 
u'DetailSection23': lambda x: ('detail_section_23', None), 
u'OtherInformation': extract_other_info, 
u'EntryBy': extract_entry_by, 
u'EntryDate': extract_entry_date, 
u'InformationSources': extract_info_sources,
u'Links': extract_links,
u'NotableFeatures': extract_notable_features,
u'GPSReferences': extract_gps_references,
u'rsNZMS260': extract_aasn,
u'HeritageCovenant': extract_heritage_covenant,
u'AreaDescription': extract_area_description
}

available_keys = set(extract.keys())

def extract_sections(html):
    return scrape(FIND_SECTION_PATTERN, html=html)['sections']

def extract_basics(url):
    return scrape(BASICS, url=url)

def do_place(ref):
    url = "http://www.historic.org.nz/TheRegister/RegisterSearch/RegisterResults.aspx?RID=%d&m=advanced" % ref    
    basics = extract_basics(url)
    if not basics:
        print >>sys.stderr, "Skipping: %d doesn't exist" % ref
        store.save(['place_id'],
                    data=dict(place_id=ref, exists=0, accessed_at=str(datetime.now())), 
                    table_name='_places_accessed')
    else:
        print 'Processing: ', ref
        place = {}
        place['place_id'] = ref
        place['images'] = '|'.join(img['large_link'] for img in basics['images'])
        place['title'] = basics['title']
        place['subtitle'] = basics['subtitle']
        place['address'] = basics['address']

        for image in basics['images']:
            details = [d.strip() for d in image['caption'].split('. ')]
            for d in details :
                if d.startswith('Copyright'): 
                    image['copyright'] = d.strip('Copyright ')
                elif d.startswith('Photographed by'):
                    image['photographer'] = d.strip('Photographed by ')
                    taken_at = ''
                    try:
                        orig = d.split()[-1][:-1]
                        taken_at = finddate(orig)
                    except ValueError, e:
                        print 'DEBUG: %s: Could not parse date of photo : %s (%s)' % (ref, d, e)
                        pass
                    if taken_at:
                        store.save(['place_id','dates'],
                            data=dict(place_id=ref, dates=taken_at, date_orig=orig, description=details[0], type='photo_taken'),
                            table_name='events')
                        image['taken_at'] = taken_at
                elif d.startswith('From'):
                    image['source'] = d.strip('From: ')[:1]
                    store.save(['link', 'place_id'], data=dict(place_id=ref, link=image['source'], domain=urlsplit(image['source'])[1], title=details[0]), table_name='links')

                    
            image['place_id'] = ref
            
        store.save(['place_id', 'large_link'], data=basics['images'], table_name='images') 

        sections = extract_sections(basics['details'])
        for s in sections:
            try:
                res = extract[s['key']](s['contents'])
                place[res[0]] = res[1]
            except KeyError:
                troublemaker = s['key']
                if troublemaker.endswith('b') or troublemaker.endswith('2') or u'Linksbr' in troublemaker:
                    pass
                else:
                    print >>sys.stderr, "TODO: %s: %s is not being handled properly." % (ref, s['key'])
            except IndexError, e:
                print "Response: ", res
                print e
                raise

        if 'associated' in place:
            for assoc in place['associated']:
                store.save(['place_id','assoc_id'], data=dict(place_id=ref, assoc_id=assoc['assoc_id']), table_name='associated_places')
            place['associated_ids'] = '|'.join(p['assoc_id'] for p in place['associated'])
            place['associated_titles'] = '|'.join(p['assoc_title'] for p in place['associated'])
            del place['associated']

        if 'cdates' in place:
            cdates = place['cdates']
            for date in cdates:
                date['approx'] = 0
                dates = []
                for datestr in date['dates'].split():
                    if datestr.isdigit():
                        dates.append(finddate(datestr))
                    elif 'c' in datestr.lower():
                        date['approx'] = 1
                if len(dates) > 1:
                    store.save(['place_id','dates'],
                            data=dict(place_id=ref, dates=dates[0], date_range_start=dates[0], date_range_end=dates[1], is_range=1, description=date['desc'], type='construction', date_orig=date['dates'], approx=date['approx']),
                            table_name='events')
                else:
                    store.save(['place_id','dates'], data=dict(place_id=ref, dates=' '.join(dates), date_orig=date['dates'], description=date['desc'], type='construction'), table_name='events')
            place['construction_dates'] = '|'.join('%s:%s' % (d['desc'], d['dates']) for d in cdates)
            del place['cdates']

        if 'councils' in place:
            place['councils'] = '|'.join(place['councils'])

        if 'current_uses' in place:
            uses = place['current_uses']
            for use in uses:
                store.save(['place_id', 'use'], data=dict(place_id=ref, use=use, type='current'), table_name='uses')
            place['current_uses'] = u'|'.join(uses)

        if 'links' in place:
            links = place['links']
            for l in links:
                link = dict(
                    place_id=ref,
                    link = l['href'],
                    domain = urlsplit(l['href'])[1],
                    title = l['title'])
                store.save(['link', 'place_id'], data=link, table_name='links')
            place['links'] = '|'.join(l['href'] for l in links)

        if 'info_sources' in place:
            sources = place['info_sources']
            for source in sources:
                store.save(['place_id', 'source'], data=dict(place_id=ref, source=source, author_last_name=source.split(',')[0]), table_name='sources')
                orig=[d for d in source.replace(',',' ').split() if d.isdigit()]
                if orig:
                    try:
                        dates = finddate(orig[-1])
                        store.save(['place_id','dates'], data=dict(place_id=ref, dates=dates, date_orig=orig, description=source, type='publication_written'),
                            table_name='events')
                    except ValueError:
                        print >>sys.stderr, 'DEBUG : %d : Cant parse string as date (%s)' % (ref, orig)
            place['info_sources'] = u'|'.join(sources)

        if 'former_uses' in place:
            uses = place['former_uses']
            for use in uses:
                store.save(['place_id', 'use'], data=dict(place_id=ref, use=use, type='former'), table_name='uses')
            place['former_uses'] = u'|'.join(uses)

        locations = []
        if 'gps' in place:
            for coords in place['gps']:
                locations.append(dict(place_id=ref, x=coords['x'], y=coords['y'], type='gps'))

        if 'aasn' in place:
            for coords in place['aasn']:
                locations.append(dict(place_id=ref, x=coords['x'], y=coords['y'], type='aasn'))
        
        if locations:
            place['locations'] = '|'.join('%s,%s' % (l['x'], l['y']) for l in locations)
            for l in locations:
                l['map_series'] = 'NZMS 260'
                l['gps_proj'] = "NZMG (EPSG:27200)"
            store.save(['place_id', 'x', 'y', 'type'], data=locations, table_name='locations')

        if 'other_names' in place:
            place['other_names'] = '|'.join(place['other_names'])

        if 'registration_details' in place and place['registration_details'] is not None:
            details = place['registration_details']
            place['registration_type'] = details['register_type']
            place['registration_category'] = details['register_category'].split()[-1]
            del place['registration_details']

        if 'pros' in place:
            pros = place['pros']
            if isinstance(pros, list):
                for pro in pros:
                    store.save(['prof_id', 'place_id'], data=dict(place_id=ref, prof_id=pro['id'], name=pro['name']), table_name='construction_professionals')
                place['construction_professionals_name'] = '|'.join(p['name'] for p in pros)
                place['construction_professionals_id'] = '|'.join(p['id'] for p in pros)
            else:
                store.save(['place_id'],
                            data=dict(place_id=ref, details=pros), 
                            table_name='construction_professionals_unsorted')
                place['construction_professionals_name'] = pros
        store.save(['place_id'], data=place, table_name='places')
        store.save(['place_id'], data=dict(place_id=ref, exists=1, accessed_at=str(datetime.now())), table_name='_places_accessed')
        print 'Done'


def main(mode="initial"):
    end = 10000 # seems like most recent from http://www.historic.org.nz/en/TheRegister/RecentReg.aspx
    if mode == "initial":
        accessed = [p['place_id'] for p in store.select("place_id FROM _places_accessed")]
        #start = max(accessed)        
        for ref in xrange(end):
            if ref not in accessed:
                print ref
                do_place(ref)

    elif mode == "crawl":
        start = 0
        for ref in xrange(start, end):
            do_place(ref)
main()
