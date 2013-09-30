import scraperwiki
import gviz_api

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'typ' in get:
        table='xlsReturns_'+get['typ']
        tablename=table
    else: 
        table='xlsReturns'
        tablename="Local councils"
    #university, department, parish_council,npte,nhsTrust_and_PCT, non_ministerial_department,executive_agency
else:
    table='xlsReturns'
    tablename="Local councils"

def ascii(s): return "".join(i for i in s if ord(i)<128)

tablename=ascii(tablename)

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html


page_template = """
<html><head><title>Spreadsheet Returning FOI Responses via WhatDoTheyKnow</title>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="http://visapi-gadgets.googlecode.com/svn/trunk/wordcloud/wc.css"/>
    <script type="text/javascript" src="http://visapi-gadgets.googlecode.com/svn/trunk/wordcloud/wc.js"></script>
  <script>
    google.load('visualization', '1.1', {packages:['controls']});

    google.setOnLoadCallback(drawTable);

    function drawTable() {

      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
   

    var json_table = new google.visualization.ChartWrapper({'chartType': 'Table','containerId':'table_div_json','options': {allowHtml: true,page:'enable',pageSize:50 , 'pagingSymbols': {prev: 'prev', next: 'next'}}});

    var formatter = new google.visualization.PatternFormat('<a href="http://www.whatdotheyknow.com{1}">{0}</a>');
    formatter.format(json_data, [0,2]); 

//http://www.whatdotheyknow.com/body/kent_county_council
    formatter = new google.visualization.PatternFormat('<a href="http://www.whatdotheyknow.com/body/{0}">{0}</a>');
    formatter.format(json_data, [1]); 

    var view = new google.visualization.DataView(json_data);
    view.setColumns([0,1])


    var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'Request',
        'matchType': 'any'
      }
    });

 /*
var slider = new google.visualization.ControlWrapper({
    'controlType': 'NumberRangeFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Laptime (s)',
      'minValue': 90,
      'maxValue': 150
    }
  });


   var posFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control3',
      'options': {
        'filterColumnLabel': 'Position',
        'matchType': 'any'
      }
    });
*/
var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Council',
      'ui': {
      'labelStacking': 'vertical',
        'allowTyping': false,
        'allowMultiple': false
      }
    }
  });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind(stringFilter,categoryPicker).bind([categoryPicker], json_table).draw(view);

var outputDiv = document.getElementById('wcdiv');
        var wc = new WordCloud(outputDiv);
        wc.draw(view, {stopWords: 'a an and is or the of for to by in on with into mod dh dfe dcsf moj'});

    }
  </script></head>
  <body>
<h1>WhatDoTheyKnow FOI Requests Returning Data</h1>
<div>Search a particular class of organisation on WhatDoTheyKnow for FOI requests that received one or more responses containing XLS (Excel spreadsheet) data files.</div>
<div>Default is to search over <em>local councils</em>; to search other body types, add <em>?typ=<strong>TYP</strong></em> to the URL of this page where <em>TYP</em> is one of : <tt>university, department, parish_council,npte,nhsTrust_and_PCT, non_ministerial_department,executive_agency</tt></div>
<div><em>Request</em> allows you to filter results according to a particular word or phrase; the <em>Council</em> drop down list is populated with council names that return results in the filtered list after the filter term (if any) is applied.</div>
<div>For a little bit of background context that lead to the development of this scraper/view, see <a href="http://blog.ouseful.info/2012/04/24/foi-signals-on-useful-open-data/">OUseful.info: FOI Signals on Useful Open Data?</a></div>

<div id="dashboard">
    <div id="control1"></div><div id="control2"></div><div id="control3"></div>
    <div id="table_div_json"></div>
</div>
<div>The wordcloud widget is a crude one and runs over the complete (unfiltered) list for this <tt>typ</tt> of data.</div>
<div id="wcdiv"></div>
<script type="text/javascript" language="javascript"
src="http://static.polldaddy.com/p/6167043.js"></script>
<noscript>
<a href="http://polldaddy.com/poll/6167043/">What percentage of your FOI requests come from whatdotheyknow?</a><br/>
<span style="font:9px;">(<a href="http://www.polldaddy.com">polls</a>)</span>
</noscript>
  </body>
</html>
"""


sourcescraper = 'whatdotheyknow_requests'
scraperwiki.sqlite.attach( sourcescraper )
#table='xlsReturns'
q = '* FROM "'+table+'"'
data = scraperwiki.sqlite.select(q)

#for item in data[]:

description = {"body": ("string", "Council"),"requestTitle": ("string", "Request"),'requestPath':("string","path")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("requestTitle","body","requestPath" ),order_by="request")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()import scraperwiki
import gviz_api

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'typ' in get:
        table='xlsReturns_'+get['typ']
        tablename=table
    else: 
        table='xlsReturns'
        tablename="Local councils"
    #university, department, parish_council,npte,nhsTrust_and_PCT, non_ministerial_department,executive_agency
else:
    table='xlsReturns'
    tablename="Local councils"

def ascii(s): return "".join(i for i in s if ord(i)<128)

tablename=ascii(tablename)

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html


page_template = """
<html><head><title>Spreadsheet Returning FOI Responses via WhatDoTheyKnow</title>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="http://visapi-gadgets.googlecode.com/svn/trunk/wordcloud/wc.css"/>
    <script type="text/javascript" src="http://visapi-gadgets.googlecode.com/svn/trunk/wordcloud/wc.js"></script>
  <script>
    google.load('visualization', '1.1', {packages:['controls']});

    google.setOnLoadCallback(drawTable);

    function drawTable() {

      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
   

    var json_table = new google.visualization.ChartWrapper({'chartType': 'Table','containerId':'table_div_json','options': {allowHtml: true,page:'enable',pageSize:50 , 'pagingSymbols': {prev: 'prev', next: 'next'}}});

    var formatter = new google.visualization.PatternFormat('<a href="http://www.whatdotheyknow.com{1}">{0}</a>');
    formatter.format(json_data, [0,2]); 

//http://www.whatdotheyknow.com/body/kent_county_council
    formatter = new google.visualization.PatternFormat('<a href="http://www.whatdotheyknow.com/body/{0}">{0}</a>');
    formatter.format(json_data, [1]); 

    var view = new google.visualization.DataView(json_data);
    view.setColumns([0,1])


    var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'Request',
        'matchType': 'any'
      }
    });

 /*
var slider = new google.visualization.ControlWrapper({
    'controlType': 'NumberRangeFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Laptime (s)',
      'minValue': 90,
      'maxValue': 150
    }
  });


   var posFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control3',
      'options': {
        'filterColumnLabel': 'Position',
        'matchType': 'any'
      }
    });
*/
var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'control2',
    'options': {
      'filterColumnLabel': 'Council',
      'ui': {
      'labelStacking': 'vertical',
        'allowTyping': false,
        'allowMultiple': false
      }
    }
  });

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind(stringFilter,categoryPicker).bind([categoryPicker], json_table).draw(view);

var outputDiv = document.getElementById('wcdiv');
        var wc = new WordCloud(outputDiv);
        wc.draw(view, {stopWords: 'a an and is or the of for to by in on with into mod dh dfe dcsf moj'});

    }
  </script></head>
  <body>
<h1>WhatDoTheyKnow FOI Requests Returning Data</h1>
<div>Search a particular class of organisation on WhatDoTheyKnow for FOI requests that received one or more responses containing XLS (Excel spreadsheet) data files.</div>
<div>Default is to search over <em>local councils</em>; to search other body types, add <em>?typ=<strong>TYP</strong></em> to the URL of this page where <em>TYP</em> is one of : <tt>university, department, parish_council,npte,nhsTrust_and_PCT, non_ministerial_department,executive_agency</tt></div>
<div><em>Request</em> allows you to filter results according to a particular word or phrase; the <em>Council</em> drop down list is populated with council names that return results in the filtered list after the filter term (if any) is applied.</div>
<div>For a little bit of background context that lead to the development of this scraper/view, see <a href="http://blog.ouseful.info/2012/04/24/foi-signals-on-useful-open-data/">OUseful.info: FOI Signals on Useful Open Data?</a></div>

<div id="dashboard">
    <div id="control1"></div><div id="control2"></div><div id="control3"></div>
    <div id="table_div_json"></div>
</div>
<div>The wordcloud widget is a crude one and runs over the complete (unfiltered) list for this <tt>typ</tt> of data.</div>
<div id="wcdiv"></div>
<script type="text/javascript" language="javascript"
src="http://static.polldaddy.com/p/6167043.js"></script>
<noscript>
<a href="http://polldaddy.com/poll/6167043/">What percentage of your FOI requests come from whatdotheyknow?</a><br/>
<span style="font:9px;">(<a href="http://www.polldaddy.com">polls</a>)</span>
</noscript>
  </body>
</html>
"""


sourcescraper = 'whatdotheyknow_requests'
scraperwiki.sqlite.attach( sourcescraper )
#table='xlsReturns'
q = '* FROM "'+table+'"'
data = scraperwiki.sqlite.select(q)

#for item in data[]:

description = {"body": ("string", "Council"),"requestTitle": ("string", "Request"),'requestPath':("string","path")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("requestTitle","body","requestPath" ),order_by="request")

# Putting the JS code and JSon string into the template
#print "Content-type: text/html"
#print
print page_template % vars()