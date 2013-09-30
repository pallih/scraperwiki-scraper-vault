<?php
# Blank PHP
$sourceScraper = 'testi-scraper_1';
scraperwiki::attach($sourceScraper);
$data = scraperwiki::select("SELECT * FROM swdata WHERE (Minutes_late > 0)"); 
print_r($data);

print "<table>"; 
print "<tr><th>Country</th><th>Years in school</th>"; 
foreach($data as $d){ 
    print "<tr>"; 
    print "<td>" . $d["Primary_code"] . "</td>"; 
    print "<td>" . $d["Actual_time"] . "</td>"; 
    print "</tr>";
} 
print "</table>";

print "This is a <em>fragment</em> of HTML."; 



?>
<?php
# Blank PHP
$sourceScraper = 'testi-scraper_1';
scraperwiki::attach($sourceScraper);
$data = scraperwiki::select("SELECT * FROM swdata WHERE (Minutes_late > 0)"); 
print_r($data);

print "<table>"; 
print "<tr><th>Country</th><th>Years in school</th>"; 
foreach($data as $d){ 
    print "<tr>"; 
    print "<td>" . $d["Primary_code"] . "</td>"; 
    print "<td>" . $d["Actual_time"] . "</td>"; 
    print "</tr>";
} 
print "</table>";

print "This is a <em>fragment</em> of HTML."; 



?>
