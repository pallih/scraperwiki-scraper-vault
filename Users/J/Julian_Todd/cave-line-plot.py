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
var paper = Raphael(10, 50, 320, 200);

var d = %s; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+d[i][1]+" "+d[i][2]+"L"+d[i][4]+" "+d[i][5]);
}""" % json.dumps(list(data))



print '<html><head><script src="http://raphaeljs.com/raphael.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'
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
var paper = Raphael(10, 50, 320, 200);

var d = %s; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+d[i][1]+" "+d[i][2]+"L"+d[i][4]+" "+d[i][5]);
}""" % json.dumps(list(data))



print '<html><head><script src="http://raphaeljs.com/raphael.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'
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
var paper = Raphael(10, 50, 320, 200);

var d = %s; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+d[i][1]+" "+d[i][2]+"L"+d[i][4]+" "+d[i][5]);
}""" % json.dumps(list(data))



print '<html><head><script src="http://raphaeljs.com/raphael.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'
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
var paper = Raphael(10, 50, 320, 200);

var d = %s; 

for (var i = 0; i < d.length; i++)
    var c = paper.path("M"+d[i][1]+" "+d[i][2]+"L"+d[i][4]+" "+d[i][5]);
}""" % json.dumps(list(data))



print '<html><head><script src="http://raphaeljs.com/raphael.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'
