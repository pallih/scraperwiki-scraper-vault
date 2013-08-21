<?php
require 'scraperwiki/simple_html_dom.php';
$page_counter = 0;
$record_counter = 0;
do // loop through pages
{ 
    $page_counter++;
    $pageurl = "http://www.autotrader.co.uk/search/used/cars/land_rover/discovery/postcode/g699dw/radius/1500/keywords/hse/price-to/25000/maximum-age/up_to_5_years_old/sort/default/price-from/9000/page/{$page_counter}";
    $html_content = scraperwiki::scrape($pageurl) ;
    $html = str_get_html($html_content);
    foreach ($html->find("div.searchResult") as $el) {  // for each record on this page
        $advertReference = intval(preg_replace('[advert]', '', $el->id)); //scrape advert reference number
        $eg = $el->find("div.vehicleTitle a",0 )->innertext;
        $model = preg_replace('[Land Rover ]', '', $eg);
        if (strpos($eg," GS")>0 ) { $type = "GS" ; }   //scrape discovery type
        elseif (strpos($eg," SPECIAL EDITION ")>0 ){$type =  "SE" ; }
        elseif (strpos($eg," HSE ")>0 ){$type =  "HSE" ; }
        elseif (strpos($eg," SE ")>0 ){$type =  "SE" ; }
        elseif (strpos($eg," S ")>0 ){$type =  "S" ; }
        elseif (strpos($eg," XS ")>0 ){$type =  "XS" ; }
        else {$type =  "Other" ; }; 
        $year = $el->find("h3",0 )->innertext;
        $age = 12.5 - intval(substr($year,7,1)) - intval(substr($year,6,1))*0.1 ;
        $year =  preg_replace('[, 4x4]', '', $year); // scrape year
        $eg = $el->find("div.offerPrice span",0 )->innertext;
        $price = intval(preg_replace('[\D]', '', $eg)); // scrape price as integer
        $mileage = $el->find("span.mileage",0 )->innertext;
        $mileage = intval(preg_replace('[\D]', '', $mileage)); // scrape milage as integer
        $distance = $el->find("span.distanceAmount",0 )->innertext;
        $distance = intval(preg_replace('[\D]', '', $distance)); // scrape distance as integer
        $url = $el->find("h2 a",0 )->href;// scrape url
        //$url = $el->find("div.vehicleTitle a",0 ); // scrape url ->href;
        $advertType = $el->find("span.advertType",0 )->innertext;
        $record_counter++;
        print 
            $record_counter . "\t" .  //print record to console

            $model . "\t".
            $type . "\t".
            $year . "\t".


            $mileage . "\t".
            $price  . "\t".
            $advertType  . "\n";

        $description = $el->find("div.searchResultMainText",0 )->innertext;
        if (strpos($description," Cloth ")>0 ) break ; //dont save cloth seats 
        if($page_counter <20) {
            scraperwiki::save(   // and save to database
                array(
                    'guid'
                ),
                array(
                    'guid' => $advertReference,
                    'record' => $record_counter,
                    'model' => $model,
                    'type' => $type,
                    'year' => $year,
                    'age' => $age,
                    'distance' => $distance,
                    'mileage' => $mileage,
                    'price' => $price,
                    'adverttype' => $advertType,
                    'updated' => date("Y-m-d H"),
                    'url' => $url
                 ) //endarray
             ); //endsave
         }; //endif
    }; //endforeach
} //enddo
while ($page_counter <20 );

?>
