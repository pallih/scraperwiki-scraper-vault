<?php
# Blank PHP
scraperwiki::attach("top_free_android_apps");   

$data = scraperwiki::select(           
    "* from top_free_android_apps.swdata"
);
print "<table>";           
print "<tr><th>App Name</th><th>Image</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["name"] . "</td>";
  print "<td>" . "<img src='" . $d["thumbnail"] . "' /></td>";
  print "</tr>";
}
print "</table>";
?>
