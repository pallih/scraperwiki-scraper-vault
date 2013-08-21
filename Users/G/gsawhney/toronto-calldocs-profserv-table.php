<?php
# Blank PHP
$sourcescraper = 'city_of_toronto_-_call_documents_-_professional_se';
$purchasersscraper = 'toronto_-_call_docs_-_purchasers';
$purchaserstable = "purchasers20121215";

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select(           
    "callnumber,description,issuedate,closingdate,doc from tod20121103 
    order by issuedate desc"
);
//print_r($data);

print "<table>";           
print "<tr bgcolor='#999999'><th>Call number</th><th>Description</th><th>Closing Date</th><th>Issue Date</th><th>Purchasers</th>";
$count = 0;
foreach($data as $d){
  $count++;
  if ($count % 2) {
    $rowcolor = "#eeeeee";
  } else { 
    $rowcolor = "#dddddd"; 
  }

  //count the number of purchasers
  scraperwiki::attach('toronto_-_call_docs_-_purchasers'); 
  $res = scraperwiki::select("count(*) as pcount from ".$purchaserstable." WHERE callnumber = '".$d['callnumber']."'");

//var_dump($res[0]['pcount']);

  print "<tr bgcolor='". $rowcolor ."'>";
  print "<td><a href='" . $d["doc"]. "'>" . $d["callnumber"] . "</a></td>";
  print "<td>" . substr($d["description"],0,100) . "...</td>";
  print "<td>" . $d["closingdate"] . "</td>";
  print "<td>" . $d["issuedate"] . "</td>";
  print "<td>" . $res[0]['pcount'] . "</td>";
  print "</tr>";
}
print "</table>";

?>
