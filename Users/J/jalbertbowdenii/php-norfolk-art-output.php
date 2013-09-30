<?php
# Blank PHP
scraperwiki::attach("php-norfolk-art"); 

$data = scraperwiki::select(           
    "* from swdata 
    order by linktitle desc"
);
// print_r($data);

print "<table>";           
print "<tr><th>Link Title</th><th>Link Url</th><th>Link Content</th></tr>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["linktitle"] . "</td>";
  print "<td>" . $d["linkhref"] . "</td>";
 print "<td>" . $d["linktext"] . "</td>";
  print "</tr>";
}
print "</table>";

print "<table>";           
print "<tr><th>Img Link Title</th><th>Img Link Url</th></tr>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["linksimgtitle"] . "</td>";
  print "<td>" . $d["linksimgsrc"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
<?php
# Blank PHP
scraperwiki::attach("php-norfolk-art"); 

$data = scraperwiki::select(           
    "* from swdata 
    order by linktitle desc"
);
// print_r($data);

print "<table>";           
print "<tr><th>Link Title</th><th>Link Url</th><th>Link Content</th></tr>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["linktitle"] . "</td>";
  print "<td>" . $d["linkhref"] . "</td>";
 print "<td>" . $d["linktext"] . "</td>";
  print "</tr>";
}
print "</table>";

print "<table>";           
print "<tr><th>Img Link Title</th><th>Img Link Url</th></tr>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["linksimgtitle"] . "</td>";
  print "<td>" . $d["linksimgsrc"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
