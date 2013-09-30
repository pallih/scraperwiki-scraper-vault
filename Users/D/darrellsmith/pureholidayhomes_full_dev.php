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
 scraperwiki::attach("pureholidayhomes_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_URL from 'pureholidayhomes_summary'.SWDATA order by COTTAGE_URL");

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


  scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);
  // check the cottage url against the blacklist
  foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }

  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url = $value['COTTAGE_URL'];
   
  foreach($dom->find('div[class=summary]') as $data){
    $summaryArr =  explode(":",$data->plaintext);
    $sleeps = str_replace("Bedrooms","", $summaryArr[2]);
    $bedrooms = $summaryArr[3];
    $bathrooms = $summaryArr[4];
    $bedrooms = str_replace("Bedrooms","",$bedrooms); 
    $bedrooms = str_replace("Bathrooms","",$bedrooms );
    $bathrooms = str_replace("Bathrooms","",$bathrooms );
    $bathrooms = substr($bathrooms,0,2);
  }

  // LAT / LONG
  
  # echo $dom;

  foreach($dom->find('meta[itemprop=latitude]') as $data){
    $lat = $data->content;
  }

  foreach($dom->find('meta[itemprop=longitude]') as $data){
    $lng = $data->content;
  }
  
  // features 
  $cottage_facil = "";
  foreach($dom->find('div[id=facilitiesContenerWrap]')as $facility){
    foreach($facility->find('div[class=list_menu_wrapper]') as $data){
      foreach($data->find('li')as $item){
        $cottage_facil .=  $item->plaintext.",";
      }
    }
  }


  // Pets
  foreach($dom->find('table[class=phh_page_property_DataTable phh_page_property_DataTable_pivot]')as $table){
    $pets = 0;
    if(strpos($table->plaintext,"Pets")){
      $pets = 1;
    }
  }

  $paragraph="";
  $para = "";
  // Description
  foreach($dom->find('div[id=ptabs-1]')as $description){
     
     $para .=  $description; 
  }
  $cottDescArr =  explode("region:",$para);
  $limit =  @strrpos_string($cottDescArr[1], "<br/><br/>");
  $cottLocationDesc =@substr($cottDescArr[1],0,$limit);
  $cottLocationDesc = str_replace("<br/><br/>","\n",$cottLocationDesc);


  if(!isset($cottDescArr[1])){
     $cottDesc =  strip_tags($para);
     $cottLocationDesc = "N/A";
  }else{
    $cottDesc =  strip_tags($cottDescArr[0]);
  }
  $cottDesc =  str_replace("Description ","",  $cottDesc);
  $cottDesc =  substr($cottDesc,0,strpos($cottDesc,"... read more")-14);

  foreach($dom->find('H1')as $description){
     $cottageName=  $description->plaintext; 
  }


  foreach($dom->find('div[class=prices]')as $id){
    $cottID = $id->plaintext;
    $end = strpos($cottID,")");
    $start = strpos($cottID,"property id")+11;
    $cottageID= substr($cottID,$start,$end ); 
    $cottageID = str_replace(")","",$cottageID);    
  }

  $pic = "";
  foreach($dom->find('div[class=scroll]')as $item){
    foreach($item->find('div[class=phh_page_ui_widgets_ImagesWidget_thumb]')as $ele){
      foreach($ele->find('a')as $thumb){   
        $pic .= $thumb->href.",";
      }
    }
  }


  $priceArray = array();
  if($found == 0){
    foreach($dom->find('div[class=box_bw]')as $item){
      $found = 1;
      foreach($item->find('div[class=price-message]')as $data){
        $lowPrice = $data->plaintext;
        $lowPrice = preg_replace('/[^0-9.]+/', '', $lowPrice );
      }
    }
  }


    
    
    if($lowPrice != "" && intval($lowPrice) != 0){
        $highPrice = $lowPrice * 2.5; 
    }else{
      $highPrice = "N/A";
      $lowPrice = "N/A";
    }  
  

echo $cottage_url;
echo "\n".$highPrice."\n";
echo $lowPrice."\n";  
  
   
   /*  save the data  */
   $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($highPrice),
      'PRICE_LOW'           => trim($lowPrice),
      'CHANGEOVERDAY'       => "Flexible",
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottageID),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottDesc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($cottLocationDesc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "pureholidayhomes.com",
   );


   if(strlen(trim(clean_text($cottDesc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
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
 scraperwiki::attach("pureholidayhomes_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_URL from 'pureholidayhomes_summary'.SWDATA order by COTTAGE_URL");

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


  scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);
  // check the cottage url against the blacklist
  foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }

  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url = $value['COTTAGE_URL'];
   
  foreach($dom->find('div[class=summary]') as $data){
    $summaryArr =  explode(":",$data->plaintext);
    $sleeps = str_replace("Bedrooms","", $summaryArr[2]);
    $bedrooms = $summaryArr[3];
    $bathrooms = $summaryArr[4];
    $bedrooms = str_replace("Bedrooms","",$bedrooms); 
    $bedrooms = str_replace("Bathrooms","",$bedrooms );
    $bathrooms = str_replace("Bathrooms","",$bathrooms );
    $bathrooms = substr($bathrooms,0,2);
  }

  // LAT / LONG
  
  # echo $dom;

  foreach($dom->find('meta[itemprop=latitude]') as $data){
    $lat = $data->content;
  }

  foreach($dom->find('meta[itemprop=longitude]') as $data){
    $lng = $data->content;
  }
  
  // features 
  $cottage_facil = "";
  foreach($dom->find('div[id=facilitiesContenerWrap]')as $facility){
    foreach($facility->find('div[class=list_menu_wrapper]') as $data){
      foreach($data->find('li')as $item){
        $cottage_facil .=  $item->plaintext.",";
      }
    }
  }


  // Pets
  foreach($dom->find('table[class=phh_page_property_DataTable phh_page_property_DataTable_pivot]')as $table){
    $pets = 0;
    if(strpos($table->plaintext,"Pets")){
      $pets = 1;
    }
  }

  $paragraph="";
  $para = "";
  // Description
  foreach($dom->find('div[id=ptabs-1]')as $description){
     
     $para .=  $description; 
  }
  $cottDescArr =  explode("region:",$para);
  $limit =  @strrpos_string($cottDescArr[1], "<br/><br/>");
  $cottLocationDesc =@substr($cottDescArr[1],0,$limit);
  $cottLocationDesc = str_replace("<br/><br/>","\n",$cottLocationDesc);


  if(!isset($cottDescArr[1])){
     $cottDesc =  strip_tags($para);
     $cottLocationDesc = "N/A";
  }else{
    $cottDesc =  strip_tags($cottDescArr[0]);
  }
  $cottDesc =  str_replace("Description ","",  $cottDesc);
  $cottDesc =  substr($cottDesc,0,strpos($cottDesc,"... read more")-14);

  foreach($dom->find('H1')as $description){
     $cottageName=  $description->plaintext; 
  }


  foreach($dom->find('div[class=prices]')as $id){
    $cottID = $id->plaintext;
    $end = strpos($cottID,")");
    $start = strpos($cottID,"property id")+11;
    $cottageID= substr($cottID,$start,$end ); 
    $cottageID = str_replace(")","",$cottageID);    
  }

  $pic = "";
  foreach($dom->find('div[class=scroll]')as $item){
    foreach($item->find('div[class=phh_page_ui_widgets_ImagesWidget_thumb]')as $ele){
      foreach($ele->find('a')as $thumb){   
        $pic .= $thumb->href.",";
      }
    }
  }


  $priceArray = array();
  if($found == 0){
    foreach($dom->find('div[class=box_bw]')as $item){
      $found = 1;
      foreach($item->find('div[class=price-message]')as $data){
        $lowPrice = $data->plaintext;
        $lowPrice = preg_replace('/[^0-9.]+/', '', $lowPrice );
      }
    }
  }


    
    
    if($lowPrice != "" && intval($lowPrice) != 0){
        $highPrice = $lowPrice * 2.5; 
    }else{
      $highPrice = "N/A";
      $lowPrice = "N/A";
    }  
  

echo $cottage_url;
echo "\n".$highPrice."\n";
echo $lowPrice."\n";  
  
   
   /*  save the data  */
   $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($highPrice),
      'PRICE_LOW'           => trim($lowPrice),
      'CHANGEOVERDAY'       => "Flexible",
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottageID),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottDesc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($cottLocationDesc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "pureholidayhomes.com",
   );


   if(strlen(trim(clean_text($cottDesc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
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
 scraperwiki::attach("pureholidayhomes_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_URL from 'pureholidayhomes_summary'.SWDATA order by COTTAGE_URL");

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


  scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);
  // check the cottage url against the blacklist
  foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }

  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url = $value['COTTAGE_URL'];
   
  foreach($dom->find('div[class=summary]') as $data){
    $summaryArr =  explode(":",$data->plaintext);
    $sleeps = str_replace("Bedrooms","", $summaryArr[2]);
    $bedrooms = $summaryArr[3];
    $bathrooms = $summaryArr[4];
    $bedrooms = str_replace("Bedrooms","",$bedrooms); 
    $bedrooms = str_replace("Bathrooms","",$bedrooms );
    $bathrooms = str_replace("Bathrooms","",$bathrooms );
    $bathrooms = substr($bathrooms,0,2);
  }

  // LAT / LONG
  
  # echo $dom;

  foreach($dom->find('meta[itemprop=latitude]') as $data){
    $lat = $data->content;
  }

  foreach($dom->find('meta[itemprop=longitude]') as $data){
    $lng = $data->content;
  }
  
  // features 
  $cottage_facil = "";
  foreach($dom->find('div[id=facilitiesContenerWrap]')as $facility){
    foreach($facility->find('div[class=list_menu_wrapper]') as $data){
      foreach($data->find('li')as $item){
        $cottage_facil .=  $item->plaintext.",";
      }
    }
  }


  // Pets
  foreach($dom->find('table[class=phh_page_property_DataTable phh_page_property_DataTable_pivot]')as $table){
    $pets = 0;
    if(strpos($table->plaintext,"Pets")){
      $pets = 1;
    }
  }

  $paragraph="";
  $para = "";
  // Description
  foreach($dom->find('div[id=ptabs-1]')as $description){
     
     $para .=  $description; 
  }
  $cottDescArr =  explode("region:",$para);
  $limit =  @strrpos_string($cottDescArr[1], "<br/><br/>");
  $cottLocationDesc =@substr($cottDescArr[1],0,$limit);
  $cottLocationDesc = str_replace("<br/><br/>","\n",$cottLocationDesc);


  if(!isset($cottDescArr[1])){
     $cottDesc =  strip_tags($para);
     $cottLocationDesc = "N/A";
  }else{
    $cottDesc =  strip_tags($cottDescArr[0]);
  }
  $cottDesc =  str_replace("Description ","",  $cottDesc);
  $cottDesc =  substr($cottDesc,0,strpos($cottDesc,"... read more")-14);

  foreach($dom->find('H1')as $description){
     $cottageName=  $description->plaintext; 
  }


  foreach($dom->find('div[class=prices]')as $id){
    $cottID = $id->plaintext;
    $end = strpos($cottID,")");
    $start = strpos($cottID,"property id")+11;
    $cottageID= substr($cottID,$start,$end ); 
    $cottageID = str_replace(")","",$cottageID);    
  }

  $pic = "";
  foreach($dom->find('div[class=scroll]')as $item){
    foreach($item->find('div[class=phh_page_ui_widgets_ImagesWidget_thumb]')as $ele){
      foreach($ele->find('a')as $thumb){   
        $pic .= $thumb->href.",";
      }
    }
  }


  $priceArray = array();
  if($found == 0){
    foreach($dom->find('div[class=box_bw]')as $item){
      $found = 1;
      foreach($item->find('div[class=price-message]')as $data){
        $lowPrice = $data->plaintext;
        $lowPrice = preg_replace('/[^0-9.]+/', '', $lowPrice );
      }
    }
  }


    
    
    if($lowPrice != "" && intval($lowPrice) != 0){
        $highPrice = $lowPrice * 2.5; 
    }else{
      $highPrice = "N/A";
      $lowPrice = "N/A";
    }  
  

echo $cottage_url;
echo "\n".$highPrice."\n";
echo $lowPrice."\n";  
  
   
   /*  save the data  */
   $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($highPrice),
      'PRICE_LOW'           => trim($lowPrice),
      'CHANGEOVERDAY'       => "Flexible",
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottageID),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottDesc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($cottLocationDesc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "pureholidayhomes.com",
   );


   if(strlen(trim(clean_text($cottDesc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
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
 scraperwiki::attach("pureholidayhomes_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_URL from 'pureholidayhomes_summary'.SWDATA order by COTTAGE_URL");

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


  scraperwiki::save_var("cottURL",$value['COTTAGE_URL']);
  // check the cottage url against the blacklist
  foreach($blacklist as $blItem){
    if($value['COTTAGE_URL'] == $blItem)
      continue 2;
  }

  //load the page into the scraper
  $html = scraperWiki::scrape($value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }
  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_url = $value['COTTAGE_URL'];
   
  foreach($dom->find('div[class=summary]') as $data){
    $summaryArr =  explode(":",$data->plaintext);
    $sleeps = str_replace("Bedrooms","", $summaryArr[2]);
    $bedrooms = $summaryArr[3];
    $bathrooms = $summaryArr[4];
    $bedrooms = str_replace("Bedrooms","",$bedrooms); 
    $bedrooms = str_replace("Bathrooms","",$bedrooms );
    $bathrooms = str_replace("Bathrooms","",$bathrooms );
    $bathrooms = substr($bathrooms,0,2);
  }

  // LAT / LONG
  
  # echo $dom;

  foreach($dom->find('meta[itemprop=latitude]') as $data){
    $lat = $data->content;
  }

  foreach($dom->find('meta[itemprop=longitude]') as $data){
    $lng = $data->content;
  }
  
  // features 
  $cottage_facil = "";
  foreach($dom->find('div[id=facilitiesContenerWrap]')as $facility){
    foreach($facility->find('div[class=list_menu_wrapper]') as $data){
      foreach($data->find('li')as $item){
        $cottage_facil .=  $item->plaintext.",";
      }
    }
  }


  // Pets
  foreach($dom->find('table[class=phh_page_property_DataTable phh_page_property_DataTable_pivot]')as $table){
    $pets = 0;
    if(strpos($table->plaintext,"Pets")){
      $pets = 1;
    }
  }

  $paragraph="";
  $para = "";
  // Description
  foreach($dom->find('div[id=ptabs-1]')as $description){
     
     $para .=  $description; 
  }
  $cottDescArr =  explode("region:",$para);
  $limit =  @strrpos_string($cottDescArr[1], "<br/><br/>");
  $cottLocationDesc =@substr($cottDescArr[1],0,$limit);
  $cottLocationDesc = str_replace("<br/><br/>","\n",$cottLocationDesc);


  if(!isset($cottDescArr[1])){
     $cottDesc =  strip_tags($para);
     $cottLocationDesc = "N/A";
  }else{
    $cottDesc =  strip_tags($cottDescArr[0]);
  }
  $cottDesc =  str_replace("Description ","",  $cottDesc);
  $cottDesc =  substr($cottDesc,0,strpos($cottDesc,"... read more")-14);

  foreach($dom->find('H1')as $description){
     $cottageName=  $description->plaintext; 
  }


  foreach($dom->find('div[class=prices]')as $id){
    $cottID = $id->plaintext;
    $end = strpos($cottID,")");
    $start = strpos($cottID,"property id")+11;
    $cottageID= substr($cottID,$start,$end ); 
    $cottageID = str_replace(")","",$cottageID);    
  }

  $pic = "";
  foreach($dom->find('div[class=scroll]')as $item){
    foreach($item->find('div[class=phh_page_ui_widgets_ImagesWidget_thumb]')as $ele){
      foreach($ele->find('a')as $thumb){   
        $pic .= $thumb->href.",";
      }
    }
  }


  $priceArray = array();
  if($found == 0){
    foreach($dom->find('div[class=box_bw]')as $item){
      $found = 1;
      foreach($item->find('div[class=price-message]')as $data){
        $lowPrice = $data->plaintext;
        $lowPrice = preg_replace('/[^0-9.]+/', '', $lowPrice );
      }
    }
  }


    
    
    if($lowPrice != "" && intval($lowPrice) != 0){
        $highPrice = $lowPrice * 2.5; 
    }else{
      $highPrice = "N/A";
      $lowPrice = "N/A";
    }  
  

echo $cottage_url;
echo "\n".$highPrice."\n";
echo $lowPrice."\n";  
  
   
   /*  save the data  */
   $record = array(
      'COTTAGE_LINK'        => trim($cottage_url),
      'PRICE_HIGH'          => trim($highPrice),
      'PRICE_LOW'           => trim($lowPrice),
      'CHANGEOVERDAY'       => "Flexible",
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms ),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottageID),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottDesc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($cottLocationDesc)),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Agent'               => "pureholidayhomes.com",
   );


   if(strlen(trim(clean_text($cottDesc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
}

?>


