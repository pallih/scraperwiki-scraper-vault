import scraperwiki
import lxml.html
import re
from time import sleep

"""
distance.py

Usage distance.py --way=way-id --follow-rel=rel-id [--distance=dist]
"""

import getopt
import math
import sys
import httplib
import urllib
import urllib2
from xml.etree.ElementTree import XML
import xml.etree.ElementTree as ET

_debug = False
osm_api = "http://www.openstreetmap.org/api/0.6"
http_headers = { "User-Agent": "ItenaryBot (http://www.wabson.org/)" }

def main():

    # Defaults
    dist = 0.0
    
    rules = [
        {
            'way_id': '109152248',
            'way_name': None,
            'way_type': 'waterway:canal',
            'relation_id': '152791',
            'stop_way_ids': None
        },
        {
            'way_id': '109221549',
            'way_name': 'River Thames',
            'way_type': 'waterway:river',
            'relation_id': None,
            'stop_way_ids': [ '4625497', '97885921', '2641951', '145306501' ]
        }
    ]

    for rule in rules:
        # TODO Check that the overall navigated is continuous
        dist = navigate(rule['way_id'], rule['way_name'], rule['way_type'], rule['relation_id'], rule['stop_way_ids'], dist)

def navigate(way_id, way_name=None, way_type=None, relation_id=None, stop_way_ids=None, dist=0.0):

    if way_id is None or way_id == "":
        print "No way specified"
        sys.exit(1)

    followrel = None
    if relation_id is None:
        print "No relationship was specified to follow. Will attempt to autodetect ways to follow."
    else:
        followrel = get_relation(relation_id)

    # TODO Support reversing node in config
    way = get_way(way_id)

    print "Following way %s" % (way['tags']['name'])
    add_sw_point({'way_id': way["id"], 'node_id': way["nodes"][0]["id"], 'lat': way["nodes"][0]["lat"], 'lon': way["nodes"][0]["lon"], 'otype': 'way', 'otag': '', 'name': "Enter %s" % (way['tags']['name']), 'distance': dist })
    scraperwiki.sqlite.save_var('route_name', way['tags']['name'] if 'name' in way['tags'] else '')
    #TODO Check way is a canal/river and has a name

    old_way_ids = []

    while way is not None:
        old_way_ids.append(way['id'])
        dist = print_itenary(way, dist)
        # Look for a continuation of the way on the last node
        wn = way["nodes"]
        nways = wn[len(wn)-1]["ways"]
        nextway = None
        if len(nways) > 0:
            for ow in nways:
                # Check it is not the same way, has not been seen before and not a 'stop' way
                if ow["id"] not in old_way_ids and (stop_way_ids is None or ow["id"] not in stop_way_ids):
                    if followrel is not None:
                        if relation_is_member(ow["id"], "way", followrel):
                            nextway = ow
                            break
                    else:
                        ow = api_get_way_info(ow['id'])
                        if "waterway" in ow["tags"] and ow["tags"]["waterway"] in ("canal", "river") and \
                               (way_name is None or ("name" in ow["tags"] and ow["tags"]["name"].strip() == way_name)) and \
                               ("boat" not in ow["tags"] or ow["tags"]["boat"].strip() == "yes"):
                            nextway = ow
                            break
        else:
            add_sw_point({'way_id': way["id"], 'node_id': way["nodes"][len(way["nodes"])-1]["id"], 'lat': way["nodes"][len(way["nodes"])-1]["lat"], 'lon': way["nodes"][len(way["nodes"])-1]["lon"], 'otype': 'way', 'otag': '', 'name': "Leave %s" % (way['tags']['name']), 'distance': dist })

        if nextway is not None:
            # Load full way
            nextway = get_way(nextway["id"])
            if nextway["nodes"][len(nextway["nodes"])-1]["id"] == way["nodes"][len(way["nodes"])-1]["id"]: # Check next way starts with the last node from the previous node
                nextway["nodes"].reverse()
            # Note if we enter a tunnel/bridge/lock way
            if "lock" in nextway["tags"] and nextway["tags"]["lock"] == "yes" and (not "lock" in way["tags"] or way["tags"]["lock"] == "no"):
                print_waypoint(get_lock_name(nextway), dist)
                add_sw_point({'way_id': way["id"], 'node_id': nextway["nodes"][0]["id"], 'lat': nextway["nodes"][0]["lat"], 'lon': nextway["nodes"][0]["lon"], 'otype': 'way', 'otag': 'lock=yes', 'name': get_lock_name(nextway), 'distance': dist })
            if "tunnel" in nextway["tags"] and nextway["tags"]["tunnel"] == "yes" and (not "tunnel" in way["tags"] or way["tags"]["tunnel"] == "no"):
                print_waypoint("Start tunnel", dist)
                add_sw_point({'way_id': way["id"], 'node_id': nextway["nodes"][0]["id"], 'lat': nextway["nodes"][0]["lat"], 'lon': nextway["nodes"][0]["lon"], 'otype': 'way', 'otag': 'tunnel=yes', 'name': "Start tunnel", 'distance': dist })
            if "bridge" in nextway["tags"] and nextway["tags"]["bridge"] == "yes" and (not "bridge" in way["tags"] or way["tags"]["bridge"] == "no"):
                print_waypoint("Start bridge", dist)
                add_sw_point({'way_id': way["id"], 'node_id': nextway["nodes"][0]["id"], 'lat': nextway["nodes"][0]["lat"], 'lon': nextway["nodes"][0]["lon"], 'otype': 'way', 'otag': 'bridge=yes', 'name': "Start bridge", 'distance': dist })
            # Note if we leave a tunnel/bridge way
            if ("tunnel" not in nextway["tags"] or nextway["tags"]["tunnel"] == "no") and "tunnel" in way["tags"] and way["tags"]["tunnel"] == "yes":
                print_waypoint("End tunnel", dist)
                add_sw_point({'way_id': way["id"], 'node_id': nextway["nodes"][0]["id"], 'lat': nextway["nodes"][0]["lat"], 'lon': nextway["nodes"][0]["lon"], 'otype': 'way', 'otag': 'tunnel=no', 'name': "End tunnel", 'distance': dist })
            if ("bridge" not in nextway["tags"] or nextway["tags"]["bridge"] == "no") and "bridge" in way["tags"] and way["tags"]["bridge"] == "yes":
                print_waypoint("End bridge", dist)
                add_sw_point({'way_id': way["id"], 'node_id': nextway["nodes"][0]["id"], 'lat': nextway["nodes"][0]["lat"], 'lon': nextway["nodes"][0]["lon"], 'otype': 'way', 'otag': 'bridge=no', 'name': "End bridge", 'distance': dist })
            way = nextway
        else:
            add_sw_point({'way_id': way["id"], 'node_id': way["nodes"][len(way["nodes"])-1]["id"], 'lat': way["nodes"][len(way["nodes"])-1]["lat"], 'lon': way["nodes"][len(way["nodes"])-1]["lon"], 'otype': 'way', 'otag': '', 'name': "Leave %s" % (way['tags']['name']), 'distance': dist })
            way = None

    # Print summary
    print "TOTAL DISTANCE: %.3f km" % (dist)
    return dist

def get_lock_name(item):
    lockname = "Lock"
    if "lock_name" in item["tags"]:
        lockname = item["tags"]["lock_name"]
        if "lock_ref" in item["tags"]:
            lockname = "%s (%s)" % (lockname, item["tags"]["lock_ref"])
    return lockname

def print_itenary(way, dist=0.0):
    # Step through 2nd to last node
    if _debug:
        print "Way %s - %.3f" % (way["id"], dist)
    for i in range(1, len(way["nodes"])):
        n = way["nodes"][i]
        # Note if we find a lock node
        if ("lock" in n["tags"] and n["tags"]["lock"] == "yes") or ("waterway" in n["tags"] and n["tags"]["waterway"] == "lock"):
            lockname = get_lock_name(n)
            print_waypoint(lockname, dist)
            add_sw_point({'way_id': way["id"], 'node_id': n['id'], 'lat': n["lat"], 'lon': n["lon"], 'otype': 'node', 'otag': 'waterway=lock', 'name': lockname, 'distance': dist })
        # Calculate distance between this and last node
        dist += geo_distance(way["nodes"][i-1], n)
        otherways = []
        for w in n["ways"]:
            if w["id"] != "%s" % (way["id"]):
                otherways.append(w)
        for w in otherways:
            wname = None
            wtag = None
            if "highway" in w["tags"]:
                wtag = "%s=%s" % ("highway", w["tags"]["highway"])
                if "name" in w["tags"]:
                    wname = w["tags"]["name"]
                else:
                    hwtype = w["tags"]["highway"]
                    if hwtype == "motorway":
                        wname = "Motorway"
                    elif hwtype == "trunk":
                        wname = "Trunk road"
                    elif hwtype == "primary":
                        wname = "Primary road"
                    elif hwtype == "secondary":
                        wname = "Secondary road"
                    elif hwtype == "tertiary":
                        wname = "Tertiary road"
                    elif hwtype == "residential":
                        wname = "Residential road"
                    elif hwtype == "unclassified":
                        wname = "Unclassified road"
                    elif hwtype == "road":
                        wname = "Unknown road"
                    elif hwtype == "service":
                        wname = "Service road"
                    elif hwtype == "track":
                        wname = "Track"
                    elif hwtype == "pedestrian":
                        wname = "Pedestrianised road"
                    elif hwtype == "path":
                        wname = "Path"
                    elif hwtype == "cycleway":
                        wname = "Cycleway"
                    elif hwtype == "footway":
                        wname = "Footpath"
                    elif hwtype == "bridleway":
                        wname = "Bridleway"
                    else:
                        wname = "Unknown highway"
                if "ref" in w["tags"]:
                    wname = "%s (%s)" % (wname, w["tags"]["ref"])
            elif "railway" in w["tags"] and w["tags"]["railway"] == "rail":
                wtag = "%s=%s" % ("railway", w["tags"]["railway"])
                if "name" in w["tags"]:
                    wname = w["tags"]["name"]
                else:
                    wname = "Railway"
            else:
                #wname = "Unknown way"
                pass
            if wname is not None:
                print_waypoint(wname, dist)
                add_sw_point({'way_id': way["id"], 'node_id': n['id'], 'lat': n["lat"], 'lon': n["lon"], 'otype': 'way', 'otag': wtag, 'name': wname, 'distance': dist })
    return dist

def print_waypoint(name, dist):
    print "%.3f,%s" % (dist, name)

# keys are way_id, node_id, otype, otype, oname, distance
def add_sw_point(data):
    scraperwiki.sqlite.save(unique_keys=['way_id', 'node_id'], data=data)

# Calculate distance based on haversine formula
# Based on http://www.movable-type.co.uk/scripts/latlong.html
def geo_distance(node1, node2):
    R = 6371; # km
    lat1 = float(node1["lat"])
    lat2 = float(node2["lat"])
    lon1 = float(node1["lon"])
    lon2 = float(node2["lon"])
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d # distance in km

def get_way(wid):
    return web_get_way(wid)

def web_get_way(wid):
    way = { "id": wid }
    html = http_scrape("http://www.openstreetmap.org/browse/way/%s" % (str(wid)))
    root = lxml.html.fromstring(html)
    nodeways = {} # dict of wid => ways list of dict objects with struct { id, tags{name} }
    for tr in root.cssselect("table.browse_details tr"):
        th = tr.find("th")
        if th is not None:
            heading = th.text_content().strip().rstrip(":")
            if heading == "Tags":
                wtags = {}
                for td in th.getnext().cssselect("table tr td a"): # el.getnext() is xml.etree specific
                    taglist = td.text_content().strip().split("=")
                    if len(taglist) == 2:
                        wtags[taglist[0].strip()] = taglist[1].strip()
                #way["tags"] = wtags
            elif heading == "Nodes":
                wnodes = []
                for td in th.getnext().cssselect("table tr td"):
                    wnode = {}
                    nodelink = td.cssselect("a.node")[0]
                    nodename = nodelink.text_content().strip()
                    nodeid = nodelink.get("href").strip().replace("/browse/node/", "")
                    ways = []
                    for waylink in td.cssselect("a.way"):
                        wayname = waylink.text_content().strip()
                        intmatch = re.search('^\d*$', wayname)
                        if intmatch is not None:
                            wayname = ""
                        else:
                            wayname = re.sub('\s\(\d+\)$', '', wayname)
                        wayid = waylink.get("href").strip().replace("/browse/way/", "")
                        waytags = {}
                        taglist = waylink.get("title").strip().split("=")
                        if wayname != "":
                            waytags["name"] = wayname
                        if len(taglist) == 2:
                            waytags[taglist[0].strip()] = taglist[1].strip()
                        thisway = { "id": wayid, "tags": waytags }
                        ways.append(thisway)
                    nodeways[nodeid] = ways;
                    #way["nodes"] = wnodes

    # Load minimum information on the way, from the API
    way = api_get_way_info(wid, full=False)
    # For each node, add in the information on additional ways from the web page
    for n in way["nodes"]:
        n["ways"] = nodeways[n["id"]]
    return way

def api_get_way_info(wid, full=True):
    tree = api_get("way/%s/full" % (wid))
    wayElem = tree.find("way")
    nodeElems = tree.getiterator("node")
    # Put included nodes into a temporary dictionary, keyed by id
    nodes = {}
    for ne in nodeElems:
        nid = ne.get("id")
        # Put node tags into dict structure
        nodetags = {}
        for t in ne.getiterator("tag"):
            nodetags[t.get("k")] = t.get("v")
        n = { "id": nid, "lat": ne.get("lat"), "lon": ne.get("lon"), "tags": nodetags }
        # Get list of ways associated with the node, if needed
        if (full):
            nodeways = api_get_node_ways(nid)
            n["ways"] = nodeways
        # Add to the temp dict
        nodes[nid] = n
    waynds = wayElem.getiterator("nd")
    # Form the ordered list of nodes in the way
    waynodes = []
    for wn in waynds:
        n = nodes[wn.get("ref")]
        waynodes.append(n)
    tags = {}
    for t in wayElem.getiterator("tag"):
        tags[t.get("k")] = t.get("v")
    return { "id": wid, "nodes": waynodes, "tags": tags }

def get_node(nid):
    tree = api_get("node/%s" % (nid))
    node = tree.find("node")
    lat = node.get("lat")
    lon = node.get("lon")
    return { "id": nid, "lat": lat, "lon": lon }

def get_relation(rid):
    members = []
    tree = api_get("relation/%s" % (rid))
    el = tree.find("relation")
    rid = el.get("id")
    mels = el.getiterator("member")
    for m in mels:
        members.append({ "type": m.get("type"), "ref": m.get("ref") })
    return { "id": rid, "members": members }

def relation_is_member(item_id, item_type, relation):
    for m in relation["members"]:
        if item_id == m["ref"] and item_type == m["type"]:
            return True
    return False

def api_get_node_ways(nid):
    tree = api_get("node/%s/ways" % (nid))
    ways = []
    wayElems = tree.getiterator("way")
    for we in wayElems:
        tags = {}
        for t in we.getiterator("tag"):
            tags[t.get("k")] = t.get("v")
        ways.append({ "id": we.get("id"), "tags": tags })
    return ways

def api_get(path):
    i = 0
    ex = None
    while i < 3:
        try:
            req = urllib2.Request("%s/%s" % (osm_api, path), headers=http_headers)
            resp = urllib2.urlopen(req)
            tree = ET.XML(resp.read())
            resp.close()
            return tree
        except urllib2.HTTPError as e:
            if e.code == 502:
                i = i + 1
                ex = e
                continue
            else:
                raise e
    raise Exception("Encountered too many exceptions", ex)

def http_scrape(path):
    #html = scraperwiki.scrape(path)
    req = urllib2.Request(path, headers=http_headers)
    resp = urllib2.urlopen(req)
    html = resp.read()
    resp.close()
    return html

main()


