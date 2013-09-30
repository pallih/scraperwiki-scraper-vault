<?php
$sourcescraper = 'test_77';

scraperwiki::attach("test_77"); 

$data = scraperwiki::select(
    "* from test_77.swdata"
);

print "<table>";
print "<tr><th>user_input</th><th>babelfish_output</th><th>timestamp_scrape</th><th>page</th><th>language</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["user_input"] . "</td>";
  print "<td>" . $d["babelfish_output"] . "</td>";
  print "<td>" . $d["timestamp_scrape"] . "</td>";
  print "<td>" . $d["page"] . "</td>";
  print "<td>" . $d["language"] . "</td>";
  print "</tr>";
}
print "</table>";


?>
<?php
$sourcescraper = 'test_77';

scraperwiki::attach("test_77"); 

$data = scraperwiki::select(
    "* from test_77.swdata"
);

print "<table>";
print "<tr><th>user_input</th><th>babelfish_output</th><th>timestamp_scrape</th><th>page</th><th>language</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["user_input"] . "</td>";
  print "<td>" . $d["babelfish_output"] . "</td>";
  print "<td>" . $d["timestamp_scrape"] . "</td>";
  print "<td>" . $d["page"] . "</td>";
  print "<td>" . $d["language"] . "</td>";
  print "</tr>";
}
print "</table>";


?>
