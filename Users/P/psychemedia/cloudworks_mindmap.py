#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    key=qsenv["KEY"]
    if 'cloudscapeID' in qsenv: cloudscapeID=qsenv['cloudscapeID']
    else: cloudscapeID='2451'
except:
    exit(-1)

qstring=os.getenv("QUERY_STRING")
search=''
typ='unit'

if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'unit' in get: search=get['unit']
    elif 'unitset' in get:
        search=get['unitset']
        typ='unitset'


#http://cloudworks.ac.uk/api/clouds/{cloud_id}.{format}?api_key={api_key}


import urllib2,json, networkx as nx
from networkx.readwrite import json_graph

id=cloudscapeID #need logic
typ='cloudscape'


urlstub="http://cloudworks.ac.uk/api/"
urlcloudstub=urlstub+"clouds/"+str(id)
urlcloudscapestub=urlstub+"cloudscapes/"+str(id)
urlsuffix=".json?api_key="+str(key)


#Need 2 sorts of logic
#Calling data back from cloud or cloudscape?
#What data are we calling back?

ctyp="/clouds"
url=urlcloudscapestub+ctyp+urlsuffix

#print url

#------

page_template="""
<!-- via mbostock.github.com/d3/talk/20111018/tree.html-->
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
    <!--<link type="text/css" rel="stylesheet" href="http://mbostock.github.com/d3/talk/20111018/style.css"/>-->
    <script type="text/javascript" src="https://raw.github.com/mbostock/d3/master/d3.js"></script>
    <!--<script type="text/javascript" src="http://mbostock.github.com/d3/talk/20111018/d3/d3.layout.js"></script>-->
    <style type="text/css">


.node circle {
  cursor: pointer;
  fill: #fff;
  stroke: steelblue;
  stroke-width: 1.5px;
}

.node text {
  font-size: 11px;
}

path.link {
  fill: none;
  stroke: #ccc;
  stroke-width: 1.5px;
}

    </style>
  </head>
  <body>
    <div id="body">
     
    </div>
    <script type="text/javascript">

var m = [0, 100, 20, 220],
    w = 1460 - m[1] - m[3],
    h = 800 - m[0] - m[2],
    i = 0,
    root;

var tree = d3.layout.tree()
    .size([h, w]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

var vis = d3.select("#body").append("svg:svg")
    .attr("width", w + m[1] + m[3])
    .attr("height", h + m[0] + m[2])
  .append("svg:g")
    .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

//d3.json("../openlearn_tree_json/", function(json) {
  //root = json;
root=%(jdata)s
  root.x0 = h / 2;
  root.y0 = 0;

  function toggleAll(d) {
    if (d.children) {
      d.children.forEach(toggleAll);
      toggle(d);
    }
  }

  // Initialize the display to show a few nodes.
  root.children.forEach(toggleAll);
  //toggle(root.children[1]);
  //toggle(root.children[1].children[2]);
  //toggle(root.children[9]);
  //toggle(root.children[9].children[0]);

  update(root);
//});

function update(source) {
  var duration = d3.event && d3.event.altKey ? 5000 : 500;

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse();

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 280; });

  // Update the nodes
  var node = vis.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parents previous position.
  var nodeEnter = node.enter().append("svg:g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .on("click", function(d) { toggle(d); update(d); });

  nodeEnter.append("svg:circle")
      .attr("r", 1e-6)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeEnter.append("svg:text")
      .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  nodeUpdate.select("circle")
      .attr("r", 4.5)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

  nodeUpdate.select("text")
      .style("fill-opacity", 1);

  // Transition exiting nodes to the parents new position.
  var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .remove();

  nodeExit.select("circle")
      .attr("r", 1e-6);

  nodeExit.select("text")
      .style("fill-opacity", 1e-6);

  // Update the links
  var link = vis.selectAll("path.link")
      .data(tree.links(nodes), function(d) { return d.target.id; });

  // Enter any new links at the parents previous position.
  link.enter().insert("svg:path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      })
    .transition()
      .duration(duration)
      .attr("d", diagonal);

  // Transition links to their new position.
  link.transition()
      .duration(duration)
      .attr("d", diagonal);

  // Transition exiting nodes to the parents new position.
  link.exit().transition()
      .duration(duration)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// Toggle children.
function toggle(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
}

    </script>
  </body>
</html>
"""

#------


entities=json.load(urllib2.urlopen(url))

#print entities

def ascii(s): return "".join(i for i in s.encode('utf-8') if ord(i)<128)

def graphRoot(DG,title,root=1):
    DG.add_node(root,name=ascii(title))
    return DG,root

def gNodeAdd(DG,root,node,name):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name))
    DG.add_edge(root,node)
    return DG,node

DG=nx.DiGraph()
DG,root=graphRoot(DG,id)
currnode=root

for c in entities['items']:
    DG,currnode=gNodeAdd(DG,root,currnode,c['title'])
    

jdata = json_graph.tree_data(DG,root=1)
#print json.dumps(data)

print page_template % vars()