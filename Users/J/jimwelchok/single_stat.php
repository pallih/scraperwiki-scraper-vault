<?php
# Blank PHP
$sourcescraper = 'merge_previous_1';
scraperwiki::attach($sourcescraper );
$data = scraperwiki::select("* from merge_previous_1.statold where church_id=8565");
foreach($data as $stat)
{
    //print_r($stat);
    print "Church: " . $stat['church_id'] . "\n";
    print "<table border=1>";
    print "<tr><th>Year</th><th>Members</th><th>Worship</th><th>Ctb $</th></tr>";
    for ($yr=1996; $yr <= 2007; $yr++)
      {
      print "<tr>";
      print "<td>" . "mbr".$yr . "</td>";
      print "<td>" . $stat["mbr".$yr] . "</td>";
      print "<td>" . $stat["wor".$yr] . "</td>";
      print "<td>" . $stat["ctb".$yr] . "</td>";
      print "</tr>";
     }
}
print "</table>";

?>
<?php
# Blank PHP
$sourcescraper = 'merge_previous_1';
scraperwiki::attach($sourcescraper );
$data = scraperwiki::select("* from merge_previous_1.statold where church_id=8565");
foreach($data as $stat)
{
    //print_r($stat);
    print "Church: " . $stat['church_id'] . "\n";
    print "<table border=1>";
    print "<tr><th>Year</th><th>Members</th><th>Worship</th><th>Ctb $</th></tr>";
    for ($yr=1996; $yr <= 2007; $yr++)
      {
      print "<tr>";
      print "<td>" . "mbr".$yr . "</td>";
      print "<td>" . $stat["mbr".$yr] . "</td>";
      print "<td>" . $stat["wor".$yr] . "</td>";
      print "<td>" . $stat["ctb".$yr] . "</td>";
      print "</tr>";
     }
}
print "</table>";

?>
