<?php

require 'scraperwiki/simple_html_dom.php';

$page = 1;
$url =  "http://www.ebay.com/sch/i.html?_trksid=p5197.m570.l1313&_nkw=korean+war&_sacat=0" ;

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

        $id = $cd->find("span[@class='vi-xs vi-lk']", 0)->plaintext; 
        $id = html_entity_decode($id, ENT_QUOTES, 'UTF-8');
        $id = trim(str_replace("Item number:", "", $id));
        
        $price = $cd->find("span[@itemprop='price']", 0)->plaintext; 
        $price = trim(html_entity_decode($price, ENT_QUOTES, 'UTF-8'));

        $title = $cd->find("h1[@class='vi-is1-titleH1']", 0)->plaintext;
        $title = trim(html_entity_decode($title, ENT_QUOTES, 'UTF-8')); 

        $timeLeftn = $cd->find("span[@class='vi-is1-ctdn vi-is1-tml']", 0);
        $timeLeft  = '';
        if (isset($timeLeftn)) $timeLeft = trim(html_entity_decode($timeLeftn->plaintext, ENT_QUOTES, 'UTF-8'));  
 


        $itemCondition = $cd->find("span[@class='vi-is1-condText']", 0)->plaintext;
        $itemCondition = trim(html_entity_decode($itemCondition, ENT_QUOTES, 'UTF-8'));

        $itemLocation = $cd->find("span[@class='g-b']", 0)->plaintext; //differentiate itemlocation and shipsto!
        $itemLocation = trim(html_entity_decode($itemLocation, ENT_QUOTES, 'UTF-8'));

        $shipsTo = $cd->find("span[@class='g-b']", 1)->plaintext; //differentiate itemLocation and shipsto!
        $shipsTo = trim(html_entity_decode($shipsTo, ENT_QUOTES, 'UTF-8'));

        $sellerID = $cd->find("span[@class='mbg-nw']", 0)->plaintext;
        $sellerID = trim(html_entity_decode($sellerID, ENT_QUOTES, 'UTF-8'));

        $description = $cd->find("div[@id='desc_div']", 0)->plaintext;
        $description = trim(html_entity_decode($description, ENT_QUOTES, 'UTF-8'));

        $category = $cd->find("ul[@class='in']", 0)->plaintext;
        $category = trim(html_entity_decode($category, ENT_QUOTES, 'UTF-8'));

////

        $detailsTable = $cd->find("table[@class='vi-ia-attrGroup'] tr[2] td table tr th");

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
            
            //http://www.ebay.co.uk/itm/2011-VOLKSWAGEN-GOLF-S-BLUEMOTION-TDI-BLUE-HPI-CLEAR-/110915608952?pt=Automobiles_UK&hash=item19d315e178&autorefresh=true
            if (strpos($start, "Reg. Mark:") !== false)
            {
                $regMark = trim(str_replace("Get the Vehicle Status Report", "", $value));
            }
            else if (strpos($start, "Manufacturer:") !== false) $manufacturer = $value;
            else if (strpos($start, "Model:") !== false) $model = $value;

        }

        $record = array(

            'category' => $category,
            'description' => $description,
            'seller ID' => $sellerID,
            'payments' => $payments,
            'ships to' => $shipsTo,
            'item location' => $itemLocation,
            'shipping' => $shipping,
            'number of bids' => $numberOfBid,
            'item condition' => $itemCondition,
            'id' => $id,
            'title' => $title, 
            'price' =>  $price, 
            'time left' => $timeLeft,
/*
            'manufacturer' => $manufacturer,
            'model' => $model,

*/
            'url' => $carUrl,
        );

        scraperwiki::save_sqlite(array('id'), $record, $table_name="swdata", $verbose=1); 

        $images = $cd->find("input[@name='iurls']", 0)->value; 
        if (isset($images))
        {
            $images = trim(html_entity_decode($images , ENT_QUOTES, 'UTF-8'));  

            $images = explode("|", $images);
            $i = 0;
            foreach($images as $img)
            { 
                //0#http://i.ebayimg.com/t/chrysler-grand-voyager-3-3-auto-petrol-/00/s/MTIwMFgxNjAw#$(KGrHqNHJE!E92ClN+7LBP+!08)cw!~~60_39.JPG#$(KGrHqNHJE!E92ClN+7LBP+!08)cw!~~60_12.JPG
                $img_data = explode("#", $img);
                $img_path = $img_data[1];
                $img_name = $img_data[3];
                
                //print $img_path . "/" . $img_name . "\n";
                
                $irecord = array(
                    'carId' => $id,
                    'imageId' => $i,
                    'image' => $img_path . "/" . $img_name,
                );
                
                scraperwiki::save_sqlite(array('imageId', 'carId'), $irecord, $table_name="images", $verbose=1); 
                $i++;

                copy($img_path, 'local//Users/sohinhwang/Desktop/KW/' . $id . '_' . $i);

            }
        }
        //print $images  . "\n" ;
    }

    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';

$page = 1;
$url =  "http://www.ebay.com/sch/i.html?_trksid=p5197.m570.l1313&_nkw=korean+war&_sacat=0" ;

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

        $id = $cd->find("span[@class='vi-xs vi-lk']", 0)->plaintext; 
        $id = html_entity_decode($id, ENT_QUOTES, 'UTF-8');
        $id = trim(str_replace("Item number:", "", $id));
        
        $price = $cd->find("span[@itemprop='price']", 0)->plaintext; 
        $price = trim(html_entity_decode($price, ENT_QUOTES, 'UTF-8'));

        $title = $cd->find("h1[@class='vi-is1-titleH1']", 0)->plaintext;
        $title = trim(html_entity_decode($title, ENT_QUOTES, 'UTF-8')); 

        $timeLeftn = $cd->find("span[@class='vi-is1-ctdn vi-is1-tml']", 0);
        $timeLeft  = '';
        if (isset($timeLeftn)) $timeLeft = trim(html_entity_decode($timeLeftn->plaintext, ENT_QUOTES, 'UTF-8'));  
 


        $itemCondition = $cd->find("span[@class='vi-is1-condText']", 0)->plaintext;
        $itemCondition = trim(html_entity_decode($itemCondition, ENT_QUOTES, 'UTF-8'));

        $itemLocation = $cd->find("span[@class='g-b']", 0)->plaintext; //differentiate itemlocation and shipsto!
        $itemLocation = trim(html_entity_decode($itemLocation, ENT_QUOTES, 'UTF-8'));

        $shipsTo = $cd->find("span[@class='g-b']", 1)->plaintext; //differentiate itemLocation and shipsto!
        $shipsTo = trim(html_entity_decode($shipsTo, ENT_QUOTES, 'UTF-8'));

        $sellerID = $cd->find("span[@class='mbg-nw']", 0)->plaintext;
        $sellerID = trim(html_entity_decode($sellerID, ENT_QUOTES, 'UTF-8'));

        $description = $cd->find("div[@id='desc_div']", 0)->plaintext;
        $description = trim(html_entity_decode($description, ENT_QUOTES, 'UTF-8'));

        $category = $cd->find("ul[@class='in']", 0)->plaintext;
        $category = trim(html_entity_decode($category, ENT_QUOTES, 'UTF-8'));

////

        $detailsTable = $cd->find("table[@class='vi-ia-attrGroup'] tr[2] td table tr th");

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
            
            //http://www.ebay.co.uk/itm/2011-VOLKSWAGEN-GOLF-S-BLUEMOTION-TDI-BLUE-HPI-CLEAR-/110915608952?pt=Automobiles_UK&hash=item19d315e178&autorefresh=true
            if (strpos($start, "Reg. Mark:") !== false)
            {
                $regMark = trim(str_replace("Get the Vehicle Status Report", "", $value));
            }
            else if (strpos($start, "Manufacturer:") !== false) $manufacturer = $value;
            else if (strpos($start, "Model:") !== false) $model = $value;

        }

        $record = array(

            'category' => $category,
            'description' => $description,
            'seller ID' => $sellerID,
            'payments' => $payments,
            'ships to' => $shipsTo,
            'item location' => $itemLocation,
            'shipping' => $shipping,
            'number of bids' => $numberOfBid,
            'item condition' => $itemCondition,
            'id' => $id,
            'title' => $title, 
            'price' =>  $price, 
            'time left' => $timeLeft,
/*
            'manufacturer' => $manufacturer,
            'model' => $model,

*/
            'url' => $carUrl,
        );

        scraperwiki::save_sqlite(array('id'), $record, $table_name="swdata", $verbose=1); 

        $images = $cd->find("input[@name='iurls']", 0)->value; 
        if (isset($images))
        {
            $images = trim(html_entity_decode($images , ENT_QUOTES, 'UTF-8'));  

            $images = explode("|", $images);
            $i = 0;
            foreach($images as $img)
            { 
                //0#http://i.ebayimg.com/t/chrysler-grand-voyager-3-3-auto-petrol-/00/s/MTIwMFgxNjAw#$(KGrHqNHJE!E92ClN+7LBP+!08)cw!~~60_39.JPG#$(KGrHqNHJE!E92ClN+7LBP+!08)cw!~~60_12.JPG
                $img_data = explode("#", $img);
                $img_path = $img_data[1];
                $img_name = $img_data[3];
                
                //print $img_path . "/" . $img_name . "\n";
                
                $irecord = array(
                    'carId' => $id,
                    'imageId' => $i,
                    'image' => $img_path . "/" . $img_name,
                );
                
                scraperwiki::save_sqlite(array('imageId', 'carId'), $irecord, $table_name="images", $verbose=1); 
                $i++;

                copy($img_path, 'local//Users/sohinhwang/Desktop/KW/' . $id . '_' . $i);

            }
        }
        //print $images  . "\n" ;
    }

    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
