<?php

require 'scraperwiki/simple_html_dom.php';

$page = 1;
$url =  "http://fieldlibrary.net/film_url.htm";

while (true)
{
    $html = scraperWiki::scrape( $url );           
    $dom = new simple_html_dom();
    $dom->load($html); 

    $results = $dom->find("a[@class='Body']");
    print " found " . count($results) . " results on page " . $page . "\n"; 
    print $results;

    foreach($results as $data)
    {
        set_time_limit(25);

        $carUrl = $data ->href;
        $carHtml = scraperWiki::scrape($carUrl); 
        $cd = new simple_html_dom(); 
        $cd->load($carHtml); 

        $title = $cd->find("h1[@class='itemTitle']", 0)->plaintext;
        $title = trim(html_entity_decode($title, ENT_QUOTES, 'UTF-8')); 

        $info = $cd->find("div[@class='information']", 0)->plaintext; 
        $info = trim(html_entity_decode($info, ENT_QUOTES, 'UTF-8'));

        $details = $cd->find("div[@class='accordion']", 0)->plaintext; 
        $details = trim(html_entity_decode($details, ENT_QUOTES, 'UTF-8'));

        $path = $cd->find("div[@class='hlr-box sidebar-box']", 0)->plaintext; 
        $path = trim(html_entity_decode($path, ENT_QUOTES, 'UTF-8'));

        $image = $cd->find("ul[@class='media-list']", 0);
        $image = trim(html_entity_decode($image, ENT_QUOTES, 'UTF-8'));



//  $repImage = $cd->find("img[@id='icImg']", 0)->src;
  //      $repImage = str_replace("35.JPG", "57.JPG", $repImage);

       
//        $repImage2 = $cd->find("a[@class='download-link']", 0)->str;
//        $repImage2 = str_replace("35.JPG", "57.JPG", $repImage2);


    
/*    
        $price = $cd->find("span[@itemprop='price']", 0)->plaintext; 
        $price = trim(html_entity_decode($price, ENT_QUOTES, 'UTF-8'));

      

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

       
*/


        $record = array(
            'url' => $carUrl,

            'title' => $title,
            'info' => $info,
            'image' => $image,
            'path' => $path,
            'detaills' => $details,

   //         'rep Image2' => $repImage2,
        );

/*

           'price' =>  $price, 
         
           'item location' => $itemLocation,
           'ships to' => $shipsTo,
           'seller ID' => $sellerID,
           'categories' => $category,
           'descriptions' => $description,
           'id' => $id,
*/



        scraperwiki::save_sqlite(array('title'), $record, $table_name="swdata", $verbose=1);





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

$page = 1;
$url =  "http://fieldlibrary.net/film_url.htm";

while (true)
{
    $html = scraperWiki::scrape( $url );           
    $dom = new simple_html_dom();
    $dom->load($html); 

    $results = $dom->find("a[@class='Body']");
    print " found " . count($results) . " results on page " . $page . "\n"; 
    print $results;

    foreach($results as $data)
    {
        set_time_limit(25);

        $carUrl = $data ->href;
        $carHtml = scraperWiki::scrape($carUrl); 
        $cd = new simple_html_dom(); 
        $cd->load($carHtml); 

        $title = $cd->find("h1[@class='itemTitle']", 0)->plaintext;
        $title = trim(html_entity_decode($title, ENT_QUOTES, 'UTF-8')); 

        $info = $cd->find("div[@class='information']", 0)->plaintext; 
        $info = trim(html_entity_decode($info, ENT_QUOTES, 'UTF-8'));

        $details = $cd->find("div[@class='accordion']", 0)->plaintext; 
        $details = trim(html_entity_decode($details, ENT_QUOTES, 'UTF-8'));

        $path = $cd->find("div[@class='hlr-box sidebar-box']", 0)->plaintext; 
        $path = trim(html_entity_decode($path, ENT_QUOTES, 'UTF-8'));

        $image = $cd->find("ul[@class='media-list']", 0);
        $image = trim(html_entity_decode($image, ENT_QUOTES, 'UTF-8'));



//  $repImage = $cd->find("img[@id='icImg']", 0)->src;
  //      $repImage = str_replace("35.JPG", "57.JPG", $repImage);

       
//        $repImage2 = $cd->find("a[@class='download-link']", 0)->str;
//        $repImage2 = str_replace("35.JPG", "57.JPG", $repImage2);


    
/*    
        $price = $cd->find("span[@itemprop='price']", 0)->plaintext; 
        $price = trim(html_entity_decode($price, ENT_QUOTES, 'UTF-8'));

      

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

       
*/


        $record = array(
            'url' => $carUrl,

            'title' => $title,
            'info' => $info,
            'image' => $image,
            'path' => $path,
            'detaills' => $details,

   //         'rep Image2' => $repImage2,
        );

/*

           'price' =>  $price, 
         
           'item location' => $itemLocation,
           'ships to' => $shipsTo,
           'seller ID' => $sellerID,
           'categories' => $category,
           'descriptions' => $description,
           'id' => $id,
*/



        scraperwiki::save_sqlite(array('title'), $record, $table_name="swdata", $verbose=1);





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

$page = 1;
$url =  "http://fieldlibrary.net/film_url.htm";

while (true)
{
    $html = scraperWiki::scrape( $url );           
    $dom = new simple_html_dom();
    $dom->load($html); 

    $results = $dom->find("a[@class='Body']");
    print " found " . count($results) . " results on page " . $page . "\n"; 
    print $results;

    foreach($results as $data)
    {
        set_time_limit(25);

        $carUrl = $data ->href;
        $carHtml = scraperWiki::scrape($carUrl); 
        $cd = new simple_html_dom(); 
        $cd->load($carHtml); 

        $title = $cd->find("h1[@class='itemTitle']", 0)->plaintext;
        $title = trim(html_entity_decode($title, ENT_QUOTES, 'UTF-8')); 

        $info = $cd->find("div[@class='information']", 0)->plaintext; 
        $info = trim(html_entity_decode($info, ENT_QUOTES, 'UTF-8'));

        $details = $cd->find("div[@class='accordion']", 0)->plaintext; 
        $details = trim(html_entity_decode($details, ENT_QUOTES, 'UTF-8'));

        $path = $cd->find("div[@class='hlr-box sidebar-box']", 0)->plaintext; 
        $path = trim(html_entity_decode($path, ENT_QUOTES, 'UTF-8'));

        $image = $cd->find("ul[@class='media-list']", 0);
        $image = trim(html_entity_decode($image, ENT_QUOTES, 'UTF-8'));



//  $repImage = $cd->find("img[@id='icImg']", 0)->src;
  //      $repImage = str_replace("35.JPG", "57.JPG", $repImage);

       
//        $repImage2 = $cd->find("a[@class='download-link']", 0)->str;
//        $repImage2 = str_replace("35.JPG", "57.JPG", $repImage2);


    
/*    
        $price = $cd->find("span[@itemprop='price']", 0)->plaintext; 
        $price = trim(html_entity_decode($price, ENT_QUOTES, 'UTF-8'));

      

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

       
*/


        $record = array(
            'url' => $carUrl,

            'title' => $title,
            'info' => $info,
            'image' => $image,
            'path' => $path,
            'detaills' => $details,

   //         'rep Image2' => $repImage2,
        );

/*

           'price' =>  $price, 
         
           'item location' => $itemLocation,
           'ships to' => $shipsTo,
           'seller ID' => $sellerID,
           'categories' => $category,
           'descriptions' => $description,
           'id' => $id,
*/



        scraperwiki::save_sqlite(array('title'), $record, $table_name="swdata", $verbose=1);





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
