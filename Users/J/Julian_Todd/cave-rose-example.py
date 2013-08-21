import sqlite3
import urllib
import tempfile
import json
import scraperwiki

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = [ ]
for l, n, g in c.execute('select sum(tape), count(*), round(compass/10) as g from legs group by g'):
    data.append((g*10, l))

jcode = """
window.onload = function() {
var paper = Raphael(10, 50, 320, 200);
var rad = Math.PI / 180;

function sector(cx, cy, r, startAngle, endAngle, params) 
{
    var x1 = cx + r * Math.cos(-startAngle * rad),
            x2 = cx + r * Math.cos(-endAngle * rad),
            y1 = cy + r * Math.sin(-startAngle * rad),
            y2 = cy + r * Math.sin(-endAngle * rad);
    return paper.path(["M", cx, cy, "L", x1, y1, "A", r, r, 0, +(endAngle - startAngle > 180), 0, x2, y2, "z"]).attr(params);
}

var data = %s; 

color = "hsb(0.1, 1, .5)"; 
bcolor = "hsb(0.3, 1, 1)"; 
for (var i = 0; i < data.length; i++)
    p = sector(150, 100, data[i][1], data[i][0], data[i][0]+10, {gradient: "90-" + bcolor + "-" + color, stroke: "#000", "stroke-width": 2}); 

}
""" % json.dumps(data)

print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'

import sqlite3
import urllib
import tempfile
import json
import scraperwiki

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = [ ]
for l, n, g in c.execute('select sum(tape), count(*), round(compass/10) as g from legs group by g'):
    data.append((g*10, l))

jcode = """
window.onload = function() {
var paper = Raphael(10, 50, 320, 200);
var rad = Math.PI / 180;

function sector(cx, cy, r, startAngle, endAngle, params) 
{
    var x1 = cx + r * Math.cos(-startAngle * rad),
            x2 = cx + r * Math.cos(-endAngle * rad),
            y1 = cy + r * Math.sin(-startAngle * rad),
            y2 = cy + r * Math.sin(-endAngle * rad);
    return paper.path(["M", cx, cy, "L", x1, y1, "A", r, r, 0, +(endAngle - startAngle > 180), 0, x2, y2, "z"]).attr(params);
}

var data = %s; 

color = "hsb(0.1, 1, .5)"; 
bcolor = "hsb(0.3, 1, 1)"; 
for (var i = 0; i < data.length; i++)
    p = sector(150, 100, data[i][1], data[i][0], data[i][0]+10, {gradient: "90-" + bcolor + "-" + color, stroke: "#000", "stroke-width": 2}); 

}
""" % json.dumps(data)

print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'

import sqlite3
import urllib
import tempfile
import json
import scraperwiki

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = [ ]
for l, n, g in c.execute('select sum(tape), count(*), round(compass/10) as g from legs group by g'):
    data.append((g*10, l))

jcode = """
window.onload = function() {
var paper = Raphael(10, 50, 320, 200);
var rad = Math.PI / 180;

function sector(cx, cy, r, startAngle, endAngle, params) 
{
    var x1 = cx + r * Math.cos(-startAngle * rad),
            x2 = cx + r * Math.cos(-endAngle * rad),
            y1 = cy + r * Math.sin(-startAngle * rad),
            y2 = cy + r * Math.sin(-endAngle * rad);
    return paper.path(["M", cx, cy, "L", x1, y1, "A", r, r, 0, +(endAngle - startAngle > 180), 0, x2, y2, "z"]).attr(params);
}

var data = %s; 

color = "hsb(0.1, 1, .5)"; 
bcolor = "hsb(0.3, 1, 1)"; 
for (var i = 0; i < data.length; i++)
    p = sector(150, 100, data[i][1], data[i][0], data[i][0]+10, {gradient: "90-" + bcolor + "-" + color, stroke: "#000", "stroke-width": 2}); 

}
""" % json.dumps(data)

print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'

import sqlite3
import urllib
import tempfile
import json
import scraperwiki

temp = tempfile.NamedTemporaryFile()
contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/kforgecavedatastations").read()
open(temp.name, "wb").write(contents)

conn = sqlite3.connect(temp.name)
c = conn.cursor()

data = [ ]
for l, n, g in c.execute('select sum(tape), count(*), round(compass/10) as g from legs group by g'):
    data.append((g*10, l))

jcode = """
window.onload = function() {
var paper = Raphael(10, 50, 320, 200);
var rad = Math.PI / 180;

function sector(cx, cy, r, startAngle, endAngle, params) 
{
    var x1 = cx + r * Math.cos(-startAngle * rad),
            x2 = cx + r * Math.cos(-endAngle * rad),
            y1 = cy + r * Math.sin(-startAngle * rad),
            y2 = cy + r * Math.sin(-endAngle * rad);
    return paper.path(["M", cx, cy, "L", x1, y1, "A", r, r, 0, +(endAngle - startAngle > 180), 0, x2, y2, "z"]).attr(params);
}

var data = %s; 

color = "hsb(0.1, 1, .5)"; 
bcolor = "hsb(0.3, 1, 1)"; 
for (var i = 0; i < data.length; i++)
    p = sector(150, 100, data[i][1], data[i][0], data[i][0]+10, {gradient: "90-" + bcolor + "-" + color, stroke: "#000", "stroke-width": 2}); 

}
""" % json.dumps(data)

print '<html><head><script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode
print '<h4>This is an example of a cave rose using <a href="http://raphaeljs.com/">raphael</a> technology</h4></body></html>'

