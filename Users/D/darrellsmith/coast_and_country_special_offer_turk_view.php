<?php

scraperwiki::attach("special_offers_coast_and_country_1"); 
print("Special Offers Coast and Country~");
$data = scraperwiki::select( "* from special_offers_coast_and_country_1.turk_table order by COTTAGE_REFERENCE desc " ); 
$data = array_filter($data);

foreach($data as $d){ 
    if($d["DATE_FROM"]){
        print "" .   str_replace(",","+",$d["COTTAGE_REFERENCE"]); 
        print "," .  str_replace(",","+",$d["DATE_FROM"]); 
        print "," .  str_replace(",","+",$d["DATE_TO"]);
        print "," .  str_replace(",","+",$d["DURATION"]); 
        print "," .  str_replace(",","+",$d["WAS_PRICE"]); 
        print "," .  str_replace(",","+",$d["NOW_PRICE"]);
        print "," .  str_replace(",","+",$d["DISCOUNT_PERCENT"]); 
        print "," .  str_replace(",","+",$d["DISCOUNT_AMOUNT"]); 
    }
} 


?>
