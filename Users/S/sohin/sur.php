<?php

require 'scraperwiki/simple_html_dom.php';

$page = 59;
$url =  "http://www.ebay.com/sch/Photographic-Images-/14277/i.html?_sop=15&_nkw=Korean+War";

while (true)
{
    $html = scraperWiki::scrape( $url );           
    $dom = new simple_html_dom();
    $dom->load($html); 

    $results = $dom->find("a[@itemprop='name']");
    print " found " . count($results) . " results on page " . $page . "\n"; 

    foreach($results as $data)
    {
        set_time_limit(25);

        $carUrl = $data ->href;
        $carHtml = scraperWiki::scrape($carUrl); 
        $cd = new simple_html_dom(); 
        $cd->load($carHtml); 

        $id = $cd->find("div[@class='iti-eu-txt iti-eu-pd u-flR iti-ncntr u-cb']", 0)->plaintext; 
        $id = html_entity_decode($id, ENT_QUOTES, 'UTF-8');
        $id = trim(str_replace("Item number:", "", $id));
        
        $price = $cd->find("span[@itemprop='price']", 0)->plaintext; 
        $price = trim(html_entity_decode($price, ENT_QUOTES, 'UTF-8'));

        $title = $cd->find("h1[@class='it-ttl']", 0)->plaintext;
        $title = trim(html_entity_decode($title, ENT_QUOTES, 'UTF-8')); 

        $timeLeftn = $cd->find("span[@class='vi-is1-ctdn vi-is1-tml']", 0);
        $timeLeft  = '';
        if (isset($timeLeftn)) $timeLeft = trim(html_entity_decode($timeLeftn->plaintext, ENT_QUOTES, 'UTF-8'));  

        $description = $cd->find("div[@id='desc_div']", 0)->plaintext;
        $description = trim(html_entity_decode($description, ENT_QUOTES, 'UTF-8'));

        $itemLocation = $cd->find("div[@class='iti-eu-bld-gry']", 0)->plaintext; //differentiate itemlocation and shipsto!
        $itemLocation = trim(html_entity_decode($itemLocation, ENT_QUOTES, 'UTF-8'));

        $shipsTo = $cd->find("div[@class='iti-eu-bld-gry vi-shp-pdg-rt']", 0)->plaintext; //differentiate itemLocation and shipsto!
        $shipsTo = trim(html_entity_decode($shipsTo, ENT_QUOTES, 'UTF-8'));

        $sellerID = $cd->find("span[@class='mbg-nw']", 0)->plaintext;
        $sellerID = trim(html_entity_decode($sellerID, ENT_QUOTES, 'UTF-8'));

        $category = $cd->find("ul[@class='bc-ul u-flL']", 0)->plaintext;
        $category = trim(html_entity_decode($category, ENT_QUOTES, 'UTF-8'));

        $itemSpec = $cd->find("div[@class='section']", 0)->plaintext;
        $itemSpec = trim(html_entity_decode($itemSpec, ENT_QUOTES, 'UTF-8')); 

        $itemSpec00 = $cd->find("td[@width='50.0%']", 0)->plaintext;
        $itemSpec00 = trim(html_entity_decode($itemSpec00, ENT_QUOTES, 'UTF-8'));       

        $itemSpec01 = $cd->find("td[@width='50.0%']", 1)->plaintext;
        $itemSpec01 = trim(html_entity_decode($itemSpec01, ENT_QUOTES, 'UTF-8'));   

        $itemSpec02 = $cd->find("td[@width='50.0%']", 2)->plaintext;
        $itemSpec02 = trim(html_entity_decode($itemSpec02, ENT_QUOTES, 'UTF-8'));   


        $repImage = $cd->find("img[@id='icImg']", 0)->src;
        $repImage = str_replace("35.JPG", "57.JPG", $repImage);


        $all = $cd->find("div[@class='enlargeImgZout']", 0)->plaintext;

        $detailsTable = $cd->find("table[@class='vi-ia-attrGroup'] tr[2] td table tr th");

        $condition = "";

        $manufacturer = "";
        $model = "";
        $type = "";
        $doors = "";
        $colour = "";
        $year = "";
        $regDate = "";
        $engineSize = "";
        $transmission = "";
        $fuel = "";
        $previousOwners = "";
        $metallicPaint = "";
        $modelYear = "";
        $seats = "";
        $regMark = "";
        $mileage = "";
        $power = "";
        $manufacturersWarranty = "";
        $safetyFeatures = "";
        $exterior = "";
        $interiorComfortOptions = "";
        $serviceHistoryAvailable = "";
        $v5RegistrationDocument = "";
        $inCarAudio = "";
        $driveSide = "";
        $roadTax = "";
        $motExpiry = "";
        $previouslyRegisteredOverseas = "";
        
        foreach($detailsTable as $dn)
        { 
            $start = $dn->plaintext;
            $value = $dn->nextSibling()->plaintext;
            $value02 = $cd->find("td[@width='50.0%']", 0)->plaintext;
            
            //http://www.ebay.co.uk/itm/2011-VOLKSWAGEN-GOLF-S-BLUEMOTION-TDI-BLUE-HPI-CLEAR-/110915608952?pt=Automobiles_UK&hash=item19d315e178&autorefresh=true
            if (strpos($start, "Reg. Mark:") !== false)
            {
                $regMark = trim(str_replace("Get the Vehicle Status Report", "", $value));
            }
            else if (strpos($start, "Manufacturer:") !== false) $manufacturer = $value;
            else if (strpos($start, "Model:") !== false) $model = $value;
            else if (strpos($start, "Type:") !== false) $type = $value;
            else if (strpos($start, "Doors:") !== false) $doors = $value;
            else if (strpos($start, "Colour:") !== false) $colour = $value;
            else if (strpos($start, "Year:") !== false) $year = $value;
            else if (strpos($start, "Reg. Date:") !== false) $regDate = $value;
            else if (strpos($start, "Engine Size:") !== false) $engineSize = $value;
            else if (strpos($start, "Transmission:") !== false) $transmission = $value;
            else if (strpos($start, "Fuel:") !== false) $fuel = $value;
            else if (strpos($start, "Fuel Type:") !== false) $fuel = $value;
            else if (strpos($start, "Previous Owners:") !== false) $previousOwners = $value;
            else if (strpos($start, "Metallic Paint:") !== false) $metallicPaint = $value;
            else if (strpos($start, "Drive Side:") !== false) $driveSide = $value;
            else if (strpos($start, "MOT Expiry:") !== false) $motExpiry = $value;
            else if (strpos($start, "Road Tax:") !== false) $roadTax = $value;
            else if (strpos($start, "Previously Registered Overseas:") !== false) $previouslyRegisteredOverseas = $value;
            else if (strpos($start, "Model Year:") !== false) $modelYear = $value;
            else if (strpos($start, "Seats:") !== false) $seats = $value;
            else if (strpos($start, "Mileage:") !== false) $mileage = "";
            else if (strpos($start, "Power: ") !== false) $power = "";
            else if (strpos($start, "Manufacturer's Warranty: ") !== false) $manufacturersWarranty = "";
            else if (strpos($start, "Safety Features:") !== false) $safetyFeatures = "";
            else if (strpos($start, "Exterior:") !== false) $exterior = "";
            else if (strpos($start, "Interior/Comfort Options:") !== false) $interiorComfortOptions = "";
            else if (strpos($start, "Service History Available:") !== false) $serviceHistoryAvailable = "";
            else if (strpos($start, "Service History:") !== false) $serviceHistoryAvailable = "";
            else if (strpos($start, "V5 Document:") !== false) $v5RegistrationDocument = "";
            else if (strpos($start, "V5 Registration Document:") !== false) $v5RegistrationDocument = "";
            else if (strpos($start, "In-Car Audio:") !== false) $inCarAudio = "";

            else if (strpos($start, "Country of Manufacture:") !== false) $condition = $value02;
        }

        $record = array(
            'images' => $images,
            'rep Image' => $repImage,
            'item location' => $itemLocation,
            'ships to' => $shipsTo,
            'seller ID' => $sellerID,
            'categories' => $category,
            'descriptions' => $description,
            'id' => $id,
            'title' => $title, 
            'price' =>  $price, 
//            'condition' => $condition,
            'item spec' => $itemSpec,
            'url' => $carUrl,
            'all' => $all,
            'all02' => $all02,
/*
            'time left' => $timeLeft,
            'manufacturer' => $manufacturer,
            'model' => $model,
            'type' => $type,
            'doors' => $doors,
            'colour' => $colour,
            'year' => $year,
            'reg data' => $regDate,
            'engine size' => $engineSize,
            'transmission' => $transmission,
            'fuel' => $fuel,
            'previous owners' => $previousOwners,
            'metallic paint' => $metallicPaint,
            'model year' => $modelYear,
            'seats' => $seats,
            'reg mark' => $regMark,
            'mileage' => $mileage,
            'power' => $power,
            'manufacturers warranty' => $manufacturersWarranty,
            'safety features' => $safetyFeatures,
            'exterior' => $exterior,
            'interior comfort options' => $interiorComfortOptions,
            'service history available' => $serviceHistoryAvailable,
            'v5 document' => $v5RegistrationDocument,
            'in car audio' => $inCarAudio,
            'drive side' => $driveSide,
            'road tax' => $roadTax,
            'MOT expiry' => $motExpiry,
            'previously registered overseas' => $previouslyRegisteredOverseas,
*/

        );

        scraperwiki::save_sqlite(array('id'), $record, $table_name="swdata", $verbose=1); 






    }

    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
