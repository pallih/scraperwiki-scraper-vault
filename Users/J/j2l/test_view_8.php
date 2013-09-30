<?php
# Blank PHP
$sourcescraper = 'tuto_scrape';
scraperwiki::attach("tuto_scrape");
$data = scraperwiki::select(
    "* from tuto_scrape.swdata"
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
<?php
# Blank PHP
$sourcescraper = 'tuto_scrape';
scraperwiki::attach("tuto_scrape");
$data = scraperwiki::select(
    "* from tuto_scrape.swdata"
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
