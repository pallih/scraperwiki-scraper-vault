<?php

require 'scraperwiki/simple_html_dom.php';

//scraperwiki::attach('itemfilter_utils');
$state = "Oregon,Washington"; //Must be Titlecase e.g, Alabama, Michigan. or use an array separated by commas Alabama, Washington
$states = explode(",",$state);
print_r($states);

//$jsonManufacturerScraper = scraperwiki::get_var('manufacturer_scraper');
//Get a unique list of item manufacturers
//$jsonSearchData = file_get_contents($jsonManufacturerScraper);
//echo $jsonSearchData;
$jsonSearchData = '[
                    {"manufacturer":"Apogee","name":"Duet"},
                    {"manufacturer":"Apogee","name":"Ensemble"},
                    {"manufacturer":"Mackie","name":"Onyx 1640i"},
                    {"manufacturer":"Mackie","name":"Audio Interface"},
                    {"manufacturer":"Metric","name":"Halo"},
                    {"manufacturer":"M-Audio","name":"MidiSport"},
                    {"manufacturer":"Motu","name":"Ultralite Mk3"},
                    {"manufacturer":"Motu","name":"Ultralite MKIII"},
                    {"manufacturer":"Motu","name":"Ultralite MK111"},
                    {"manufacturer":"Motu","name":"Ultralite MKIII"},
                    {"manufacturer":"Motu","name":"8 pre"},
                    {"manufacturer":"Motu","name":"828 mk3"},
                    {"manufacturer":"Motu","name":"896 mk3"},
                    {"manufacturer":"Motu","name":"2408 mk3"},
                    {"manufacturer":"Motu","name":"24IO"},
                    {"manufacturer":"Motu","name":"Firewire Audio Interface"},
                    {"manufacturer":"Native Instruments","name":"audio interface"},
                    {"manufacturer":"Native Instruments","name":"Audio 6"},
                    {"manufacturer":"Native Instruments","name":"Audio 8"},
                    {"manufacturer":"Native Instruments","name":"Audio 10"},
                    {"manufacturer":"Native Instruments","name":"Audio 2"},
                    {"manufacturer":"Traktor","name":"audio interface"},
                    {"manufacturer":"Traktor","name":"Audio 6"},
                    {"manufacturer":"Traktor","name":"Audio 8"},
                    {"manufacturer":"Traktor","name":"Audio 10"},
                    {"manufacturer":"Traktor","name":"Audio 2"},
                    {"manufacturer":"PreSonus","name":"FireStudio"},
                    {"manufacturer":"RME","name":"Fireface 400"},
                    {"manufacturer":"Tascam","name":"FW 1884"}
                ]';

$wordsToIgnore = "keyboard,horn,polk audio,shure,Audio Rack,Starter Set,Starter Audio,Pro Starter,Stereo Compressor,Kerzweil,subwoofer,digital piano,controller,compressor";
$ignoreWords = explode(',',$wordsToIgnore);
echo "Total ignored words: ".count($ignoreWords)."\n";

$cityDepth = 0; //Set to 0 to search all cities found in the database  
$manufacturerDepth = 0; //Set to 0 to search all item manufacturers found in the database
$depthOverride = true; //Cancels the depth variables

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}


if(!empty($jsonSearchData)){
    $manufacturerCounter = 0;
    $jsonManufacturers = json_decode($jsonSearchData);
    //echo "<pre>";
    //print_r($jsonManufacturers);
    //echo "</pre>";
    foreach($states as $state){
        $state = trim($state);
        echo "Searching state: ".$state."\n";
        $state = urlencode($state);
        if(empty($foundItems)){
            $foundItems = findOnCraigslist($state,$jsonManufacturers,$ignoreWords,$cityDepth,$depthOverride);
        }else{
            $foundItems = array_merge($foundItems,findOnCraigslist($state,$jsonManufacturers,$ignoreWords,$cityDepth,$depthOverride));
        }
    }
    if(!empty($foundItems)){
        $saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link'), $foundItems);
        print strval($saveMessage); 
    }else{
        //Delete existing data
        $info = scraperwiki::table_info($name="swdata");
        if(!empty($info)){
            scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
        }
    }
}



/**
* Parses craigslist and returns items
* @param String state
* @param String itemManufacturer
* @param ignoreWords
* @param cityDepth
* @param depthOverride
* @return Array foundItems
*/
function findOnCraigslist($state = "Oregon",$jsonManufacturers = null,$ignoreWords=array(),$cityDepth=null,$depthOverride=true){
     $cityCounter = 0;
     $itemFoundCounter = 0;
     $foundItems = array();
     //Use the Scraper Web API and pull the results in JSON format
     $jsonData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=craigslist_cities_1&query=select%20*%20from%20%60swdata%60%20WHERE%20state%20%3D%20'".$state."'");
     $jsonCraigCities = json_decode($jsonData);
     //$jsonItemManufacturerData = file_get_contents($manufacturerScraperURL."%20WHERE%20manufacturer%20%3D%20'".$itemManufacturer."'");
     //$jsonItemsFromManufacturer = json_decode($jsonItemManufacturerData);
     //echo "There are ".count($jsonItemsFromManufacturer)." ".$itemManufacturer." items in the system.\n";
     $foundURLS = array();    
     if(!empty($jsonData)){
          foreach($jsonCraigCities as $city){
                $itemCounter = 0;
                echo "-> Parsing link: ".$city->link."\n";
                //Search each city for each item for a certain item manufacturer in the vintage item database.
                if($cityCounter < $cityDepth || $depthOverride == true || $cityDepth == 0){
                     foreach($jsonManufacturers as $item){
                          //Example musical instrument search string http://portland.craigslist.org/search/msg?query=korg+microkorg&srchType=A&minAsk=5&maxAsk=&hasPic=1     
                          if(!empty($item)){
                                $itemName = urlencode(trim($item->name));
                                if(!empty($itemName)){         
                                      $tManName = preg_replace("/\s/","_",$item->manufacturer);//Build a temp name for the array key
                                      $itemManufacturer = urlencode($item->manufacturer);
                                      $search_string = '"'.strtolower($itemManufacturer)."+".$itemName.'"';
                                      //$search_string = urlencode($search_string);
                                      $search_string2 = urlencode($itemName);
                                      //"%7C" = | (This establishes Craiglist's OR search.)
                                      if(!empty($search_string) && !empty($search_string2)){
                                            $search_url = $city->link."/search/msg?query=".$search_string."+%7C+".$search_string2."&srchType=T&minAsk=5&maxAsk=&hasPic=1";//Title only and has image
                                            echo "--> Scraping: ".$search_url."\n";
                                            $html = scraperWiki::scrape($search_url); 
                                            $dom = new simple_html_dom();
                                            $dom->load($html); //Load the HTML 
                                            foreach($dom->find("p.row") as $item){
                                                 $itemLink = $item->find('a',0); //Find the second link (not the image link)
                                                 if(!empty($itemLink->href)){
                                                      $itemName = $itemLink->innertext;
                                                      $itemName = preg_replace('/\s-/','',$itemName);
                                                      $itemName = trim($itemName);
                                                      //Check the name against the ignore words
                                                      $addItem = 1;
                                                      foreach($ignoreWords as $word){
                                                            //Make sure that the itemName doesn't include a word to ignore
                                                            if(strpos(strtolower($itemName),strtolower($word))===false){
                                                                 //Do something
                                                            }else{
                                                                 $addItem = 0;
                                                            }
                                                      }
                                                      //Check to make sure that the item link matches the search city link. 
                                                      $searchCity = preg_match("@http://([a-z]*+)\.@",$city->link,$cityMatches);
                                                      $searchCity = trim($cityMatches[1]);
                                                      $itemCity = preg_match("@http://([a-z]*+)\.@",$itemLink->href,$itemCityMatches);
                                                      $itemCity = trim($itemCityMatches[1]);
                                                      //echo "Search city: ".$searchCity."\n";
                                                      //echo "Item city: ".$itemCity."\n";
                                                      if($itemCity != $searchCity){
                                                            $addItem = 0;
                                                      }
                                                      if($addItem == 1 && in_array($itemLink->href,$foundURLS) == 0){
                                                            echo $itemName."\n";
                                                            $itemInfo = $item->plaintext;
                                                            $itemInfo = explode('$',$itemInfo);
                                                            $itemPrice = "$".trim($itemInfo[1]);
                                                            $itemInfo = $itemInfo[0];
                                                            $itemInfo = explode('-',$itemInfo);
                                                            $itemInfo = preg_replace('/&nbsp;/','',$itemInfo);
                                                            $foundItems[$itemFoundCounter]['manufacturer'] = $itemManufacturer;
                                                            $foundItems[$itemFoundCounter]['name'] = $itemName;
                                                            $foundItems[$itemFoundCounter]['post_item_name'] = $itemName;
                                                            //Find the date and price
                                                            if(!empty($itemInfo)){
                                                                 if(isset($itemInfo[0])){
                                                                      $itemDate = trim($itemInfo[0]);
                                                                      $itemDate = preg_replace('/\s\s+/',' ',$itemDate); //Strip excess whitespace
                                                                      //Change date string
                                                                      $itemDateArray = explode(" ",$itemDate);
                                                                      $monthNumVal = getMonthNum($itemDateArray[0]); //ex Nov
                                                                      $curYear = date("Y");
                                                                      $itemDate = $curYear."-".$monthNumVal."-".$itemDateArray[1];
                                                                      echo "Date posted: ".$itemDate."\n";
                                                                      $foundItems[$itemFoundCounter]['post_item_date'] = $itemDate;
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_date'] = "";
                                                                 }
                                                                 if(isset($itemPrice)){
                                                                      $itemPrice = trim($itemPrice);
                                                                      $itemPrice = preg_replace('/\(.*\)/','',$itemPrice);
                                                                      $itemPrice = preg_replace('/[a-z]+|[A-Z]+/','',$itemPrice);
                                                                      $itemPrice = trim($itemPrice);
                                                                      echo "Price: ".$itemPrice."\n";
                                                                      //Only add the price if a dollar sign exists
                                                                      if($itemPrice[0] == "$"){
                                                                            $foundItems[$itemFoundCounter]['post_item_price'] = $itemPrice;
                                                                      }else{
                                                                            $foundItems[$itemFoundCounter]['post_item_price'] = "$".$itemPrice;
                                                                      }
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_price'] = "";
                                                                 }
                                                            }else{
                                                                 $foundItems[$itemFoundCounter]['post_item_date'] = "";
                                                                 $foundItems[$itemFoundCounter]['post_item_price'] = "";
                                                            }
                                                            $foundURLS[] = $itemLink->href; //Add the url to keep track and make sure that only unique URLs are added.
                                                            $foundItems[$itemFoundCounter]['post_item_link'] = $city->link;
                                                            $foundItems[$itemFoundCounter]['post_item_state'] = $city->state;
                                                            $foundItems[$itemFoundCounter]['query'] = $search_string."+%7C+".$search_string2;
                                                            $foundItems[$itemFoundCounter]['link'] = $itemLink->href;
                                                            //Find the page details on the page
                                                            $craigSynthItemPage = scraperWiki::scrape($itemLink->href); 
                                                            $craigSynthItemPageDOM = new simple_html_dom();
                                                            $craigSynthItemPageDOM->load($craigSynthItemPage); //Load the HTML
                                                            if(!empty($craigSynthItemPageDOM)){
                                                                 $craigSynthItemDesc = $craigSynthItemPageDOM->find("div#userbody",0);
                                                                 //print_r($craigSynthItemDesc);
                                                                 if(!empty($craigSynthItemDesc)) $craigSynthItemDesc = $craigSynthItemDesc->plaintext;
                                                                 $craigSynthItemBlurb = $craigSynthItemPageDOM->find("div#userbody] ul.blurbs",0);
                                                                 if(!empty($craigSynthItemBlurb)) $craigSynthItemBlurb = $craigSynthItemBlurb->plaintext;
                                                                 $craigSynthItemDesc = str_replace($craigSynthItemBlurb,"",$craigSynthItemDesc);
                                                                 $postImages = array();
                                                                 foreach($craigSynthItemPageDOM->find("table[summary='craigslist hosted images'] tbody tr") as $imageGroup){
                                                                      if(!empty($imageGroup)){
                                                                            $image = $imageGroup->find("img",0);
                                                                            if(!empty($image)){
                                                                                 $postImages[] = $image->src;
                                                                            }
                                                                     }
                                                                 }
                                                                 //print_r($postImages);
                                                                 $postImageStr = implode(",",$postImages);
                                                                 //echo $postImageStr;
                                                                 $craigSynthItemDesc = preg_replace("/(\r|\n|\r\n){2,}/","",$craigSynthItemDesc);
                                                                 $craigSynthItemDesc = preg_replace('/[^(\x20-\x7F)]*/','', $craigSynthItemDesc); //Remove non-ASCII characters
                                                                 echo $craigSynthItemDesc;
                                                                 if(!empty($postImageStr)){
                                                                      $foundItems[$itemFoundCounter]['post_item_images'] = $postImageStr;
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_images'] = "";
                                                                 }
                                                                 if(!empty($craigSynthItemDesc)){
                                                                      $foundItems[$itemFoundCounter]['post_item_description'] = $craigSynthItemDesc;
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_description'] = "";
                                                                 }
                                                            }
                                                            $itemFoundCounter++;
                                                      }else{
                                                            //Do something if the item wasn't added
                                                      }
                                                 }else{
                                                      //Do something if the link is empty
                                                 }
                                            }
                                      }
                                 }else{
                                      break;
                                 }
                                 $itemCounter++;      
                            }
                     }
                }else{
                     break;
                }
                $cityCounter++;
          }
     }else{
          echo "There were no results found for ".$state.".";
     }
     
     return $foundItems;
}

//Returns the month as a number
function getMonthNum($monthString){
     $months = array('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec');
     for($i=0;$i<count($months);$i++){
          if($months[$i] == strtolower($monthString)){
                return $i;
          }     
     }
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';

//scraperwiki::attach('itemfilter_utils');
$state = "Oregon,Washington"; //Must be Titlecase e.g, Alabama, Michigan. or use an array separated by commas Alabama, Washington
$states = explode(",",$state);
print_r($states);

//$jsonManufacturerScraper = scraperwiki::get_var('manufacturer_scraper');
//Get a unique list of item manufacturers
//$jsonSearchData = file_get_contents($jsonManufacturerScraper);
//echo $jsonSearchData;
$jsonSearchData = '[
                    {"manufacturer":"Apogee","name":"Duet"},
                    {"manufacturer":"Apogee","name":"Ensemble"},
                    {"manufacturer":"Mackie","name":"Onyx 1640i"},
                    {"manufacturer":"Mackie","name":"Audio Interface"},
                    {"manufacturer":"Metric","name":"Halo"},
                    {"manufacturer":"M-Audio","name":"MidiSport"},
                    {"manufacturer":"Motu","name":"Ultralite Mk3"},
                    {"manufacturer":"Motu","name":"Ultralite MKIII"},
                    {"manufacturer":"Motu","name":"Ultralite MK111"},
                    {"manufacturer":"Motu","name":"Ultralite MKIII"},
                    {"manufacturer":"Motu","name":"8 pre"},
                    {"manufacturer":"Motu","name":"828 mk3"},
                    {"manufacturer":"Motu","name":"896 mk3"},
                    {"manufacturer":"Motu","name":"2408 mk3"},
                    {"manufacturer":"Motu","name":"24IO"},
                    {"manufacturer":"Motu","name":"Firewire Audio Interface"},
                    {"manufacturer":"Native Instruments","name":"audio interface"},
                    {"manufacturer":"Native Instruments","name":"Audio 6"},
                    {"manufacturer":"Native Instruments","name":"Audio 8"},
                    {"manufacturer":"Native Instruments","name":"Audio 10"},
                    {"manufacturer":"Native Instruments","name":"Audio 2"},
                    {"manufacturer":"Traktor","name":"audio interface"},
                    {"manufacturer":"Traktor","name":"Audio 6"},
                    {"manufacturer":"Traktor","name":"Audio 8"},
                    {"manufacturer":"Traktor","name":"Audio 10"},
                    {"manufacturer":"Traktor","name":"Audio 2"},
                    {"manufacturer":"PreSonus","name":"FireStudio"},
                    {"manufacturer":"RME","name":"Fireface 400"},
                    {"manufacturer":"Tascam","name":"FW 1884"}
                ]';

$wordsToIgnore = "keyboard,horn,polk audio,shure,Audio Rack,Starter Set,Starter Audio,Pro Starter,Stereo Compressor,Kerzweil,subwoofer,digital piano,controller,compressor";
$ignoreWords = explode(',',$wordsToIgnore);
echo "Total ignored words: ".count($ignoreWords)."\n";

$cityDepth = 0; //Set to 0 to search all cities found in the database  
$manufacturerDepth = 0; //Set to 0 to search all item manufacturers found in the database
$depthOverride = true; //Cancels the depth variables

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}


if(!empty($jsonSearchData)){
    $manufacturerCounter = 0;
    $jsonManufacturers = json_decode($jsonSearchData);
    //echo "<pre>";
    //print_r($jsonManufacturers);
    //echo "</pre>";
    foreach($states as $state){
        $state = trim($state);
        echo "Searching state: ".$state."\n";
        $state = urlencode($state);
        if(empty($foundItems)){
            $foundItems = findOnCraigslist($state,$jsonManufacturers,$ignoreWords,$cityDepth,$depthOverride);
        }else{
            $foundItems = array_merge($foundItems,findOnCraigslist($state,$jsonManufacturers,$ignoreWords,$cityDepth,$depthOverride));
        }
    }
    if(!empty($foundItems)){
        $saveMessage = scraperWiki::save_sqlite(array('manufacturer','name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link'), $foundItems);
        print strval($saveMessage); 
    }else{
        //Delete existing data
        $info = scraperwiki::table_info($name="swdata");
        if(!empty($info)){
            scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
        }
    }
}



/**
* Parses craigslist and returns items
* @param String state
* @param String itemManufacturer
* @param ignoreWords
* @param cityDepth
* @param depthOverride
* @return Array foundItems
*/
function findOnCraigslist($state = "Oregon",$jsonManufacturers = null,$ignoreWords=array(),$cityDepth=null,$depthOverride=true){
     $cityCounter = 0;
     $itemFoundCounter = 0;
     $foundItems = array();
     //Use the Scraper Web API and pull the results in JSON format
     $jsonData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=craigslist_cities_1&query=select%20*%20from%20%60swdata%60%20WHERE%20state%20%3D%20'".$state."'");
     $jsonCraigCities = json_decode($jsonData);
     //$jsonItemManufacturerData = file_get_contents($manufacturerScraperURL."%20WHERE%20manufacturer%20%3D%20'".$itemManufacturer."'");
     //$jsonItemsFromManufacturer = json_decode($jsonItemManufacturerData);
     //echo "There are ".count($jsonItemsFromManufacturer)." ".$itemManufacturer." items in the system.\n";
     $foundURLS = array();    
     if(!empty($jsonData)){
          foreach($jsonCraigCities as $city){
                $itemCounter = 0;
                echo "-> Parsing link: ".$city->link."\n";
                //Search each city for each item for a certain item manufacturer in the vintage item database.
                if($cityCounter < $cityDepth || $depthOverride == true || $cityDepth == 0){
                     foreach($jsonManufacturers as $item){
                          //Example musical instrument search string http://portland.craigslist.org/search/msg?query=korg+microkorg&srchType=A&minAsk=5&maxAsk=&hasPic=1     
                          if(!empty($item)){
                                $itemName = urlencode(trim($item->name));
                                if(!empty($itemName)){         
                                      $tManName = preg_replace("/\s/","_",$item->manufacturer);//Build a temp name for the array key
                                      $itemManufacturer = urlencode($item->manufacturer);
                                      $search_string = '"'.strtolower($itemManufacturer)."+".$itemName.'"';
                                      //$search_string = urlencode($search_string);
                                      $search_string2 = urlencode($itemName);
                                      //"%7C" = | (This establishes Craiglist's OR search.)
                                      if(!empty($search_string) && !empty($search_string2)){
                                            $search_url = $city->link."/search/msg?query=".$search_string."+%7C+".$search_string2."&srchType=T&minAsk=5&maxAsk=&hasPic=1";//Title only and has image
                                            echo "--> Scraping: ".$search_url."\n";
                                            $html = scraperWiki::scrape($search_url); 
                                            $dom = new simple_html_dom();
                                            $dom->load($html); //Load the HTML 
                                            foreach($dom->find("p.row") as $item){
                                                 $itemLink = $item->find('a',0); //Find the second link (not the image link)
                                                 if(!empty($itemLink->href)){
                                                      $itemName = $itemLink->innertext;
                                                      $itemName = preg_replace('/\s-/','',$itemName);
                                                      $itemName = trim($itemName);
                                                      //Check the name against the ignore words
                                                      $addItem = 1;
                                                      foreach($ignoreWords as $word){
                                                            //Make sure that the itemName doesn't include a word to ignore
                                                            if(strpos(strtolower($itemName),strtolower($word))===false){
                                                                 //Do something
                                                            }else{
                                                                 $addItem = 0;
                                                            }
                                                      }
                                                      //Check to make sure that the item link matches the search city link. 
                                                      $searchCity = preg_match("@http://([a-z]*+)\.@",$city->link,$cityMatches);
                                                      $searchCity = trim($cityMatches[1]);
                                                      $itemCity = preg_match("@http://([a-z]*+)\.@",$itemLink->href,$itemCityMatches);
                                                      $itemCity = trim($itemCityMatches[1]);
                                                      //echo "Search city: ".$searchCity."\n";
                                                      //echo "Item city: ".$itemCity."\n";
                                                      if($itemCity != $searchCity){
                                                            $addItem = 0;
                                                      }
                                                      if($addItem == 1 && in_array($itemLink->href,$foundURLS) == 0){
                                                            echo $itemName."\n";
                                                            $itemInfo = $item->plaintext;
                                                            $itemInfo = explode('$',$itemInfo);
                                                            $itemPrice = "$".trim($itemInfo[1]);
                                                            $itemInfo = $itemInfo[0];
                                                            $itemInfo = explode('-',$itemInfo);
                                                            $itemInfo = preg_replace('/&nbsp;/','',$itemInfo);
                                                            $foundItems[$itemFoundCounter]['manufacturer'] = $itemManufacturer;
                                                            $foundItems[$itemFoundCounter]['name'] = $itemName;
                                                            $foundItems[$itemFoundCounter]['post_item_name'] = $itemName;
                                                            //Find the date and price
                                                            if(!empty($itemInfo)){
                                                                 if(isset($itemInfo[0])){
                                                                      $itemDate = trim($itemInfo[0]);
                                                                      $itemDate = preg_replace('/\s\s+/',' ',$itemDate); //Strip excess whitespace
                                                                      //Change date string
                                                                      $itemDateArray = explode(" ",$itemDate);
                                                                      $monthNumVal = getMonthNum($itemDateArray[0]); //ex Nov
                                                                      $curYear = date("Y");
                                                                      $itemDate = $curYear."-".$monthNumVal."-".$itemDateArray[1];
                                                                      echo "Date posted: ".$itemDate."\n";
                                                                      $foundItems[$itemFoundCounter]['post_item_date'] = $itemDate;
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_date'] = "";
                                                                 }
                                                                 if(isset($itemPrice)){
                                                                      $itemPrice = trim($itemPrice);
                                                                      $itemPrice = preg_replace('/\(.*\)/','',$itemPrice);
                                                                      $itemPrice = preg_replace('/[a-z]+|[A-Z]+/','',$itemPrice);
                                                                      $itemPrice = trim($itemPrice);
                                                                      echo "Price: ".$itemPrice."\n";
                                                                      //Only add the price if a dollar sign exists
                                                                      if($itemPrice[0] == "$"){
                                                                            $foundItems[$itemFoundCounter]['post_item_price'] = $itemPrice;
                                                                      }else{
                                                                            $foundItems[$itemFoundCounter]['post_item_price'] = "$".$itemPrice;
                                                                      }
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_price'] = "";
                                                                 }
                                                            }else{
                                                                 $foundItems[$itemFoundCounter]['post_item_date'] = "";
                                                                 $foundItems[$itemFoundCounter]['post_item_price'] = "";
                                                            }
                                                            $foundURLS[] = $itemLink->href; //Add the url to keep track and make sure that only unique URLs are added.
                                                            $foundItems[$itemFoundCounter]['post_item_link'] = $city->link;
                                                            $foundItems[$itemFoundCounter]['post_item_state'] = $city->state;
                                                            $foundItems[$itemFoundCounter]['query'] = $search_string."+%7C+".$search_string2;
                                                            $foundItems[$itemFoundCounter]['link'] = $itemLink->href;
                                                            //Find the page details on the page
                                                            $craigSynthItemPage = scraperWiki::scrape($itemLink->href); 
                                                            $craigSynthItemPageDOM = new simple_html_dom();
                                                            $craigSynthItemPageDOM->load($craigSynthItemPage); //Load the HTML
                                                            if(!empty($craigSynthItemPageDOM)){
                                                                 $craigSynthItemDesc = $craigSynthItemPageDOM->find("div#userbody",0);
                                                                 //print_r($craigSynthItemDesc);
                                                                 if(!empty($craigSynthItemDesc)) $craigSynthItemDesc = $craigSynthItemDesc->plaintext;
                                                                 $craigSynthItemBlurb = $craigSynthItemPageDOM->find("div#userbody] ul.blurbs",0);
                                                                 if(!empty($craigSynthItemBlurb)) $craigSynthItemBlurb = $craigSynthItemBlurb->plaintext;
                                                                 $craigSynthItemDesc = str_replace($craigSynthItemBlurb,"",$craigSynthItemDesc);
                                                                 $postImages = array();
                                                                 foreach($craigSynthItemPageDOM->find("table[summary='craigslist hosted images'] tbody tr") as $imageGroup){
                                                                      if(!empty($imageGroup)){
                                                                            $image = $imageGroup->find("img",0);
                                                                            if(!empty($image)){
                                                                                 $postImages[] = $image->src;
                                                                            }
                                                                     }
                                                                 }
                                                                 //print_r($postImages);
                                                                 $postImageStr = implode(",",$postImages);
                                                                 //echo $postImageStr;
                                                                 $craigSynthItemDesc = preg_replace("/(\r|\n|\r\n){2,}/","",$craigSynthItemDesc);
                                                                 $craigSynthItemDesc = preg_replace('/[^(\x20-\x7F)]*/','', $craigSynthItemDesc); //Remove non-ASCII characters
                                                                 echo $craigSynthItemDesc;
                                                                 if(!empty($postImageStr)){
                                                                      $foundItems[$itemFoundCounter]['post_item_images'] = $postImageStr;
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_images'] = "";
                                                                 }
                                                                 if(!empty($craigSynthItemDesc)){
                                                                      $foundItems[$itemFoundCounter]['post_item_description'] = $craigSynthItemDesc;
                                                                 }else{
                                                                      $foundItems[$itemFoundCounter]['post_item_description'] = "";
                                                                 }
                                                            }
                                                            $itemFoundCounter++;
                                                      }else{
                                                            //Do something if the item wasn't added
                                                      }
                                                 }else{
                                                      //Do something if the link is empty
                                                 }
                                            }
                                      }
                                 }else{
                                      break;
                                 }
                                 $itemCounter++;      
                            }
                     }
                }else{
                     break;
                }
                $cityCounter++;
          }
     }else{
          echo "There were no results found for ".$state.".";
     }
     
     return $foundItems;
}

//Returns the month as a number
function getMonthNum($monthString){
     $months = array('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec');
     for($i=0;$i<count($months);$i++){
          if($months[$i] == strtolower($monthString)){
                return $i;
          }     
     }
}
?>
