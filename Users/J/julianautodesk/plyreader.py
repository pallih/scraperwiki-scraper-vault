import scraperwiki
import urllib2


def ReadFile(url, name):
    fin = urllib2.urlopen(url)
    properties = [ ]
    while True:
        ln = fin.readline().split()
        print ln
        if ln[0] == 'property':
            if ln[1] != 'list':
                properties.append(ln[2])
        if ln[0] == "end_header":
            break
    print properties
    
    ldata = [ ]
    i = 0
    while True:
        ln = fin.readline().split()
        if not ln:
            break
        data = dict(zip(properties, map(float, ln)))
        data["name"] = name
        data["i"] = i
        i += 1
        ldata.append(data)
        if len(ldata) == 2000:
            if i >= 0: # 1600000:
                scraperwiki.sqlite.save(["i"], ldata, "points")
            ldata = [ ]
    
    if len(ldata):
        scraperwiki.sqlite.save(["i"], ldata, "points")


#ReadFile("https://fluff.bris.ac.uk/fluff/u1/ggpls/2efxpVDBNP8MOYV6FhS_zAEYf/top2.ply", "top2")
ReadFile("https://fluff.bris.ac.uk/fluff/u3/ggpls/rJ2sLthALcaYQwlx4yfhBQEYC/bottom2.ply", "bottom2")

