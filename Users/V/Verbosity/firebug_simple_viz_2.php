<?php
# Blank PHP
    $sourcescraper = 'central_scotland_fire_incidents';
    $all_data = scraperwiki::getData($sourcescraper, $limit=5000); 
    //$keys = scraperwiki::getKeys($sourcescraper); 
    //print_r($keys);
    $keyindex = getenv("URLQUERY");
    //print_r($keyindex);
    //print_r($all_data);

    $is_malicious = FALSE;

    $results = array();


    foreach ($all_data as $item){

    $location = $item->location;
    $location = explode(',', $location);
    $location = trim($location[1]);


    $regex_malicious = '@malicious@';
    $regex_false_alarm = '@false alarm@';

    $summary = $item->summary;
    $is_malicious = (preg_match ($regex_malicious , $summary)); //&& preg_match($regex_false_alarm, $summary));

    //$is_malicious = (preg_match ($regex_malicious , $summary) && preg_match($regex_false_alarm, $summary));

    $results[$location]['total']++;
    
    if ($is_malicious){
              
        $results[$location]['malicious']++;
     };
};

$graph = array();

$string_js='' ;
//sort out the percentages
foreach ($results as $key => $value){
       
//if there are malicious fires
    if ($results[$key]['malicious'] == TRUE) {
    
    $results[$key]['percentage'] = (double)(($results[$key]['malicious'] / $results[$key]['total'] ) * 100);

    };


    if ($results[$key]['percentage']){

    $graph[$key] = $results[$key]['percentage'];
 
     }; 
  

};
foreach ($graph as $key => $value ){
  if ($key!= '' && $value!='') {
     $string_js .='"'. $key .'"'.':{'.'"'.$key.'"'.':'. $value.'} , ';
  }
};   
 
 $String_js_output=substr($string_js , 0 , -3);
//print_r($graph);

?>  


<body>
<script type="text/javascript" src="http://vis.stanford.edu/protovis/protovis-r3.2.js"></script>
<script type="text/javascript+protovis">
 var flare = { <? echo   $String_js_output ; ?> };


/** Computes the full class name of a given node. */
function title(d) {
  return d.parentNode ? (title(d.parentNode) + "." + d.nodeName) : d.nodeName;
}

var re = "",
    color = pv.Colors.category19().by(function(d) d.parentNode.nodeName)
    nodes = pv.dom(flare).root("flare").nodes();

var vis = new pv.Panel()
    .width(860)
    .height(568);

var treemap = vis.add(pv.Layout.Treemap)
    .nodes(nodes)
    .round(true);

treemap.leaf.add(pv.Panel)
    .fillStyle(function(d) color(d).alpha(title(d).match(re) ? 1 : .2))
    .strokeStyle("#fff")
    .lineWidth(2)
    .antialias(false);

treemap.label.add(pv.Label)
    .textStyle(function(d) pv.rgb(0, 0, 0, title(d).match(re) ? 1 : .2));

vis.render();

/** Counts the number of matching classes, updating the title element. */
function count() {
  var classes = 0, bytes = 0, total = 0;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if(n.firstChild) continue;
    total += n.nodeValue;
    if (title(n).match(re)) {
      classes++;
      bytes += n.nodeValue;
    }
  }
  var percent = bytes / total * 100;
  document.getElementById("title").innerHTML
      = classes + " classes; "
      + bytes + " bytes ("
      + percent.toFixed(percent < 10) + "%).";
}

/** Updates the visualization and count when a new query is entered. */
function update(query) {
  if (query != re) {
    re = new RegExp(query, "i");
    count();
    vis.render();
  }
}

count();

    </script>
   </body>  
<?php
# Blank PHP
    $sourcescraper = 'central_scotland_fire_incidents';
    $all_data = scraperwiki::getData($sourcescraper, $limit=5000); 
    //$keys = scraperwiki::getKeys($sourcescraper); 
    //print_r($keys);
    $keyindex = getenv("URLQUERY");
    //print_r($keyindex);
    //print_r($all_data);

    $is_malicious = FALSE;

    $results = array();


    foreach ($all_data as $item){

    $location = $item->location;
    $location = explode(',', $location);
    $location = trim($location[1]);


    $regex_malicious = '@malicious@';
    $regex_false_alarm = '@false alarm@';

    $summary = $item->summary;
    $is_malicious = (preg_match ($regex_malicious , $summary)); //&& preg_match($regex_false_alarm, $summary));

    //$is_malicious = (preg_match ($regex_malicious , $summary) && preg_match($regex_false_alarm, $summary));

    $results[$location]['total']++;
    
    if ($is_malicious){
              
        $results[$location]['malicious']++;
     };
};

$graph = array();

$string_js='' ;
//sort out the percentages
foreach ($results as $key => $value){
       
//if there are malicious fires
    if ($results[$key]['malicious'] == TRUE) {
    
    $results[$key]['percentage'] = (double)(($results[$key]['malicious'] / $results[$key]['total'] ) * 100);

    };


    if ($results[$key]['percentage']){

    $graph[$key] = $results[$key]['percentage'];
 
     }; 
  

};
foreach ($graph as $key => $value ){
  if ($key!= '' && $value!='') {
     $string_js .='"'. $key .'"'.':{'.'"'.$key.'"'.':'. $value.'} , ';
  }
};   
 
 $String_js_output=substr($string_js , 0 , -3);
//print_r($graph);

?>  


<body>
<script type="text/javascript" src="http://vis.stanford.edu/protovis/protovis-r3.2.js"></script>
<script type="text/javascript+protovis">
 var flare = { <? echo   $String_js_output ; ?> };


/** Computes the full class name of a given node. */
function title(d) {
  return d.parentNode ? (title(d.parentNode) + "." + d.nodeName) : d.nodeName;
}

var re = "",
    color = pv.Colors.category19().by(function(d) d.parentNode.nodeName)
    nodes = pv.dom(flare).root("flare").nodes();

var vis = new pv.Panel()
    .width(860)
    .height(568);

var treemap = vis.add(pv.Layout.Treemap)
    .nodes(nodes)
    .round(true);

treemap.leaf.add(pv.Panel)
    .fillStyle(function(d) color(d).alpha(title(d).match(re) ? 1 : .2))
    .strokeStyle("#fff")
    .lineWidth(2)
    .antialias(false);

treemap.label.add(pv.Label)
    .textStyle(function(d) pv.rgb(0, 0, 0, title(d).match(re) ? 1 : .2));

vis.render();

/** Counts the number of matching classes, updating the title element. */
function count() {
  var classes = 0, bytes = 0, total = 0;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if(n.firstChild) continue;
    total += n.nodeValue;
    if (title(n).match(re)) {
      classes++;
      bytes += n.nodeValue;
    }
  }
  var percent = bytes / total * 100;
  document.getElementById("title").innerHTML
      = classes + " classes; "
      + bytes + " bytes ("
      + percent.toFixed(percent < 10) + "%).";
}

/** Updates the visualization and count when a new query is entered. */
function update(query) {
  if (query != re) {
    re = new RegExp(query, "i");
    count();
    vis.render();
  }
}

count();

    </script>
   </body>  
