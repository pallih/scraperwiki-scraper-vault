import scraperwiki
import urllib2
import urlparse
import re
import os
import time

filename = ""

# to do.  
#  Detect dates
#  Do equates
#  Detect use of DistoX to distinguish computer generated numbers
print "2"
irebyurl = "http://cave-registry.org.uk/svn/Yorkshire/mmmmc/survexdata/all.svx"
treextract = scraperwiki.swimport("apache_directory_tree_extractor")
print treextract.ParseSVNRevPageTree("http://cave-registry.org.uk/svn/Yorkshire/mmmmc/survexdata/")
print "3"
allteam = set()


def Main():
    survexblock = SurvexBlock(name="root", survexpath="caves", parent=None, begin_char=0, cave="Ireby", survexfile=irebyurl, totalleglength=0.0)
    fin = GetFile(irebyurl)
    textlines = [ ]
    #print "before", fin
    RecursiveLoad(survexblock, irebyurl, fin, textlines)
    return survexblock

def GetFile(url):
    try:
        print url
        gfile = urllib2.urlopen(url)
        print gfile
    except Exception, reason:
        print "error:", reason
        gfile = StepFile(url)
    print "returning Getfile"
    return gfile

def StepFile(url):
    print "Stepfile:", url
    urlarray=url.split("/")
    print urlarray
    if urlarray[-1] == u"":
        del urlarray[-1]
    for value in range(5,len(urlarray)):
        urlarray2=[]
        for x in range(0,value):
            urlarray2.append(urlarray[x])
        getfileurl=urllib2.urlopen("/".join(urlarray2))
        indexstr = getfileurl.read().strip()
        if value != len(urlarray):
            properloc=re.findall(urlarray[value]+"(?i)",indexstr)
            urlarray[value]=properloc[0]
        del urlarray2
    gfile =urllib2.urlopen("/".join(urlarray))
    return gfile

# save the whole lot in one batch
def SaveAll(survexblock):
    survexblocks = [ survexblock ]
    survexlegs = [ ]
    i = 0
    while i < len(survexblocks):
        survexblocks.extend(survexblocks[i].survexblocks)
        survexlegs.extend(survexblocks[i].survexlegs)
        i += 1
    ldata = [ survexleg.ToDict()  for survexleg in survexlegs ]
    scraperwiki.sqlite.save(["stationfrom", "stationto"], ldata, "survexlegs")

    
class SurvexBlock:
    def __init__(self, name, survexpath, begin_char, cave, parent, survexfile, totalleglength):
        self.name = name
        self.survexpath = survexpath
        self.begin_char = begin_char
        self.cave = cave
        self.survexfile = survexfile
        self.totalleglength = totalleglength
        self.parent = parent
        self.team = [ ]
        self.date = ""
        self.survexblocks = [ ]
        self.survexlegs = [ ]
        
        
class SurvexLeg:
    def __init__(self, survexblock, stationfrom, stationto):
        self.survexblock = survexblock
        self.stationfrom = stationfrom
        self.stationto = stationto
        self.tape = None
        self.compass = None
        self.clino = None
        
    def ToDict(self):
        return { "blockname":self.survexblock.name, "cave":self.survexblock.cave, "stationfrom":self.stationfrom, "stationto":self.stationto, 
                 "tape":self.tape, "compass":self.compass, "clino":self.clino }


def LoadSurvexLineLeg(survexblock, stardata, sline, comment):
    ls = sline.lower().split()
    #print ls
    #print stardata
    ssfrom = ls[stardata["from"]] # survexblock.MakeSurvexStation(ls[stardata["from"]])
    ssto = ls[stardata["to"]] # survexblock.MakeSurvexStation(ls[stardata["to"]])
    
    survexleg = SurvexLeg(survexblock=survexblock, stationfrom=ssfrom, stationto=ssto)
    if stardata["type"] == "normal":
        survexleg.tape = float(ls[stardata["tape"]])
        lclino = ls[stardata["clino"]]
        lcompass = ls[stardata["compass"]]
        if lclino in ["up","UP","V+","v+","+V","+v"]:
            lclino ="up"
            survexleg.compass = 0.0
            survexleg.clino = 90.0
        elif lclino in ["down","DOWN","V-","v-","-V","-v"]:
            lclino ="down"
            survexleg.compass = 0.0
            survexleg.clino = -90.0
        elif lclino == "-" or lclino == "level":
            survexleg.compass = float(lcompass)
            survexleg.clino = -90.0
        else:
            assert re.match("[\d\-+.]+$", lcompass), ls
            assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
            survexleg.compass = float(lcompass)
            survexleg.clino = float(lclino)
        
    itape = stardata.get("tape")
    if itape:
        survexblock.totalleglength += float(ls[itape])
    survexblock.survexlegs.append(survexleg)
        
def LoadSurvexEquate(survexblock, sline):
    pass

def LoadSurvexLinePassage(survexblock, stardata, sline, comment):
    pass
    

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, survexfile, fin, textlines):
    global allteam
    iblankbegins = 0
    text = [ ]
    stardata = stardatadefault
    
    while True:
        #print fin
        svxline = fin.readline().decode("latin1")
        if not svxline:
            break
        textlines.append(svxline)
        # break the line at the comment
        sline, comment = re.match("([^;]*?)\s*(?:;\s*(.*))?\n?$", svxline.strip()).groups()

        dtype = re.findall('<\w*>', sline)
        if dtype:
            print "dtype wrong"
            print survexblock, survexfile, fin, textlines
            break


        cnames = re.split("\s*[,:/]\s*", comment or "")
        if len(cnames) >= 2:
            if re.match("(?i)Instruments|Surveyors|Book", cnames[0]):
                #print cnames
                for cname in cnames:
                    if not re.match("(?i)Instruments|Surveyors|Book|PAG|RRCPC", cname):
                        allteam.add(cname)
        
        if not sline:
            continue
        
        # detect the star command
        mstar = re.match('\s*\*(\w+)\s*(.*?)\s*(?:;.*)?$', sline)
        
        if not mstar:
            if "from" in stardata:
                try:
                    LoadSurvexLineLeg(survexblock, stardata, sline, comment)
                except ValueError, e:
                    print "problem parsing", (survexblock, sline, stardata)
            elif stardata["type"] == "passage":
                LoadSurvexLinePassage(survexblock, stardata, sline, comment)
            continue
        
        # detect the star command
        cmd, line = mstar.groups()
        
        if re.match("include$(?i)", cmd):
            tail = re.sub("\.svx$", "", line.strip('"'))
            tail = re.sub("[\.\\\\]", "/", tail)
            #print survexfile, os.path.split(survexfile), tail
            includesurvexfile = os.path.join(os.path.split(survexfile)[0], tail) + ".svx"
            #print includesurvexfile
            print "recurse"
            if includesurvexfile not in ["http://cave-registry.org.uk/svn/Yorkshire/mmmmc/survexdata/3cgps.svx","3cgps.svx"]: 
                fininclude = GetFile(includesurvexfile)
                # print fininclude
                RecursiveLoad(survexblock, includesurvexfile, fininclude, textlines)
        
        elif re.match("begin$(?i)", cmd):
            if line: 
                name = line.lower()
                lcave = (survexblock.cave or survexfile.cave)  # in the mmmmc case we set the file with the cave first
                # begin_char=fin.tell()
                survexblockdown = SurvexBlock(name=name, begin_char=0, parent=survexblock, 
                                              survexpath=survexblock.survexpath+"."+name, cave=lcave, 
                                              survexfile=survexfile, totalleglength=0.0)
                survexblock.survexblocks.append(survexblockdown)
                textlinesdown = [ ]
                RecursiveLoad(survexblockdown, survexfile, fin, textlinesdown)
            else:
                iblankbegins += 1
        
        elif re.match("end$(?i)", cmd):
            if iblankbegins:
                iblankbegins -= 1
            else:
                survexblock.text = "".join(textlines)
                return
        
        elif re.match("date$(?i)", cmd):
            if len(line) == 10:
                survexblock.date = re.sub("\.", "-", line)
                    
        elif re.match("team$(?i)", cmd):
            mteammember = re.match("(Insts|Notes|Tape|Dog|Useless|Pics|Helper|Disto|Consultant)\s+(.*)$(?i)", line)
            if mteammember:
                for tm in re.split(' and | / |, | & | \+ |"|^both$|^none$(?i)', mteammember.group(2)):
                    if tm:
                        survexblock.team.append(tm)
                        allteam.add(tm)
                            
        elif cmd == "title":
            survextitle = line.strip('"') # models.SurvexTitle(survexblock=survexblock, title=line.strip('"'), cave=survexblock.cave)
            
        elif cmd == "data":
            ls = line.lower().split()
            stardata = { "type":ls[0] }
            for i in range(0, len(ls)):
                stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
            if ls[0] in ["normal", "cartesian", "nosurvey"]:
                assert "from" in stardata, line
                assert "to" in stardata, line
            elif ls[0] == "default":
                stardata = stardatadefault
            else:
                print ls
                assert (ls[0] == "passage" or ls[0] == "diving"), line
        
        elif cmd == "equate":
            LoadSurvexEquate(survexblock, sline)
        
        else:
            assert cmd.lower() in [ "sd", "equate", "include", "units", "entrance", "fix", "data", "flags", "title", "export", "instrument", "calibrate", "solve" ], (cmd, line, survexblock)
    
    #print allteam
    

# main function calls 
print "1"
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS 'survexlegs'")      
rootsurvexblock = Main()
SaveAll(rootsurvexblock)
            