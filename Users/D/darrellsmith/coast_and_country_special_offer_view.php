<?php

scraperwiki::attach("special_offers_coast_and_country_1"); 
print("Special Offers Coast and Country~");
$data = scraperwiki::select( "* from special_offers_coast_and_country_1.swdata order by COTTAGE_REFERENCE desc limit 30 " ); 
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
        print "," .  str_replace(",","+",$d["Text"]);
        print "," .  str_replace(",","+",$d["TIMESTAMP"]);
        print "," .  str_replace(",","+",$d["FEATURES"]); 
        print "," .  str_replace(",","+",$d["BEDROOMS"]); 
        print "," .  str_replace(",","+",$d["CHANGEOVERDAY"]); 
        print "," .  str_replace(",","+",$d["Location"]); 
        print "," .  str_replace(",","+",$d["IMAGES"]);
        print "," .  str_replace(",","+",$d["BATHROOMS"]); 
        print "," .  str_replace(",","+",$d["SLEEPS"]); 
        print "," .  str_replace(",","+",$d["PETS"]);
        print "," .  str_replace(",","+",$d["PRICE_LOW"]);
        print "," .  str_replace(",","+",$d["PRICE_HIGH"]);
        print "," .  str_replace(",","+",$d["COTTAGE_LINK"]);
        print "," .  str_replace(",","+",$d["LONGITUDE"]);
        print "," .  str_replace(",","+",$d["LATITUDE"]);
        print "," .  str_replace(",","+",$d["Summary"]);
        print "," .  str_replace(",","+",$d["DESCRIPTION"]);
        print "," .  str_replace(",","+",$d["Agent"]);       
        print "," .  str_replace(",","+",$d["COTTAGE_NAME"]);
        print "," .  str_replace(",","+",$d["ID"]);
        print "," ;
        print "**END**"; 
    }
} 


?>
