import scraperwiki
import lxml.html
import urllib
from imposm.parser import OSMParser
from scraperwiki import CPUTimeExceededError


refsSet = set()
nodesLookup = dict()
unknownValueLookup = dict()
otherTagLookup = dict()
country = ""


def createPreferredTermsDict():
    preferredTermsLookup = dict()
    preferredTermsLookup['name'] = 'name'
    preferredTermsLookup['power'] = 'type'
    preferredTermsLookup['voltage'] = 'voltage'
    preferredTermsLookup['operator'] = 'operator'
    preferredTermsLookup['cables'] = 'cables'
    preferredTermsLookup['wires'] = 'wires'
    preferredTermsLookup['frequency'] = 'frequency'
    preferredTermsLookup['power_source'] = 'source'
    preferredTermsLookup['generator_source'] = 'source'
    preferredTermsLookup['generator_method'] = 'method'
    preferredTermsLookup['generator_output'] = 'output'
    preferredTermsLookup['generator_output_electricity'] = 'output_electricity'
    preferredTermsLookup['generator_output_heat'] = 'output_heat'
    preferredTermsLookup['generator_output_steam'] = 'output_steam'
    preferredTermsLookup['generator_output_hot_water'] = 'output_hot_water'
    preferredTermsLookup['frequency'] = 'frequency'
    return preferredTermsLookup


def createCountriesDict():
    countriesTermsLookup = dict()
    countriesTermsLookup ['Great_Britain'] = 'UK'
    countriesTermsLookup ['England'] = 'UK'
    countriesTermsLookup ['Bayern'] = 'Germany'
    countriesTermsLookup ['Baden-Wuerttemberg'] = 'Germany'
    countriesTermsLookup ['Nordrhein-Westfalen'] = 'Germany'
    return countriesTermsLookup


def centroid(ring):
    nb = 0
    sumlat = 0
    sumlon = 0
    for pt in ring.split(" "):
        coords = pt.split(",")
        sumlat += float(coords[0])
        sumlon += float(coords[1])
        nb = nb + 1
    return "%.6f,%.6f" % (sumlat/nb, sumlon/nb)


def refs_handler(ways):
    for osmid, tags, refs in ways:
        if 'power' in tags:
            refsSet.update(refs)

def coords_handler(coords):
    for osm_id, lon, lat in coords:
        if osm_id in refsSet:
            nodesLookup[osm_id] = "%.6f,%.6f" % (lat, lon)

def ways_handler(ways):
    for osmid, tags, refs in ways:
        if 'power' in tags:
            wayInfo = dict()
            wayInfo['misc'] = ""
            for key in tags:
                dbkey = key
                if key.find(":") > 0:
                    dbkey = key.replace(':', '_')
                if dbkey in preferredTermsLookup:
                    wayInfo[preferredTermsLookup[dbkey]] = tags[key]
                else:
                    wayInfo['misc'] += "%s = %s\n" % (dbkey, tags[key])
                    otherTagLookup[dbkey] = 1
            wayInfo['osmid'] = osmid
            path = ""
            for ref in refs:
                path += nodesLookup[ref] + " "
            wayInfo['country'] = country
            if tags['power'] == 'line' or tags['power'] == 'cable' or tags['power'] == 'underground_cable':
                wayInfo['path'] = path.rstrip()
                scraperwiki.sqlite.save(unique_keys=['osmid'], data=wayInfo, table_name="powerlines")
            elif tags['power'] == 'generator':
                wayInfo['ring'] = path.rstrip()
                wayInfo['centroid'] = centroid(wayInfo['ring'])
                scraperwiki.sqlite.save(unique_keys=['osmid'], data=wayInfo, table_name="powerplants")
            elif tags['power'] == 'station' or tags['power'] == 'sub_station'or tags['power'] == 'transformer':
                wayInfo['ring'] = path.rstrip()
                wayInfo['centroid'] = centroid(wayInfo['ring'])
                scraperwiki.sqlite.save(unique_keys=['osmid'], data=wayInfo, table_name="stations")
            else:
                unknownValueLookup[tags['power']] = 1


def process_file(filename, baseurl = 'http://download.geofabrik.de/osm/europe/', parentCountry = ""):
    print "retrieving file " + filename + "..."
    urllib.urlretrieve(baseurl+filename, '/tmp/'+filename)

    global country
    refsSet = set()
    nodesLookup = dict()

    if parentCountry == "":
        country = filename[0:-8].replace('_',' ').title()
        if country in countriesLookup:
            country = countriesLookup[country]
    
    print "parsing for refs..."
    parser = OSMParser(ways_callback=refs_handler)
    parser.parse('/tmp/'+filename)

    print "parsing for coords..."
    parser = OSMParser(coords_callback=coords_handler)
    parser.parse('/tmp/'+filename)
    
    print "parsing for ways..."
    parser = OSMParser(ways_callback=ways_handler)
    parser.parse('/tmp/'+filename)

    scraperwiki.sqlite.save_var(filename, 1)


def process_list(url, parentCountry = "", initflag = 2):
    global country

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    dirs = root.xpath("//tr[.//img[@src='/icons/folder.gif']]//a/@href")
    for dir in dirs:
        if parentCountry == "":
            country = dir.rstrip('/').title()
            if country in countriesLookup:
                country = countriesLookup[country]
        process_list(url+dir, country, initflag)

    links = root.xpath("//tr//a/@href[contains(.,'osm.pbf')]")
    for link in links:
        if scraperwiki.sqlite.get_var(link, -1) == 0:
            process_file(link, url, parentCountry)
        if initflag < 2:
            scraperwiki.sqlite.save_var(link, initflag)


preferredTermsLookup = createPreferredTermsDict()
countriesLookup = createCountriesDict()

#init variables
#process_list("http://download.geofabrik.de/osm/europe/", -1)
#scraperwiki.sqlite.save_var('netherlands.osm.pbf', -1)

#scraperwiki.sqlite.execute("update swvariables set value_blob = 0")
#scraperwiki.sqlite.execute("update swvariables set value_blob = ? where name like ?", ["-1","%regbez%"])


try:
    process_list("http://download.geofabrik.de/osm/europe/")

except CPUTimeExceededError:
    print "Scraper terminated (CPU time exceeded)"


for value in unknownValueLookup:
    print "unhandled value for power tag: " + value

for value in otherTagLookup:
    print "misc tag: " + value

