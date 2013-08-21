scrapername = 'uk-offshore-oil-wells'

import simplejson as json
import urllib2


def Main():
    datalist = LoadData(scrapername)
    chartdata = { }
    for data in datalist:
        month = data["Spud_Date"][:7]
        lookup = chartdata.setdefault(month, {"Exploration":0, "Development":0})
        lookup[data["Original_Intent"]] = lookup.setdefault(data["Original_Intent"], 0) + 1
    print htmlheader
    print "jdata = %s;" % json.dumps(sorted(chartdata.items()))
    print makechart
    print footer
    
    

# load all data a scraper that we can work with (this might be part of scraperlibs)
def LoadData(scrapername):
    llimit = 100
    offset = 0
    limit = 4000
    result = [ ]
    while True:
        url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&name=%s&limit=%s&offset=%d" % (scrapername, llimit, offset)
        a = urllib2.urlopen(url).read()
        lresult = json.loads(a)
        result.extend(lresult)
        if len(lresult) < llimit:
            break
        if len(result) > limit:
            break
        #print len(result)
        offset += llimit
    return result

    
htmlheader = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
google.load('visualization', '1', {'packages':['annotatedtimeline']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdata.length);
    data.addColumn('date', 'Month');
    data.addColumn('number', 'Exploration');
    data.addColumn('number', 'Development');
    for (i = 0; i < jdata.length; i++) 
    {
        smonth = jdata[i][0]; 
        month = new Date(parseInt(smonth.substring(0, 4)), parseInt(smonth.substring(5, 7)), 1)
        data.setValue(i, 0, month);
        data.setValue(i, 1, jdata[i][1]["Exploration"]);  // Appraisal, Development
        data.setValue(i, 2, jdata[i][1]["Development"]);  // Appraisal, Development
    }

    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));
    chart.draw(data, {displayAnnotations: true});
};
"""



footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">North sea exploration and development</h2>
<div id="visualization" style="width: 800px; height: 600px;"></div>
</body>
</html>
"""
     
     
Main()

scrapername = 'uk-offshore-oil-wells'

import simplejson as json
import urllib2


def Main():
    datalist = LoadData(scrapername)
    chartdata = { }
    for data in datalist:
        month = data["Spud_Date"][:7]
        lookup = chartdata.setdefault(month, {"Exploration":0, "Development":0})
        lookup[data["Original_Intent"]] = lookup.setdefault(data["Original_Intent"], 0) + 1
    print htmlheader
    print "jdata = %s;" % json.dumps(sorted(chartdata.items()))
    print makechart
    print footer
    
    

# load all data a scraper that we can work with (this might be part of scraperlibs)
def LoadData(scrapername):
    llimit = 100
    offset = 0
    limit = 4000
    result = [ ]
    while True:
        url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&name=%s&limit=%s&offset=%d" % (scrapername, llimit, offset)
        a = urllib2.urlopen(url).read()
        lresult = json.loads(a)
        result.extend(lresult)
        if len(lresult) < llimit:
            break
        if len(result) > limit:
            break
        #print len(result)
        offset += llimit
    return result

    
htmlheader = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
google.load('visualization', '1', {'packages':['annotatedtimeline']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdata.length);
    data.addColumn('date', 'Month');
    data.addColumn('number', 'Exploration');
    data.addColumn('number', 'Development');
    for (i = 0; i < jdata.length; i++) 
    {
        smonth = jdata[i][0]; 
        month = new Date(parseInt(smonth.substring(0, 4)), parseInt(smonth.substring(5, 7)), 1)
        data.setValue(i, 0, month);
        data.setValue(i, 1, jdata[i][1]["Exploration"]);  // Appraisal, Development
        data.setValue(i, 2, jdata[i][1]["Development"]);  // Appraisal, Development
    }

    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));
    chart.draw(data, {displayAnnotations: true});
};
"""



footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">North sea exploration and development</h2>
<div id="visualization" style="width: 800px; height: 600px;"></div>
</body>
</html>
"""
     
     
Main()

scrapername = 'uk-offshore-oil-wells'

import simplejson as json
import urllib2


def Main():
    datalist = LoadData(scrapername)
    chartdata = { }
    for data in datalist:
        month = data["Spud_Date"][:7]
        lookup = chartdata.setdefault(month, {"Exploration":0, "Development":0})
        lookup[data["Original_Intent"]] = lookup.setdefault(data["Original_Intent"], 0) + 1
    print htmlheader
    print "jdata = %s;" % json.dumps(sorted(chartdata.items()))
    print makechart
    print footer
    
    

# load all data a scraper that we can work with (this might be part of scraperlibs)
def LoadData(scrapername):
    llimit = 100
    offset = 0
    limit = 4000
    result = [ ]
    while True:
        url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&name=%s&limit=%s&offset=%d" % (scrapername, llimit, offset)
        a = urllib2.urlopen(url).read()
        lresult = json.loads(a)
        result.extend(lresult)
        if len(lresult) < llimit:
            break
        if len(result) > limit:
            break
        #print len(result)
        offset += llimit
    return result

    
htmlheader = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
google.load('visualization', '1', {'packages':['annotatedtimeline']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdata.length);
    data.addColumn('date', 'Month');
    data.addColumn('number', 'Exploration');
    data.addColumn('number', 'Development');
    for (i = 0; i < jdata.length; i++) 
    {
        smonth = jdata[i][0]; 
        month = new Date(parseInt(smonth.substring(0, 4)), parseInt(smonth.substring(5, 7)), 1)
        data.setValue(i, 0, month);
        data.setValue(i, 1, jdata[i][1]["Exploration"]);  // Appraisal, Development
        data.setValue(i, 2, jdata[i][1]["Development"]);  // Appraisal, Development
    }

    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));
    chart.draw(data, {displayAnnotations: true});
};
"""



footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">North sea exploration and development</h2>
<div id="visualization" style="width: 800px; height: 600px;"></div>
</body>
</html>
"""
     
     
Main()

scrapername = 'uk-offshore-oil-wells'

import simplejson as json
import urllib2


def Main():
    datalist = LoadData(scrapername)
    chartdata = { }
    for data in datalist:
        month = data["Spud_Date"][:7]
        lookup = chartdata.setdefault(month, {"Exploration":0, "Development":0})
        lookup[data["Original_Intent"]] = lookup.setdefault(data["Original_Intent"], 0) + 1
    print htmlheader
    print "jdata = %s;" % json.dumps(sorted(chartdata.items()))
    print makechart
    print footer
    
    

# load all data a scraper that we can work with (this might be part of scraperlibs)
def LoadData(scrapername):
    llimit = 100
    offset = 0
    limit = 4000
    result = [ ]
    while True:
        url = "http://api.scraperwiki.com/api/1.0/datastore/getdata?&name=%s&limit=%s&offset=%d" % (scrapername, llimit, offset)
        a = urllib2.urlopen(url).read()
        lresult = json.loads(a)
        result.extend(lresult)
        if len(lresult) < llimit:
            break
        if len(result) > limit:
            break
        #print len(result)
        offset += llimit
    return result

    
htmlheader = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Google Visualization API Sample</title>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
google.load('visualization', '1', {packages: ['BarChart']});
google.load('visualization', '1', {'packages':['annotatedtimeline']});
"""


makechart = """
function realcall()
{
    var data = new google.visualization.DataTable();
    data.addRows(jdata.length);
    data.addColumn('date', 'Month');
    data.addColumn('number', 'Exploration');
    data.addColumn('number', 'Development');
    for (i = 0; i < jdata.length; i++) 
    {
        smonth = jdata[i][0]; 
        month = new Date(parseInt(smonth.substring(0, 4)), parseInt(smonth.substring(5, 7)), 1)
        data.setValue(i, 0, month);
        data.setValue(i, 1, jdata[i][1]["Exploration"]);  // Appraisal, Development
        data.setValue(i, 2, jdata[i][1]["Development"]);  // Appraisal, Development
    }

    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));
    chart.draw(data, {displayAnnotations: true});
};
"""



footer = """
google.setOnLoadCallback(realcall);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">North sea exploration and development</h2>
<div id="visualization" style="width: 800px; height: 600px;"></div>
</body>
</html>
"""
     
     
Main()

