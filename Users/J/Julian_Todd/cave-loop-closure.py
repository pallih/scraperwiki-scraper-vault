import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

import sqlite3
import urllib
import tempfile
import json
import scraperwiki
import math
scraperwiki.cache(False)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedata").read()
open(temp.name, "wb").write(contents)
conn = sqlite3.connect(temp.name)
c = conn.cursor()

stationlegs = { }
for leg in c.execute("""
        SELECT coalesce(eqfrom.eto, sfrom), coalesce(eqto.eto, sto), tape, compass, clino FROM legs 
        LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
        LEFT JOIN equates as eqto on eqto.efrom = sto"""):
    stationlegs.setdefault(leg[0], []).append(leg)
    stationlegs.setdefault(leg[1], []).append(leg)


station = (stationlegs.keys())[0]
stationpos = {station:(0.0, 0.0, 0.0)}  # first position
lstations = [ station ]
while lstations:
    station = lstations.pop(0)
    for leg in stationlegs[station]:
        ostation = (station == leg[0] and leg[1] or leg[0])
        if ostation in stationpos:
            continue
        tape, compass, clino = leg[2], math.radians(leg[3]), math.radians(leg[4])
        if station == leg[0]:
            tape = -tape
        stationpos[ostation] = (stationpos[station][0] + tape*math.cos(compass)*math.cos(clino), 
                                stationpos[station][1] + tape*math.sin(compass)*math.cos(clino),
                                stationpos[station][2] + tape*math.sin(clino))
        lstations.append(ostation)


c.execute("create table stations (station text, x real, y real, z real)")
for station, pos in stationpos.items():
    c.execute("insert into stations values (?,?,?,?)", (station, pos[0], pos[1], pos[2]))
conn.commit()


data = {"contents":open(temp.name, "rb").read()}
dbname = "kforgecavedatastations"
print len(data["contents"])
print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                     urllib.urlencode(data)).read()

