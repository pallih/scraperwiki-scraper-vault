import scraperwiki
from scrapemark import scrape
from urllib2 import HTTPError

URL = "http://www.geonet.org.nz/earthquake/quakes/recent_quakes.html"
RECENT_QUAKES_PATTERN = """
{*

<li>
    <ul>
        <li class="one">
        <a class="icn-lgmmi" href="{{ [quakes].google_maps_felt_reports_url }}"></a>
        <a class="icn-lgmap" href="{{ [quakes].google_maps_location_url }}"></a>
        <a class="icn-l" href="{{ [quakes].shaking_map_url }}"></a>
        <a class="icn-c" href="{{ [quakes].add_felt_report_url }}"></a>
        <a class="icn-r" href="{{ [quakes].maps_url }}"><img src="{{ [quakes].img_of_quake_location_url }}"/></a>
        </li>
        <li><strong>Reference Number:</strong>{{ [quakes].geonet_ref }}</li>
        <li><strong>NZST:</strong>{{ [quakes].time }}</li>
        <li><strong>Magnitude:</strong> {{ [quakes].magnitude }}</li>
        <li><strong>Depth:</strong>{{ [quakes].depth }}</li>
        <li><strong>Details:</strong> <a href="{{ [quakes].url }}">{{ [quakes].location }}</a></li>
    </ul>
</li>

*}

"""

FELT_REPORTS_PATTERN = """
{* 
    <Placemark>
        <name></name>
        <styleUrl></styleUrl>
        <description>
            <table>
                <tr><th>Intensity (MMI)</th><td><a>MM{{ [felt_reports].mmi }}</a></td></tr>
                <tr><th>Location</th><td>{{ [felt_reports].nearest_place }}</td></tr>
                <tr><th>Reported Date</th><td>{{ [felt_reports].reported_date }}</td></tr>
            </table>
        </description>
        <Point>
            <coordinates>{{ [felt_reports].lat }},{{ [felt_reports].long }}</coordinates>
        </Point>
    </Placemark>
*}
"""

QUAKE_KML_PATTERN = """
<ExtendedData>
<Data name="ref"><displayName>Reference</displayName><value>{{ geonet_ref|int }}</value></Data>
<Data name="z"><displayName>Depth (km)</displayName><value>{{ depth|float }}</value></Data>
<Data name="mag"><displayName>Magnitude</displayName><value>{{ magnitude|float }}</value></Data>
<Data name="date"><displayName>Date (UTC)</displayName><value>{{ datetime }}</value></Data>
<Data name="kmlstations">
  <displayName>Stations</displayName>
  <value>Click &lt;a href="{{ stations_url }}"&gt;here&lt;/a&gt; for a list of seismic stations with confirmed picks for this event (KML).</value>
</Data>
</ExtendedData>
<Point>
<coordinates>{{ lat|float }},{{ long|float }}</coordinates>
"""

QUAKE_HTML_PATTERN = """
<div id="quake-info"> 
<table>
    <tr><th>Reference Number</th><td></td></tr>
    <tr><th>Universal Time</th><td>{{ time_utc_human }}</td></tr>
    <tr><th>NZ Standard Time</th><td>{{ time_nzst_human }}</td></tr>
    <tr><th>Latitude, Longitude</th><td>{{ lat_degrees }},{{ long_degrees }}</td></tr>
    <tr><th>Focal Depth</th><td>{{ depth|float }}</td></tr>
    <tr><th>Richter magnitude</th><td>{{ magnitude|float }}</td></tr>
    <tr><th>Region</th><td>{{ region }}</td></tr>
    <tr>
        <th>Location</th>
        <td>
            <ul>
                {* <li>{{ [locations] }}</li> *}
            </ul>
        </td>
    </tr>
</table>
</div>
"""

PIPERMAIL_INDEX_PATTERN = """
{*
<td>
  <A>[ Thread ]</a>
  <A>[ Subject ]</a>
  <A>[ Author ]</a>
  <A href="{{ [] }}">[ Date ]</a>
</td>
*}
"""

PIPERMAIL_MONTH_PATTERN = """
{* HREF="{{ [] }}" *}
"""

PIPERMAIL_MESSAGE_PATTERN ="""
<PRE>
    Reference number:{{ }}
    Universal Time:
</PRE>
"""


STATION_PATTERN = """
{*
<Placemark>
<NAME>{{ [stations].name }}</NAME>
    <styleUrl>#station</styleUrl>
    <ExtendedData>
        <Data name="evalmode">
            <value>{{ [stations].evalmode }}</value>
        </Data>
        <Data name="evalstatus">
            <value>{{ [stations].evalstatus }}</value>
        </Data>
        <Data name="time">
            <value>{{ [stations].datetime }} </value>
        </Data>
        <Data name="etl">
            <value>{{ [stations].lower_uncertainty|float }} </value>
        </Data>
        <Data name="etu">
            <value>{{ [stations].upper_uncertainty|float }}</value>
        </Data>
    </ExtendedData>
    <Point>
        <coordinates>{{ [stations].coordinates }}</coordinates>
    </Point>
</Placemark>

*}
"""

def fetch_quake_kml(ref):
    url = 'http://magma.geonet.org.nz/services/quake/kml/2.2/search?externalRef=%s' % ref
    print '   Fetching: ', url
    res = scrape(pattern=QUAKE_KML_PATTERN, url=url)
    print '   Done. (KML data)'
    return res

def fetch_quake_html(ref):
    url = "http://www.geonet.org.nz/earthquake/quakes/%sg.html" % ref
    print '   Fetching: ', url
    res = scrape(pattern=QUAKE_HTML_PATTERN, url=url)
    print '   Done. (HTML data)'
    return res

def fetch_quake_data(ref):
    quake = fetch_quake_kml(ref)
    try:
        for k, val in fetch_quake_html(ref).iteritems():
            try:
                quake[k] = val
            except TypeError:
                print 'ERROR processing : ', k, val  
                pass
    except AttributeError:
        pass
    except HTTPError:
        print "HTTP ERROR: Skipping"
        pass
    try:
        if 'locations' in quake:
            quake['locations'] = '\n'.join(quake['locations'])
    except TypeError:
        quake = {}
    return quake

def add_urls(quake):
    ref = quake['geonet_ref']
    quake['felt_reports_kml_url'] = 'http://magma.geonet.org.nz/services/quake/reports/kml/2.2?externalRef=%s&agency=g' % ref
    quake['location_map_url'] = "http://www.geonet.org.nz/images/earthquake/quakes/%sgm.png" % ref
    quake['isoseismal_map_url'] = "http://www.geonet.org.nz/images/earthquake/quakes/%sgi.png" % ref
    quake['seismicity_map_url'] = "http://www.geonet.org.nz/images/earthquake/quakes/%sgc.png" % ref
    return quake

def do_felt_reports(ref):
    url = 'http://magma.geonet.org.nz/services/quake/reports/kml/2.2?externalRef=%s&agency=g' % ref
    print 'Fetching felt reports:  ' + url
    reports = []
    try:
        reports = scrape(pattern=FELT_REPORTS_PATTERN, url=url)['felt_reports']
        print '   Done. (%s felt reports)' % len(reports)
    except HTTPError:
        print 'HTTP ERROR - skipping'
    for report in reports:
        report['geonet_ref'] = ref
        report['source_url'] = url
    return reports

def _do_felt_reports(parent_quake):
    return do_felt_reports(parent_quake['geonet_ref'])

def do_stations(ref):
    url = 'http://magma.geonet.org.nz/services/quake/stations/kml/2.2/ref/%s' % ref
    print 'Fetching station data:  ' + url
    stations = []
    try:
        stations = scrape(pattern=STATION_PATTERN, url=url)['stations']
        print '   Done. (%s stations)' % len(stations)
    except HTTPError:
        print 'HTTP ERROR - skipping'
    for station in stations:
        station['geonet_ref'] = int(ref)
        station['source_url'] = url
    return stations

def _do_stations(parent_quake):
    return do_stations(parent_quake['geonet_ref'])

def iter_recent_quakes():
    for quake in scrape(pattern=RECENT_QUAKES_PATTERN,url=URL)['quakes']:
        quake['url'] = 'http://www.geonet.org.nz' + quake['url']
        quake['shaking_map_url'] = 'http://www.geonet.org.nz' + quake['shaking_map_url']
        quake['maps_url'] = 'http://www.geonet.org.nz' + quake['maps_url']
        quake['img_of_quake_location_url'] = 'http://www.geonet.org.nz' + quake['img_of_quake_location_url']
        for k, val in fetch_quake_data(quake['geonet_ref']).iteritems():
            quake[k] = val
        yield quake


def iter_mailing_list_quake_refs():
    base = "http://lists.geonet.org.nz/pipermail/eqnews/"
    index_urls = scrape(PIPERMAIL_INDEX_PATTERN, url=base)
    index_urls.reverse()
    index_urls= index_urls[96:]  ### REMEMBER TO DELETE WHEN FIRST COMPELETE RUN WORKS
    print index_urls
    for month in index_urls:
        print month
        messages = scrape(PIPERMAIL_MONTH_PATTERN, url = base + month)
        messages = [base + month.replace('date.html', link) for link in messages if '0' in link]
        print messages
        for message in messages:
            yield scrape(PIPERMAIL_MESSAGE_PATTERN, url=message)

def process_child_data(quake):
    ref = quake['geonet_ref']
    felt_reports = do_felt_reports(ref)
    if felt_reports:
        scraperwiki.sqlite.save(['geonet_ref', 'lat', 'long', 'reported_date', 'nearest_place'], table_name="felt_reports", data=felt_reports)
    station_readings = do_stations(ref)
    if station_readings:
        scraperwiki.sqlite.save(['geonet_ref', 'name'], table_name="station_reports", data=station_readings)

def process_quake_data(quake):
    quake = add_urls(quake)
    scraperwiki.sqlite.save(['geonet_ref'], table_name="quakes", data=quake)

def main():
    quakes_done = scraperwiki.sqlite.select('geonet_ref FROM quakes')
    quakes_done = set([q['geonet_ref'] for q in quakes_done])

#    for quake in iter_recent_quakes():
#        print 'Processing:  %s' % quake['geonet_ref']
#        process_quake_data(quake)
#        process_child_data(quake)

    for ref in iter_mailing_list_quake_refs():
        print ref
        try:
            ref = int(ref.split('/')[0])
        except:
            print u'ERROR with %s' % ref
            continue
        if ref in quakes_done:
            print 'Skipping: %s (Already exists)' % ref
        else:
            print 'Processing: %s' % ref
            quake = fetch_quake_data(ref)
            quake['geonet_ref'] = ref
            process_quake_data(quake)
            process_child_data(quake)
            quakes_done.add(ref)

#main()

station_test_data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<kml xmlns:ns2="http://www.w3.org/2005/Atom" xmlns="http://www.opengis.net/kml/2.2" xmlns:ns3="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0">
<Document>
<name>Quake 3508353</name>
<description>Stations with confirmed picks used in earthquake location</description>
<LookAt>
<longitude>172</longitude>
<latitude>-41</latitude>
<range>2000000</range>
</LookAt>
<StyleMap id="station">
<Pair>
<key>normal</key>
<styleUrl>#inactive-station</styleUrl>
</Pair>
<Pair>
<key>highlight</key>
<styleUrl>#active-station</styleUrl>
</Pair>
</StyleMap>
<Style id="active-station">
<IconStyle>
<Icon>
<href>http://magma.geonet.org.nz/services/quake/images/triangle-red.png</href>
</Icon>
</IconStyle>
<LabelStyle>
<scale>1.0</scale>
</LabelStyle>
</Style>
<Style id="inactive-station">
<IconStyle>
<Icon>
<href>http://magma.geonet.org.nz/services/quake/images/triangle-red.png</href>
</Icon>
</IconStyle>
<LabelStyle>
<scale>0.0</scale>
</LabelStyle>
</Style>
<Folder>
<name>18 Operational Weak Motion Stations</name>
<description>Updated Fri May 06 11:24:33 UTC 2011</description>
<Placemark>
<name>CRLZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:49.917Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>LTZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:56.577Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>INZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:00.138Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>RPZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:59.099Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>WVZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:04.487Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>KHZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:08.038Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>FOZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:13.638Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>LBZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:12.238Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>THZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:12.863Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>ODZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:14.268Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>EAZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:25.348Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>JCZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:23.778Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>TUZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:29.948Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>DFHS-HNZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:44.525Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>OXZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:46.288Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>EYRS-HNZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:46.255Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>MQZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:51.238Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>MQZ-HHN-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:57.398Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>CRLZ-HHN-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:54.967Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>EYRS-BNZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:48.260Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
</Folder>
</Document>
</kml>"""

html_test_data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>GeoNet &ndash; New Zealand Earthquake Report - Jul 9 2007 at 0:48 am (NZST)</title>
<meta name="revised" content="2007-07-08T13:03:57"/>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<meta name="description" content="The GeoNet Project - Monitoring geological hazards in New Zealand" />
<meta name="keywords" content="Earthquake, New Zealand, NZ, GeoNet, tsunami, seismic, seismic drum, volcano, volcanic, eruption, hazard, new zealand, volcano cam, volcano cams, volcano camera, White Island, Mt Ruapehu, Wairakei" />
<meta name="generator" content="Plone - http://www.plone.org/" />

<script type="text/javascript" src="/js/dply-functions.js"></script>


<!-- the content cell -->
<div id="quake-info">
<div class="details-l">
<h2>Quake Details</h2>
<p>Information about this earthquake:</p>
<table summary="Table to display specific details pertaining to this earthquake like: Time, depth, magnitude etc.">
<tr valign="top">
<th>Reference Number</th>
<td>2763595/G</td>
</tr>
<tr valign="top">
<th>Universal Time</th>
<td>July 8 2007 at 12:48</td>
</tr>
<tr valign="top">
<th>NZ Standard Time</th>
<td>Monday, July 9 2007 at 0:48 am</td>
</tr>
<tr valign="top">
<th>Latitude, Longitude</th>
<td>40.34&deg;S, 176.58&deg;E</td>
</tr>
<tr valign="top">
<th>Focal Depth</th>
<td>20 km</td>
</tr>
<tr valign="top">
<th>Richter magnitude</th>
<td>4.3</td>
</tr>
<tr valign="top">
<th>Region</th>
<td>Hawke's Bay</td>
</tr>
<tr valign="top">
<th>Location</th>
<td>
<ul>

<li>10 km south-west of Porangahau</li>

<li>40 km south of Waipukurau</li>

<li>80 km south of Hastings</li>

<li>190 km north-east of Wellington</li>

</ul>
</td>
</tr>
</table>


<p>Probably felt in the Hawkes Bay.</p>

<p>Did you feel this earthquake? We would appreciate it if you could fill out a <a href="http://magma.geonet.org.nz/felt/app?service=external/Felt&amp;sp=S2763595&amp;sp=SG">GeoNet Felt Earthquake Report</a> and let us know of your experiences.</p>
</div>
<div class="details-r">
<!-- rider/disclaimer -->
<h2>Disclaimer</h2>

<ul>

<li>The GeoNet project is core funded by the Earthquake Commission (EQC) and is being designed, installed and operated by GNS Science on behalf of EQC and all New Zealanders.</li>

<li>GNS Science accepts no liability for any loss or damage, direct or indirect, resulting from the use of the information provided. GNS Science does not make any representation in respect of the information's accuracy, completeness or fitness for any particular purpose.</li>

<li>Earthquake information last modified: 2007 Jul 08 13:01 (UT).</li>
</ul>

</div>
</div>

<!-- end of the content cell -->
</div>

<div id="relatedItems"></div>
<div class="discussion"></div>
</div>
</div>
</div>

<!-- end of main content block -->
<!-- start of the left (by default at least) column -->
<!-- end of the left (by default at least) column -->

</div>

<!-- end of the main and left columns -->
<!-- start of right (by default at least) column -->
<!-- end of the right (by default at least) column -->
</div>
</div>
<!-- end column wrapper -->
<hr class="netscape4" />
<div id="portal-colophon">
</div>
<div id="portal-footer">
<a href="http://www.gns.cri.nz/" class="img-logo-l" title=" GNS Science"><img src="/images/logo-gns.gif" alt="GNS Science" /></a>
<a href="http://www.eqc.govt.nz/" class="img-logo-r" title=" Earthquake Commission"><img src="/images/logo-eqc.gif" alt="EQC (Earthquake Commission)" /></a>
<p>GeoNet is a collaboration between the Earthquake Commission<br /> and GNS Science.</p>
<p class="base">GeoNet content is &copy; by <a href="http://www.gns.cri.nz/">GNS Science</a> | Powered by <a href="http://www.plone.org/">Plone CMS</a> | <a href="/about/">about</a> | <a href="/contact.html">contact</a> | <a href="/privacy.html">privacy</a> | <a href="/disclaimer.html">disclaimer</a></p>
</div>
</body>
</html>"""

def test_stations():
    res = scrape(STATION_PATTERN, html=station_test_data)
    assert 'stations' in res
    assert res['stations']


def test_html():
    res = scrape(QUAKE_HTML_PATTERN, html=html_test_data)
    print res
    for k, v in res.iteritems():
        print k, v

main()import scraperwiki
from scrapemark import scrape
from urllib2 import HTTPError

URL = "http://www.geonet.org.nz/earthquake/quakes/recent_quakes.html"
RECENT_QUAKES_PATTERN = """
{*

<li>
    <ul>
        <li class="one">
        <a class="icn-lgmmi" href="{{ [quakes].google_maps_felt_reports_url }}"></a>
        <a class="icn-lgmap" href="{{ [quakes].google_maps_location_url }}"></a>
        <a class="icn-l" href="{{ [quakes].shaking_map_url }}"></a>
        <a class="icn-c" href="{{ [quakes].add_felt_report_url }}"></a>
        <a class="icn-r" href="{{ [quakes].maps_url }}"><img src="{{ [quakes].img_of_quake_location_url }}"/></a>
        </li>
        <li><strong>Reference Number:</strong>{{ [quakes].geonet_ref }}</li>
        <li><strong>NZST:</strong>{{ [quakes].time }}</li>
        <li><strong>Magnitude:</strong> {{ [quakes].magnitude }}</li>
        <li><strong>Depth:</strong>{{ [quakes].depth }}</li>
        <li><strong>Details:</strong> <a href="{{ [quakes].url }}">{{ [quakes].location }}</a></li>
    </ul>
</li>

*}

"""

FELT_REPORTS_PATTERN = """
{* 
    <Placemark>
        <name></name>
        <styleUrl></styleUrl>
        <description>
            <table>
                <tr><th>Intensity (MMI)</th><td><a>MM{{ [felt_reports].mmi }}</a></td></tr>
                <tr><th>Location</th><td>{{ [felt_reports].nearest_place }}</td></tr>
                <tr><th>Reported Date</th><td>{{ [felt_reports].reported_date }}</td></tr>
            </table>
        </description>
        <Point>
            <coordinates>{{ [felt_reports].lat }},{{ [felt_reports].long }}</coordinates>
        </Point>
    </Placemark>
*}
"""

QUAKE_KML_PATTERN = """
<ExtendedData>
<Data name="ref"><displayName>Reference</displayName><value>{{ geonet_ref|int }}</value></Data>
<Data name="z"><displayName>Depth (km)</displayName><value>{{ depth|float }}</value></Data>
<Data name="mag"><displayName>Magnitude</displayName><value>{{ magnitude|float }}</value></Data>
<Data name="date"><displayName>Date (UTC)</displayName><value>{{ datetime }}</value></Data>
<Data name="kmlstations">
  <displayName>Stations</displayName>
  <value>Click &lt;a href="{{ stations_url }}"&gt;here&lt;/a&gt; for a list of seismic stations with confirmed picks for this event (KML).</value>
</Data>
</ExtendedData>
<Point>
<coordinates>{{ lat|float }},{{ long|float }}</coordinates>
"""

QUAKE_HTML_PATTERN = """
<div id="quake-info"> 
<table>
    <tr><th>Reference Number</th><td></td></tr>
    <tr><th>Universal Time</th><td>{{ time_utc_human }}</td></tr>
    <tr><th>NZ Standard Time</th><td>{{ time_nzst_human }}</td></tr>
    <tr><th>Latitude, Longitude</th><td>{{ lat_degrees }},{{ long_degrees }}</td></tr>
    <tr><th>Focal Depth</th><td>{{ depth|float }}</td></tr>
    <tr><th>Richter magnitude</th><td>{{ magnitude|float }}</td></tr>
    <tr><th>Region</th><td>{{ region }}</td></tr>
    <tr>
        <th>Location</th>
        <td>
            <ul>
                {* <li>{{ [locations] }}</li> *}
            </ul>
        </td>
    </tr>
</table>
</div>
"""

PIPERMAIL_INDEX_PATTERN = """
{*
<td>
  <A>[ Thread ]</a>
  <A>[ Subject ]</a>
  <A>[ Author ]</a>
  <A href="{{ [] }}">[ Date ]</a>
</td>
*}
"""

PIPERMAIL_MONTH_PATTERN = """
{* HREF="{{ [] }}" *}
"""

PIPERMAIL_MESSAGE_PATTERN ="""
<PRE>
    Reference number:{{ }}
    Universal Time:
</PRE>
"""


STATION_PATTERN = """
{*
<Placemark>
<NAME>{{ [stations].name }}</NAME>
    <styleUrl>#station</styleUrl>
    <ExtendedData>
        <Data name="evalmode">
            <value>{{ [stations].evalmode }}</value>
        </Data>
        <Data name="evalstatus">
            <value>{{ [stations].evalstatus }}</value>
        </Data>
        <Data name="time">
            <value>{{ [stations].datetime }} </value>
        </Data>
        <Data name="etl">
            <value>{{ [stations].lower_uncertainty|float }} </value>
        </Data>
        <Data name="etu">
            <value>{{ [stations].upper_uncertainty|float }}</value>
        </Data>
    </ExtendedData>
    <Point>
        <coordinates>{{ [stations].coordinates }}</coordinates>
    </Point>
</Placemark>

*}
"""

def fetch_quake_kml(ref):
    url = 'http://magma.geonet.org.nz/services/quake/kml/2.2/search?externalRef=%s' % ref
    print '   Fetching: ', url
    res = scrape(pattern=QUAKE_KML_PATTERN, url=url)
    print '   Done. (KML data)'
    return res

def fetch_quake_html(ref):
    url = "http://www.geonet.org.nz/earthquake/quakes/%sg.html" % ref
    print '   Fetching: ', url
    res = scrape(pattern=QUAKE_HTML_PATTERN, url=url)
    print '   Done. (HTML data)'
    return res

def fetch_quake_data(ref):
    quake = fetch_quake_kml(ref)
    try:
        for k, val in fetch_quake_html(ref).iteritems():
            try:
                quake[k] = val
            except TypeError:
                print 'ERROR processing : ', k, val  
                pass
    except AttributeError:
        pass
    except HTTPError:
        print "HTTP ERROR: Skipping"
        pass
    try:
        if 'locations' in quake:
            quake['locations'] = '\n'.join(quake['locations'])
    except TypeError:
        quake = {}
    return quake

def add_urls(quake):
    ref = quake['geonet_ref']
    quake['felt_reports_kml_url'] = 'http://magma.geonet.org.nz/services/quake/reports/kml/2.2?externalRef=%s&agency=g' % ref
    quake['location_map_url'] = "http://www.geonet.org.nz/images/earthquake/quakes/%sgm.png" % ref
    quake['isoseismal_map_url'] = "http://www.geonet.org.nz/images/earthquake/quakes/%sgi.png" % ref
    quake['seismicity_map_url'] = "http://www.geonet.org.nz/images/earthquake/quakes/%sgc.png" % ref
    return quake

def do_felt_reports(ref):
    url = 'http://magma.geonet.org.nz/services/quake/reports/kml/2.2?externalRef=%s&agency=g' % ref
    print 'Fetching felt reports:  ' + url
    reports = []
    try:
        reports = scrape(pattern=FELT_REPORTS_PATTERN, url=url)['felt_reports']
        print '   Done. (%s felt reports)' % len(reports)
    except HTTPError:
        print 'HTTP ERROR - skipping'
    for report in reports:
        report['geonet_ref'] = ref
        report['source_url'] = url
    return reports

def _do_felt_reports(parent_quake):
    return do_felt_reports(parent_quake['geonet_ref'])

def do_stations(ref):
    url = 'http://magma.geonet.org.nz/services/quake/stations/kml/2.2/ref/%s' % ref
    print 'Fetching station data:  ' + url
    stations = []
    try:
        stations = scrape(pattern=STATION_PATTERN, url=url)['stations']
        print '   Done. (%s stations)' % len(stations)
    except HTTPError:
        print 'HTTP ERROR - skipping'
    for station in stations:
        station['geonet_ref'] = int(ref)
        station['source_url'] = url
    return stations

def _do_stations(parent_quake):
    return do_stations(parent_quake['geonet_ref'])

def iter_recent_quakes():
    for quake in scrape(pattern=RECENT_QUAKES_PATTERN,url=URL)['quakes']:
        quake['url'] = 'http://www.geonet.org.nz' + quake['url']
        quake['shaking_map_url'] = 'http://www.geonet.org.nz' + quake['shaking_map_url']
        quake['maps_url'] = 'http://www.geonet.org.nz' + quake['maps_url']
        quake['img_of_quake_location_url'] = 'http://www.geonet.org.nz' + quake['img_of_quake_location_url']
        for k, val in fetch_quake_data(quake['geonet_ref']).iteritems():
            quake[k] = val
        yield quake


def iter_mailing_list_quake_refs():
    base = "http://lists.geonet.org.nz/pipermail/eqnews/"
    index_urls = scrape(PIPERMAIL_INDEX_PATTERN, url=base)
    index_urls.reverse()
    index_urls= index_urls[96:]  ### REMEMBER TO DELETE WHEN FIRST COMPELETE RUN WORKS
    print index_urls
    for month in index_urls:
        print month
        messages = scrape(PIPERMAIL_MONTH_PATTERN, url = base + month)
        messages = [base + month.replace('date.html', link) for link in messages if '0' in link]
        print messages
        for message in messages:
            yield scrape(PIPERMAIL_MESSAGE_PATTERN, url=message)

def process_child_data(quake):
    ref = quake['geonet_ref']
    felt_reports = do_felt_reports(ref)
    if felt_reports:
        scraperwiki.sqlite.save(['geonet_ref', 'lat', 'long', 'reported_date', 'nearest_place'], table_name="felt_reports", data=felt_reports)
    station_readings = do_stations(ref)
    if station_readings:
        scraperwiki.sqlite.save(['geonet_ref', 'name'], table_name="station_reports", data=station_readings)

def process_quake_data(quake):
    quake = add_urls(quake)
    scraperwiki.sqlite.save(['geonet_ref'], table_name="quakes", data=quake)

def main():
    quakes_done = scraperwiki.sqlite.select('geonet_ref FROM quakes')
    quakes_done = set([q['geonet_ref'] for q in quakes_done])

#    for quake in iter_recent_quakes():
#        print 'Processing:  %s' % quake['geonet_ref']
#        process_quake_data(quake)
#        process_child_data(quake)

    for ref in iter_mailing_list_quake_refs():
        print ref
        try:
            ref = int(ref.split('/')[0])
        except:
            print u'ERROR with %s' % ref
            continue
        if ref in quakes_done:
            print 'Skipping: %s (Already exists)' % ref
        else:
            print 'Processing: %s' % ref
            quake = fetch_quake_data(ref)
            quake['geonet_ref'] = ref
            process_quake_data(quake)
            process_child_data(quake)
            quakes_done.add(ref)

#main()

station_test_data = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<kml xmlns:ns2="http://www.w3.org/2005/Atom" xmlns="http://www.opengis.net/kml/2.2" xmlns:ns3="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0">
<Document>
<name>Quake 3508353</name>
<description>Stations with confirmed picks used in earthquake location</description>
<LookAt>
<longitude>172</longitude>
<latitude>-41</latitude>
<range>2000000</range>
</LookAt>
<StyleMap id="station">
<Pair>
<key>normal</key>
<styleUrl>#inactive-station</styleUrl>
</Pair>
<Pair>
<key>highlight</key>
<styleUrl>#active-station</styleUrl>
</Pair>
</StyleMap>
<Style id="active-station">
<IconStyle>
<Icon>
<href>http://magma.geonet.org.nz/services/quake/images/triangle-red.png</href>
</Icon>
</IconStyle>
<LabelStyle>
<scale>1.0</scale>
</LabelStyle>
</Style>
<Style id="inactive-station">
<IconStyle>
<Icon>
<href>http://magma.geonet.org.nz/services/quake/images/triangle-red.png</href>
</Icon>
</IconStyle>
<LabelStyle>
<scale>0.0</scale>
</LabelStyle>
</Style>
<Folder>
<name>18 Operational Weak Motion Stations</name>
<description>Updated Fri May 06 11:24:33 UTC 2011</description>
<Placemark>
<name>CRLZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:49.917Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>LTZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:56.577Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>INZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:00.138Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>RPZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:59.099Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>WVZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:04.487Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>KHZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:08.038Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>FOZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:13.638Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>LBZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:12.238Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>THZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:12.863Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>ODZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:14.268Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>EAZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:25.348Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>JCZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:23.778Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>TUZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:57:29.948Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.5</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>1.0</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>DFHS-HNZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>automatic</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:44.525Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>OXZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:46.288Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>EYRS-HNZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:46.255Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.1</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.25</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>MQZ-HHZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:51.238Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.0</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.1</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>MQZ-HHN-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:57.398Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>CRLZ-HHN-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:54.967Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
<Placemark>
<name>EYRS-BNZ-NZ</name>
<styleUrl>#station</styleUrl>
<Style>
<IconStyle>
<scale>0.3</scale>
</IconStyle>
</Style>
<ExtendedData>
<Data name="evalmode">
<displayName>Evaluation Mode</displayName>
<value>manual</value>
</Data>
<Data name="evalstatus">
<displayName>Evaluation Status</displayName>
<value>confirmed</value>
</Data>
<Data name="time">
<displayName>Time</displayName>
<value>2011-05-06T10:56:48.260Z</value>
</Data>
<Data name="etl">
<displayName>Lower Uncertainty</displayName>
<value>0.25</value>
</Data>
<Data name="etu">
<displayName>Upper Uncertainty</displayName>
<value>0.5</value>
</Data>
</ExtendedData>
<Point>
<coordinates>null</coordinates>
</Point>
</Placemark>
</Folder>
</Document>
</kml>"""

html_test_data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>GeoNet &ndash; New Zealand Earthquake Report - Jul 9 2007 at 0:48 am (NZST)</title>
<meta name="revised" content="2007-07-08T13:03:57"/>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<meta name="description" content="The GeoNet Project - Monitoring geological hazards in New Zealand" />
<meta name="keywords" content="Earthquake, New Zealand, NZ, GeoNet, tsunami, seismic, seismic drum, volcano, volcanic, eruption, hazard, new zealand, volcano cam, volcano cams, volcano camera, White Island, Mt Ruapehu, Wairakei" />
<meta name="generator" content="Plone - http://www.plone.org/" />

<script type="text/javascript" src="/js/dply-functions.js"></script>


<!-- the content cell -->
<div id="quake-info">
<div class="details-l">
<h2>Quake Details</h2>
<p>Information about this earthquake:</p>
<table summary="Table to display specific details pertaining to this earthquake like: Time, depth, magnitude etc.">
<tr valign="top">
<th>Reference Number</th>
<td>2763595/G</td>
</tr>
<tr valign="top">
<th>Universal Time</th>
<td>July 8 2007 at 12:48</td>
</tr>
<tr valign="top">
<th>NZ Standard Time</th>
<td>Monday, July 9 2007 at 0:48 am</td>
</tr>
<tr valign="top">
<th>Latitude, Longitude</th>
<td>40.34&deg;S, 176.58&deg;E</td>
</tr>
<tr valign="top">
<th>Focal Depth</th>
<td>20 km</td>
</tr>
<tr valign="top">
<th>Richter magnitude</th>
<td>4.3</td>
</tr>
<tr valign="top">
<th>Region</th>
<td>Hawke's Bay</td>
</tr>
<tr valign="top">
<th>Location</th>
<td>
<ul>

<li>10 km south-west of Porangahau</li>

<li>40 km south of Waipukurau</li>

<li>80 km south of Hastings</li>

<li>190 km north-east of Wellington</li>

</ul>
</td>
</tr>
</table>


<p>Probably felt in the Hawkes Bay.</p>

<p>Did you feel this earthquake? We would appreciate it if you could fill out a <a href="http://magma.geonet.org.nz/felt/app?service=external/Felt&amp;sp=S2763595&amp;sp=SG">GeoNet Felt Earthquake Report</a> and let us know of your experiences.</p>
</div>
<div class="details-r">
<!-- rider/disclaimer -->
<h2>Disclaimer</h2>

<ul>

<li>The GeoNet project is core funded by the Earthquake Commission (EQC) and is being designed, installed and operated by GNS Science on behalf of EQC and all New Zealanders.</li>

<li>GNS Science accepts no liability for any loss or damage, direct or indirect, resulting from the use of the information provided. GNS Science does not make any representation in respect of the information's accuracy, completeness or fitness for any particular purpose.</li>

<li>Earthquake information last modified: 2007 Jul 08 13:01 (UT).</li>
</ul>

</div>
</div>

<!-- end of the content cell -->
</div>

<div id="relatedItems"></div>
<div class="discussion"></div>
</div>
</div>
</div>

<!-- end of main content block -->
<!-- start of the left (by default at least) column -->
<!-- end of the left (by default at least) column -->

</div>

<!-- end of the main and left columns -->
<!-- start of right (by default at least) column -->
<!-- end of the right (by default at least) column -->
</div>
</div>
<!-- end column wrapper -->
<hr class="netscape4" />
<div id="portal-colophon">
</div>
<div id="portal-footer">
<a href="http://www.gns.cri.nz/" class="img-logo-l" title=" GNS Science"><img src="/images/logo-gns.gif" alt="GNS Science" /></a>
<a href="http://www.eqc.govt.nz/" class="img-logo-r" title=" Earthquake Commission"><img src="/images/logo-eqc.gif" alt="EQC (Earthquake Commission)" /></a>
<p>GeoNet is a collaboration between the Earthquake Commission<br /> and GNS Science.</p>
<p class="base">GeoNet content is &copy; by <a href="http://www.gns.cri.nz/">GNS Science</a> | Powered by <a href="http://www.plone.org/">Plone CMS</a> | <a href="/about/">about</a> | <a href="/contact.html">contact</a> | <a href="/privacy.html">privacy</a> | <a href="/disclaimer.html">disclaimer</a></p>
</div>
</body>
</html>"""

def test_stations():
    res = scrape(STATION_PATTERN, html=station_test_data)
    assert 'stations' in res
    assert res['stations']


def test_html():
    res = scrape(QUAKE_HTML_PATTERN, html=html_test_data)
    print res
    for k, v in res.iteritems():
        print k, v

main()