<?php
 
 
// As scraperwiki's sqlite doesn't support Joins !?!?!?!?!? 
 
// Get the data 
scraperwiki::attach("coastandcountrycouk");


$sql = " 'coastandcountrycouk'.swdata.COTTAGE_URL FROM 'coastandcountrycouk_check'.swdata  
inner join 'coastandcountrycouk'.swdata 
ON 'coastandcountrycouk_check'.swdata.COTTAGE_URL = 'coastandcountrycouk'.swdata.COTTAGE_URL ";

$dataA = scraperwiki::select($sql);

print_r($dataA);

scraperwiki::attach("coastandcountrycouk_check");

# get an array of the cottage data to scrape
$dataB = scraperwiki::select("COTTAGE_URL from SWDATA order by COTTAGE_URL");

print_r($dataB);





/*

 
 # get an array of the cottage data to scrape
 $dataA = scraperwiki::select("COTTAGE_URL from 'coastandcountrycouk'.SWDATA order by COTTAGE_URL");
 
 # get an array of the cottage data to scrape
 $dataB = scraperwiki::select("COTTAGE_URL from 'coastandcountrycouk'.SWDATA order by COTTAGE_URL");
 
 foreach($dataA as $idA){ 
   foreach($dataB as $idB){
     
     if($idA==$idB)
        
   }
 }
 */
 
  
 
