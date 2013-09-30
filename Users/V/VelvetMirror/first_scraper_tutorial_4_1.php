<?php
# Blank PHP
# $sourcescraper = 'first_scraper_tutorial_4';
scraperwiki::attach("first_scraper_tutorial_4");  
$data = scraperwiki::select(           
    "* from first_scraper_tutorial_4.swdata 
    order by years_in_school desc limit 10"
);
print "<table>";           
print "<tr><th>Country</th><th>Years in school</th></tr>";
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
# $sourcescraper = 'first_scraper_tutorial_4';
scraperwiki::attach("first_scraper_tutorial_4");  
$data = scraperwiki::select(           
    "* from first_scraper_tutorial_4.swdata 
    order by years_in_school desc limit 10"
);
print "<table>";           
print "<tr><th>Country</th><th>Years in school</th></tr>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["country"] . "</td>";
  print "<td>" . $d["years_in_school"] . "</td>";
  print "</tr>";
}
print "</table>"; 
?>
