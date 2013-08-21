<?php
$sourcescraper = 'bp_parser_1';
scraperwiki::attach($sourcescraper) ;

$data = scraperwiki::select(
    "* from date_20121027"
);
//print_r($data);


print "<table>";
print "<tr><th>Index</th><th>Page_Name</th><th>html</th>";
foreach($data as $d){

$i++ ;
if ( $i == 3 ) break

  print "<tr>";
  print "<td>" . $d["page_ID_20121027"] . "</td>";
  print "<td>" . $d["name"] . "</td>";
  print "<td>" . $d["html"] . "</td>";
  print "</tr>";
}
print "</table>";



?>
