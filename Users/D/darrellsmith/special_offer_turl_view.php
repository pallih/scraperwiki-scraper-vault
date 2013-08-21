<?php

scraperwiki::attach("special_offers_coast_and_country_267_single_table"); 
print("special_offers_sandbox~");
$data = scraperwiki::select( "* from special_offers_coast_and_country_267_single_table.swdata order by ID desc limit 30" ); 
$data = array_filter($data);


//print_r($data);


foreach($data as $d){ 
    if($d["DATE_FROM"]){
        print "" .  $d["COTTAGE_LINK"]; 
        print "," . $d["DATE_FROM"] ; 
        print "," . $d["DATE_TO"] ;
        print "," . $d["DURATION"] ; 
        print "," . $d["WAS_PRICE"] ; 
        print "," . $d["NOW_PRICE"] ;
        print "," . $d["DISCOUNT_PERCENT"]; 
        print "," . $d["DISCOUNT_AMOUNT"] ; 
        print "," . str_replace(",","&#44;",$d["Text"]);
        print "," . $d["TIMESTAMP"] ;
        print "," . $d["RTYPE"] ;
        print "|"; 
    }
} 


?>
