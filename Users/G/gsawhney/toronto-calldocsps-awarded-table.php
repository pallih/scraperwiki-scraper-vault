<?php
$sourcescraper = 'toronto_-_call_docs_ps_-_awarded';
$awardedtable = '';

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select(           
    "callnumber,description,dateawarded,link,winner,category,amount from awarded20121215 
    order by dateawarded desc"
);
//print_r($data);

print "<table>";           
print "<tr bgcolor='#999999'><th>Category</th><th>Call number</th><th>Description</th><th>Winner</th><th>Amount</th><th>Awarded Date</th>";
$count = 0;
foreach($data as $d){
  $count++;
  if ($count % 2) {
    $rowcolor = "#eeeeee";
  } else { 
    $rowcolor = "#dddddd"; 
  }
  print "<tr bgcolor='". $rowcolor ."'>";
  print "<td>" . $d["category"] . "</td>";
  print "<td><a href='https://wx.toronto.ca/" . $d["link"]. "&ExpandSection=1'>" . $d["callnumber"] . "</a></td>";
  print "<td>" . substr($d["description"],0,100) . "...</td>";
  print "<td>" . $d["winner"] . "</td>";
  print "<td>" . $d["amount"] . "</td>";
  print "<td>" . $d["dateawarded"] . "</td>";
  print "</tr>";
}
print "</table>";

?>
<?php
$sourcescraper = 'toronto_-_call_docs_ps_-_awarded';
$awardedtable = '';

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select(           
    "callnumber,description,dateawarded,link,winner,category,amount from awarded20121215 
    order by dateawarded desc"
);
//print_r($data);

print "<table>";           
print "<tr bgcolor='#999999'><th>Category</th><th>Call number</th><th>Description</th><th>Winner</th><th>Amount</th><th>Awarded Date</th>";
$count = 0;
foreach($data as $d){
  $count++;
  if ($count % 2) {
    $rowcolor = "#eeeeee";
  } else { 
    $rowcolor = "#dddddd"; 
  }
  print "<tr bgcolor='". $rowcolor ."'>";
  print "<td>" . $d["category"] . "</td>";
  print "<td><a href='https://wx.toronto.ca/" . $d["link"]. "&ExpandSection=1'>" . $d["callnumber"] . "</a></td>";
  print "<td>" . substr($d["description"],0,100) . "...</td>";
  print "<td>" . $d["winner"] . "</td>";
  print "<td>" . $d["amount"] . "</td>";
  print "<td>" . $d["dateawarded"] . "</td>";
  print "</tr>";
}
print "</table>";

?>
