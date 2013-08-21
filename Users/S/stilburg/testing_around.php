<?php

require 'scraperwiki/simple_html_dom.php'; 

$html = scraperWiki::scrape("http://roanokechamber.chambermaster.com/list/QuickLinkMembers/health-care-11.htm");           

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div#cm_2colmemberinfo") as $record){

        
        $name = $record->find("div#cm_2colmembername a",0);
        $address = $record->find("div#cm_2colmbradrs_street",0);
        $phone = $record->find("div#cm_2colmemberphone",0);
        $city = $record->find("div#cm_2colmbradrs_citystatezip",0);


        print $name->innertext . ", ";
        print $address->innertext . ", ";
        print $city->innertext . ", ";

        print " Phone: " . $phone->innertext . "\n ";

        $sql = array (
                "name" => $name->innertext,
                "address" => $address->innertext,
                "city" => $city->innertext,
                "phone" => $phone->innertext
            );
           
         //scraperwiki::save_sqlite(array("a"),array('name'=>$name->innertext));
        scraperwiki::save_sqlite(array("name"),$sql); 

   
}

?>
