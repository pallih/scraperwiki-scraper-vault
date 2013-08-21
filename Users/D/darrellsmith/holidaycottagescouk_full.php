<?php

scraperwiki::save_var('dummy', 0);


function strrpos_string($haystack, $needle, $offset = 0) 
{ 
    if(trim($haystack) != "" && trim($needle) != "" && $offset <= strlen($haystack)) 
    { 
        $last_pos = $offset; 
        $found = false; 
        while(($curr_pos = strpos($haystack, $needle, $last_pos)) !== false) 
        { 
            $found = true; 
            $last_pos = $curr_pos + 1; 
        } 
        if($found) 
        { 
            return $last_pos - 1; 
        } 
        else 
        { 
            return false; 
        } 
    } 
    else 
    { 
        return false; 
    } 
} 



 function clean_text($txt){
    $txt= str_replace("\n"," ",$txt);
    $txt= str_replace("\r"," ",$txt);
    $txt= str_replace("&nbsp;"," ",$txt);
    $txt= str_replace("\t"," ",$txt);
    $txt= str_replace("&eacute","e",$txt);
    $txt= str_replace("&frac12;"," and a half",$txt);
    $txt= str_replace("&frac14;"," and a quarter",$txt);
    $txt= str_replace("&amp;","&",$txt);
    $txt= str_replace("&pound;","£",$txt);
    $txt= str_replace("&#8220;","'",$txt);
    $txt= str_replace("&#8221;","'",$txt);
    $txt= str_replace("&#8217;","'",$txt);
    $txt= str_replace("&#8216;","'",$txt);
    $txt= str_replace("&#145;","'",$txt);
    $txt= str_replace("&#146;","'",$txt);
    $txt= str_replace("</li>","",$txt);
    $txt= str_replace("&#233;","e",$txt);
    $txt= str_replace("&#8211;","-",$txt);
    $txt= str_replace("&#189;","1/2",$txt);
    $txt= str_replace(",,",",",$txt);
    $txt= str_replace("&lsquo;",'"',$txt);
    $txt= str_replace("&rsquo;",'"',$txt);
    $txt= str_replace("</p>","",$txt);
    $txt= str_replace("</div>","",$txt);
    $txt= str_replace("&#163;","£",$txt);
    $txt= str_replace("&#039;","£",$txt);

    $txt= preg_replace('/\s+/', ' ',$txt);

    return $txt;
 }

function searchForId($id, $array) {
   foreach ($array as $key => $val) {
     if ($val['COTTAGE_URL'] === $id) {
       return $key;
     }
   }
   return null;
 }

# Check for pages with no usable data
function fourOhFour($html){
    if(strpos($html,'Home not available',1200)!==false){
        return true;
    }
    return false;
}
 $blacklist = array();

 # get an array of the cottage data to scrape
 scraperwiki::attach("holidaycottagescouk_summary") ;
 $cottData = scraperwiki::select("COTTAGE_URL  from 'holidaycottagescouk_summary'.SWDATA order by COTTAGE_URL");

 $placeholder = scraperwiki::get_var("cottURL");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 $apidom = new simple_html_dom();
 foreach($cottData as $value){

  $highPrice = "";
  $lowPrice = "";
  $found = 0;
  $count = 0;



  scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);


  // check the cottage url against the blacklist
  foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }

  // image




  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url   = $value['COTTAGE_URL'];

 // Details
 $details ="";
 foreach($dom->find('div[class=leftColRightPanel]')as $sec){

  foreach($sec->find('ul[class=glanceList]')as $ele){
    $details .= $ele->plaintext;
   }
 
   $areaDescArr = explode(":",$details);
   $sleeps= str_replace("Bedrooms","",$areaDescArr[1]);
   $bedrooms = str_replace("bathrooms","",$areaDescArr[2]);
   $bedrooms = str_replace("Bathrooms","",$bedrooms);
 
   $bathrooms = substr($areaDescArr[3],0,strpos($areaDescArr[3],"Dogs")); 
   $pets = 0;
   if(strpos($areaDescArr[4],"Yes"))
     $pets = 1;
   $changeoverDay = str_replace("Price band","",$areaDescArr[5]);

   foreach($sec->find('ul[class=glanceList]')as $ele){
    $details .= $ele->plaintext;
   }
       
   $lastEleArr = explode(" ",end($areaDescArr));
   foreach($lastEleArr as $item)
     if(strlen($item)>1 )
       $cottID = $item;

   $features = "";
   foreach($sec->find('ul[class=featList]')as $ele){
     foreach($ele->find('li')as $ele){
       $features .= $ele->plaintext.",";
     }
   }
 }

 //Description
 $description ="";
 foreach($dom->find('div[class=leftColLeftPanel divideInner]')as $data){
   foreach($data->find('p')as $desc){
    $description .= " ".$desc->plaintext;
   }
 }

 // long lat 

 foreach($dom->find('h2[id=ctl00_ContentPlaceHolder1_marketingAddress]')as $ele){
    $placeName = $ele->plaintext;
    if(strpos($placeName,"(") ){
      $offset_first =  strpos($placeName,"(");
      $offset_second =  strpos($placeName,")");
      $firstPart = substr($placeName,0,$offset_first);
      $secondPart = substr($placeName,$offset_second+1);
      $location = $firstPart.$secondPart.", UK";
    }else
      $location =$placeName.", UK";
 }


$cottage_name_offest  =  strpos($placeName,"(");
$cottage_name = substr($placeName,0,$cottage_name_offest);
$cottage_name = $cottage_name ." Cottage";

$location = str_replace(" ","+",$location);

 # get the geocoding of the location
 $apiCall = "http://maps.googleapis.com/maps/api/geocode/xml?address=".$location."&sensor=false";
print_r($apiCall );

 $apihtml = scraperWiki::scrape($apiCall);
 $apidom->load($apihtml);
 $lat = "";
 $lng = "";   
 foreach($apidom->find('location') as $ele){
     foreach($ele->find('lat') as $lats){
        $lat = $lats->plaintext;
     }
     foreach($ele->find('lng')as $lngs){ 
        $lng = $lngs->plaintext;
     }
 }
 
print_r($lat);
print_r($lng);

 $imgs = "";
 $imgURL = "";
 foreach($dom->find('div[id=slides]')as $data){
  foreach($data->find('a')as $ele){
    $imgs .= str_replace("../../","","http://www.holidaycottages.co.uk/".$ele->href.",");
    $imgsURL = str_replace("../../","","".$ele->href);
    $imgsURL = str_replace("../","","".$ele->href);
    $imgs .="http://www.holidaycottages.co.uk/".$imgURL.",";
  }
 }

 
// Prices
foreach($dom->find('div[class=leftColRightPanel]')as $sec){
  foreach($sec->find('ul[class=glanceList]')as $ele){
    $priceband = substr($ele->plaintext,strpos($ele->plaintext,"Price band:"));
    $priceband = str_replace("Price band: ","",$priceband);
    $priceband = substr($priceband,0,strpos($priceband," ")); 

switch(trim($priceband)){
 case "A":
    $priceHigh = 215;
    $priceLow = 355;
    break;
 case "B":
    $priceHigh = 230 ;
    $priceLow = 405;
    break;
 case "C":
    $priceHigh = 240;
    $priceLow = 455;
    break;
 case "D":
    $priceHigh = 250;
    $priceLow = 485;
    break;
 case "E":
    $priceHigh = 260;
    $priceLow = 505;
    break;
 case "F":
    $priceHigh = 260;
    $priceLow = 550;
    break;
 case "G":
    $priceHigh = 275;
    $priceLow = 585;
    break;
 case "H":
    $priceHigh = 275;
    $priceLow = 585;
    break;
 case "I":
    $priceHigh = 275;
    $priceLow = 625;
    break;
 case "J":
    $priceHigh = 275;
    $priceLow = 665;
    break;
 case "K":
    $priceHigh = 285;
    $priceLow = 690;
    break;
 case "L":
    $priceHigh = 340;
    $priceLow = 710;
    break;
 case "M":
    $priceHigh = 355;
    $priceLow = 735;
    break;
 case "N":
    $priceHigh = 375;
    $priceLow = 790;
    break;
  case "O":
    $priceHigh = 390;
    $priceLow = 810;
    break;
  case "P":
    $priceHigh = 410;
    $priceLow = 825;
    break;
  case "Q":
    $priceHigh = 430;
    $priceLow = 875;
    break;
  case "R":
    $priceHigh = 450;
    $priceLow = 945;
    break;
  case "S":
    $priceHigh = 470;
    $priceLow = 1005;
    break;
  case "T":
    $priceHigh = 495;
    $priceLow = 1045;
    break;
  case "U":
    $priceHigh = 525;
    $priceLow = 1135;
    break;
  case "V":
    $priceHigh = 555;
    $priceLow = 1225;
    break;
  case "W":
    $priceHigh = 610;
    $priceLow = 1325;
    break;
  case "X":
    $priceHigh = 680;
    $priceLow = 1475;
    break;
 case "Y":
    $priceHigh = 795;
    $priceLow = 1685;
    break;
 case "Z":
    $priceHigh = 860;
    $priceLow = 1965;
    break;
 default:
    $priceHigh = "N/A";
    $priceLow = "N/A";
    }


 /*  save the data  */

 $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => trim($changeoverDay),
      'COTTAGE_NAME'        => trim($cottage_name),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => $pets,
      'COTTAGE_REFERENCE'   => trim($cottID),
      'FEATURES'            => trim(clean_text($features)),  
      'DESCRIPTION'         => trim(clean_text($description)),
      'LOCATION_DESCRIPTON' => "N/A",
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($imgs),
      'Agent'               => "holidaycottages.co.uk",
      'area'                => $location,     
      'priceband'           => $priceband,          
   );

 # print_r($record);
   scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
  }
 }
}

?>


<?php

scraperwiki::save_var('dummy', 0);


function strrpos_string($haystack, $needle, $offset = 0) 
{ 
    if(trim($haystack) != "" && trim($needle) != "" && $offset <= strlen($haystack)) 
    { 
        $last_pos = $offset; 
        $found = false; 
        while(($curr_pos = strpos($haystack, $needle, $last_pos)) !== false) 
        { 
            $found = true; 
            $last_pos = $curr_pos + 1; 
        } 
        if($found) 
        { 
            return $last_pos - 1; 
        } 
        else 
        { 
            return false; 
        } 
    } 
    else 
    { 
        return false; 
    } 
} 



 function clean_text($txt){
    $txt= str_replace("\n"," ",$txt);
    $txt= str_replace("\r"," ",$txt);
    $txt= str_replace("&nbsp;"," ",$txt);
    $txt= str_replace("\t"," ",$txt);
    $txt= str_replace("&eacute","e",$txt);
    $txt= str_replace("&frac12;"," and a half",$txt);
    $txt= str_replace("&frac14;"," and a quarter",$txt);
    $txt= str_replace("&amp;","&",$txt);
    $txt= str_replace("&pound;","£",$txt);
    $txt= str_replace("&#8220;","'",$txt);
    $txt= str_replace("&#8221;","'",$txt);
    $txt= str_replace("&#8217;","'",$txt);
    $txt= str_replace("&#8216;","'",$txt);
    $txt= str_replace("&#145;","'",$txt);
    $txt= str_replace("&#146;","'",$txt);
    $txt= str_replace("</li>","",$txt);
    $txt= str_replace("&#233;","e",$txt);
    $txt= str_replace("&#8211;","-",$txt);
    $txt= str_replace("&#189;","1/2",$txt);
    $txt= str_replace(",,",",",$txt);
    $txt= str_replace("&lsquo;",'"',$txt);
    $txt= str_replace("&rsquo;",'"',$txt);
    $txt= str_replace("</p>","",$txt);
    $txt= str_replace("</div>","",$txt);
    $txt= str_replace("&#163;","£",$txt);
    $txt= str_replace("&#039;","£",$txt);

    $txt= preg_replace('/\s+/', ' ',$txt);

    return $txt;
 }

function searchForId($id, $array) {
   foreach ($array as $key => $val) {
     if ($val['COTTAGE_URL'] === $id) {
       return $key;
     }
   }
   return null;
 }

# Check for pages with no usable data
function fourOhFour($html){
    if(strpos($html,'Home not available',1200)!==false){
        return true;
    }
    return false;
}
 $blacklist = array();

 # get an array of the cottage data to scrape
 scraperwiki::attach("holidaycottagescouk_summary") ;
 $cottData = scraperwiki::select("COTTAGE_URL  from 'holidaycottagescouk_summary'.SWDATA order by COTTAGE_URL");

 $placeholder = scraperwiki::get_var("cottURL");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 $apidom = new simple_html_dom();
 foreach($cottData as $value){

  $highPrice = "";
  $lowPrice = "";
  $found = 0;
  $count = 0;



  scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);


  // check the cottage url against the blacklist
  foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }

  // image




  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url   = $value['COTTAGE_URL'];

 // Details
 $details ="";
 foreach($dom->find('div[class=leftColRightPanel]')as $sec){

  foreach($sec->find('ul[class=glanceList]')as $ele){
    $details .= $ele->plaintext;
   }
 
   $areaDescArr = explode(":",$details);
   $sleeps= str_replace("Bedrooms","",$areaDescArr[1]);
   $bedrooms = str_replace("bathrooms","",$areaDescArr[2]);
   $bedrooms = str_replace("Bathrooms","",$bedrooms);
 
   $bathrooms = substr($areaDescArr[3],0,strpos($areaDescArr[3],"Dogs")); 
   $pets = 0;
   if(strpos($areaDescArr[4],"Yes"))
     $pets = 1;
   $changeoverDay = str_replace("Price band","",$areaDescArr[5]);

   foreach($sec->find('ul[class=glanceList]')as $ele){
    $details .= $ele->plaintext;
   }
       
   $lastEleArr = explode(" ",end($areaDescArr));
   foreach($lastEleArr as $item)
     if(strlen($item)>1 )
       $cottID = $item;

   $features = "";
   foreach($sec->find('ul[class=featList]')as $ele){
     foreach($ele->find('li')as $ele){
       $features .= $ele->plaintext.",";
     }
   }
 }

 //Description
 $description ="";
 foreach($dom->find('div[class=leftColLeftPanel divideInner]')as $data){
   foreach($data->find('p')as $desc){
    $description .= " ".$desc->plaintext;
   }
 }

 // long lat 

 foreach($dom->find('h2[id=ctl00_ContentPlaceHolder1_marketingAddress]')as $ele){
    $placeName = $ele->plaintext;
    if(strpos($placeName,"(") ){
      $offset_first =  strpos($placeName,"(");
      $offset_second =  strpos($placeName,")");
      $firstPart = substr($placeName,0,$offset_first);
      $secondPart = substr($placeName,$offset_second+1);
      $location = $firstPart.$secondPart.", UK";
    }else
      $location =$placeName.", UK";
 }


$cottage_name_offest  =  strpos($placeName,"(");
$cottage_name = substr($placeName,0,$cottage_name_offest);
$cottage_name = $cottage_name ." Cottage";

$location = str_replace(" ","+",$location);

 # get the geocoding of the location
 $apiCall = "http://maps.googleapis.com/maps/api/geocode/xml?address=".$location."&sensor=false";
print_r($apiCall );

 $apihtml = scraperWiki::scrape($apiCall);
 $apidom->load($apihtml);
 $lat = "";
 $lng = "";   
 foreach($apidom->find('location') as $ele){
     foreach($ele->find('lat') as $lats){
        $lat = $lats->plaintext;
     }
     foreach($ele->find('lng')as $lngs){ 
        $lng = $lngs->plaintext;
     }
 }
 
print_r($lat);
print_r($lng);

 $imgs = "";
 $imgURL = "";
 foreach($dom->find('div[id=slides]')as $data){
  foreach($data->find('a')as $ele){
    $imgs .= str_replace("../../","","http://www.holidaycottages.co.uk/".$ele->href.",");
    $imgsURL = str_replace("../../","","".$ele->href);
    $imgsURL = str_replace("../","","".$ele->href);
    $imgs .="http://www.holidaycottages.co.uk/".$imgURL.",";
  }
 }

 
// Prices
foreach($dom->find('div[class=leftColRightPanel]')as $sec){
  foreach($sec->find('ul[class=glanceList]')as $ele){
    $priceband = substr($ele->plaintext,strpos($ele->plaintext,"Price band:"));
    $priceband = str_replace("Price band: ","",$priceband);
    $priceband = substr($priceband,0,strpos($priceband," ")); 

switch(trim($priceband)){
 case "A":
    $priceHigh = 215;
    $priceLow = 355;
    break;
 case "B":
    $priceHigh = 230 ;
    $priceLow = 405;
    break;
 case "C":
    $priceHigh = 240;
    $priceLow = 455;
    break;
 case "D":
    $priceHigh = 250;
    $priceLow = 485;
    break;
 case "E":
    $priceHigh = 260;
    $priceLow = 505;
    break;
 case "F":
    $priceHigh = 260;
    $priceLow = 550;
    break;
 case "G":
    $priceHigh = 275;
    $priceLow = 585;
    break;
 case "H":
    $priceHigh = 275;
    $priceLow = 585;
    break;
 case "I":
    $priceHigh = 275;
    $priceLow = 625;
    break;
 case "J":
    $priceHigh = 275;
    $priceLow = 665;
    break;
 case "K":
    $priceHigh = 285;
    $priceLow = 690;
    break;
 case "L":
    $priceHigh = 340;
    $priceLow = 710;
    break;
 case "M":
    $priceHigh = 355;
    $priceLow = 735;
    break;
 case "N":
    $priceHigh = 375;
    $priceLow = 790;
    break;
  case "O":
    $priceHigh = 390;
    $priceLow = 810;
    break;
  case "P":
    $priceHigh = 410;
    $priceLow = 825;
    break;
  case "Q":
    $priceHigh = 430;
    $priceLow = 875;
    break;
  case "R":
    $priceHigh = 450;
    $priceLow = 945;
    break;
  case "S":
    $priceHigh = 470;
    $priceLow = 1005;
    break;
  case "T":
    $priceHigh = 495;
    $priceLow = 1045;
    break;
  case "U":
    $priceHigh = 525;
    $priceLow = 1135;
    break;
  case "V":
    $priceHigh = 555;
    $priceLow = 1225;
    break;
  case "W":
    $priceHigh = 610;
    $priceLow = 1325;
    break;
  case "X":
    $priceHigh = 680;
    $priceLow = 1475;
    break;
 case "Y":
    $priceHigh = 795;
    $priceLow = 1685;
    break;
 case "Z":
    $priceHigh = 860;
    $priceLow = 1965;
    break;
 default:
    $priceHigh = "N/A";
    $priceLow = "N/A";
    }


 /*  save the data  */

 $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => trim($changeoverDay),
      'COTTAGE_NAME'        => trim($cottage_name),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => $pets,
      'COTTAGE_REFERENCE'   => trim($cottID),
      'FEATURES'            => trim(clean_text($features)),  
      'DESCRIPTION'         => trim(clean_text($description)),
      'LOCATION_DESCRIPTON' => "N/A",
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($imgs),
      'Agent'               => "holidaycottages.co.uk",
      'area'                => $location,     
      'priceband'           => $priceband,          
   );

 # print_r($record);
   scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
  }
 }
}

?>


