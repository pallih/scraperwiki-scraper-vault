<?php
# Blank PHP
$sourcescraper = 'scrapertest';
print "This is a testView to show ScraperWiki.";

scraperwiki::attach("scrapertest");

$data = scraperwiki::select(
    "* from scrapertest.swdata
    order by Date"
);
//print_r($data);

print "<table>";
print "<tr><th>Date</th><th>Fleet No</th><th>Details</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["DATE"] . "</td>";
  print "<td>" . $d["FLEET NO"] . "</td>";
  print "<td>" . $d["ACCIDENT DETAILS"] . "</td>";
  print "</tr>";
}
print "</table>";

?>




