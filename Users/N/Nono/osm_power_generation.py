#CD - trying to get this working with the filtered OSM power data hosted on Enipedia.
#It seems that the data from overpass-api.de is not exactly the same as the Enipedia data.  
#In particular, there seems to be some trouble in linking references, and the code below 
#has been mostly modified to include a few try/catch blocks, check if keys are present in dictionaries, etc.

#Currently checking to see if the data is filtered slightly differently, which may affect the code.
#Probably want:
#./osmfilter PlanetPowerGenerators.osm --keep-nodes="power=generator" --keep-ways="power=generator" -o=TestPowerFilter.osm
#instead of what is documented at (http://enipedia.tudelft.nl/wiki/Extracting_Power_Data_from_OpenStreetMap)

#TODO don't we want to include relations as well?  
#The query to overpass-api.de seems to only grab nodes and ways
#There's probably a few power plants that are mapped out to an incredible amount of detail, and use relations to group
#together the various bits of the site.  
#Relations may also be important for identifying wind parks, as the documentation suggests to use relations to group the nodes together.
#http://wiki.openstreetmap.org/wiki/Proposed_features/Power_generation_refinement#Advanced_tagging_2
#In my experience with NL wind farms, this isn't widespread yet.

import scraperwiki
import lxml.html
import urllib
import urllib2
from imposm.parser import OSMParser
from scraperwiki import CPUTimeExceededError
from math import *
import zipfile
from StringIO import StringIO

refsSet = set()
nodesLookup = dict()
relTagsLookup = dict()
unknownValueLookup = dict()
otherTagSet = set()
country = ""


def createPreferredTermsDict():
    preferredTermsLookup = dict()
    preferredTermsLookup['name'] = 'name'
    preferredTermsLookup['operator'] = 'operator'
    preferredTermsLookup['power_source'] = 'source'
    preferredTermsLookup['generator_source'] = 'source'
    preferredTermsLookup['generator_method'] = 'method'
    preferredTermsLookup['generator_output'] = 'output'
    preferredTermsLookup['generator_output_electricity'] = 'output_electricity'
    preferredTermsLookup['generator_output_heat'] = 'output_heat'
    preferredTermsLookup['generator_output_steam'] = 'output_steam'
    preferredTermsLookup['generator_output_hot_water'] = 'output_hot_water'
    return preferredTermsLookup


def getCentroid(ring):
    nb = 0
    sumlat = 0
    sumlon = 0
    for pt in ring.split(" "):
        coords = pt.split(",")
        sumlat += float(coords[0])
        sumlon += float(coords[1])
        nb += 1
    return [sumlat/nb, sumlon/nb]

# adapted from http://msdn.microsoft.com/en-us/library/bb259689.aspx
def buildQuadKey(lon, lat, level):
    quadKey = ""
    x = int(((lon + 180) // 360) * (2 ** level))
    y = int((0.5 - log((1 + sin(radians(lat))) / (1 - sin(radians(lat)))) // (4 * pi)) * (2 ** level))
    for i in range(level, 0, -1):
        digit = 0;
        mask = 1 << (i - 1);
        if (x & mask) != 0:
            digit += 1
        if (y & mask) != 0:
            digit += 2
        quadKey += str(digit)
    return quadKey

    
def rels_handler(relations):
    for rel_id, tags, members in relations:
        for osm_id, type, role in members:
            relTagsLookup[osm_id] = tags
    
def refs_handler(ways):
    for osm_id, tags, refs in ways:
#        if 'power' in tags:
#            refsSet.update(refs)

        #CD - not all refs seem to be in this dictionary, trying to add everything by default
        refsSet.update(refs)

def coords_handler(coords):
    for osm_id, lon, lat in coords:
        if osm_id in refsSet:
            nodesLookup[osm_id] = "%.6f,%.6f" % (lat, lon)

def get_tags(tags):
    info = dict()
    info ['misc'] = ""
    for key in tags:
        dbkey = key
        if key.find(":") > 0:
            dbkey = key.replace(':', '_')
        if dbkey in preferredTermsLookup and tags[key] not in ["yes","no","fixme"]:
            info[preferredTermsLookup[dbkey]] = tags[key]
        elif dbkey != "power":
            info ['misc'] += "%s = %s\n" % (dbkey, tags[key])
            otherTagSet.add(dbkey)
    return info


def nodes_handler(nodes):
    cpt = 1
    nodeList = list()
    for osmid, tags, coords in nodes:
        if 'power' in tags and tags['power'] == 'generator':
            nodeInfo = get_tags(tags)
            if osmid in relTagsLookup:
                nodeInfo.update(get_tags(relTagsLookup[osmid]))
            nodeInfo['osmid'] = osmid
            nodeInfo['centroid_lon'] = coords[0]
            nodeInfo['centroid_lat'] = coords[1]
            nodeInfo['quadkey'] = buildQuadKey(coords[0], coords[1], 20)
            if cpt % 1000 == 0:
                scraperwiki.sqlite.save(unique_keys=['osmid'], data=nodeList)
                print "   handled %d nodes" % cpt
                nodeList= list()
            else:
                nodeList.append(nodeInfo)
            cpt += 1
    #CD - write any data that hasn't been saved yet
    if nodeList:
        scraperwiki.sqlite.save(unique_keys=['osmid'], data=nodeList)


def ways_handler(ways):
    cpt = 1
    wayList = list()
    for osmid, tags, refs in ways:
        if 'power' in tags and tags['power'] == 'generator':
            wayInfo = get_tags(tags)
            if osmid in relTagsLookup:
                wayInfo.update(get_tags(relTagsLookup[osmid]))
            wayInfo['osmid'] = osmid
            path = ""
            for ref in refs:
                #CD - getting KeyError: 1914214717, or alternatively 1901397644
                #It seems that not all of the refs are the nodesLookup dict
                #at least when using the osm data from Enipedia
                #the refs_handler function has been update to grab as many refs as possible
                if ref in nodesLookup:
                    #print "ref is " + str(ref)
                    #print "nodeslookup is " + str(nodesLookup[ref])
                    path += nodesLookup[ref] + " "
                else:
                    print "ref not found"
            wayInfo['ring'] = path.rstrip()

            try: 
                centroid = getCentroid(wayInfo['ring'])
                wayInfo['centroid_lat'] = centroid[0]
                wayInfo['centroid_lon'] = centroid[1]
                wayInfo['quadkey'] = buildQuadKey(centroid[1], centroid[0], 20)
            except: #CD - when using Enipedia osm data, occasionally run into issues when no coordinates are found
                    #still need to go through the original data and figure out why this is occurring.
                print "can't calculate centroid"

            if cpt % 1000 == 0:
                scraperwiki.sqlite.save(unique_keys=['osmid'], data=wayList)
                print "   handled %d ways" % cpt
                wayList= list()
            else:
                wayList.append(wayInfo)
            cpt += 1

    #CD - write any data that hasn't been saved yet
    if wayList:
        scraperwiki.sqlite.save(unique_keys=['osmid'], data=wayList)



def process_file(filename):
    refsSet = set()
    nodesLookup = dict()

    print "parsing for refs..."
    parser = OSMParser(ways_callback=refs_handler, relations_callback=rels_handler)
    parser.parse('/tmp/'+filename)

    print "parsing for coords..."
    parser = OSMParser(coords_callback=coords_handler)
    parser.parse('/tmp/'+filename)
    
    print "parsing for ways and nodes..."
    parser = OSMParser(ways_callback=ways_handler, nodes_callback=nodes_handler)
    parser.parse('/tmp/'+filename)

preferredTermsLookup = createPreferredTermsDict()

scraperwiki.sqlite.execute("create table if not exists swdata (osmid integer, name text, operator text, source text, method text, output text, output_electricity text, output_heat text, output_hot_water text, output_steam text, misc text, ring text, centroid_lon real, centroid_lat real, quadkey text)")
scraperwiki.sqlite.execute("create index if not exists spatial_quadkey on swdata(quadkey)")

base_url = "http://overpass-api.de/api/interpreter?"
query = "data=%5Bmaxsize%3A1073741824%5D%5Btimeout%3A900%5D%3B%28way%5B%22power%22%3D%22generator%22%5D%3Bnode%28w%29%3Bnode%5B%22power%22%3D%22generator%22%5D%3B%29%3Bout%3B"

try:
    #code for retrieving data from overpass-api.de
    #urllib.urlretrieve(base_url+query, '/tmp/powerplants.osm')
    #process_file("powerplants.osm")

    #alternative code for retrieving the same data from Enipedia - http://enipedia.tudelft.nl/wiki/Extracting_Power_Data_from_OpenStreetMap
    #this data is updated every day
    response = urllib2.urlopen('http://enipedia.tudelft.nl/OpenStreetMap/PlanetPowerGenerators.zip')
    zippedData = zipfile.ZipFile(StringIO(response.read()))
    osmData = zippedData.open("PlanetPowerGenerators.osm").read()
    output = open('/tmp/powerplants.osm','wb')
    output.write(osmData)
    output.close()
    process_file('powerplants.osm')


except CPUTimeExceededError:
    print "Scraper terminated (CPU time exceeded)"

print "misc tags: " + ', '.join(otherTagSet)

