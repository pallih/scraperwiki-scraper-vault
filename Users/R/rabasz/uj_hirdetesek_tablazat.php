<?php
# Blank PHP
$sourcescraper = 'hahu-query';
// select id,url,evjarat,ar,kivitel,allapot,uzemanyag,sebvalto,urtartalom,hengerelrend,hajtas,teljesitmeny,ajtok,szin,klima from `swdata` 

scraperwiki::attach("hahu-query");  
$data = scraperwiki::select("* from hahu-query.swdata");

print "<table>";           
print "<tr><th>kód</th><th>link</th><th>évjárat</th><th>vételár</th><th>kivitel</th><th>állapot</th><th>Üzemanyag</th><th>sebváltó</th><th>űrtartalom</th><th>henger-elrendezés</th><th>hajtás</th><th>teljesítmény</th><th>ajtók</th><th>szín</th><th>klíma</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["id"] . "</td>";
  print "<td>" . $d["url"] . "</td>";
  print "<td>" . $d["evjarat"] . "</td>";
  print "<td>" . $d["ar"] . "</td>";
  print "<td>" . $d["kivitel"] . "</td>";
  print "<td>" . $d["allapot"] . "</td>";
  print "<td>" . $d["uzemanyag"] . "</td>";
  print "<td>" . $d["sebvalto"] . "</td>";
  print "<td>" . $d["urtartalom"] . "</td>";
  print "<td>" . $d["hengerelrend"] . "</td>";
  print "<td>" . $d["hajtas"] . "</td>";
  print "<td>" . $d["teljesitmeny"] . "</td>";
  print "<td>" . $d["ajtok"] . "</td>";
  print "<td>" . $d["szin"] . "</td>";
  print "<td>" . $d["klima"] . "</td>";
  print "</tr>";
}
print "</table>";

?>
<?php
# Blank PHP
$sourcescraper = 'hahu-query';
// select id,url,evjarat,ar,kivitel,allapot,uzemanyag,sebvalto,urtartalom,hengerelrend,hajtas,teljesitmeny,ajtok,szin,klima from `swdata` 

scraperwiki::attach("hahu-query");  
$data = scraperwiki::select("* from hahu-query.swdata");

print "<table>";           
print "<tr><th>kód</th><th>link</th><th>évjárat</th><th>vételár</th><th>kivitel</th><th>állapot</th><th>Üzemanyag</th><th>sebváltó</th><th>űrtartalom</th><th>henger-elrendezés</th><th>hajtás</th><th>teljesítmény</th><th>ajtók</th><th>szín</th><th>klíma</th>";
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["id"] . "</td>";
  print "<td>" . $d["url"] . "</td>";
  print "<td>" . $d["evjarat"] . "</td>";
  print "<td>" . $d["ar"] . "</td>";
  print "<td>" . $d["kivitel"] . "</td>";
  print "<td>" . $d["allapot"] . "</td>";
  print "<td>" . $d["uzemanyag"] . "</td>";
  print "<td>" . $d["sebvalto"] . "</td>";
  print "<td>" . $d["urtartalom"] . "</td>";
  print "<td>" . $d["hengerelrend"] . "</td>";
  print "<td>" . $d["hajtas"] . "</td>";
  print "<td>" . $d["teljesitmeny"] . "</td>";
  print "<td>" . $d["ajtok"] . "</td>";
  print "<td>" . $d["szin"] . "</td>";
  print "<td>" . $d["klima"] . "</td>";
  print "</tr>";
}
print "</table>";

?>
