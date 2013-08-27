<?php
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

 $url = "http://www.holidaycottages.co.uk/ProductFeeds/cottagedetails.xml";
 $file = file_get_contents($url);
 $fArray = explode('<property id',$file);

 foreach($fArray as $value){
    $imagesList = "";
    // Get the cottage reference, this is used to check validity and to complete the clickthrough
    $cottageID = parseString($value,"<reference>","</reference>");;
    $sleeps = parseString($value,"<sleeps>","</sleeps>");
    $bedrooms = parseString($value,"<bedrooms>","</bedrooms>");
    $bathrooms = parseString($value,"<bathrooms>","</bathrooms>");
    $town = parseString($value,"<marketing_address>","</marketing_address>");
    $changeover_day= parseString($value,"<changeover_day>","</changeover_day>");
    $pets = parseString($value,"<dogs>","</dogs>");
    if($pets == "No")
       $pets = 0;
    else
       $pets = 1;
    
    $description = strip_tags(parseString($value,"<description>","</description>"));
    $cottage_link = parseString($value,"<URL>","</URL>");

    // Get the High / Low Price
    $pricemin = parseString($value,'<min>','</min>');
    $pricemax = parseString($value,'<max>','</max>');

    // Get the geocoding
    $long = parseString($value,'<long>','</long>');
    $lat = parseString($value,'<lat>','</lat>');

    // images
    $pic = "";
    $images = parseString($value,"<images>","</images>");
    $images = substr($images,strpos("<image>",$images));
    $imageArr = explode("<image>",$images);
    unset($imageArr[0]);
    foreach($imageArr as $item){
      $pic .= str_replace("</image>","",$item.",");
    }
  
    
    $features = parseString($value,"<features>","</features>");
    $cottfeatures = "";
    $featuresArr = explode("label",$features);
    unset($featuresArr[0]);
    foreach($featuresArr as $item){
      $length = strpos($item,"id=");
      $cottfeatures .=  substr($item,2,$length).",";
      $cottfeatures = str_replace('" id',"",$cottfeatures);
    }

    $town = str_replace("<![CDATA[","",$town);
    $town = substr($town,0,strpos($town,"("));
    if(strlen($town)<1)
       $town = parseString($value,"<postal_town>","</postal_town>");

    $record = array(
      'COTTAGE_LINK'        => trim(clean_text($cottage_link)),
      'PRICE_HIGH'          => trim(clean_text($pricemax)),
      'PRICE_LOW'           => trim(clean_text($pricemin)),
      'CHANGEOVERDAY'       => trim(clean_text($changeover_day)),
      'SLEEPS'              => trim(clean_text($sleeps)),
      'BEDROOMS'            => trim(clean_text($bedrooms)),
      'BATHROOMS'           => trim(clean_text($bathrooms)),
      'PETS'                => trim(clean_text($pets)),
      'COTTAGE_REFERENCE'   => trim(clean_text($cottageID)),
      'FEATURES'            => trim(clean_text($cottfeatures)),  
      'DESCRIPTION'         => trim(clean_text($description)),
      'LOCATION_DESCRIPTON' => "N/A",
      'LONGITUDE'           => trim($long),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Town'                => trim(clean_text($town)),
      'Agent'               => "holidaycottages.co.uk",
   );
        
    if(!strpos($cottage_link,'version="1.0"')){
        scraperwiki::save(array('COTTAGE_LINK'), $record); 
    }

}


 function parseString($passage, $startStr, $endStr){
    $start = strpos($passage, $startStr)+strlen($startStr);
    $end = strpos($passage, $endStr);
    $length = $end - $start;
    $txt = substr($passage,$start,$length);
    return  clean_text($txt);
 }




?>
<?php
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

 $url = "http://www.holidaycottages.co.uk/ProductFeeds/cottagedetails.xml";
 $file = file_get_contents($url);
 $fArray = explode('<property id',$file);

 foreach($fArray as $value){
    $imagesList = "";
    // Get the cottage reference, this is used to check validity and to complete the clickthrough
    $cottageID = parseString($value,"<reference>","</reference>");;
    $sleeps = parseString($value,"<sleeps>","</sleeps>");
    $bedrooms = parseString($value,"<bedrooms>","</bedrooms>");
    $bathrooms = parseString($value,"<bathrooms>","</bathrooms>");
    $town = parseString($value,"<marketing_address>","</marketing_address>");
    $changeover_day= parseString($value,"<changeover_day>","</changeover_day>");
    $pets = parseString($value,"<dogs>","</dogs>");
    if($pets == "No")
       $pets = 0;
    else
       $pets = 1;
    
    $description = strip_tags(parseString($value,"<description>","</description>"));
    $cottage_link = parseString($value,"<URL>","</URL>");

    // Get the High / Low Price
    $pricemin = parseString($value,'<min>','</min>');
    $pricemax = parseString($value,'<max>','</max>');

    // Get the geocoding
    $long = parseString($value,'<long>','</long>');
    $lat = parseString($value,'<lat>','</lat>');

    // images
    $pic = "";
    $images = parseString($value,"<images>","</images>");
    $images = substr($images,strpos("<image>",$images));
    $imageArr = explode("<image>",$images);
    unset($imageArr[0]);
    foreach($imageArr as $item){
      $pic .= str_replace("</image>","",$item.",");
    }
  
    
    $features = parseString($value,"<features>","</features>");
    $cottfeatures = "";
    $featuresArr = explode("label",$features);
    unset($featuresArr[0]);
    foreach($featuresArr as $item){
      $length = strpos($item,"id=");
      $cottfeatures .=  substr($item,2,$length).",";
      $cottfeatures = str_replace('" id',"",$cottfeatures);
    }

    $town = str_replace("<![CDATA[","",$town);
    $town = substr($town,0,strpos($town,"("));
    if(strlen($town)<1)
       $town = parseString($value,"<postal_town>","</postal_town>");

    $record = array(
      'COTTAGE_LINK'        => trim(clean_text($cottage_link)),
      'PRICE_HIGH'          => trim(clean_text($pricemax)),
      'PRICE_LOW'           => trim(clean_text($pricemin)),
      'CHANGEOVERDAY'       => trim(clean_text($changeover_day)),
      'SLEEPS'              => trim(clean_text($sleeps)),
      'BEDROOMS'            => trim(clean_text($bedrooms)),
      'BATHROOMS'           => trim(clean_text($bathrooms)),
      'PETS'                => trim(clean_text($pets)),
      'COTTAGE_REFERENCE'   => trim(clean_text($cottageID)),
      'FEATURES'            => trim(clean_text($cottfeatures)),  
      'DESCRIPTION'         => trim(clean_text($description)),
      'LOCATION_DESCRIPTON' => "N/A",
      'LONGITUDE'           => trim($long),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Town'                => trim(clean_text($town)),
      'Agent'               => "holidaycottages.co.uk",
   );
        
    if(!strpos($cottage_link,'version="1.0"')){
        scraperwiki::save(array('COTTAGE_LINK'), $record); 
    }

}


 function parseString($passage, $startStr, $endStr){
    $start = strpos($passage, $startStr)+strlen($startStr);
    $end = strpos($passage, $endStr);
    $length = $end - $start;
    $txt = substr($passage,$start,$length);
    return  clean_text($txt);
 }




?>
<?php
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

 $url = "http://www.holidaycottages.co.uk/ProductFeeds/cottagedetails.xml";
 $file = file_get_contents($url);
 $fArray = explode('<property id',$file);

 foreach($fArray as $value){
    $imagesList = "";
    // Get the cottage reference, this is used to check validity and to complete the clickthrough
    $cottageID = parseString($value,"<reference>","</reference>");;
    $sleeps = parseString($value,"<sleeps>","</sleeps>");
    $bedrooms = parseString($value,"<bedrooms>","</bedrooms>");
    $bathrooms = parseString($value,"<bathrooms>","</bathrooms>");
    $town = parseString($value,"<marketing_address>","</marketing_address>");
    $changeover_day= parseString($value,"<changeover_day>","</changeover_day>");
    $pets = parseString($value,"<dogs>","</dogs>");
    if($pets == "No")
       $pets = 0;
    else
       $pets = 1;
    
    $description = strip_tags(parseString($value,"<description>","</description>"));
    $cottage_link = parseString($value,"<URL>","</URL>");

    // Get the High / Low Price
    $pricemin = parseString($value,'<min>','</min>');
    $pricemax = parseString($value,'<max>','</max>');

    // Get the geocoding
    $long = parseString($value,'<long>','</long>');
    $lat = parseString($value,'<lat>','</lat>');

    // images
    $pic = "";
    $images = parseString($value,"<images>","</images>");
    $images = substr($images,strpos("<image>",$images));
    $imageArr = explode("<image>",$images);
    unset($imageArr[0]);
    foreach($imageArr as $item){
      $pic .= str_replace("</image>","",$item.",");
    }
  
    
    $features = parseString($value,"<features>","</features>");
    $cottfeatures = "";
    $featuresArr = explode("label",$features);
    unset($featuresArr[0]);
    foreach($featuresArr as $item){
      $length = strpos($item,"id=");
      $cottfeatures .=  substr($item,2,$length).",";
      $cottfeatures = str_replace('" id',"",$cottfeatures);
    }

    $town = str_replace("<![CDATA[","",$town);
    $town = substr($town,0,strpos($town,"("));
    if(strlen($town)<1)
       $town = parseString($value,"<postal_town>","</postal_town>");

    $record = array(
      'COTTAGE_LINK'        => trim(clean_text($cottage_link)),
      'PRICE_HIGH'          => trim(clean_text($pricemax)),
      'PRICE_LOW'           => trim(clean_text($pricemin)),
      'CHANGEOVERDAY'       => trim(clean_text($changeover_day)),
      'SLEEPS'              => trim(clean_text($sleeps)),
      'BEDROOMS'            => trim(clean_text($bedrooms)),
      'BATHROOMS'           => trim(clean_text($bathrooms)),
      'PETS'                => trim(clean_text($pets)),
      'COTTAGE_REFERENCE'   => trim(clean_text($cottageID)),
      'FEATURES'            => trim(clean_text($cottfeatures)),  
      'DESCRIPTION'         => trim(clean_text($description)),
      'LOCATION_DESCRIPTON' => "N/A",
      'LONGITUDE'           => trim($long),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pic),
      'Town'                => trim(clean_text($town)),
      'Agent'               => "holidaycottages.co.uk",
   );
        
    if(!strpos($cottage_link,'version="1.0"')){
        scraperwiki::save(array('COTTAGE_LINK'), $record); 
    }

}


 function parseString($passage, $startStr, $endStr){
    $start = strpos($passage, $startStr)+strlen($startStr);
    $end = strpos($passage, $endStr);
    $length = $end - $start;
    $txt = substr($passage,$start,$length);
    return  clean_text($txt);
 }




?>
