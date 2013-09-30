<?php
# Blank PHP
$sourcescraper = '';
scraperwiki::attach("boletintiempo_1");
$data = scraperwiki::select(           
    "* from boletintiempo_1.swdata 
    order by ciudad asc limit 15"
);
print_r($data);
print "<table>";
print "<tr><th>Hora</th><th>Ciudad</th><th>Temperatura</th><th>Nubosidad</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["hora"] . "</td>";
  print "<td>" . $d["ciudad"] . "</td>";
  print "<td>" . $d["temperatura"] . "</td>";
  print "<td>" . $d["nubosidad"] . "</td>";
  print "</tr>";
}
print "</table>";

?>
<?php
# Blank PHP
$sourcescraper = '';
scraperwiki::attach("boletintiempo_1");
$data = scraperwiki::select(           
    "* from boletintiempo_1.swdata 
    order by ciudad asc limit 15"
);
print_r($data);
print "<table>";
print "<tr><th>Hora</th><th>Ciudad</th><th>Temperatura</th><th>Nubosidad</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["hora"] . "</td>";
  print "<td>" . $d["ciudad"] . "</td>";
  print "<td>" . $d["temperatura"] . "</td>";
  print "<td>" . $d["nubosidad"] . "</td>";
  print "</tr>";
}
print "</table>";

?>
