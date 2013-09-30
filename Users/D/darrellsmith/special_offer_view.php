<?php

scraperwiki::attach("special_offers_sandbox"); 
print("special_offers_sandbox~");
$data = scraperwiki::select( "* from special_offers_sandbox.swdata order by ID desc " ); 
$data = array_filter($data);

foreach($data as $d){ 
    if($d["DATE_FROM"]){
        print "" .  $d["COTTAGE_ID"]; 
        print "," . $d["DATE_FROM"] ; 
        print "," . $d["DATE_TO"] ;
        print "," . $d["DURATION"] ; 
        print "," . $d["WAS_PRICE"] ; 
        print "," . $d["NOW_PRICE"] ;
        print "," . $d["DISCOUNT_PERCENT"]; 
        print "," . $d["DISCOUNT_AMOUNT"] ; 
        print "," . $d["REF"] ;
        print "," . str_replace(",","&#44;",$d["Text"]);
        print "," . $d["TIMESTAMP"] ;
        print "," ;
        print "|"; 
    }
} 


?>
<?php

scraperwiki::attach("special_offers_sandbox"); 
print("special_offers_sandbox~");
$data = scraperwiki::select( "* from special_offers_sandbox.swdata order by ID desc " ); 
$data = array_filter($data);

foreach($data as $d){ 
    if($d["DATE_FROM"]){
        print "" .  $d["COTTAGE_ID"]; 
        print "," . $d["DATE_FROM"] ; 
        print "," . $d["DATE_TO"] ;
        print "," . $d["DURATION"] ; 
        print "," . $d["WAS_PRICE"] ; 
        print "," . $d["NOW_PRICE"] ;
        print "," . $d["DISCOUNT_PERCENT"]; 
        print "," . $d["DISCOUNT_AMOUNT"] ; 
        print "," . $d["REF"] ;
        print "," . str_replace(",","&#44;",$d["Text"]);
        print "," . $d["TIMESTAMP"] ;
        print "," ;
        print "|"; 
    }
} 


?>
<?php

scraperwiki::attach("special_offers_sandbox"); 
print("special_offers_sandbox~");
$data = scraperwiki::select( "* from special_offers_sandbox.swdata order by ID desc " ); 
$data = array_filter($data);

foreach($data as $d){ 
    if($d["DATE_FROM"]){
        print "" .  $d["COTTAGE_ID"]; 
        print "," . $d["DATE_FROM"] ; 
        print "," . $d["DATE_TO"] ;
        print "," . $d["DURATION"] ; 
        print "," . $d["WAS_PRICE"] ; 
        print "," . $d["NOW_PRICE"] ;
        print "," . $d["DISCOUNT_PERCENT"]; 
        print "," . $d["DISCOUNT_AMOUNT"] ; 
        print "," . $d["REF"] ;
        print "," . str_replace(",","&#44;",$d["Text"]);
        print "," . $d["TIMESTAMP"] ;
        print "," ;
        print "|"; 
    }
} 


?>
<?php

scraperwiki::attach("special_offers_sandbox"); 
print("special_offers_sandbox~");
$data = scraperwiki::select( "* from special_offers_sandbox.swdata order by ID desc " ); 
$data = array_filter($data);

foreach($data as $d){ 
    if($d["DATE_FROM"]){
        print "" .  $d["COTTAGE_ID"]; 
        print "," . $d["DATE_FROM"] ; 
        print "," . $d["DATE_TO"] ;
        print "," . $d["DURATION"] ; 
        print "," . $d["WAS_PRICE"] ; 
        print "," . $d["NOW_PRICE"] ;
        print "," . $d["DISCOUNT_PERCENT"]; 
        print "," . $d["DISCOUNT_AMOUNT"] ; 
        print "," . $d["REF"] ;
        print "," . str_replace(",","&#44;",$d["Text"]);
        print "," . $d["TIMESTAMP"] ;
        print "," ;
        print "|"; 
    }
} 


?>
