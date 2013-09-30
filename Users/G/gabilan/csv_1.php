<?php
# Blank PHP
$sourcescraper = '';
scraperwiki::attach("test_bm"); 


$data = scraperwiki::select( "* from test_bm.swdata" ); 
print "#,INCIDENT TITLE,INCIDENT DATE,LOCATION,DESCRIPTION,CATEGORY,APPROVED,VERIFIED<br>";
foreach($data as $d){
$i++;
print $i.',"' . $d["Titulo"] . '","'. $d["Ingresada"] . '","'. $d["Lat"] . ','. $d["Lng"] . '","'. htmlspecialchars($d["Mas_info"]) . ' Link Original: ' . $d["URL"] . '","Mascotas extraviadas",YES,NO<br>';
} 


?>
<?php
# Blank PHP
$sourcescraper = '';
scraperwiki::attach("test_bm"); 


$data = scraperwiki::select( "* from test_bm.swdata" ); 
print "#,INCIDENT TITLE,INCIDENT DATE,LOCATION,DESCRIPTION,CATEGORY,APPROVED,VERIFIED<br>";
foreach($data as $d){
$i++;
print $i.',"' . $d["Titulo"] . '","'. $d["Ingresada"] . '","'. $d["Lat"] . ','. $d["Lng"] . '","'. htmlspecialchars($d["Mas_info"]) . ' Link Original: ' . $d["URL"] . '","Mascotas extraviadas",YES,NO<br>';
} 


?>
