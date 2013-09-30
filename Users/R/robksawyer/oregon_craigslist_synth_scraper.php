<?php

require 'scraperwiki/simple_html_dom.php';

//scraperwiki::attach("craigslist_cities"); //Attach the craigslist city scraper
//print_r(scraperwiki::select("* from craigslist_cities.swdata WHERE state = 'Alabama'"));

$state = "Oregon"; //Must be Titlecase e.g, Alabama, Michigan. or use an array separated by commas Alabama, Washington
$states = explode(",",$state);
print_r($states);
$ignoreWords = array('guitar','guitars','Guitar','Guitars','amp','Amp','pedal','bass cab','SPEAKERS',);
$cityDepth = 10; 
$synthDepth = 2;
$manufacturerQuery = ''; //You can choose to search only a specific manufacturer or if not, just leave it blank
$manufacturerDepth = 0;
$depthOverride = false; //Cancels the depth variables

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

//$synthManufacturer = 'Access Music'; //Must be Titlecase e.g, Korg, Yamaha

//Get a unique list of synth manufacturers
$jsonManufacturerData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synths&query=select%20DISTINCT%20manufacturer%20from%20%60vintagesynth-scrape-11-15-2011%60");
if(!empty($jsonManufacturerData)){
    $manufacturerCounter = 0;
    $jsonManufacturers = json_decode($jsonManufacturerData);
    foreach($states as $state){
        $state = trim($state);
        echo "Searching state: ".$state."\n";
        $state = urlencode($state);
        if(empty($manufacturerQuery)){
            foreach($jsonManufacturers as $synthManufacturer){
                if($manufacturerCounter < $manufacturerDepth || $manufacturerDepth == 0){
                    $tManName = preg_replace("/\s/","_",$synthManufacturer->manufacturer);//Build a temp name for the array key
                    $synthManufacturer = urlencode($synthManufacturer->manufacturer);
                    echo "Searching manufacturer: ". $synthManufacturer."\n"; 
                    $foundSynths[$state][$tManName] = findSynthsOnCraigslist($state,$synthManufacturer,$ignoreWords,$cityDepth,$synthDepth,$depthOverride);
                    if(!empty($foundSynths[$state][$tManName])){
                        //scraperwiki::save_var($state.'-'.$synthManufacturer.'-'.'synths', json_encode($foundSynths[$state][$synthManufacturer])); 
                        $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link'), $foundSynths[$state][$tManName]);
                        print strval($saveMessage); 
                    }
                    $manufacturerCounter++;
                }else{
                    break;
                }
            }
        }else{
            $synthManufacturer = $manufacturerQuery;
            //Search for a specific manufacturer
            $tManName = preg_replace("/\s/","_",$synthManufacturer);//Build a temp name for the array key
            $synthManufacturer = urlencode($synthManufacturer);
            echo "Searching manufacturer: ". $synthManufacturer."\n"; 
            $foundSynths[$state][$tManName] = findSynthsOnCraigslist($state,$synthManufacturer,$ignoreWords,$cityDepth,$synthDepth,$depthOverride);
            if(!empty($foundSynths[$state][$tManName])){
                //scraperwiki::save_var($state.'-'.$synthManufacturer.'-'.'synths', json_encode($foundSynths[$state][$synthManufacturer])); 
                $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link','post_item_description','post_item_images'), $foundSynths[$state][$tManName]);
                print strval($saveMessage); 
            }
        }
    }
}

//print_r($foundSynths);
/*if(!empty($foundSynths)){
    //$dbName = "craigslist-synth-scrape-".$state."-".$synthManufacturer."-".$today = date("m-d-Y");
    //$dbName = "craigslist-synth-scrape-".$state."-".$synthManufacturer;
    $saveSynthArray = array();
    $counter = 0;
    foreach($foundSynths[$state] as $sythSet){
        if(!empty($sythSet)){
            $saveSynthArray = array_merge($saveSynthArray, $sythSet);
        }
    }
    //print_r($saveSynthArray);
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link'), $saveSynthArray);
    print strval($saveMessage);
    
    scraperwiki::save_var('total_results', count($saveSynthArray));          
    print scraperWiki::get_var('total_results');
}*/


/**
* Parses craigslist and returns synths
* @param String state
* @param String synthManufacturer
* @param ignoreWords
* @param cityDepth
* @param synthDepth
* @param depthOverride
* @return Array foundSynths
*/
function findSynthsOnCraigslist($state = "Oregon",$synthManufacturer = null,$ignoreWords=array(),$cityDepth=null,$synthDepth=null,$depthOverride=true){
    $cityCounter = 0;
    $synthsFoundCounter = 0;
    $foundSynths = array();
    //Use the Scraper Web API and pull the results in JSON format
    $jsonData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=craigslist_cities_1&query=select%20*%20from%20%60swdata%60%20WHERE%20state%20%3D%20'".$state."'");
    $jsonCraigCities = json_decode($jsonData);
    $jsonSynthManufacturerData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synths&query=select%20name%20from%20%60vintagesynth-scrape-11-15-2011%60%20WHERE%20manufacturer%20%3D%20'".$synthManufacturer."'");
    $jsonSynthsFromManufacturer = json_decode($jsonSynthManufacturerData);
    if(!empty($jsonData)){
        foreach($jsonCraigCities as $city){
            $synthCounter = 0;
            echo "-> Parsing link: ".$city->link."\n";
            //Search each city for each synth for a certain synth manufacturer in the vintage synth database.
            if($cityCounter < $cityDepth || $depthOverride == true){
                foreach($jsonSynthsFromManufacturer as $synth){
                    //Example musical instrument search string http://portland.craigslist.org/search/msg?query=korg+microkorg&srchType=A&minAsk=5&maxAsk=&hasPic=1    
                    if(!empty($synth)){
                        $synthName = urlencode(trim($synth->name));
                        if(!empty($synthName)){
                            if($synthCounter < $synthDepth || $depthOverride == true){     
                                $search_string = '"'.strtolower($synthManufacturer)."+".$synthName.'"';
                                //$search_string = urlencode($search_string);
                                $search_string2 = urlencode($synthName);
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
                                                if(strpos($itemName,$word)===false){
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
                                            if($addItem == 1){
                                                echo $itemName."\n";
                                                $itemInfo = $item->plaintext;
                                                $itemInfo = explode('$',$itemInfo);
                                                $itemPrice = "$".trim($itemInfo[1]);
                                                $itemInfo = $itemInfo[0];
                                                $itemInfo = explode('-',$itemInfo);
                                                $itemInfo = preg_replace('/&nbsp;/','',$itemInfo);
                                                $foundSynths[$synthsFoundCounter]['manufacturer'] = $synthManufacturer;
                                                $foundSynths[$synthsFoundCounter]['synth_name'] = $synthName;
                                                $foundSynths[$synthsFoundCounter]['post_item_name'] = $itemName;
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
                                                        $foundSynths[$synthsFoundCounter]['post_item_date'] = $itemDate;
                                                    }else{
                                                        $foundSynths[$synthsFoundCounter]['post_item_date'] = "";
                                                    }
                                                    if(isset($itemPrice)){
                                                        $itemPrice = trim($itemPrice);
                                                        $itemPrice = preg_replace('/\(.*\)/','',$itemPrice);
                                                        $itemPrice = preg_replace('/[a-z]+|[A-Z]+/','',$itemPrice);
                                                        $itemPrice = trim($itemPrice);
                                                        echo "Price: ".$itemPrice."\n";
                                                        //Only add the price if a dollar sign exists
                                                        if($itemPrice[0] == "$"){
                                                            $foundSynths[$synthsFoundCounter]['post_item_price'] = $itemPrice;
                                                        }else{
                                                            $foundSynths[$synthsFoundCounter]['post_item_price'] = "$".$itemPrice;
                                                        }
                                                    }else{
                                                        $foundSynths[$synthsFoundCounter]['post_item_price'] = "";
                                                    }
                                                }else{
                                                    $foundSynths[$synthsFoundCounter]['post_item_date'] = "";
                                                    $foundSynths[$synthsFoundCounter]['post_item_price'] = "";
                                                }
                                                $foundSynths[$synthsFoundCounter]['post_item_link'] = $city->link;
                                                $foundSynths[$synthsFoundCounter]['post_item_state'] = $city->state;
                                                $foundSynths[$synthsFoundCounter]['query'] = $search_string."+%7C+".$search_string2;
                                                $foundSynths[$synthsFoundCounter]['link'] = $itemLink->href;
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
                                                    echo $craigSynthItemDesc;
                                                    $foundSynths[$synthsFoundCounter]['post_item_images'] = $postImageStr;
                                                    $foundSynths[$synthsFoundCounter]['post_item_description'] = $craigSynthItemDesc;
                                                }
                                                $synthsFoundCounter++;
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
                            $synthCounter++;   
                        }
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
    
    return $foundSynths;
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

//scraperwiki::attach("craigslist_cities"); //Attach the craigslist city scraper
//print_r(scraperwiki::select("* from craigslist_cities.swdata WHERE state = 'Alabama'"));

$state = "Oregon"; //Must be Titlecase e.g, Alabama, Michigan. or use an array separated by commas Alabama, Washington
$states = explode(",",$state);
print_r($states);
$ignoreWords = array('guitar','guitars','Guitar','Guitars','amp','Amp','pedal','bass cab','SPEAKERS',);
$cityDepth = 10; 
$synthDepth = 2;
$manufacturerQuery = ''; //You can choose to search only a specific manufacturer or if not, just leave it blank
$manufacturerDepth = 0;
$depthOverride = false; //Cancels the depth variables

//Delete existing data
$info = scraperwiki::table_info($name="swdata");
if(!empty($info)){
    scraperwiki::sqliteexecute("DELETE FROM swdata"); //Truncate the table before adding new results
}

//$synthManufacturer = 'Access Music'; //Must be Titlecase e.g, Korg, Yamaha

//Get a unique list of synth manufacturers
$jsonManufacturerData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synths&query=select%20DISTINCT%20manufacturer%20from%20%60vintagesynth-scrape-11-15-2011%60");
if(!empty($jsonManufacturerData)){
    $manufacturerCounter = 0;
    $jsonManufacturers = json_decode($jsonManufacturerData);
    foreach($states as $state){
        $state = trim($state);
        echo "Searching state: ".$state."\n";
        $state = urlencode($state);
        if(empty($manufacturerQuery)){
            foreach($jsonManufacturers as $synthManufacturer){
                if($manufacturerCounter < $manufacturerDepth || $manufacturerDepth == 0){
                    $tManName = preg_replace("/\s/","_",$synthManufacturer->manufacturer);//Build a temp name for the array key
                    $synthManufacturer = urlencode($synthManufacturer->manufacturer);
                    echo "Searching manufacturer: ". $synthManufacturer."\n"; 
                    $foundSynths[$state][$tManName] = findSynthsOnCraigslist($state,$synthManufacturer,$ignoreWords,$cityDepth,$synthDepth,$depthOverride);
                    if(!empty($foundSynths[$state][$tManName])){
                        //scraperwiki::save_var($state.'-'.$synthManufacturer.'-'.'synths', json_encode($foundSynths[$state][$synthManufacturer])); 
                        $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link'), $foundSynths[$state][$tManName]);
                        print strval($saveMessage); 
                    }
                    $manufacturerCounter++;
                }else{
                    break;
                }
            }
        }else{
            $synthManufacturer = $manufacturerQuery;
            //Search for a specific manufacturer
            $tManName = preg_replace("/\s/","_",$synthManufacturer);//Build a temp name for the array key
            $synthManufacturer = urlencode($synthManufacturer);
            echo "Searching manufacturer: ". $synthManufacturer."\n"; 
            $foundSynths[$state][$tManName] = findSynthsOnCraigslist($state,$synthManufacturer,$ignoreWords,$cityDepth,$synthDepth,$depthOverride);
            if(!empty($foundSynths[$state][$tManName])){
                //scraperwiki::save_var($state.'-'.$synthManufacturer.'-'.'synths', json_encode($foundSynths[$state][$synthManufacturer])); 
                $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link','post_item_description','post_item_images'), $foundSynths[$state][$tManName]);
                print strval($saveMessage); 
            }
        }
    }
}

//print_r($foundSynths);
/*if(!empty($foundSynths)){
    //$dbName = "craigslist-synth-scrape-".$state."-".$synthManufacturer."-".$today = date("m-d-Y");
    //$dbName = "craigslist-synth-scrape-".$state."-".$synthManufacturer;
    $saveSynthArray = array();
    $counter = 0;
    foreach($foundSynths[$state] as $sythSet){
        if(!empty($sythSet)){
            $saveSynthArray = array_merge($saveSynthArray, $sythSet);
        }
    }
    //print_r($saveSynthArray);
    $saveMessage = scraperWiki::save_sqlite(array('manufacturer','synth_name','post_item_date','post_item_name','post_item_price','post_item_link','post_item_state','query','link'), $saveSynthArray);
    print strval($saveMessage);
    
    scraperwiki::save_var('total_results', count($saveSynthArray));          
    print scraperWiki::get_var('total_results');
}*/


/**
* Parses craigslist and returns synths
* @param String state
* @param String synthManufacturer
* @param ignoreWords
* @param cityDepth
* @param synthDepth
* @param depthOverride
* @return Array foundSynths
*/
function findSynthsOnCraigslist($state = "Oregon",$synthManufacturer = null,$ignoreWords=array(),$cityDepth=null,$synthDepth=null,$depthOverride=true){
    $cityCounter = 0;
    $synthsFoundCounter = 0;
    $foundSynths = array();
    //Use the Scraper Web API and pull the results in JSON format
    $jsonData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=craigslist_cities_1&query=select%20*%20from%20%60swdata%60%20WHERE%20state%20%3D%20'".$state."'");
    $jsonCraigCities = json_decode($jsonData);
    $jsonSynthManufacturerData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=synths&query=select%20name%20from%20%60vintagesynth-scrape-11-15-2011%60%20WHERE%20manufacturer%20%3D%20'".$synthManufacturer."'");
    $jsonSynthsFromManufacturer = json_decode($jsonSynthManufacturerData);
    if(!empty($jsonData)){
        foreach($jsonCraigCities as $city){
            $synthCounter = 0;
            echo "-> Parsing link: ".$city->link."\n";
            //Search each city for each synth for a certain synth manufacturer in the vintage synth database.
            if($cityCounter < $cityDepth || $depthOverride == true){
                foreach($jsonSynthsFromManufacturer as $synth){
                    //Example musical instrument search string http://portland.craigslist.org/search/msg?query=korg+microkorg&srchType=A&minAsk=5&maxAsk=&hasPic=1    
                    if(!empty($synth)){
                        $synthName = urlencode(trim($synth->name));
                        if(!empty($synthName)){
                            if($synthCounter < $synthDepth || $depthOverride == true){     
                                $search_string = '"'.strtolower($synthManufacturer)."+".$synthName.'"';
                                //$search_string = urlencode($search_string);
                                $search_string2 = urlencode($synthName);
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
                                                if(strpos($itemName,$word)===false){
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
                                            if($addItem == 1){
                                                echo $itemName."\n";
                                                $itemInfo = $item->plaintext;
                                                $itemInfo = explode('$',$itemInfo);
                                                $itemPrice = "$".trim($itemInfo[1]);
                                                $itemInfo = $itemInfo[0];
                                                $itemInfo = explode('-',$itemInfo);
                                                $itemInfo = preg_replace('/&nbsp;/','',$itemInfo);
                                                $foundSynths[$synthsFoundCounter]['manufacturer'] = $synthManufacturer;
                                                $foundSynths[$synthsFoundCounter]['synth_name'] = $synthName;
                                                $foundSynths[$synthsFoundCounter]['post_item_name'] = $itemName;
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
                                                        $foundSynths[$synthsFoundCounter]['post_item_date'] = $itemDate;
                                                    }else{
                                                        $foundSynths[$synthsFoundCounter]['post_item_date'] = "";
                                                    }
                                                    if(isset($itemPrice)){
                                                        $itemPrice = trim($itemPrice);
                                                        $itemPrice = preg_replace('/\(.*\)/','',$itemPrice);
                                                        $itemPrice = preg_replace('/[a-z]+|[A-Z]+/','',$itemPrice);
                                                        $itemPrice = trim($itemPrice);
                                                        echo "Price: ".$itemPrice."\n";
                                                        //Only add the price if a dollar sign exists
                                                        if($itemPrice[0] == "$"){
                                                            $foundSynths[$synthsFoundCounter]['post_item_price'] = $itemPrice;
                                                        }else{
                                                            $foundSynths[$synthsFoundCounter]['post_item_price'] = "$".$itemPrice;
                                                        }
                                                    }else{
                                                        $foundSynths[$synthsFoundCounter]['post_item_price'] = "";
                                                    }
                                                }else{
                                                    $foundSynths[$synthsFoundCounter]['post_item_date'] = "";
                                                    $foundSynths[$synthsFoundCounter]['post_item_price'] = "";
                                                }
                                                $foundSynths[$synthsFoundCounter]['post_item_link'] = $city->link;
                                                $foundSynths[$synthsFoundCounter]['post_item_state'] = $city->state;
                                                $foundSynths[$synthsFoundCounter]['query'] = $search_string."+%7C+".$search_string2;
                                                $foundSynths[$synthsFoundCounter]['link'] = $itemLink->href;
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
                                                    echo $craigSynthItemDesc;
                                                    $foundSynths[$synthsFoundCounter]['post_item_images'] = $postImageStr;
                                                    $foundSynths[$synthsFoundCounter]['post_item_description'] = $craigSynthItemDesc;
                                                }
                                                $synthsFoundCounter++;
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
                            $synthCounter++;   
                        }
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
    
    return $foundSynths;
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
