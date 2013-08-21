import scraperwiki
import scraperwiki.metadata
import re
import datetime
import urllib
import pygooglechart

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# also needs the google charts visualization, and we do by week,
# maybe striped by party

# convert a dict value into a pie chart
def PieChart():
    aa = scraperwiki.datastore.retrieve({"party":None})
    d = { }
    for a in aa:
        p = a["data"]["party"]
        if p not in d:
            d[p] = 0
        d[p] += 1
        
    
    chart = pygooglechart.PieChart3D(550, 200, colours=["556600"])

    # put in descending order
    ld = [ (v, k)  for k, v in d.items() ]
    ld.sort()
    ld.reverse()
    
    # truncate at 10 items
    if len(ld) > 7:
        rest = sum([v  for v, k in ld[7:]])
        ld[7] = (rest, "other")
        del ld[8:]
        
    chart.add_data([v  for v, k in ld])
    chart.set_pie_labels([k  for v, k in ld])
    chart.set_title("Leaflets pr party")
    scraperwiki.metadata.save("chart", chart.get_url())


partycolour = { "The Labour Party":"ff0000", "Conservative Party":"0000ff", "Liberal Democrats":"ff00ff", "Green Party":"00ff00" }

def getLatestLeafletId():
    # first find the latest leaflet id
    url = "http://www.electionleaflets.org/leaflets/"
    html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
    mlatestleafletid = re.search('<a class="leaflet" href="http://www.thestraightchoice.org/leaflets/(\d+)/">', html)
    return mlatestleafletid and int(mlatestleafletid.group(1)) or 4500

def Main():
    latestleaflet = getLatestLeafletId()
    print "Latest leaflet", latestleaflet
    for n in range(latestleaflet-10, latestleaflet):  # keep up to date over the last 50
        url = "http://www.electionleaflets.org/leaflet.php?q=%d" % n
        try:
            html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
        except:
            continue
        mud = re.search("Uploaded on \w+,\s+(\d+) (\w+), ([\-\d]+) at (\d\d):(\d\d)\.", html)
        mparty = re.search('Published by <a.*?>(.*?)</a>', html)
        mconstituency = re.search('Delivered in <a.*?>(.*?)</a>', html)
        mlocation = re.search("showMap\('openstreetmap', ([-.\d]+), (5[-.\d]+)", html)
        imageurls = re.findall('(http://thestraightchoice.s3.amazonaws.com/medium/[0-9a-f]+\.jpg)', html)
        if mud:
            year = int(mud.group(3))
            if year == -1:
                year = 2009
            d = datetime.datetime(year, months.index(mud.group(2)) + 1, 
                                  int(mud.group(1)), int(mud.group(4)), int(mud.group(5)))
    
            party = mparty.group(1)
            constituency = mconstituency and mconstituency.group(1) or ""
            imageurl = imageurls and imageurls[0] or ""
            data = {"url":url, "party":party, "constituency":constituency, "imageurl":imageurl}
            latlng = mlocation and (float(mlocation.group(2)), float(mlocation.group(1))) or None
            print n, d, party, imageurl, latlng
            data["colour"] = partycolour.get(party, "ffffff")
            data["date"] = d
            data["latlng_lat"] = latlng[0]
            data["latlng_lng"] = latlng[1]
            scraperwiki.sqlite.save(unique_keys=["url"], data=data)
        else:
            print n, "missing"
            print html
            assert re.search("Sorry", html)

Main()
#PieChart()        
    

import scraperwiki
import scraperwiki.metadata
import re
import datetime
import urllib
import pygooglechart

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# also needs the google charts visualization, and we do by week,
# maybe striped by party

# convert a dict value into a pie chart
def PieChart():
    aa = scraperwiki.datastore.retrieve({"party":None})
    d = { }
    for a in aa:
        p = a["data"]["party"]
        if p not in d:
            d[p] = 0
        d[p] += 1
        
    
    chart = pygooglechart.PieChart3D(550, 200, colours=["556600"])

    # put in descending order
    ld = [ (v, k)  for k, v in d.items() ]
    ld.sort()
    ld.reverse()
    
    # truncate at 10 items
    if len(ld) > 7:
        rest = sum([v  for v, k in ld[7:]])
        ld[7] = (rest, "other")
        del ld[8:]
        
    chart.add_data([v  for v, k in ld])
    chart.set_pie_labels([k  for v, k in ld])
    chart.set_title("Leaflets pr party")
    scraperwiki.metadata.save("chart", chart.get_url())


partycolour = { "The Labour Party":"ff0000", "Conservative Party":"0000ff", "Liberal Democrats":"ff00ff", "Green Party":"00ff00" }

def getLatestLeafletId():
    # first find the latest leaflet id
    url = "http://www.electionleaflets.org/leaflets/"
    html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
    mlatestleafletid = re.search('<a class="leaflet" href="http://www.thestraightchoice.org/leaflets/(\d+)/">', html)
    return mlatestleafletid and int(mlatestleafletid.group(1)) or 4500

def Main():
    latestleaflet = getLatestLeafletId()
    print "Latest leaflet", latestleaflet
    for n in range(latestleaflet-10, latestleaflet):  # keep up to date over the last 50
        url = "http://www.electionleaflets.org/leaflet.php?q=%d" % n
        try:
            html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
        except:
            continue
        mud = re.search("Uploaded on \w+,\s+(\d+) (\w+), ([\-\d]+) at (\d\d):(\d\d)\.", html)
        mparty = re.search('Published by <a.*?>(.*?)</a>', html)
        mconstituency = re.search('Delivered in <a.*?>(.*?)</a>', html)
        mlocation = re.search("showMap\('openstreetmap', ([-.\d]+), (5[-.\d]+)", html)
        imageurls = re.findall('(http://thestraightchoice.s3.amazonaws.com/medium/[0-9a-f]+\.jpg)', html)
        if mud:
            year = int(mud.group(3))
            if year == -1:
                year = 2009
            d = datetime.datetime(year, months.index(mud.group(2)) + 1, 
                                  int(mud.group(1)), int(mud.group(4)), int(mud.group(5)))
    
            party = mparty.group(1)
            constituency = mconstituency and mconstituency.group(1) or ""
            imageurl = imageurls and imageurls[0] or ""
            data = {"url":url, "party":party, "constituency":constituency, "imageurl":imageurl}
            latlng = mlocation and (float(mlocation.group(2)), float(mlocation.group(1))) or None
            print n, d, party, imageurl, latlng
            data["colour"] = partycolour.get(party, "ffffff")
            data["date"] = d
            data["latlng_lat"] = latlng[0]
            data["latlng_lng"] = latlng[1]
            scraperwiki.sqlite.save(unique_keys=["url"], data=data)
        else:
            print n, "missing"
            print html
            assert re.search("Sorry", html)

Main()
#PieChart()        
    

import scraperwiki
import scraperwiki.metadata
import re
import datetime
import urllib
import pygooglechart

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# also needs the google charts visualization, and we do by week,
# maybe striped by party

# convert a dict value into a pie chart
def PieChart():
    aa = scraperwiki.datastore.retrieve({"party":None})
    d = { }
    for a in aa:
        p = a["data"]["party"]
        if p not in d:
            d[p] = 0
        d[p] += 1
        
    
    chart = pygooglechart.PieChart3D(550, 200, colours=["556600"])

    # put in descending order
    ld = [ (v, k)  for k, v in d.items() ]
    ld.sort()
    ld.reverse()
    
    # truncate at 10 items
    if len(ld) > 7:
        rest = sum([v  for v, k in ld[7:]])
        ld[7] = (rest, "other")
        del ld[8:]
        
    chart.add_data([v  for v, k in ld])
    chart.set_pie_labels([k  for v, k in ld])
    chart.set_title("Leaflets pr party")
    scraperwiki.metadata.save("chart", chart.get_url())


partycolour = { "The Labour Party":"ff0000", "Conservative Party":"0000ff", "Liberal Democrats":"ff00ff", "Green Party":"00ff00" }

def getLatestLeafletId():
    # first find the latest leaflet id
    url = "http://www.electionleaflets.org/leaflets/"
    html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
    mlatestleafletid = re.search('<a class="leaflet" href="http://www.thestraightchoice.org/leaflets/(\d+)/">', html)
    return mlatestleafletid and int(mlatestleafletid.group(1)) or 4500

def Main():
    latestleaflet = getLatestLeafletId()
    print "Latest leaflet", latestleaflet
    for n in range(latestleaflet-10, latestleaflet):  # keep up to date over the last 50
        url = "http://www.electionleaflets.org/leaflet.php?q=%d" % n
        try:
            html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
        except:
            continue
        mud = re.search("Uploaded on \w+,\s+(\d+) (\w+), ([\-\d]+) at (\d\d):(\d\d)\.", html)
        mparty = re.search('Published by <a.*?>(.*?)</a>', html)
        mconstituency = re.search('Delivered in <a.*?>(.*?)</a>', html)
        mlocation = re.search("showMap\('openstreetmap', ([-.\d]+), (5[-.\d]+)", html)
        imageurls = re.findall('(http://thestraightchoice.s3.amazonaws.com/medium/[0-9a-f]+\.jpg)', html)
        if mud:
            year = int(mud.group(3))
            if year == -1:
                year = 2009
            d = datetime.datetime(year, months.index(mud.group(2)) + 1, 
                                  int(mud.group(1)), int(mud.group(4)), int(mud.group(5)))
    
            party = mparty.group(1)
            constituency = mconstituency and mconstituency.group(1) or ""
            imageurl = imageurls and imageurls[0] or ""
            data = {"url":url, "party":party, "constituency":constituency, "imageurl":imageurl}
            latlng = mlocation and (float(mlocation.group(2)), float(mlocation.group(1))) or None
            print n, d, party, imageurl, latlng
            data["colour"] = partycolour.get(party, "ffffff")
            data["date"] = d
            data["latlng_lat"] = latlng[0]
            data["latlng_lng"] = latlng[1]
            scraperwiki.sqlite.save(unique_keys=["url"], data=data)
        else:
            print n, "missing"
            print html
            assert re.search("Sorry", html)

Main()
#PieChart()        
    

import scraperwiki
import scraperwiki.metadata
import re
import datetime
import urllib
import pygooglechart

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# also needs the google charts visualization, and we do by week,
# maybe striped by party

# convert a dict value into a pie chart
def PieChart():
    aa = scraperwiki.datastore.retrieve({"party":None})
    d = { }
    for a in aa:
        p = a["data"]["party"]
        if p not in d:
            d[p] = 0
        d[p] += 1
        
    
    chart = pygooglechart.PieChart3D(550, 200, colours=["556600"])

    # put in descending order
    ld = [ (v, k)  for k, v in d.items() ]
    ld.sort()
    ld.reverse()
    
    # truncate at 10 items
    if len(ld) > 7:
        rest = sum([v  for v, k in ld[7:]])
        ld[7] = (rest, "other")
        del ld[8:]
        
    chart.add_data([v  for v, k in ld])
    chart.set_pie_labels([k  for v, k in ld])
    chart.set_title("Leaflets pr party")
    scraperwiki.metadata.save("chart", chart.get_url())


partycolour = { "The Labour Party":"ff0000", "Conservative Party":"0000ff", "Liberal Democrats":"ff00ff", "Green Party":"00ff00" }

def getLatestLeafletId():
    # first find the latest leaflet id
    url = "http://www.electionleaflets.org/leaflets/"
    html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
    mlatestleafletid = re.search('<a class="leaflet" href="http://www.thestraightchoice.org/leaflets/(\d+)/">', html)
    return mlatestleafletid and int(mlatestleafletid.group(1)) or 4500

def Main():
    latestleaflet = getLatestLeafletId()
    print "Latest leaflet", latestleaflet
    for n in range(latestleaflet-10, latestleaflet):  # keep up to date over the last 50
        url = "http://www.electionleaflets.org/leaflet.php?q=%d" % n
        try:
            html = urllib.urlopen(url).read() # scraperwiki.scrape(url)
        except:
            continue
        mud = re.search("Uploaded on \w+,\s+(\d+) (\w+), ([\-\d]+) at (\d\d):(\d\d)\.", html)
        mparty = re.search('Published by <a.*?>(.*?)</a>', html)
        mconstituency = re.search('Delivered in <a.*?>(.*?)</a>', html)
        mlocation = re.search("showMap\('openstreetmap', ([-.\d]+), (5[-.\d]+)", html)
        imageurls = re.findall('(http://thestraightchoice.s3.amazonaws.com/medium/[0-9a-f]+\.jpg)', html)
        if mud:
            year = int(mud.group(3))
            if year == -1:
                year = 2009
            d = datetime.datetime(year, months.index(mud.group(2)) + 1, 
                                  int(mud.group(1)), int(mud.group(4)), int(mud.group(5)))
    
            party = mparty.group(1)
            constituency = mconstituency and mconstituency.group(1) or ""
            imageurl = imageurls and imageurls[0] or ""
            data = {"url":url, "party":party, "constituency":constituency, "imageurl":imageurl}
            latlng = mlocation and (float(mlocation.group(2)), float(mlocation.group(1))) or None
            print n, d, party, imageurl, latlng
            data["colour"] = partycolour.get(party, "ffffff")
            data["date"] = d
            data["latlng_lat"] = latlng[0]
            data["latlng_lng"] = latlng[1]
            scraperwiki.sqlite.save(unique_keys=["url"], data=data)
        else:
            print n, "missing"
            print html
            assert re.search("Sorry", html)

Main()
#PieChart()        
    

