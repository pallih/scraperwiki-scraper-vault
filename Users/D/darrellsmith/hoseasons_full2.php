<?php

echo("This is stupid");

#scraperwiki::save_var('dummy', 0);


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
 scraperwiki::attach("hoseasons_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_ID, COTTAGE_URL, SLEEPS, BEDROOMS, PETS,COTTAGE_NAME, PRICE_LOW, PRICE_HIGH from 'hoseasons_summary'.SWDATA order by COTTAGE_URL");

 $placeholder = scraperwiki::get_var("cottURL");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

 foreach($cottData as $value){

  $highPrice = "";
  $lowPrice = "";
  $found = 0;
  $count = 0;



 # scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);


  // check the cottage url against the blacklist
 /* foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }
*/





  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']."#activeTabId=inTheArea");
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url   = $value['COTTAGE_URL'];
  $cottage_name  = $value['COTTAGE_NAME'];  
  $cottage_id    = $value['COTTAGE_ID'];
  $sleeps        = $value['SLEEPS'];
  $bedrooms      = $value['BEDROOMS']; 
  $pets          = $value['PETS'];
  $priceLow      = $value['PRICE_LOW'];
  $priceHigh     = $value['PRICE_HIGH'];
  $changeover    = "Flexible";

 
 


 // Description
 $cottage_facil = "";
 foreach($dom->find('div[class=cottageDetailsLeft]')as $data){
   $descArr = explode("<br />",$data);
   $description = strip_tags($descArr[5]);
   $description .= strip_tags($descArr[6]);
   $facilities = str_replace("Facilities:","",strip_tags($descArr[7]));
 }
 
# echo $description;
# echo $facilities;
 

#echo $dom;
/* foreach($dom->find('div[class=inTheAreRight]')as $data){
   foreach($dom->find('div[class=inTheAreRight]')as $data){
     $area_desc = $data->plaintext;
     echo  $area_desc;
   }
 }
 
 */
 
 
 
// get the count
// append to the url
// load the url 
// scrape the page for images



 // long lat
 $coords = substr($html,strpos($html,"#property-map-frame",20000),100); 

 $coordsTrimmed =  substr($coords,strpos($coords,"latitude"),50);
 $coordsArr = explode(",",$coordsTrimmed);
 $lat =  str_replace("latitude: ","",$coordsArr[0]);
 $lng =  str_replace("longitude: ","",$coordsArr[1]);
 $lng =  str_replace("}]","",$lng);



   
   /*  save the data  */

 $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottage_id),
      'FEATURES'            => trim(clean_text($features ) ),  
      'DESCRIPTION'         => trim(clean_text($cott_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "suffolk-secrets.co.uk",
   );


 if(strlen(trim(clean_text($cott_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);

}

?>


<?php

echo("This is stupid");

#scraperwiki::save_var('dummy', 0);


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
 scraperwiki::attach("hoseasons_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_ID, COTTAGE_URL, SLEEPS, BEDROOMS, PETS,COTTAGE_NAME, PRICE_LOW, PRICE_HIGH from 'hoseasons_summary'.SWDATA order by COTTAGE_URL");

 $placeholder = scraperwiki::get_var("cottURL");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

 foreach($cottData as $value){

  $highPrice = "";
  $lowPrice = "";
  $found = 0;
  $count = 0;



 # scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);


  // check the cottage url against the blacklist
 /* foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }
*/





  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']."#activeTabId=inTheArea");
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url   = $value['COTTAGE_URL'];
  $cottage_name  = $value['COTTAGE_NAME'];  
  $cottage_id    = $value['COTTAGE_ID'];
  $sleeps        = $value['SLEEPS'];
  $bedrooms      = $value['BEDROOMS']; 
  $pets          = $value['PETS'];
  $priceLow      = $value['PRICE_LOW'];
  $priceHigh     = $value['PRICE_HIGH'];
  $changeover    = "Flexible";

 
 


 // Description
 $cottage_facil = "";
 foreach($dom->find('div[class=cottageDetailsLeft]')as $data){
   $descArr = explode("<br />",$data);
   $description = strip_tags($descArr[5]);
   $description .= strip_tags($descArr[6]);
   $facilities = str_replace("Facilities:","",strip_tags($descArr[7]));
 }
 
# echo $description;
# echo $facilities;
 

#echo $dom;
/* foreach($dom->find('div[class=inTheAreRight]')as $data){
   foreach($dom->find('div[class=inTheAreRight]')as $data){
     $area_desc = $data->plaintext;
     echo  $area_desc;
   }
 }
 
 */
 
 
 
// get the count
// append to the url
// load the url 
// scrape the page for images



 // long lat
 $coords = substr($html,strpos($html,"#property-map-frame",20000),100); 

 $coordsTrimmed =  substr($coords,strpos($coords,"latitude"),50);
 $coordsArr = explode(",",$coordsTrimmed);
 $lat =  str_replace("latitude: ","",$coordsArr[0]);
 $lng =  str_replace("longitude: ","",$coordsArr[1]);
 $lng =  str_replace("}]","",$lng);



   
   /*  save the data  */

 $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottage_id),
      'FEATURES'            => trim(clean_text($features ) ),  
      'DESCRIPTION'         => trim(clean_text($cott_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "suffolk-secrets.co.uk",
   );


 if(strlen(trim(clean_text($cott_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);

}

?>


<?php

echo("This is stupid");

#scraperwiki::save_var('dummy', 0);


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
 scraperwiki::attach("hoseasons_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_ID, COTTAGE_URL, SLEEPS, BEDROOMS, PETS,COTTAGE_NAME, PRICE_LOW, PRICE_HIGH from 'hoseasons_summary'.SWDATA order by COTTAGE_URL");

 $placeholder = scraperwiki::get_var("cottURL");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

 foreach($cottData as $value){

  $highPrice = "";
  $lowPrice = "";
  $found = 0;
  $count = 0;



 # scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);


  // check the cottage url against the blacklist
 /* foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }
*/





  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']."#activeTabId=inTheArea");
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url   = $value['COTTAGE_URL'];
  $cottage_name  = $value['COTTAGE_NAME'];  
  $cottage_id    = $value['COTTAGE_ID'];
  $sleeps        = $value['SLEEPS'];
  $bedrooms      = $value['BEDROOMS']; 
  $pets          = $value['PETS'];
  $priceLow      = $value['PRICE_LOW'];
  $priceHigh     = $value['PRICE_HIGH'];
  $changeover    = "Flexible";

 
 


 // Description
 $cottage_facil = "";
 foreach($dom->find('div[class=cottageDetailsLeft]')as $data){
   $descArr = explode("<br />",$data);
   $description = strip_tags($descArr[5]);
   $description .= strip_tags($descArr[6]);
   $facilities = str_replace("Facilities:","",strip_tags($descArr[7]));
 }
 
# echo $description;
# echo $facilities;
 

#echo $dom;
/* foreach($dom->find('div[class=inTheAreRight]')as $data){
   foreach($dom->find('div[class=inTheAreRight]')as $data){
     $area_desc = $data->plaintext;
     echo  $area_desc;
   }
 }
 
 */
 
 
 
// get the count
// append to the url
// load the url 
// scrape the page for images



 // long lat
 $coords = substr($html,strpos($html,"#property-map-frame",20000),100); 

 $coordsTrimmed =  substr($coords,strpos($coords,"latitude"),50);
 $coordsArr = explode(",",$coordsTrimmed);
 $lat =  str_replace("latitude: ","",$coordsArr[0]);
 $lng =  str_replace("longitude: ","",$coordsArr[1]);
 $lng =  str_replace("}]","",$lng);



   
   /*  save the data  */

 $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottage_id),
      'FEATURES'            => trim(clean_text($features ) ),  
      'DESCRIPTION'         => trim(clean_text($cott_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "suffolk-secrets.co.uk",
   );


 if(strlen(trim(clean_text($cott_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);

}

?>


<?php

echo("This is stupid");

#scraperwiki::save_var('dummy', 0);


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
 scraperwiki::attach("hoseasons_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_ID, COTTAGE_URL, SLEEPS, BEDROOMS, PETS,COTTAGE_NAME, PRICE_LOW, PRICE_HIGH from 'hoseasons_summary'.SWDATA order by COTTAGE_URL");

 $placeholder = scraperwiki::get_var("cottURL");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

 foreach($cottData as $value){

  $highPrice = "";
  $lowPrice = "";
  $found = 0;
  $count = 0;



 # scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);


  // check the cottage url against the blacklist
 /* foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }
*/





  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']."#activeTabId=inTheArea");
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url   = $value['COTTAGE_URL'];
  $cottage_name  = $value['COTTAGE_NAME'];  
  $cottage_id    = $value['COTTAGE_ID'];
  $sleeps        = $value['SLEEPS'];
  $bedrooms      = $value['BEDROOMS']; 
  $pets          = $value['PETS'];
  $priceLow      = $value['PRICE_LOW'];
  $priceHigh     = $value['PRICE_HIGH'];
  $changeover    = "Flexible";

 
 


 // Description
 $cottage_facil = "";
 foreach($dom->find('div[class=cottageDetailsLeft]')as $data){
   $descArr = explode("<br />",$data);
   $description = strip_tags($descArr[5]);
   $description .= strip_tags($descArr[6]);
   $facilities = str_replace("Facilities:","",strip_tags($descArr[7]));
 }
 
# echo $description;
# echo $facilities;
 

#echo $dom;
/* foreach($dom->find('div[class=inTheAreRight]')as $data){
   foreach($dom->find('div[class=inTheAreRight]')as $data){
     $area_desc = $data->plaintext;
     echo  $area_desc;
   }
 }
 
 */
 
 
 
// get the count
// append to the url
// load the url 
// scrape the page for images



 // long lat
 $coords = substr($html,strpos($html,"#property-map-frame",20000),100); 

 $coordsTrimmed =  substr($coords,strpos($coords,"latitude"),50);
 $coordsArr = explode(",",$coordsTrimmed);
 $lat =  str_replace("latitude: ","",$coordsArr[0]);
 $lng =  str_replace("longitude: ","",$coordsArr[1]);
 $lng =  str_replace("}]","",$lng);



   
   /*  save the data  */

 $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottage_id),
      'FEATURES'            => trim(clean_text($features ) ),  
      'DESCRIPTION'         => trim(clean_text($cott_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "suffolk-secrets.co.uk",
   );


 if(strlen(trim(clean_text($cott_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);

}

?>


