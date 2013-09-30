<?php
scraperwiki::attach("gw2leatherworker");
$data = scraperwiki::select(
    "* from data 
    ORDER BY CAST(`col2` AS SIGNED) ASC, col4 ASC"
);
//print_r($data);
print "<table>";
print "<tr><th>col1</th><th>col2</th><th>col3</th><th>col4</th><th></th><th></th><th>col6</th><th></th><th></th><th>col8</th><th></th><th></th><th>col10</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["col1"] . "</td>";
  print "<td>" . $d["col2"] . "</td>";
  print "<td>" . $d["col3"] . "</td>";
  print "<td>" . $d["col4"] . "</td>";
  print "<td></td>";
  print "<td></td>";
  print "<td>" . $d["col6"] . $d["col7"] . "</td>";
  print "<td></td>";
  print "<td></td>";
  print "<td>" . $d["col8"] . $d["col9"] . "</td>";
  print "<td></td>";
  print "<td></td>";
  print "<td>" . $d["col10"] . $d["col11"] . "</td>";
 
  print "</tr>";
}
print "</table>";
?>

<?php
scraperwiki::attach("gw2leatherworker");
$data = scraperwiki::select(
    "* from data 
    ORDER BY CAST(`col2` AS SIGNED) ASC, col4 ASC"
);
//print_r($data);
print "<table>";
print "<tr><th>col1</th><th>col2</th><th>col3</th><th>col4</th><th></th><th></th><th>col6</th><th></th><th></th><th>col8</th><th></th><th></th><th>col10</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["col1"] . "</td>";
  print "<td>" . $d["col2"] . "</td>";
  print "<td>" . $d["col3"] . "</td>";
  print "<td>" . $d["col4"] . "</td>";
  print "<td></td>";
  print "<td></td>";
  print "<td>" . $d["col6"] . $d["col7"] . "</td>";
  print "<td></td>";
  print "<td></td>";
  print "<td>" . $d["col8"] . $d["col9"] . "</td>";
  print "<td></td>";
  print "<td></td>";
  print "<td>" . $d["col10"] . $d["col11"] . "</td>";
 
  print "</tr>";
}
print "</table>";
?>

