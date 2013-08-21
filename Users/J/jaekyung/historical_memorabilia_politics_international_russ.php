<?php

require 'scraperwiki/simple_html_dom.php';

$page = 166;
$url =  "http://www.ebay.com/sch/Russia-/12517/i.html?_from=R40&_nkw=historical+memorabilia";

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

        $id = $cd->find("div[@class='u-flR']", 0)->plaintext; 
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

        $category = $cd->find("td[@class='vi-VR-brumblnkLst vi-VR-brumb-hasNoPrdlnks']", 0)->plaintext;
        $category = trim(html_entity_decode($category, ENT_QUOTES, 'UTF-8'));

       $repImage = $cd->find("img[@id='icImg']", 0)->src;
        $repImage = str_replace("35.JPG", "57.JPG", $repImage);


        $record = array(
            'rep Image' => $repImage,
            'item location' => $itemLocation,
            'ships to' => $shipsTo,
            'seller ID' => $sellerID,
            'categories' => $category,
            'descriptions' => $description,
            'id' => $id,
            'title' => $title, 
            'price' =>  $price, 
            'url' => $carUrl,
        );

      scraperwiki::save_sqlite(array('id'), $record, $table_name="swdata", $verbose=1); 












/*        
        $images = $cd->find("img[@class='img']", 2)->src; 
              
        print $images;
                
         $irecord = array(
                    'carId' => $id,
                    'imageId' => $id,
                    'image' => $images,
                );
                

        scraperwiki::save_sqlite(array('imageId', 'carId'), $irecord, $table_name="images", $verbose=1); 
        //$i++;


*/






    }




    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';

$page = 166;
$url =  "http://www.ebay.com/sch/Russia-/12517/i.html?_from=R40&_nkw=historical+memorabilia";

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

        $id = $cd->find("div[@class='u-flR']", 0)->plaintext; 
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

        $category = $cd->find("td[@class='vi-VR-brumblnkLst vi-VR-brumb-hasNoPrdlnks']", 0)->plaintext;
        $category = trim(html_entity_decode($category, ENT_QUOTES, 'UTF-8'));

       $repImage = $cd->find("img[@id='icImg']", 0)->src;
        $repImage = str_replace("35.JPG", "57.JPG", $repImage);


        $record = array(
            'rep Image' => $repImage,
            'item location' => $itemLocation,
            'ships to' => $shipsTo,
            'seller ID' => $sellerID,
            'categories' => $category,
            'descriptions' => $description,
            'id' => $id,
            'title' => $title, 
            'price' =>  $price, 
            'url' => $carUrl,
        );

      scraperwiki::save_sqlite(array('id'), $record, $table_name="swdata", $verbose=1); 












/*        
        $images = $cd->find("img[@class='img']", 2)->src; 
              
        print $images;
                
         $irecord = array(
                    'carId' => $id,
                    'imageId' => $id,
                    'image' => $images,
                );
                

        scraperwiki::save_sqlite(array('imageId', 'carId'), $irecord, $table_name="images", $verbose=1); 
        //$i++;


*/






    }




    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
