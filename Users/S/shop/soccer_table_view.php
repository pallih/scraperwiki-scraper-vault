<?php
scraperwiki::attach("soccer_table_reviersport");
$data = scraperwiki::select(           
    "Platz, Mannschaft, Logo from soccer_table_reviersport.swdata 
    order by Platz asc"
);

print "<table>";           
print "<tr><th>Platz</th><th>Mannschaft</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["Platz"] . "</td>";
  print "<td>" . $d["Mannschaft"] . "</td>";
  if (!empty($d["Logo"])){
    print "<td><img src=\"" . $d["Logo"] . "\" height=\"20\"></td>";
  }
  print "</tr>";
}
print "</table>";

?>

<?php
scraperwiki::attach("soccer_table_reviersport");
$data = scraperwiki::select(           
    "Platz, Mannschaft, Logo from soccer_table_reviersport.swdata 
    order by Platz asc"
);

print "<table>";           
print "<tr><th>Platz</th><th>Mannschaft</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["Platz"] . "</td>";
  print "<td>" . $d["Mannschaft"] . "</td>";
  if (!empty($d["Logo"])){
    print "<td><img src=\"" . $d["Logo"] . "\" height=\"20\"></td>";
  }
  print "</tr>";
}
print "</table>";

?>

