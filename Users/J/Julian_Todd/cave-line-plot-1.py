import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
import sqlite3
import urllib
import tempfile
import json
import scraperwiki
scraperwiki.cache(True)

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = c.execute("""SELECT coalesce(eqfrom.eto, sfrom) AS cfrom, stfrom.x, stfrom.y,
                             coalesce(eqto.eto, sto) AS cto, stto.x, stto.y FROM legs
                      LEFT JOIN equates AS eqfrom ON eqfrom.efrom = sfrom 
                      LEFT JOIN equates AS eqto ON eqto.efrom = sto
                      LEFT JOIN stations AS stfrom ON cfrom = stfrom.station
                      LEFT JOIN stations AS stto ON cto = stto.station""")


jcode = """
window.onload = function() {
var paper = Raphael("rrr", 400, 400);

var d = %s; 

function h(x) { return (x+70)*2 }; 
function v(x) { return 350-(x+70)*2 }; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+h(d[i][1])+" "+v(d[i][2])+"L"+h(d[i][4])+" "+v(d[i][5]));
}""" % json.dumps(list(data))



print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of plotting the centreline of a cave using <a href="http://raphaeljs.com/">raphael</a> technology</h4>'
print '<div id="rrr" style="height:400px; width:400px; background:#eee"></div></body></html>'
