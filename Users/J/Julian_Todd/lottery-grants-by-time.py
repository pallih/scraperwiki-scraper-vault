# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

# Complex template for setting up an annotated timeline
# see http://code.google.com/apis/visualization/documentation/gallery/annotatedtimeline.html

scrapername = 'uk-lottery-grants'

import json
#from scraperwiki.api import getData

# convert a data point into a date and a category
# in this case we are keeping only the year and 
# describing the intent accordingly
def DataCategory(data):
    region = data.get("Region")
    if not region:
        region = "None"
    if region not in categories:
        #print region
        region = "Other"
    d = data.get("date")
    return d[:10], region 

categories = ["London", "East Midlands", "South East", "South West", "North West", "North East", "Eastern", "Wales", "Scotland", "Yorkshire and Humberside", "West Midlands", "Northern Ireland", "None", "Other"]
#categories = ["None"]

# code that generates the necessary javascript to fill the timeline
def Main():
    chartdata = { }
    for data in getDataByDate(scrapername, start_date="2007-01-01", end_date="2007-12-01", limit=4500):
        d, cat = DataCategory(data)
        if not d:
            continue
        icat = categories.index(cat)
        if d not in chartdata:
            chartdata[d] = [d] + [0]*len(categories)

        chartdata[d][icat+1] += int(data.get("Award_Amount", 0))
        #print data
        
        
    # now generate the html/javascript output
    print part1
    print "    var jdata = %s;" % json.dumps(sorted(chartdata.values()))
    print "    data.addRows(jdata.length);"
    print "    data.addColumn('date', 'Year');"
    for cat in categories:
        print "    data.addColumn('number', '%s');" % cat
    print "    for (var i = 0; i < jdata.length; i++)"
    print "    {"
    print "        sdate = jdata[i][0];" 
    print "        d = new Date(parseInt(sdate.substring(0, 4)), parseInt(sdate.substring(5, 7)), parseInt(sdate.substring(8, 10)))"
    print "        data.setValue(i, 0, d);"
    for j in range(len(categories)):
        print "    data.setValue(i, %d, jdata[i][%d]);" % (j+1, j+1)
    print "    }"
    print "    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('visualization'));"
    print "    chart.draw(data, {displayAnnotations: true});"
    print "}"
    print part3
    
    
# boilerplate html and javascript code included above
part1 = """
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

function loaddata()
{
    var data = new google.visualization.DataTable();
"""

part3 = """
google.setOnLoadCallback(loaddata);

</script>
</head>
<body style="font-family: Arial;border: 0 none;">
<h2 id="message">Lottery spend by region</h2>
<div id="visualization" style="width: 800px; height: 300px;"></div>
</body>
</html>
"""
     
     
     
### code to be moved to scraperlibs     
import urllib
import json

apiurl = "http://api.scraperwiki.com/api/1.0/datastore/"
apilimit = 500

def generateData(urlbase, limit, offset):
    count = 0
    loffset = 0
    while True:
        if limit == -1:
            llimit = apilimit
        else:
            llimit = min(apilimit, limit-count)
            
        url = "%s&limit=%s&offset=%d" % (urlbase, llimit, offset+loffset)
        ljson = urllib.urlopen(url).read()
        lresult = json.loads(ljson)
        for row in lresult:
            yield row

        count += len(lresult)
           
        if len(lresult) < llimit:  # run out of records
            break
            
        if limit != -1 and count >= limit:    # exceeded the limit
            break

        loffset += llimit

def getData(name, limit=-1, offset=0):
    urlbase = "%sgetdata?name=%s" % (apiurl, name)
    return generateData(urlbase, limit, offset)

def getDataByDate(name, start_date, end_date, limit=-1, offset=0):
    urlbase = "%sgetdatabydate?name=%s&start_date=%s&end_date=%s" % (apiurl, name, start_date, end_date)
    return generateData(urlbase, limit, offset)

## leave this in the scraper
Main()

