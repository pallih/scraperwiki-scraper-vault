import urllib
import tempfile
import sqlite3
import simplejson as json
import os
import cgi


numberrecords = 10
scrapername = 'vca-car-fuel-data'

import scraperwiki
print scraperwiki.sqlite.attach('vca-car-fuel-data', "src")




# main
def CreateDatalist(makeselect):

    makecount = dict(scraperwiki.sqlite.execute("select make, count(*) from src.swdata group by make")["data"])
    totalcars = sum(makecount.values())
    onecars = makecount[makeselect]

    callmakes = scraperwiki.sqlite.execute('select labelletter, 100*count(*)/%f from src.swdata group by labelletter order by labelletter' % totalcars)
    allmakes = dict(callmakes["data"])
    conemake = scraperwiki.sqlite.execute(('select labelletter, 100*count(*)/%f from src.swdata where make=? group by labelletter '+\
                                          'order by labelletter') % onecars, (makeselect,))
    onemake = dict(conemake["data"])
    datalist = [ (letter, allmakes.get(letter, 0), onemake.get(letter, 0))  for letter in 'ABCDEFGHIJKLM' ]

    htmlpre = "<p>There are %d car variants in total, %d of which are %s.</p>" % (totalcars, onecars, makeselect)

    ccarlinklist = scraperwiki.sqlite.execute('select make, count(*) from src.swdata group by make order by make')
    carlinklist = [ '<a href="?%s">%s</a> (%d variants)' % (urllib.urlencode({'make':make}), make, count)  for make, count in ccarlinklist["data"] ]
    htmlpost = "<ul><li>%s</li></ul>" % "</li><li>".join(carlinklist)
    
    return datalist, htmlpre, htmlpost

                
def Main():
    makeselect = 'BMW'
    lmake = cgi.parse_qs(os.getenv("URLQUERY")).get("make")
    if lmake:
        makeselect = lmake[0]

    print header
    datalist, htmlpre, htmlpost = CreateDatalist(makeselect)
    print 'var jdatalist = %s;' % json.dumps(datalist)
    print makechart % makeselect
    print footer % (htmlpre, htmlpost)

                
header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdatalist.length);
    data.addColumn('string', 'Efficiency Letter');
    data.addColumn('number', 'All cars');
    data.addColumn('number', '%s cars');
    for (i = 0; i < jdatalist.length; i++) 
    {
        data.setValue(i, 0, jdatalist[i][0]);
        data.setValue(i, 1, jdatalist[i][1]);
        data.setValue(i, 2, jdatalist[i][2]);
    }
      
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 300, title: 'Percentage of car variants on sale in each VED band', vAxis: {title: 'Letter', titleColor: 'red'} });
};"""

footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
%s
<div id="visualization" style="width: 800px; height: 300px;"></div>
<a href="http://www.vcacarfueldata.org.uk/search/vedSearch.asp">VED band definitions</a>
%s
</body>
</html>
"""

Main()
     import urllib
import tempfile
import sqlite3
import simplejson as json
import os
import cgi


numberrecords = 10
scrapername = 'vca-car-fuel-data'

import scraperwiki
print scraperwiki.sqlite.attach('vca-car-fuel-data', "src")




# main
def CreateDatalist(makeselect):

    makecount = dict(scraperwiki.sqlite.execute("select make, count(*) from src.swdata group by make")["data"])
    totalcars = sum(makecount.values())
    onecars = makecount[makeselect]

    callmakes = scraperwiki.sqlite.execute('select labelletter, 100*count(*)/%f from src.swdata group by labelletter order by labelletter' % totalcars)
    allmakes = dict(callmakes["data"])
    conemake = scraperwiki.sqlite.execute(('select labelletter, 100*count(*)/%f from src.swdata where make=? group by labelletter '+\
                                          'order by labelletter') % onecars, (makeselect,))
    onemake = dict(conemake["data"])
    datalist = [ (letter, allmakes.get(letter, 0), onemake.get(letter, 0))  for letter in 'ABCDEFGHIJKLM' ]

    htmlpre = "<p>There are %d car variants in total, %d of which are %s.</p>" % (totalcars, onecars, makeselect)

    ccarlinklist = scraperwiki.sqlite.execute('select make, count(*) from src.swdata group by make order by make')
    carlinklist = [ '<a href="?%s">%s</a> (%d variants)' % (urllib.urlencode({'make':make}), make, count)  for make, count in ccarlinklist["data"] ]
    htmlpost = "<ul><li>%s</li></ul>" % "</li><li>".join(carlinklist)
    
    return datalist, htmlpre, htmlpost

                
def Main():
    makeselect = 'BMW'
    lmake = cgi.parse_qs(os.getenv("URLQUERY")).get("make")
    if lmake:
        makeselect = lmake[0]

    print header
    datalist, htmlpre, htmlpost = CreateDatalist(makeselect)
    print 'var jdatalist = %s;' % json.dumps(datalist)
    print makechart % makeselect
    print footer % (htmlpre, htmlpost)

                
header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdatalist.length);
    data.addColumn('string', 'Efficiency Letter');
    data.addColumn('number', 'All cars');
    data.addColumn('number', '%s cars');
    for (i = 0; i < jdatalist.length; i++) 
    {
        data.setValue(i, 0, jdatalist[i][0]);
        data.setValue(i, 1, jdatalist[i][1]);
        data.setValue(i, 2, jdatalist[i][2]);
    }
      
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 300, title: 'Percentage of car variants on sale in each VED band', vAxis: {title: 'Letter', titleColor: 'red'} });
};"""

footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
%s
<div id="visualization" style="width: 800px; height: 300px;"></div>
<a href="http://www.vcacarfueldata.org.uk/search/vedSearch.asp">VED band definitions</a>
%s
</body>
</html>
"""

Main()
     import urllib
import tempfile
import sqlite3
import simplejson as json
import os
import cgi


numberrecords = 10
scrapername = 'vca-car-fuel-data'

import scraperwiki
print scraperwiki.sqlite.attach('vca-car-fuel-data', "src")




# main
def CreateDatalist(makeselect):

    makecount = dict(scraperwiki.sqlite.execute("select make, count(*) from src.swdata group by make")["data"])
    totalcars = sum(makecount.values())
    onecars = makecount[makeselect]

    callmakes = scraperwiki.sqlite.execute('select labelletter, 100*count(*)/%f from src.swdata group by labelletter order by labelletter' % totalcars)
    allmakes = dict(callmakes["data"])
    conemake = scraperwiki.sqlite.execute(('select labelletter, 100*count(*)/%f from src.swdata where make=? group by labelletter '+\
                                          'order by labelletter') % onecars, (makeselect,))
    onemake = dict(conemake["data"])
    datalist = [ (letter, allmakes.get(letter, 0), onemake.get(letter, 0))  for letter in 'ABCDEFGHIJKLM' ]

    htmlpre = "<p>There are %d car variants in total, %d of which are %s.</p>" % (totalcars, onecars, makeselect)

    ccarlinklist = scraperwiki.sqlite.execute('select make, count(*) from src.swdata group by make order by make')
    carlinklist = [ '<a href="?%s">%s</a> (%d variants)' % (urllib.urlencode({'make':make}), make, count)  for make, count in ccarlinklist["data"] ]
    htmlpost = "<ul><li>%s</li></ul>" % "</li><li>".join(carlinklist)
    
    return datalist, htmlpre, htmlpost

                
def Main():
    makeselect = 'BMW'
    lmake = cgi.parse_qs(os.getenv("URLQUERY")).get("make")
    if lmake:
        makeselect = lmake[0]

    print header
    datalist, htmlpre, htmlpost = CreateDatalist(makeselect)
    print 'var jdatalist = %s;' % json.dumps(datalist)
    print makechart % makeselect
    print footer % (htmlpre, htmlpost)

                
header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdatalist.length);
    data.addColumn('string', 'Efficiency Letter');
    data.addColumn('number', 'All cars');
    data.addColumn('number', '%s cars');
    for (i = 0; i < jdatalist.length; i++) 
    {
        data.setValue(i, 0, jdatalist[i][0]);
        data.setValue(i, 1, jdatalist[i][1]);
        data.setValue(i, 2, jdatalist[i][2]);
    }
      
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 300, title: 'Percentage of car variants on sale in each VED band', vAxis: {title: 'Letter', titleColor: 'red'} });
};"""

footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
%s
<div id="visualization" style="width: 800px; height: 300px;"></div>
<a href="http://www.vcacarfueldata.org.uk/search/vedSearch.asp">VED band definitions</a>
%s
</body>
</html>
"""

Main()
     import urllib
import tempfile
import sqlite3
import simplejson as json
import os
import cgi


numberrecords = 10
scrapername = 'vca-car-fuel-data'

import scraperwiki
print scraperwiki.sqlite.attach('vca-car-fuel-data', "src")




# main
def CreateDatalist(makeselect):

    makecount = dict(scraperwiki.sqlite.execute("select make, count(*) from src.swdata group by make")["data"])
    totalcars = sum(makecount.values())
    onecars = makecount[makeselect]

    callmakes = scraperwiki.sqlite.execute('select labelletter, 100*count(*)/%f from src.swdata group by labelletter order by labelletter' % totalcars)
    allmakes = dict(callmakes["data"])
    conemake = scraperwiki.sqlite.execute(('select labelletter, 100*count(*)/%f from src.swdata where make=? group by labelletter '+\
                                          'order by labelletter') % onecars, (makeselect,))
    onemake = dict(conemake["data"])
    datalist = [ (letter, allmakes.get(letter, 0), onemake.get(letter, 0))  for letter in 'ABCDEFGHIJKLM' ]

    htmlpre = "<p>There are %d car variants in total, %d of which are %s.</p>" % (totalcars, onecars, makeselect)

    ccarlinklist = scraperwiki.sqlite.execute('select make, count(*) from src.swdata group by make order by make')
    carlinklist = [ '<a href="?%s">%s</a> (%d variants)' % (urllib.urlencode({'make':make}), make, count)  for make, count in ccarlinklist["data"] ]
    htmlpost = "<ul><li>%s</li></ul>" % "</li><li>".join(carlinklist)
    
    return datalist, htmlpre, htmlpost

                
def Main():
    makeselect = 'BMW'
    lmake = cgi.parse_qs(os.getenv("URLQUERY")).get("make")
    if lmake:
        makeselect = lmake[0]

    print header
    datalist, htmlpre, htmlpost = CreateDatalist(makeselect)
    print 'var jdatalist = %s;' % json.dumps(datalist)
    print makechart % makeselect
    print footer % (htmlpre, htmlpost)

                
header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdatalist.length);
    data.addColumn('string', 'Efficiency Letter');
    data.addColumn('number', 'All cars');
    data.addColumn('number', '%s cars');
    for (i = 0; i < jdatalist.length; i++) 
    {
        data.setValue(i, 0, jdatalist[i][0]);
        data.setValue(i, 1, jdatalist[i][1]);
        data.setValue(i, 2, jdatalist[i][2]);
    }
      
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 300, title: 'Percentage of car variants on sale in each VED band', vAxis: {title: 'Letter', titleColor: 'red'} });
};"""

footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
%s
<div id="visualization" style="width: 800px; height: 300px;"></div>
<a href="http://www.vcacarfueldata.org.uk/search/vedSearch.asp">VED band definitions</a>
%s
</body>
</html>
"""

Main()
     import urllib
import tempfile
import sqlite3
import simplejson as json
import os
import cgi


numberrecords = 10
scrapername = 'vca-car-fuel-data'

import scraperwiki
print scraperwiki.sqlite.attach('vca-car-fuel-data', "src")




# main
def CreateDatalist(makeselect):

    makecount = dict(scraperwiki.sqlite.execute("select make, count(*) from src.swdata group by make")["data"])
    totalcars = sum(makecount.values())
    onecars = makecount[makeselect]

    callmakes = scraperwiki.sqlite.execute('select labelletter, 100*count(*)/%f from src.swdata group by labelletter order by labelletter' % totalcars)
    allmakes = dict(callmakes["data"])
    conemake = scraperwiki.sqlite.execute(('select labelletter, 100*count(*)/%f from src.swdata where make=? group by labelletter '+\
                                          'order by labelletter') % onecars, (makeselect,))
    onemake = dict(conemake["data"])
    datalist = [ (letter, allmakes.get(letter, 0), onemake.get(letter, 0))  for letter in 'ABCDEFGHIJKLM' ]

    htmlpre = "<p>There are %d car variants in total, %d of which are %s.</p>" % (totalcars, onecars, makeselect)

    ccarlinklist = scraperwiki.sqlite.execute('select make, count(*) from src.swdata group by make order by make')
    carlinklist = [ '<a href="?%s">%s</a> (%d variants)' % (urllib.urlencode({'make':make}), make, count)  for make, count in ccarlinklist["data"] ]
    htmlpost = "<ul><li>%s</li></ul>" % "</li><li>".join(carlinklist)
    
    return datalist, htmlpre, htmlpost

                
def Main():
    makeselect = 'BMW'
    lmake = cgi.parse_qs(os.getenv("URLQUERY")).get("make")
    if lmake:
        makeselect = lmake[0]

    print header
    datalist, htmlpre, htmlpost = CreateDatalist(makeselect)
    print 'var jdatalist = %s;' % json.dumps(datalist)
    print makechart % makeselect
    print footer % (htmlpre, htmlpost)

                
header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdatalist.length);
    data.addColumn('string', 'Efficiency Letter');
    data.addColumn('number', 'All cars');
    data.addColumn('number', '%s cars');
    for (i = 0; i < jdatalist.length; i++) 
    {
        data.setValue(i, 0, jdatalist[i][0]);
        data.setValue(i, 1, jdatalist[i][1]);
        data.setValue(i, 2, jdatalist[i][2]);
    }
      
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 300, title: 'Percentage of car variants on sale in each VED band', vAxis: {title: 'Letter', titleColor: 'red'} });
};"""

footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
%s
<div id="visualization" style="width: 800px; height: 300px;"></div>
<a href="http://www.vcacarfueldata.org.uk/search/vedSearch.asp">VED band definitions</a>
%s
</body>
</html>
"""

Main()
     