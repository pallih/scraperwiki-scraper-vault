<?php
# Blank PHP
$sourcescraper = '';
scraperwiki::attach("fernsehserien_sendetermine_1");

#$data = scraperwiki::select( "* from fernsehserien_sendetermine_1.swdata order by years_in_school desc limit 10" );
$data = scraperwiki::select( "* from fernsehserien_sendetermine_1.swdata order by Datum, Uhrzeit, Sender asc" );

#print_r($data);

print "<table>";
print "<tr><th>Datum</th><th>Uhrzeit</th><th>Sender</th><th>Name</th><th>Nummer</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["ID"] . "</td>";
  print "<td>" . $d["Datum"] . "</td>";
  print "<td>" . $d["Uhrzeit"] . "</td>";
  print "<td>" . $d["Sender"] . "</td>";
  print "<td>" . $d["Titel"] . "</td>";
  print "<td>" . $d["Nummer"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
