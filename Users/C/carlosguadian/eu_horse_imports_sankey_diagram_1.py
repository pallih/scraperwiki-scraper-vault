import urllib,gviz_api,scraperwiki,json

import networkx as nx
from networkx.readwrite import json_graph

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'company' in get: company=get['company']
    else: company='serco'
    if 'min' in get: min=int(get['min'])
    else: min=9999
else:
    company='serco'
    min=9999

page_template="""
<head><title>Intra-EU Horse Trading...</title></head>
<!-- code reused wholesale from http://bost.ocks.org/mike/sankey/ -->
<style>


#chart {
  height: 500px;
}

.node rect {
  cursor: move;
  fill-opacity: .9;
  shape-rendering: crispEdges;
}

.node text {
  pointer-events: none;
  text-shadow: 0 1px 0 #fff;
}

.link {
  fill: none;
  stroke: #000;
  stroke-opacity: .2;
}

.link:hover {
  stroke-opacity: .5;
}

</style></head>
<body>
<h1>Intra-EU Horse Exports/Imports by country</h1>
<p>
<em>Inspired by a story on the Guardian DataBlog</em>: <a href="http://www.guardian.co.uk/uk/datablog/interactive/2013/feb/15/europe-trade-horsemeat-map-interactive">The European trade in horsemeat mapped</a> [ <a href="https://docs.google.com/spreadsheet/ccc?key=0ArwVnOqE20IkdGFRU3ZxREg4NUttRUp5YllHY095X1E&usp=sharing#gid=3">original data</a>]</p>
<p>Graphical widget: <a href="https://github.com/d3/d3-plugins/tree/master/sankey">d3.js Sankey plugin</a></p>
<p>Data preparation: Python <a href="http://networkx.github.com/">networkx</a> import of edgelist and <a href="http://networkx.github.com/documentation/latest/reference/readwrite.json_graph.html">export</a> to d3.js data format.</p>
<pre>#R code reshaping of original data cells: C3:AD30 save to file horseexportsEU.txt
horseexportsEU <- read.delim("~/Downloads/horseexportsEU.txt")
require(reshape)
x=melt(horseexportsEU,id='COUNTRY')
x$value2=as.integer(as.character(gsub(",", "", x$value, fixed = TRUE) ))
x$value2[ is.na(x$value2) ] = -1
x$variable=gsub(".", " ", x$variable, fixed = TRUE)
xt=subset(x,value2>0,select=c('COUNTRY','variable','value2'))
write.table(xt, file="foo.csv", row.names=FALSE, col.names=FALSE, sep=",")</pre>
<p>Source code for this view on Scraperwiki: <a href="https://scraperwiki.com/views/eu_horse_imports_sankey_diagram/">EU Horse imports Sankey diagram</a></p>
<hr/>
<h2>Horse Exports <em>from</em> EU country <em>to</em> EU country</h2>
<p id="chart">

<script type="text/javascript" src="https://raw.github.com/mbostock/d3/master/d3.js"></script>
<!-- <script src="http://bost.ocks.org/mike/sankey/sankey.js"></script> -->
<script src="https://raw.github.com/d3/d3-plugins/master/sankey/sankey.js"></script>
<script>

var margin = {top: 1, right: 1, bottom: 6, left: 1},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var formatNumber = d3.format(",.0f"),
    format = function(d) { return formatNumber(d); },
    color = d3.scale.category20();

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var sankey = d3.sankey()
    .nodeWidth(15)
    .nodePadding(10)
    .size([width, height]);

var path = sankey.link();

//d3.json("../ergast_championship_nodelist/", function(energy) {
True=true
False=false
energy=%(json)s

  sankey
      .nodes(energy.nodes)
      .links(energy.links)
      .layout(32);

  var link = svg.append("g").selectAll(".link")
      .data(energy.links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", path)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return b.dy - a.dy; });

  link.append("title")
      .text(function(d) { return d.source.name + " -> " + d.target.name + " " + format(d.value); });

  var node = svg.append("g").selectAll(".node")
      .data(energy.nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    .call(d3.behavior.drag()
      .origin(function(d) { return d; })
      .on("dragstart", function() { this.parentNode.appendChild(this); })
      .on("drag", dragmove));

  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
      .style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
    .append("title")
      .text(function(d) { return d.name + " " + format(d.value); });

  node.append("text")
      .attr("x", -6)
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { return d.name; })
    .filter(function(d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

  function dragmove(d) {
    d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
    sankey.relayout();
    link.attr("d", path);
  }
//});

</script>
"""

import StringIO
import csv

rawdata = '''"SLOVENIA","AUSTRIA",1200
"AUSTRIA","BELGIUM",134600
"BULGARIA","BELGIUM",181900
"CYPRUS","BELGIUM",200600
"CZECH REPUBLIC","BELGIUM",38200
"DENMARK","BELGIUM",76100
"ESTONIA","BELGIUM",34300
"FINLAND","BELGIUM",832800
"FRANCE","BELGIUM",5898900
"GERMANY","BELGIUM",1108000
"HUNGARY","BELGIUM",43000
"IRELAND","BELGIUM",11500
"ITALY","BELGIUM",2573100
"LITHUANIA","BELGIUM",1700
"LUXEMBOURG","BELGIUM",113700
"MALTA","BELGIUM",55700
"NETHERLANDS","BELGIUM",7265200
"POLAND","BELGIUM",3700
"PORTUGAL","BELGIUM",100
"ROMANIA","BELGIUM",21000
"SLOVENIA","BELGIUM",8700
"SWEDEN","BELGIUM",219000
"UNITED KINGDOM","BELGIUM",4100
"BELGIUM","BULGARIA",35400
"GREECE","BULGARIA",34300
"ROMANIA","BULGARIA",226300
"POLAND","CZECH REPUBLIC",300
"SLOVAKIA","CZECH REPUBLIC",6300
"BELGIUM","DENMARK",79500
"FINLAND","DENMARK",25400
"ITALY","DENMARK",137100
"FINLAND","ESTONIA",28600
"LITHUANIA","ESTONIA",900
"SWEDEN","ESTONIA",1600
"LATVIA","FINLAND",5100
"SWEDEN","FINLAND",3700
"BELGIUM","FRANCE",2387100
"BULGARIA","FRANCE",42000
"CYPRUS","FRANCE",84800
"CZECH REPUBLIC","FRANCE",32500
"GERMANY","FRANCE",23700
"ITALY","FRANCE",2154300
"LUXEMBOURG","FRANCE",11400
"NETHERLANDS","FRANCE",5100
"PORTUGAL","FRANCE",100
"SPAIN","FRANCE",1000
"UNITED KINGDOM","FRANCE",94900
"AUSTRIA","GERMANY",3700
"BELGIUM","GERMANY",191200
"FRANCE","GERMANY",51000
"ITALY","GERMANY",16000
"LUXEMBOURG","GERMANY",100
"NETHERLANDS","GERMANY",42500
"SWEDEN","GERMANY",24800
"BELGIUM","GREECE",600
"CYPRUS","GREECE",100
"AUSTRIA","HUNGARY",13600
"BULGARIA","HUNGARY",827200
"ESTONIA","HUNGARY",110900
"LATVIA","HUNGARY",108300
"POLAND","HUNGARY",3000
"SLOVENIA","HUNGARY",500
"UNITED KINGDOM","HUNGARY",8000
"BELGIUM","IRELAND",654900
"CZECH REPUBLIC","IRELAND",63400
"DENMARK","IRELAND",44600
"FRANCE","IRELAND",528600
"GERMANY","IRELAND",95800
"ITALY","IRELAND",1172500
"NETHERLANDS","IRELAND",89100
"SWEDEN","IRELAND",73700
"UNITED KINGDOM","IRELAND",167200
"AUSTRIA","ITALY",93800
"BELGIUM","ITALY",225700
"BULGARIA","ITALY",71300
"CZECH REPUBLIC","ITALY",84000
"DENMARK","ITALY",40700
"FINLAND","ITALY",32700
"FRANCE","ITALY",20700
"GERMANY","ITALY",34000
"GREECE","ITALY",100
"HUNGARY","ITALY",1238900
"MALTA","ITALY",1200
"NETHERLANDS","ITALY",286900
"POLAND","ITALY",71000
"ROMANIA","ITALY",100
"SLOVENIA","ITALY",4800
"ESTONIA","LITHUANIA",3500
"ITALY","LITHUANIA",585400
"LATVIA","LITHUANIA",2700
"SWEDEN","LITHUANIA",300
"BELGIUM","LUXEMBOURG",400
"FRANCE","LUXEMBOURG",1411100
"GERMANY","LUXEMBOURG",2700
"AUSTRIA","NETHERLANDS",109800
"BELGIUM","NETHERLANDS",1408400
"CZECH REPUBLIC","NETHERLANDS",12300
"DENMARK","NETHERLANDS",40900
"FINLAND","NETHERLANDS",615100
"FRANCE","NETHERLANDS",2102500
"GERMANY","NETHERLANDS",38200
"ITALY","NETHERLANDS",973400
"LUXEMBOURG","NETHERLANDS",5700
"MALTA","NETHERLANDS",700
"SWEDEN","NETHERLANDS",3800
"CZECH REPUBLIC","POLAND",1100
"GERMANY","POLAND",75300
"ITALY","POLAND",10571100
"MALTA","POLAND",1200
"SLOVAKIA","POLAND",900
"SWEDEN","POLAND",9600
"ITALY","PORTUGAL",55600
"AUSTRIA","ROMANIA",6400
"BELGIUM","ROMANIA",1228600
"BULGARIA","ROMANIA",1870800
"GERMANY","ROMANIA",58800
"GREECE","ROMANIA",15900
"HUNGARY","ROMANIA",16700
"ITALY","ROMANIA",1034700
"NETHERLANDS","ROMANIA",409400
"POLAND","ROMANIA",851800
"ITALY","SLOVENIA",6400
"BELGIUM","SPAIN",5200
"BULGARIA","SPAIN",1600
"CYPRUS","SPAIN",6300
"CZECH REPUBLIC","SPAIN",3000
"DENMARK","SPAIN",4300
"ESTONIA","SPAIN",2500
"FRANCE","SPAIN",24500
"GERMANY","SPAIN",3300
"GREECE","SPAIN",24000
"HUNGARY","SPAIN",50100
"ITALY","SPAIN",4028900
"ROMANIA","SPAIN",1100
"SLOVENIA","SPAIN",100
"ESTONIA","SWEDEN",6700
"POLAND","SWEDEN",5200
"BELGIUM","UNITED KINGDOM",151400
"FRANCE","UNITED KINGDOM",1802700
"GERMANY","UNITED KINGDOM",1000
"ITALY","UNITED KINGDOM",12800
"POLAND","UNITED KINGDOM",129100'''

f = StringIO.StringIO(rawdata)
reader = csv.reader(f, delimiter=',')

def gNodeAdd(DG,nodelist,name):
    node=len(nodelist)
    DG.add_node(node,name=name)
    #DG.add_node(node,name=name)
    nodelist.append(name)
    return DG,nodelist

nodelist=[]

DG = nx.DiGraph()

for item in reader:
    importTo=item[0]+'.'
    exportFrom=item[1]
    amount=item[2]
    if importTo not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,importTo)
    if exportFrom not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,exportFrom)

    #if DG.has_edge(nodelist.index(supplyingTo),nodelist.index(supplier)):
    #    DG[nodelist.index(supplyingTo)][nodelist.index(supplier)]['value'] += total
    #else:
    DG.add_edge(nodelist.index(exportFrom),nodelist.index(importTo),value=amount)

    '''if nsupplier!='' and nsupplier!=supplier:
        if DG.has_edge(nodelist.index(supplier),nodelist.index(nsupplier)):
            DG[nodelist.index(supplier)][nodelist.index(nsupplier)]['value'] += total
        else: DG.add_edge(nodelist.index(supplier),nodelist.index(nsupplier),value=total)'''


json = json.dumps(json_graph.node_link_data(DG))
print page_template % vars()import urllib,gviz_api,scraperwiki,json

import networkx as nx
from networkx.readwrite import json_graph

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'company' in get: company=get['company']
    else: company='serco'
    if 'min' in get: min=int(get['min'])
    else: min=9999
else:
    company='serco'
    min=9999

page_template="""
<head><title>Intra-EU Horse Trading...</title></head>
<!-- code reused wholesale from http://bost.ocks.org/mike/sankey/ -->
<style>


#chart {
  height: 500px;
}

.node rect {
  cursor: move;
  fill-opacity: .9;
  shape-rendering: crispEdges;
}

.node text {
  pointer-events: none;
  text-shadow: 0 1px 0 #fff;
}

.link {
  fill: none;
  stroke: #000;
  stroke-opacity: .2;
}

.link:hover {
  stroke-opacity: .5;
}

</style></head>
<body>
<h1>Intra-EU Horse Exports/Imports by country</h1>
<p>
<em>Inspired by a story on the Guardian DataBlog</em>: <a href="http://www.guardian.co.uk/uk/datablog/interactive/2013/feb/15/europe-trade-horsemeat-map-interactive">The European trade in horsemeat mapped</a> [ <a href="https://docs.google.com/spreadsheet/ccc?key=0ArwVnOqE20IkdGFRU3ZxREg4NUttRUp5YllHY095X1E&usp=sharing#gid=3">original data</a>]</p>
<p>Graphical widget: <a href="https://github.com/d3/d3-plugins/tree/master/sankey">d3.js Sankey plugin</a></p>
<p>Data preparation: Python <a href="http://networkx.github.com/">networkx</a> import of edgelist and <a href="http://networkx.github.com/documentation/latest/reference/readwrite.json_graph.html">export</a> to d3.js data format.</p>
<pre>#R code reshaping of original data cells: C3:AD30 save to file horseexportsEU.txt
horseexportsEU <- read.delim("~/Downloads/horseexportsEU.txt")
require(reshape)
x=melt(horseexportsEU,id='COUNTRY')
x$value2=as.integer(as.character(gsub(",", "", x$value, fixed = TRUE) ))
x$value2[ is.na(x$value2) ] = -1
x$variable=gsub(".", " ", x$variable, fixed = TRUE)
xt=subset(x,value2>0,select=c('COUNTRY','variable','value2'))
write.table(xt, file="foo.csv", row.names=FALSE, col.names=FALSE, sep=",")</pre>
<p>Source code for this view on Scraperwiki: <a href="https://scraperwiki.com/views/eu_horse_imports_sankey_diagram/">EU Horse imports Sankey diagram</a></p>
<hr/>
<h2>Horse Exports <em>from</em> EU country <em>to</em> EU country</h2>
<p id="chart">

<script type="text/javascript" src="https://raw.github.com/mbostock/d3/master/d3.js"></script>
<!-- <script src="http://bost.ocks.org/mike/sankey/sankey.js"></script> -->
<script src="https://raw.github.com/d3/d3-plugins/master/sankey/sankey.js"></script>
<script>

var margin = {top: 1, right: 1, bottom: 6, left: 1},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var formatNumber = d3.format(",.0f"),
    format = function(d) { return formatNumber(d); },
    color = d3.scale.category20();

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var sankey = d3.sankey()
    .nodeWidth(15)
    .nodePadding(10)
    .size([width, height]);

var path = sankey.link();

//d3.json("../ergast_championship_nodelist/", function(energy) {
True=true
False=false
energy=%(json)s

  sankey
      .nodes(energy.nodes)
      .links(energy.links)
      .layout(32);

  var link = svg.append("g").selectAll(".link")
      .data(energy.links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", path)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return b.dy - a.dy; });

  link.append("title")
      .text(function(d) { return d.source.name + " -> " + d.target.name + " " + format(d.value); });

  var node = svg.append("g").selectAll(".node")
      .data(energy.nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    .call(d3.behavior.drag()
      .origin(function(d) { return d; })
      .on("dragstart", function() { this.parentNode.appendChild(this); })
      .on("drag", dragmove));

  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
      .style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
    .append("title")
      .text(function(d) { return d.name + " " + format(d.value); });

  node.append("text")
      .attr("x", -6)
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { return d.name; })
    .filter(function(d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

  function dragmove(d) {
    d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
    sankey.relayout();
    link.attr("d", path);
  }
//});

</script>
"""

import StringIO
import csv

rawdata = '''"SLOVENIA","AUSTRIA",1200
"AUSTRIA","BELGIUM",134600
"BULGARIA","BELGIUM",181900
"CYPRUS","BELGIUM",200600
"CZECH REPUBLIC","BELGIUM",38200
"DENMARK","BELGIUM",76100
"ESTONIA","BELGIUM",34300
"FINLAND","BELGIUM",832800
"FRANCE","BELGIUM",5898900
"GERMANY","BELGIUM",1108000
"HUNGARY","BELGIUM",43000
"IRELAND","BELGIUM",11500
"ITALY","BELGIUM",2573100
"LITHUANIA","BELGIUM",1700
"LUXEMBOURG","BELGIUM",113700
"MALTA","BELGIUM",55700
"NETHERLANDS","BELGIUM",7265200
"POLAND","BELGIUM",3700
"PORTUGAL","BELGIUM",100
"ROMANIA","BELGIUM",21000
"SLOVENIA","BELGIUM",8700
"SWEDEN","BELGIUM",219000
"UNITED KINGDOM","BELGIUM",4100
"BELGIUM","BULGARIA",35400
"GREECE","BULGARIA",34300
"ROMANIA","BULGARIA",226300
"POLAND","CZECH REPUBLIC",300
"SLOVAKIA","CZECH REPUBLIC",6300
"BELGIUM","DENMARK",79500
"FINLAND","DENMARK",25400
"ITALY","DENMARK",137100
"FINLAND","ESTONIA",28600
"LITHUANIA","ESTONIA",900
"SWEDEN","ESTONIA",1600
"LATVIA","FINLAND",5100
"SWEDEN","FINLAND",3700
"BELGIUM","FRANCE",2387100
"BULGARIA","FRANCE",42000
"CYPRUS","FRANCE",84800
"CZECH REPUBLIC","FRANCE",32500
"GERMANY","FRANCE",23700
"ITALY","FRANCE",2154300
"LUXEMBOURG","FRANCE",11400
"NETHERLANDS","FRANCE",5100
"PORTUGAL","FRANCE",100
"SPAIN","FRANCE",1000
"UNITED KINGDOM","FRANCE",94900
"AUSTRIA","GERMANY",3700
"BELGIUM","GERMANY",191200
"FRANCE","GERMANY",51000
"ITALY","GERMANY",16000
"LUXEMBOURG","GERMANY",100
"NETHERLANDS","GERMANY",42500
"SWEDEN","GERMANY",24800
"BELGIUM","GREECE",600
"CYPRUS","GREECE",100
"AUSTRIA","HUNGARY",13600
"BULGARIA","HUNGARY",827200
"ESTONIA","HUNGARY",110900
"LATVIA","HUNGARY",108300
"POLAND","HUNGARY",3000
"SLOVENIA","HUNGARY",500
"UNITED KINGDOM","HUNGARY",8000
"BELGIUM","IRELAND",654900
"CZECH REPUBLIC","IRELAND",63400
"DENMARK","IRELAND",44600
"FRANCE","IRELAND",528600
"GERMANY","IRELAND",95800
"ITALY","IRELAND",1172500
"NETHERLANDS","IRELAND",89100
"SWEDEN","IRELAND",73700
"UNITED KINGDOM","IRELAND",167200
"AUSTRIA","ITALY",93800
"BELGIUM","ITALY",225700
"BULGARIA","ITALY",71300
"CZECH REPUBLIC","ITALY",84000
"DENMARK","ITALY",40700
"FINLAND","ITALY",32700
"FRANCE","ITALY",20700
"GERMANY","ITALY",34000
"GREECE","ITALY",100
"HUNGARY","ITALY",1238900
"MALTA","ITALY",1200
"NETHERLANDS","ITALY",286900
"POLAND","ITALY",71000
"ROMANIA","ITALY",100
"SLOVENIA","ITALY",4800
"ESTONIA","LITHUANIA",3500
"ITALY","LITHUANIA",585400
"LATVIA","LITHUANIA",2700
"SWEDEN","LITHUANIA",300
"BELGIUM","LUXEMBOURG",400
"FRANCE","LUXEMBOURG",1411100
"GERMANY","LUXEMBOURG",2700
"AUSTRIA","NETHERLANDS",109800
"BELGIUM","NETHERLANDS",1408400
"CZECH REPUBLIC","NETHERLANDS",12300
"DENMARK","NETHERLANDS",40900
"FINLAND","NETHERLANDS",615100
"FRANCE","NETHERLANDS",2102500
"GERMANY","NETHERLANDS",38200
"ITALY","NETHERLANDS",973400
"LUXEMBOURG","NETHERLANDS",5700
"MALTA","NETHERLANDS",700
"SWEDEN","NETHERLANDS",3800
"CZECH REPUBLIC","POLAND",1100
"GERMANY","POLAND",75300
"ITALY","POLAND",10571100
"MALTA","POLAND",1200
"SLOVAKIA","POLAND",900
"SWEDEN","POLAND",9600
"ITALY","PORTUGAL",55600
"AUSTRIA","ROMANIA",6400
"BELGIUM","ROMANIA",1228600
"BULGARIA","ROMANIA",1870800
"GERMANY","ROMANIA",58800
"GREECE","ROMANIA",15900
"HUNGARY","ROMANIA",16700
"ITALY","ROMANIA",1034700
"NETHERLANDS","ROMANIA",409400
"POLAND","ROMANIA",851800
"ITALY","SLOVENIA",6400
"BELGIUM","SPAIN",5200
"BULGARIA","SPAIN",1600
"CYPRUS","SPAIN",6300
"CZECH REPUBLIC","SPAIN",3000
"DENMARK","SPAIN",4300
"ESTONIA","SPAIN",2500
"FRANCE","SPAIN",24500
"GERMANY","SPAIN",3300
"GREECE","SPAIN",24000
"HUNGARY","SPAIN",50100
"ITALY","SPAIN",4028900
"ROMANIA","SPAIN",1100
"SLOVENIA","SPAIN",100
"ESTONIA","SWEDEN",6700
"POLAND","SWEDEN",5200
"BELGIUM","UNITED KINGDOM",151400
"FRANCE","UNITED KINGDOM",1802700
"GERMANY","UNITED KINGDOM",1000
"ITALY","UNITED KINGDOM",12800
"POLAND","UNITED KINGDOM",129100'''

f = StringIO.StringIO(rawdata)
reader = csv.reader(f, delimiter=',')

def gNodeAdd(DG,nodelist,name):
    node=len(nodelist)
    DG.add_node(node,name=name)
    #DG.add_node(node,name=name)
    nodelist.append(name)
    return DG,nodelist

nodelist=[]

DG = nx.DiGraph()

for item in reader:
    importTo=item[0]+'.'
    exportFrom=item[1]
    amount=item[2]
    if importTo not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,importTo)
    if exportFrom not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,exportFrom)

    #if DG.has_edge(nodelist.index(supplyingTo),nodelist.index(supplier)):
    #    DG[nodelist.index(supplyingTo)][nodelist.index(supplier)]['value'] += total
    #else:
    DG.add_edge(nodelist.index(exportFrom),nodelist.index(importTo),value=amount)

    '''if nsupplier!='' and nsupplier!=supplier:
        if DG.has_edge(nodelist.index(supplier),nodelist.index(nsupplier)):
            DG[nodelist.index(supplier)][nodelist.index(nsupplier)]['value'] += total
        else: DG.add_edge(nodelist.index(supplier),nodelist.index(nsupplier),value=total)'''


json = json.dumps(json_graph.node_link_data(DG))
print page_template % vars()