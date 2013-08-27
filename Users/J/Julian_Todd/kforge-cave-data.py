import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
import urllib
import urlparse
import tempfile
import sqlite3
import lxml.etree, lxml.html
import re

import scraperwiki
#scraperwiki.cache(True) #scraperwiki apparently doesn't have a cache function

# setup the database
temp = tempfile.NamedTemporaryFile()
conn = sqlite3.connect(temp.name)
c = conn.cursor()
c.execute("create table legs (sfrom text, sto text, tape real, compass real, clino real)")
c.execute("create table equates (efrom text, eto text)")
conn.commit()


def Main():
    #url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/leckfell.svx"
    url = "http://knowledgeforge.net/sesame/club/mmmmc/survexdata/LowDouk/LowDouk.svx"
    topsurvexblock = SurvexBlock(None, url, "")
    equates = [ ]
    RecursiveLoad(topsurvexblock, urllib.urlopen(url), equates)
    ConsolidateEquates(equates)
    UploadSqlite()


def UploadSqlite():
    data = {"contents":open(temp.name, "rb").read()}
    dbname = "kforgecavedata"
    print len(data["contents"])
    print urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi?name="+dbname,
                         urllib.urlencode(data)).read()


def LoadSurvexLineLeg(survexblock, stardata, cline):
    ls = cline.lower().split()
    sfrom = "%s.%s" % (survexblock.dotpath(), ls[stardata["from"]])
    sto = "%s.%s" % (survexblock.dotpath(), ls[stardata["to"]])
    
    if ls[stardata["tape"]]!="public":
        if stardata["type"] == "normal":
            tape = float(ls[stardata["tape"]])
            lclino = ls[stardata["clino"]]
            lcompass = ls[stardata["compass"]]
            if lclino == "up":
                compass, clino = 0.0, 90.0
            elif lclino == "down":
                compass, clino = 0.0, -90.0
            elif lclino == "-" or lclino == "level":
                compass, clino = float(lcompass), 0.0
            else:
                assert re.match("[\d\-+.]+$", lcompass), ls
                assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
                compass, clino = float(lcompass), float(lclino)
            #print tape, compass, clino
    
        c.execute("insert into legs values (?,?,?,?,?)", (sfrom, sto, tape, compass, clino))
        conn.commit()



class SurvexBlock:
    def __init__(self, lupblock, lurl, beginname):
        self.lines = [ ]
        self.url = lurl
        self.upblock = lupblock
        if lupblock:
            self.path = lupblock.path[:]
            self.path.append(beginname)
            lupblock.downblocks.append(self)
        else:
            self.path = [ beginname ]
        self.downblocks = [ ]

    def dotpath(self):
        return ".".join([p  for p in self.path  if p])


def ConsolidateEquates(equates):
    eqmap = { }
    for i, equate in enumerate(equates):
        exti = set()
        for station in equates[i]:
            if station in eqmap:
                exti.update(equates[eqmap[station]])
                equates[eqmap[station]] = None
            else:
                eqmap[station] = i
        for xstation in exti:
            eqmap[xstation] = i
        equate.update(exti)

    ei = 0
    for equate in equates:
        if equate:
            for station in equate:
                c.execute("insert into equates values (?,?)", (station, "eq%d" % ei))
            ei += 1
    conn.commit()

        
def FollowInclude(furl, cline):
    lk = cline.split()[0].strip('"').replace("\\", "/")
    if lk[-4:] != '.svx':
        lk += '.svx'
    durl = urlparse.urljoin(furl.url, lk)
    try:    return urllib.urlopen(durl)
    except: pass
    durl = urlparse.urljoin(furl.url, lk.lower())
    return urllib.urlopen(durl)

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, furl, equates):
    stardata = stardatadefault 
    while True:
        line = furl.readline().decode("latin1")
        if not line:
            return
        ml = re.match("(?:\*\s*(\w+))?\s*([^;]*?)(?:\s*;\s*(.*))?$", line)
        assert ml, line
        command, cline, comment = ml.groups()
        #print command, cline, comment
        if not command:
            if cline and "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, cline)
        else:
            lcommand = command.lower()
            if lcommand == "include":
                RecursiveLoad(survexblock, FollowInclude(furl, cline), equates)
            elif lcommand == "begin":
                dsurvexblock = SurvexBlock(survexblock, furl, cline.split()[0].lower())
                dsurvexblock.lines.append(line)
                RecursiveLoad(dsurvexblock, furl, equates)
            elif lcommand == "end":
                survexblock.lines.append(line)
                return
            elif lcommand == "equate":
                equates.append(set([ ("%s.%s" % (survexblock.dotpath(), p)).lower()  for p in cline.split() ]))
            elif lcommand == "data":
                ls = cline.lower().split()
                stardata = { "type":ls[0] }
                for i in range(0, len(ls)):
                    stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
                if ls[0] in ["normal", "cartesian", "nosurvey"]:
                    assert "from" in stardata, line
                    assert "to" in stardata, line
                elif ls[0] == "default":
                    stardata = stardatadefault
                else:
                    assert ls[0] == "passage", line

Main()
