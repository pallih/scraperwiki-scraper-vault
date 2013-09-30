<?php
# Blank PHP
$sourcescraper = 'babynamen_bs';
scraperwiki::attach("babynamen_bs");
 $data = scraperwiki::select(           
    "* from babynamen_bs.swdata 
    order by gewicht desc limit 20"
);
print "<table>";           
print "<tr><th>Grösse</th><th>Gewicht</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["name"] . "</td>";
  print "<td>" . $d["gewicht"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
<?php
# Blank PHP
$sourcescraper = 'babynamen_bs';
scraperwiki::attach("babynamen_bs");
 $data = scraperwiki::select(           
    "* from babynamen_bs.swdata 
    order by gewicht desc limit 20"
);
print "<table>";           
print "<tr><th>Grösse</th><th>Gewicht</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["name"] . "</td>";
  print "<td>" . $d["gewicht"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
