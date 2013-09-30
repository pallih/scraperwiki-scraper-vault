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
<head><title>OpenlyLocal Spending Flows</title></head>
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

scraperwiki.sqlite.attach( 'local_spend_on_corporates' )
q = '* FROM "companyspend_'+company+'"'
data = scraperwiki.sqlite.select(q)

def ascii(s): return "".join(i for i in s if ord(i)<128)

def gNodeAdd(DG,nodelist,name):
    node=len(nodelist)
    DG.add_node(node,name=ascii(name))
    #DG.add_node(node,name=name)
    #DG.add_node(node,name='')
    nodelist.append(name)
    return DG,nodelist

nodelist=[]

DG = nx.DiGraph()

for item in data:
    supplier=item['supplier']
    supplyingTo=item['supplyingTo']
    nsupplier=item['supplierDetailsURL']
    total=item['total']
    if total<=min:continue
    if supplier not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,supplier)
    if supplyingTo not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,supplyingTo)
    if nsupplier not in nodelist and nsupplier!='':
        DG,nodelist=gNodeAdd(DG,nodelist,nsupplier)

    if DG.has_edge(nodelist.index(supplyingTo),nodelist.index(supplier)):
        DG[nodelist.index(supplyingTo)][nodelist.index(supplier)]['value'] += total
    else: DG.add_edge(nodelist.index(supplyingTo),nodelist.index(supplier),value=total)

    if nsupplier!='' and nsupplier!=supplier:
        if DG.has_edge(nodelist.index(supplier),nodelist.index(nsupplier)):
            DG[nodelist.index(supplier)][nodelist.index(nsupplier)]['value'] += total
        else: DG.add_edge(nodelist.index(supplier),nodelist.index(nsupplier),value=total)


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
<head><title>OpenlyLocal Spending Flows</title></head>
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

scraperwiki.sqlite.attach( 'local_spend_on_corporates' )
q = '* FROM "companyspend_'+company+'"'
data = scraperwiki.sqlite.select(q)

def ascii(s): return "".join(i for i in s if ord(i)<128)

def gNodeAdd(DG,nodelist,name):
    node=len(nodelist)
    DG.add_node(node,name=ascii(name))
    #DG.add_node(node,name=name)
    #DG.add_node(node,name='')
    nodelist.append(name)
    return DG,nodelist

nodelist=[]

DG = nx.DiGraph()

for item in data:
    supplier=item['supplier']
    supplyingTo=item['supplyingTo']
    nsupplier=item['supplierDetailsURL']
    total=item['total']
    if total<=min:continue
    if supplier not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,supplier)
    if supplyingTo not in nodelist:
        DG,nodelist=gNodeAdd(DG,nodelist,supplyingTo)
    if nsupplier not in nodelist and nsupplier!='':
        DG,nodelist=gNodeAdd(DG,nodelist,nsupplier)

    if DG.has_edge(nodelist.index(supplyingTo),nodelist.index(supplier)):
        DG[nodelist.index(supplyingTo)][nodelist.index(supplier)]['value'] += total
    else: DG.add_edge(nodelist.index(supplyingTo),nodelist.index(supplier),value=total)

    if nsupplier!='' and nsupplier!=supplier:
        if DG.has_edge(nodelist.index(supplier),nodelist.index(nsupplier)):
            DG[nodelist.index(supplier)][nodelist.index(nsupplier)]['value'] += total
        else: DG.add_edge(nodelist.index(supplier),nodelist.index(nsupplier),value=total)


json = json.dumps(json_graph.node_link_data(DG))
print page_template % vars()