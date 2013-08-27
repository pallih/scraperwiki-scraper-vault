<?php

scraperwiki::save_var('dummy', 0);

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


 $url = "http://www.holidaylettings.co.uk/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("holidaylettings_summary_check") ;
 $cottData = scraperwiki::select("COTTAGE_ID, COTTAGE_URL from 'holidaylettings_summary_check'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['COTTAGE_URL']);
    // check the cottage url against the blacklist
    foreach($blacklist as $blItem){
      if($value['COTTAGE_ID'] == $blItem)
        continue 2;
    }

  //load the page into the scraper
  $html = scraperWiki::scrape($url.$value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }


  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_id = $value['COTTAGE_ID'];
  $cottage_url = $value['COTTAGE_URL'];
     
 foreach($dom->find('div[id=advert_summary]') as $data){

     foreach($data->find('H2') as $name)
        $cottageName = $name->plaintext;

     foreach($data->find("div[id=home_type_info]") as $info){
        $infoArray =  explode("|",$info->plaintext) ;
        $bedrooms = str_replace("&nbsp;bedrooms","", $infoArray[1]);
        $sleeps = str_replace("Sleeps&nbsp;","", $infoArray[2]); 
     }

     foreach($data->find("div[class=summary_rightcol]") as $info){
        foreach($info->find("div[id=sum_prices]") as $frag){
           foreach($frag->find("strong") as $ele){          
              $prices =  explode("&pound;",$ele->plaintext);
              $price_low = str_replace("&ndash;","",$prices[1]);
              $price_high =&$prices[2];
           }       
        }
     }
  }
  foreach($dom->find("div[id=home_description]") as $data){
       $cottage_desc =  $data->plaintext;  
       $cottage_desc = str_replace("About the home","",$cottage_desc);  
  }
  

 foreach($dom->find("div[id=sum_changeover]") as $data){
       $changeover =  $data->plaintext;    
  }
  


  foreach($dom->find("div[id=facilitiesSection]") as $data){
       $cottage_facil = $data->plaintext;  
       $cottage_facil = str_replace("Facilities","",$cottage_facil );
       $cottage_facil = str_replace("Further details indoors:","",$cottage_facil ); 

  }

 $area_desc = "";
  foreach($dom->find("div[id=area]") as $data){
    foreach($data->find("p") as $ele){  
      if($area_desc=="")    
         $area_desc = $ele->plaintext;   
    }
  }


  foreach($dom->find("div[id=map_canvas]") as $data){
    foreach($data->find("input[id=lat]") as $ele){  
      $lat = $ele->value;   
    }
    foreach($data->find("input[id=lng]") as $ele){  
      $lng = $ele->value;   
    }
  }

  $pets = "-"; 
  foreach($dom->find("div[id=sum_keyinfo]") as $data){
    if(strpos($data,"no pets allowed")>0)
      $pets = 0;
    else
      $pets = 1;
  }
  
  
  $img = "";
  foreach($dom->find("div[id=photos]") as $data){
    foreach($data->find("img") as $ele){  
       $image =  str_replace("http://resources.holidaylettings.co.uk/images/photo_magnify.gif","",$ele->src);
//1280   / 320 
    
       $image =  str_replace("/320/","/1280/",$image);            
  
       if(!strpos($image,".gif"))
           $img .=  $image.",";   

    }
  }

$baths ="";
 foreach($dom->find("div[id=facilitiesSection]") as $data){
   foreach($data->find("table") as $table){
     $tab = explode("<td>",$table); 
     foreach($tab as $item){
       if(strpos($item,"bathroom")>0){
         $baths =  substr($item,strpos($item,"bathroom")-2,2);
       }
     }
   }
 }
  
    if($baths =="y ")
       $baths = 1;

  
   /*  save the data  */
    $record = array(
      'COTTAGE_LINK'        => trim("http://www.holidaylettings.co.uk".$cottage_url),
      'PRICE_HIGH'          => trim($price_high),
      'PRICE_LOW'           => trim($price_low),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($baths),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim(str_replace("/","",$cottage_id)),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottage_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc )),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($img),
      'Agent'               => "www.holidaylettings.co.uk",
    );


    if(strlen(trim(clean_text($cottage_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
    }
  

?>
<?php

scraperwiki::save_var('dummy', 0);

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


 $url = "http://www.holidaylettings.co.uk/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("holidaylettings_summary_check") ;
 $cottData = scraperwiki::select("COTTAGE_ID, COTTAGE_URL from 'holidaylettings_summary_check'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['COTTAGE_URL']);
    // check the cottage url against the blacklist
    foreach($blacklist as $blItem){
      if($value['COTTAGE_ID'] == $blItem)
        continue 2;
    }

  //load the page into the scraper
  $html = scraperWiki::scrape($url.$value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }


  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_id = $value['COTTAGE_ID'];
  $cottage_url = $value['COTTAGE_URL'];
     
 foreach($dom->find('div[id=advert_summary]') as $data){

     foreach($data->find('H2') as $name)
        $cottageName = $name->plaintext;

     foreach($data->find("div[id=home_type_info]") as $info){
        $infoArray =  explode("|",$info->plaintext) ;
        $bedrooms = str_replace("&nbsp;bedrooms","", $infoArray[1]);
        $sleeps = str_replace("Sleeps&nbsp;","", $infoArray[2]); 
     }

     foreach($data->find("div[class=summary_rightcol]") as $info){
        foreach($info->find("div[id=sum_prices]") as $frag){
           foreach($frag->find("strong") as $ele){          
              $prices =  explode("&pound;",$ele->plaintext);
              $price_low = str_replace("&ndash;","",$prices[1]);
              $price_high =&$prices[2];
           }       
        }
     }
  }
  foreach($dom->find("div[id=home_description]") as $data){
       $cottage_desc =  $data->plaintext;  
       $cottage_desc = str_replace("About the home","",$cottage_desc);  
  }
  

 foreach($dom->find("div[id=sum_changeover]") as $data){
       $changeover =  $data->plaintext;    
  }
  


  foreach($dom->find("div[id=facilitiesSection]") as $data){
       $cottage_facil = $data->plaintext;  
       $cottage_facil = str_replace("Facilities","",$cottage_facil );
       $cottage_facil = str_replace("Further details indoors:","",$cottage_facil ); 

  }

 $area_desc = "";
  foreach($dom->find("div[id=area]") as $data){
    foreach($data->find("p") as $ele){  
      if($area_desc=="")    
         $area_desc = $ele->plaintext;   
    }
  }


  foreach($dom->find("div[id=map_canvas]") as $data){
    foreach($data->find("input[id=lat]") as $ele){  
      $lat = $ele->value;   
    }
    foreach($data->find("input[id=lng]") as $ele){  
      $lng = $ele->value;   
    }
  }

  $pets = "-"; 
  foreach($dom->find("div[id=sum_keyinfo]") as $data){
    if(strpos($data,"no pets allowed")>0)
      $pets = 0;
    else
      $pets = 1;
  }
  
  
  $img = "";
  foreach($dom->find("div[id=photos]") as $data){
    foreach($data->find("img") as $ele){  
       $image =  str_replace("http://resources.holidaylettings.co.uk/images/photo_magnify.gif","",$ele->src);
//1280   / 320 
    
       $image =  str_replace("/320/","/1280/",$image);            
  
       if(!strpos($image,".gif"))
           $img .=  $image.",";   

    }
  }

$baths ="";
 foreach($dom->find("div[id=facilitiesSection]") as $data){
   foreach($data->find("table") as $table){
     $tab = explode("<td>",$table); 
     foreach($tab as $item){
       if(strpos($item,"bathroom")>0){
         $baths =  substr($item,strpos($item,"bathroom")-2,2);
       }
     }
   }
 }
  
    if($baths =="y ")
       $baths = 1;

  
   /*  save the data  */
    $record = array(
      'COTTAGE_LINK'        => trim("http://www.holidaylettings.co.uk".$cottage_url),
      'PRICE_HIGH'          => trim($price_high),
      'PRICE_LOW'           => trim($price_low),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($baths),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim(str_replace("/","",$cottage_id)),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottage_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc )),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($img),
      'Agent'               => "www.holidaylettings.co.uk",
    );


    if(strlen(trim(clean_text($cottage_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
    }
  

?>
<?php

scraperwiki::save_var('dummy', 0);

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


 $url = "http://www.holidaylettings.co.uk/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("holidaylettings_summary_check") ;
 $cottData = scraperwiki::select("COTTAGE_ID, COTTAGE_URL from 'holidaylettings_summary_check'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");

 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['COTTAGE_URL']);
    // check the cottage url against the blacklist
    foreach($blacklist as $blItem){
      if($value['COTTAGE_ID'] == $blItem)
        continue 2;
    }

  //load the page into the scraper
  $html = scraperWiki::scrape($url.$value['COTTAGE_URL']);
  $dom->load($html);
  if(fourOhfour($html)){
     continue;
  }


  $cottageDesc = "";

  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID and COTTAGE_URL
  $cottage_id = $value['COTTAGE_ID'];
  $cottage_url = $value['COTTAGE_URL'];
     
 foreach($dom->find('div[id=advert_summary]') as $data){

     foreach($data->find('H2') as $name)
        $cottageName = $name->plaintext;

     foreach($data->find("div[id=home_type_info]") as $info){
        $infoArray =  explode("|",$info->plaintext) ;
        $bedrooms = str_replace("&nbsp;bedrooms","", $infoArray[1]);
        $sleeps = str_replace("Sleeps&nbsp;","", $infoArray[2]); 
     }

     foreach($data->find("div[class=summary_rightcol]") as $info){
        foreach($info->find("div[id=sum_prices]") as $frag){
           foreach($frag->find("strong") as $ele){          
              $prices =  explode("&pound;",$ele->plaintext);
              $price_low = str_replace("&ndash;","",$prices[1]);
              $price_high =&$prices[2];
           }       
        }
     }
  }
  foreach($dom->find("div[id=home_description]") as $data){
       $cottage_desc =  $data->plaintext;  
       $cottage_desc = str_replace("About the home","",$cottage_desc);  
  }
  

 foreach($dom->find("div[id=sum_changeover]") as $data){
       $changeover =  $data->plaintext;    
  }
  


  foreach($dom->find("div[id=facilitiesSection]") as $data){
       $cottage_facil = $data->plaintext;  
       $cottage_facil = str_replace("Facilities","",$cottage_facil );
       $cottage_facil = str_replace("Further details indoors:","",$cottage_facil ); 

  }

 $area_desc = "";
  foreach($dom->find("div[id=area]") as $data){
    foreach($data->find("p") as $ele){  
      if($area_desc=="")    
         $area_desc = $ele->plaintext;   
    }
  }


  foreach($dom->find("div[id=map_canvas]") as $data){
    foreach($data->find("input[id=lat]") as $ele){  
      $lat = $ele->value;   
    }
    foreach($data->find("input[id=lng]") as $ele){  
      $lng = $ele->value;   
    }
  }

  $pets = "-"; 
  foreach($dom->find("div[id=sum_keyinfo]") as $data){
    if(strpos($data,"no pets allowed")>0)
      $pets = 0;
    else
      $pets = 1;
  }
  
  
  $img = "";
  foreach($dom->find("div[id=photos]") as $data){
    foreach($data->find("img") as $ele){  
       $image =  str_replace("http://resources.holidaylettings.co.uk/images/photo_magnify.gif","",$ele->src);
//1280   / 320 
    
       $image =  str_replace("/320/","/1280/",$image);            
  
       if(!strpos($image,".gif"))
           $img .=  $image.",";   

    }
  }

$baths ="";
 foreach($dom->find("div[id=facilitiesSection]") as $data){
   foreach($data->find("table") as $table){
     $tab = explode("<td>",$table); 
     foreach($tab as $item){
       if(strpos($item,"bathroom")>0){
         $baths =  substr($item,strpos($item,"bathroom")-2,2);
       }
     }
   }
 }
  
    if($baths =="y ")
       $baths = 1;

  
   /*  save the data  */
    $record = array(
      'COTTAGE_LINK'        => trim("http://www.holidaylettings.co.uk".$cottage_url),
      'PRICE_HIGH'          => trim($price_high),
      'PRICE_LOW'           => trim($price_low),
      'CHANGEOVERDAY'       => $changeover,
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($baths),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim(str_replace("/","",$cottage_id)),
      'FEATURES'            => trim(clean_text($cottage_facil) ),  
      'DESCRIPTION'         => trim(clean_text($cottage_desc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($area_desc )),
      'LONGITUDE'           => trim($lng),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($img),
      'Agent'               => "www.holidaylettings.co.uk",
    );


    if(strlen(trim(clean_text($cottage_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
    }
  

?>
