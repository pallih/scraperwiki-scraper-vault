<?php

require 'scraperwiki/simple_html_dom.php';

$page = 119;
$url =  "http://www.ebay.com/sch/Militaria-/13956/i.html?_from=R40&_nkw=newspaper";

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

      //  $itemSpec = $cd->find("div[@class='section']", 0)->plaintext;
     //   $itemSpec = trim(html_entity_decode($itemSpec, ENT_QUOTES, 'UTF-8')); 

      //  $itemSpec00 = $cd->find("td[@width='50.0%']", 0)->plaintext;
      //  $itemSpec00 = trim(html_entity_decode($itemSpec00, ENT_QUOTES, 'UTF-8'));       

    //    $itemSpec01 = $cd->find("td[@width='50.0%']", 1)->plaintext;
  //      $itemSpec01 = trim(html_entity_decode($itemSpec01, ENT_QUOTES, 'UTF-8'));   

     //   $itemSpec02 = $cd->find("td[@width='50.0%']", 2)->plaintext;
     //   $itemSpec02 = trim(html_entity_decode($itemSpec02, ENT_QUOTES, 'UTF-8'));   


       $repImage = $cd->find("img[@id='icImg']", 0)->src;
        $repImage = str_replace("35.JPG", "57.JPG", $repImage);
//        $repImage = trim(html_entity_decode($repImage, ENT_QUOTES, 'UTF-8'));
//        $imgLink = explode("#", $repImage);

        $all = $cd->find("div[@class='vi_zoom_trigger_mask']", 0)->plaintext;
//        $all = trim(html_entity_decode($all, ENT_QUOTES, 'UTF-8'));   
//        $all02 = $all->find("img[@index='0']", 0)->src;

//        $first = $all->plaintext;;

//        $iii = ;
//        $iii = strpos($first, "http://i.ebayimg.com/t/");

///            else if (strpos($start, "Manufacturer:") !== false) $manufacturer = $value;
 

        $record = array(
            //'images' => $images,
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
         //   'item spec' => $itemSpec,
            'url' => $carUrl,
        //    'all' => $all,
      //      'all02' => $all02,

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
            }
        }




    }

    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';

$page = 119;
$url =  "http://www.ebay.com/sch/Militaria-/13956/i.html?_from=R40&_nkw=newspaper";

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

      //  $itemSpec = $cd->find("div[@class='section']", 0)->plaintext;
     //   $itemSpec = trim(html_entity_decode($itemSpec, ENT_QUOTES, 'UTF-8')); 

      //  $itemSpec00 = $cd->find("td[@width='50.0%']", 0)->plaintext;
      //  $itemSpec00 = trim(html_entity_decode($itemSpec00, ENT_QUOTES, 'UTF-8'));       

    //    $itemSpec01 = $cd->find("td[@width='50.0%']", 1)->plaintext;
  //      $itemSpec01 = trim(html_entity_decode($itemSpec01, ENT_QUOTES, 'UTF-8'));   

     //   $itemSpec02 = $cd->find("td[@width='50.0%']", 2)->plaintext;
     //   $itemSpec02 = trim(html_entity_decode($itemSpec02, ENT_QUOTES, 'UTF-8'));   


       $repImage = $cd->find("img[@id='icImg']", 0)->src;
        $repImage = str_replace("35.JPG", "57.JPG", $repImage);
//        $repImage = trim(html_entity_decode($repImage, ENT_QUOTES, 'UTF-8'));
//        $imgLink = explode("#", $repImage);

        $all = $cd->find("div[@class='vi_zoom_trigger_mask']", 0)->plaintext;
//        $all = trim(html_entity_decode($all, ENT_QUOTES, 'UTF-8'));   
//        $all02 = $all->find("img[@index='0']", 0)->src;

//        $first = $all->plaintext;;

//        $iii = ;
//        $iii = strpos($first, "http://i.ebayimg.com/t/");

///            else if (strpos($start, "Manufacturer:") !== false) $manufacturer = $value;
 

        $record = array(
            //'images' => $images,
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
         //   'item spec' => $itemSpec,
            'url' => $carUrl,
        //    'all' => $all,
      //      'all02' => $all02,

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
            }
        }




    }

    $nextPage = $dom->find("a[@title='Next page of results']", 0); 
    if (!isset($nextPage)) break;
   
    $url = $nextPage->href;
    $page++;
}
?>
