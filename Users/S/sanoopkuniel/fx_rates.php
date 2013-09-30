<?php

$xml = simplexml_load_file("http://www.dbs.com/ratesonline/xml/Pages/XFXBRA.xml");

foreach ($xml->xpath("/rates/record/currency") as $child) {
    if($child->attributes()->value == "New Zealand Dollar"){
        $parent = $child->xpath("parent::*");
        $sell = $parent[0]->xpath("record_1/selling_ttod");
        $rate = floatval($sell[0]->attributes()->value[0]);
        $total = number_format(65000/$rate,2);
        $record = array( 'currency' => 'NZD', 'Total' => $total);
        print "Total : $total \n";
        
        scraperwiki::save(array('currency'), $record); 
    }
}

?>
<?php

$xml = simplexml_load_file("http://www.dbs.com/ratesonline/xml/Pages/XFXBRA.xml");

foreach ($xml->xpath("/rates/record/currency") as $child) {
    if($child->attributes()->value == "New Zealand Dollar"){
        $parent = $child->xpath("parent::*");
        $sell = $parent[0]->xpath("record_1/selling_ttod");
        $rate = floatval($sell[0]->attributes()->value[0]);
        $total = number_format(65000/$rate,2);
        $record = array( 'currency' => 'NZD', 'Total' => $total);
        print "Total : $total \n";
        
        scraperwiki::save(array('currency'), $record); 
    }
}

?>
