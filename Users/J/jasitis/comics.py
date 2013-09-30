import scraperwiki
#!/usr/bin/python
import urllib2
import urlparse
import os
import re
import glob
import cgi
#import cgitb; cgitb.enable()
import os.path
import sys
import md5
import datetime

DatabaseDir = "/home/smhanov/public_html/cgi-bin/comicdb"
DatabaseFile = DatabaseDir + "/" + "database.txt"

dateExpr = re.compile('\[(?P<date>.*)\]')
fileExpr = re.compile('"(P<comic>[^"]+)" (P<file>.+)')

otherChars = re.compile(r'[^A-Za-z0-9]+')
dateExpr = re.compile(r"(\d\d\d\d\d\d\d\d)")
serveExpr = re.compile(r"[a-z0-9]+_\d+")
scrubExpr = re.compile(r"[^a-z_0-9\.]")
srcExpr = re.compile(r'(src|SRC)\s?=\s?"([^"]+)"');
baseExpr = re.compile(r'BASE HREF="([^"]+)"');
        
class ComicRecord:
    def __init__(self, name, site, pattern):
        self.name = name
        self.site = site
        self.expr = re.compile(pattern)
        self.comics = {};
        self.idname = otherChars.sub('', self.name).lower()

    def filter(self, path):
        name = otherChars.sub('', self.name).lower(); 
        path = path + "/" + name + "_*";

        for file in glob.glob(path):
            m = dateExpr.search(file);
            if m:
                self.comics[m.group(0)] = os.path.basename(file);

    def add(self, fileData, date, extension):
        name = otherChars.sub('', self.name).lower(); 
        name = DatabaseDir + "/" + name + "_" + date + "." + extension
        file = open(name, "wb")
        file.write(fileData)
        file.close()
        return name

    def hash(self, hashSet):
        for key in self.comics.keys():
            file = open(DatabaseDir + "/" + self.comics[key], "rb");
            mmd5 = md5.new()
            mmd5.update(file.read())
            file.close()
            hashSet.add(mmd5.hexdigest())

# read the database file.
file = open(DatabaseFile);
lineno = 0
lines = file.readlines();
comics = [];
i = 0
while i < len( lines ):
    line = lines[i].rstrip('\n');
    if line != '-':
        print "Error in database file line %d. Expecting \'-\'" % (i)
        i += 1
        continue
    name = lines[i+1].rstrip('\n')
    site = lines[i+2].rstrip('\n')
    pattern = lines[i+3].rstrip('\n')
    comics.append( ComicRecord(name,"http://"+site,pattern) )
    i += 4

for comic in comics:
    comic.filter(DatabaseDir)

if len(sys.argv) >= 2 and sys.argv[1] == "update":
    print "Updating comics"
    hash = set([])
    today = datetime.date.today().strftime("%Y%m%d")
    
    for comic in comics:
        try:
            comic.hash(hash)
            print "Retrieving " + comic.site
            site = comic.site
            req=urllib2.Request(
                    url=site,
                    headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113'})
            file = urllib2.urlopen(req)
            page = file.read()
            file.close()
            url = None
            base = site
            m = baseExpr.search(page)
            if m: base = m.group(1)
            for m in srcExpr.findall(page):
                m2 = comic.expr.search(m[1])
                if m2:
                    url = m[1]
                    if not url.startswith("http:"):
                        url = urlparse.urljoin(base, url)
                    break;
            if url:
                print "found comic: " + url
                req = urllib2.Request(url)
                req.add_header('Referer', site)
                file = urllib2.urlopen(req)
                image = file.read()
                info = file.info()
                file.close()
                mmd5 = md5.new()
                mmd5.update(image)
                if not (mmd5.hexdigest() in hash):
                    extension = info['content-type'].rsplit("/")[-1]
                    if extension == "x-png": extension = "png"
                    if extension == "jpeg": extension = "jpg"
                    print extension
                    path = comic.add(image, today, extension);
                    print "    Added " + path
                else:
                    print "    Already have it"
        except urllib2.HTTPError, e:  
            print "Exception: HTTP" + str(e.code)
        except urllib2.URLError, e:  
            print "Exception." 
            
            

    sys.exit()

# If the argument is a comic ID, then serve the image from the database and
# quit

form = cgi.FieldStorage();
if form.has_key("id"):
    # Scrub it
    name = scrubExpr.sub('', form["id"].value) 
    name = DatabaseDir + "/" + name
    #print "Content-type: text.html\n\n",

    if name.endswith(".gif"):
        print "Content-type: image/gif\n\n",
    elif name.endswith(".png"):
        print "Content-type: image/x-png\n\n",
    elif name.endswith(".jpg"):
        print "Content-type: image/jpeg\n\n",
 
    # Search for that file
    file = open(name, mode="rb");
    if  file:
        a = file.read();
        print a,

    sys.exit()

# Create a web page
print "Content-type: text/html\n\n",
print "<html><head><title>Example Comic Page</title>"
print """
<style>
body {
    font-family: "Trebuchet MS";
}

h1 {
    font-family: "Comic Sans MS";
}
span.link {
    color: blue;
    text-decoration: underline;
    cursor: pointer;
}
</style>
</head><body>
<center><h1>
Example Comics Page</h1>
For demonstration purposes only. Please don't sue me.
</center>
<script type="text/javascript">
function myback(id, next)
{
    for( i = 0; i < comics.arr.length; i++ ) {
        if ( comics.arr[i].name == id ) {
            break
        }
    }
    
    if ( i == comics.arr.length ) {
        alert("Not found! Error tell Steve.");
        return false
    }

    comic = comics.arr[i]

    elem = document.getElementById(id)

    if ( next && comic.current < comic.dates.length-1 ) {
        comic.current++
    } else if ( !next && comic.current > 0 ) {
        comic.current--
    }

    elem.src = "?id=" + comic.dates[comic.current]

    return false
}

var comics = {
    "arr" : [
"""

afirst = True
for comic in comics:
    keys = comic.comics.keys()
    keys.sort()
    if not afirst:
        print ",\n      {"
    else:
        print "\n      {"

    print '            "name": "%s",' % (comic.idname)
    print '            "current": %s,' % (len(keys)-1)
    print '            "dates" : [',
    first = True
    for key in keys:
        if not first:
            print ", ",
        print '\"%s\"' % (comic.comics[key]),
        first = False

    print "]\n        }",
    afirst = False

print """
    ]
}
</script>
"""

# For each comic in the database, print it to the page.
for comic in comics:
    keys = comic.comics.keys()
    keys.sort()
    if len( keys ) == 0:
        continue

    first = comic.comics[keys[-1]];

    print "<hr><center><h1>" + comic.name + "</h1>"
    print "<p>"
    print "<span class=link onclick=\"myback('%s',false)\">Previous</span> |" % (comic.idname)
    print "<span class=link onclick=\"myback('%s',true)\">Next</span><p>" % (comic.idname)

    print "<img id=" + comic.idname+" src=\"?id=" + first + "\">"
    print "</center>"

print "</body></html>"
import scraperwiki
#!/usr/bin/python
import urllib2
import urlparse
import os
import re
import glob
import cgi
#import cgitb; cgitb.enable()
import os.path
import sys
import md5
import datetime

DatabaseDir = "/home/smhanov/public_html/cgi-bin/comicdb"
DatabaseFile = DatabaseDir + "/" + "database.txt"

dateExpr = re.compile('\[(?P<date>.*)\]')
fileExpr = re.compile('"(P<comic>[^"]+)" (P<file>.+)')

otherChars = re.compile(r'[^A-Za-z0-9]+')
dateExpr = re.compile(r"(\d\d\d\d\d\d\d\d)")
serveExpr = re.compile(r"[a-z0-9]+_\d+")
scrubExpr = re.compile(r"[^a-z_0-9\.]")
srcExpr = re.compile(r'(src|SRC)\s?=\s?"([^"]+)"');
baseExpr = re.compile(r'BASE HREF="([^"]+)"');
        
class ComicRecord:
    def __init__(self, name, site, pattern):
        self.name = name
        self.site = site
        self.expr = re.compile(pattern)
        self.comics = {};
        self.idname = otherChars.sub('', self.name).lower()

    def filter(self, path):
        name = otherChars.sub('', self.name).lower(); 
        path = path + "/" + name + "_*";

        for file in glob.glob(path):
            m = dateExpr.search(file);
            if m:
                self.comics[m.group(0)] = os.path.basename(file);

    def add(self, fileData, date, extension):
        name = otherChars.sub('', self.name).lower(); 
        name = DatabaseDir + "/" + name + "_" + date + "." + extension
        file = open(name, "wb")
        file.write(fileData)
        file.close()
        return name

    def hash(self, hashSet):
        for key in self.comics.keys():
            file = open(DatabaseDir + "/" + self.comics[key], "rb");
            mmd5 = md5.new()
            mmd5.update(file.read())
            file.close()
            hashSet.add(mmd5.hexdigest())

# read the database file.
file = open(DatabaseFile);
lineno = 0
lines = file.readlines();
comics = [];
i = 0
while i < len( lines ):
    line = lines[i].rstrip('\n');
    if line != '-':
        print "Error in database file line %d. Expecting \'-\'" % (i)
        i += 1
        continue
    name = lines[i+1].rstrip('\n')
    site = lines[i+2].rstrip('\n')
    pattern = lines[i+3].rstrip('\n')
    comics.append( ComicRecord(name,"http://"+site,pattern) )
    i += 4

for comic in comics:
    comic.filter(DatabaseDir)

if len(sys.argv) >= 2 and sys.argv[1] == "update":
    print "Updating comics"
    hash = set([])
    today = datetime.date.today().strftime("%Y%m%d")
    
    for comic in comics:
        try:
            comic.hash(hash)
            print "Retrieving " + comic.site
            site = comic.site
            req=urllib2.Request(
                    url=site,
                    headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113'})
            file = urllib2.urlopen(req)
            page = file.read()
            file.close()
            url = None
            base = site
            m = baseExpr.search(page)
            if m: base = m.group(1)
            for m in srcExpr.findall(page):
                m2 = comic.expr.search(m[1])
                if m2:
                    url = m[1]
                    if not url.startswith("http:"):
                        url = urlparse.urljoin(base, url)
                    break;
            if url:
                print "found comic: " + url
                req = urllib2.Request(url)
                req.add_header('Referer', site)
                file = urllib2.urlopen(req)
                image = file.read()
                info = file.info()
                file.close()
                mmd5 = md5.new()
                mmd5.update(image)
                if not (mmd5.hexdigest() in hash):
                    extension = info['content-type'].rsplit("/")[-1]
                    if extension == "x-png": extension = "png"
                    if extension == "jpeg": extension = "jpg"
                    print extension
                    path = comic.add(image, today, extension);
                    print "    Added " + path
                else:
                    print "    Already have it"
        except urllib2.HTTPError, e:  
            print "Exception: HTTP" + str(e.code)
        except urllib2.URLError, e:  
            print "Exception." 
            
            

    sys.exit()

# If the argument is a comic ID, then serve the image from the database and
# quit

form = cgi.FieldStorage();
if form.has_key("id"):
    # Scrub it
    name = scrubExpr.sub('', form["id"].value) 
    name = DatabaseDir + "/" + name
    #print "Content-type: text.html\n\n",

    if name.endswith(".gif"):
        print "Content-type: image/gif\n\n",
    elif name.endswith(".png"):
        print "Content-type: image/x-png\n\n",
    elif name.endswith(".jpg"):
        print "Content-type: image/jpeg\n\n",
 
    # Search for that file
    file = open(name, mode="rb");
    if  file:
        a = file.read();
        print a,

    sys.exit()

# Create a web page
print "Content-type: text/html\n\n",
print "<html><head><title>Example Comic Page</title>"
print """
<style>
body {
    font-family: "Trebuchet MS";
}

h1 {
    font-family: "Comic Sans MS";
}
span.link {
    color: blue;
    text-decoration: underline;
    cursor: pointer;
}
</style>
</head><body>
<center><h1>
Example Comics Page</h1>
For demonstration purposes only. Please don't sue me.
</center>
<script type="text/javascript">
function myback(id, next)
{
    for( i = 0; i < comics.arr.length; i++ ) {
        if ( comics.arr[i].name == id ) {
            break
        }
    }
    
    if ( i == comics.arr.length ) {
        alert("Not found! Error tell Steve.");
        return false
    }

    comic = comics.arr[i]

    elem = document.getElementById(id)

    if ( next && comic.current < comic.dates.length-1 ) {
        comic.current++
    } else if ( !next && comic.current > 0 ) {
        comic.current--
    }

    elem.src = "?id=" + comic.dates[comic.current]

    return false
}

var comics = {
    "arr" : [
"""

afirst = True
for comic in comics:
    keys = comic.comics.keys()
    keys.sort()
    if not afirst:
        print ",\n      {"
    else:
        print "\n      {"

    print '            "name": "%s",' % (comic.idname)
    print '            "current": %s,' % (len(keys)-1)
    print '            "dates" : [',
    first = True
    for key in keys:
        if not first:
            print ", ",
        print '\"%s\"' % (comic.comics[key]),
        first = False

    print "]\n        }",
    afirst = False

print """
    ]
}
</script>
"""

# For each comic in the database, print it to the page.
for comic in comics:
    keys = comic.comics.keys()
    keys.sort()
    if len( keys ) == 0:
        continue

    first = comic.comics[keys[-1]];

    print "<hr><center><h1>" + comic.name + "</h1>"
    print "<p>"
    print "<span class=link onclick=\"myback('%s',false)\">Previous</span> |" % (comic.idname)
    print "<span class=link onclick=\"myback('%s',true)\">Next</span><p>" % (comic.idname)

    print "<img id=" + comic.idname+" src=\"?id=" + first + "\">"
    print "</center>"

print "</body></html>"
