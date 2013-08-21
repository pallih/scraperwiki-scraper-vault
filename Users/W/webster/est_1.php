<?php
# Blank PHP
#$sourcescraper = 'est';
scraperwiki::attach("est");
$data = scraperwiki::select(           
    "* from est.swdata 
    order by years_in_school desc"
);



print "<table>";           
print "<tr><th>Country</th><th>Years in school</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["country"] . "</td>";
  print "<td>" . $d["years_in_school"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
