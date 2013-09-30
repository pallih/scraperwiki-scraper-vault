<?php
scraperwiki::attach("children");  
$data = scraperwiki::select(           
    "* from children.swdata"
);

foreach($data as $d){
  print "<h1>Title: " . $d["title"] . "</h1>";
  print "<img src=\"" . $d["url"] . "\" />";
  print "</br>";
}
?><?php
scraperwiki::attach("children");  
$data = scraperwiki::select(           
    "* from children.swdata"
);

foreach($data as $d){
  print "<h1>Title: " . $d["title"] . "</h1>";
  print "<img src=\"" . $d["url"] . "\" />";
  print "</br>";
}
?>