<?php
 $url = "http://mackays-self-catering.co.uk/xml/feed.php";
 $file = file_get_contents($url);
 $fArray = explode('<object request="update">',$file);
   
 foreach($fArray as $key => $value){
    $imagesList = "";
    // Get the cottage reference, this is used to check validity and to complete the clickthrough
    $ref = parseString($value,"<agentobjRef>","</agentobjRef>");
    
    // Get the High / Low Price
    $priceAll = parseString($value,'<seasons currency="GBP">','</seasons>');
    $priceArr = explode('price',$priceAll);
    $sortedArray = array();

    foreach($priceArr as $price_value){
      $price_value = substr($price_value,2,strpos($price_value,'till')); 
      $price_value = str_replace('" ti','',$price_value);
      array_push($sortedArray,$price_value);
    }
    rsort($sortedArray);

    // sort the prices to get high/low
    $high = $sortedArray[0];
    $low = $sortedArray[sizeof($sortedArray)-2];

    // Get the images
    $images = parseString($value,"<pictures>","</pictures>");
    $imagesList = str_replace('<picture type="1" label="" url="','',$images);
    $outside_img = substr($imagesList,0,strpos($imagesList,"/>" )); 
    $outside_img = str_replace('"',"",$outside_img);
    $imagesList = str_replace('<picture type="2" label="" url="','',$imagesList );    
    $imagesList = str_replace('" />',',',$imagesList );
    // remove the first entry as it will be a duplicate
    #  $imagesList = substr($imagesList,strpos($imagesList,',')+1); 
    $CimagesList = str_replace(trim($outside_img),"",$imagesList);
    $CimagesList = str_replace(', ','',$CimagesList);    


    $imagesList =  $outside_img.$CimagesList;
    echo  $imagesList ;

    $record = array(
      'PICTURES' =>$CimagesList,
      'PRICE_HIGH' => $high,
      'PRICE_LOW' => $low,
      'NAME' => parseString($value,"<title>","</title>"),
      'COTTAGE_REF' => $ref,
      "CLICKTHROUGH" => "http://www.mackays-self-catering.co.uk/s/process.php?r=".$ref,
      "LAT" => parseString($value,"<latitude>","</latitude>"),
      "LONG" => parseString($value,"<longitude>","</longitude>"),
      "SLEEPS" => parseString($value,"<beds>","</beds>"),
      "BEDS" => parseString($value,"<rooms>","</rooms>"),
      "BATHS" => parseString($value,"<bathroom>","</bathroom>"),
      "DESC"  => parseString($value,'<description language="EN">','</description>'), 
      "PETS"  => parseString($value,"<pets>","</pets>"),
      "CHANGEOVER" => "Saturday",
    ); 
    // check for any unwanted data in the cottage reference and skip if any is found
    if(strpos($ref,'encoding="utf-8')===false)
        scraperwiki::save(array('COTTAGE_REF'), $record); 
}

 function parseString($passage, $startStr, $endStr){
    $start = strpos($passage, $startStr)+strlen($startStr);
    $end = strpos($passage, $endStr);
    $length = $end - $start;
    $txt = substr($passage,$start,$length);
    return  clean_text($txt);
 }


 function clean_text($txt){
    $txt = str_replace("\n"," ",$txt);
    $txt = str_replace("\r"," ",$txt);
    $txt = str_replace("&nbsp;"," ",$txt);
    $txt = str_replace("\t"," ",$txt);
    $txt = str_replace("&eacute","e",$txt);
    $txt = str_replace("&frac12;"," and a half",$txt);
    $txt = str_replace("&frac14;"," and a quarter",$txt);
    $txt = str_replace("&pound;","£",$txt);
    $txt = str_replace(",,",",",$txt);
    $txt = str_replace("&lsquo;",'"',$txt);
    $txt = str_replace("&rsquo;",'"',$txt);
    $txt = str_replace("</p>","",$txt);
    $txt = str_replace("<![CDATA[","",$txt);
    $txt = str_replace("]]>","",$txt);
    $txt = preg_replace('/\s+/', ' ',$txt);
    return trim($txt);
 }

?>
<?php
 $url = "http://mackays-self-catering.co.uk/xml/feed.php";
 $file = file_get_contents($url);
 $fArray = explode('<object request="update">',$file);
   
 foreach($fArray as $key => $value){
    $imagesList = "";
    // Get the cottage reference, this is used to check validity and to complete the clickthrough
    $ref = parseString($value,"<agentobjRef>","</agentobjRef>");
    
    // Get the High / Low Price
    $priceAll = parseString($value,'<seasons currency="GBP">','</seasons>');
    $priceArr = explode('price',$priceAll);
    $sortedArray = array();

    foreach($priceArr as $price_value){
      $price_value = substr($price_value,2,strpos($price_value,'till')); 
      $price_value = str_replace('" ti','',$price_value);
      array_push($sortedArray,$price_value);
    }
    rsort($sortedArray);

    // sort the prices to get high/low
    $high = $sortedArray[0];
    $low = $sortedArray[sizeof($sortedArray)-2];

    // Get the images
    $images = parseString($value,"<pictures>","</pictures>");
    $imagesList = str_replace('<picture type="1" label="" url="','',$images);
    $outside_img = substr($imagesList,0,strpos($imagesList,"/>" )); 
    $outside_img = str_replace('"',"",$outside_img);
    $imagesList = str_replace('<picture type="2" label="" url="','',$imagesList );    
    $imagesList = str_replace('" />',',',$imagesList );
    // remove the first entry as it will be a duplicate
    #  $imagesList = substr($imagesList,strpos($imagesList,',')+1); 
    $CimagesList = str_replace(trim($outside_img),"",$imagesList);
    $CimagesList = str_replace(', ','',$CimagesList);    


    $imagesList =  $outside_img.$CimagesList;
    echo  $imagesList ;

    $record = array(
      'PICTURES' =>$CimagesList,
      'PRICE_HIGH' => $high,
      'PRICE_LOW' => $low,
      'NAME' => parseString($value,"<title>","</title>"),
      'COTTAGE_REF' => $ref,
      "CLICKTHROUGH" => "http://www.mackays-self-catering.co.uk/s/process.php?r=".$ref,
      "LAT" => parseString($value,"<latitude>","</latitude>"),
      "LONG" => parseString($value,"<longitude>","</longitude>"),
      "SLEEPS" => parseString($value,"<beds>","</beds>"),
      "BEDS" => parseString($value,"<rooms>","</rooms>"),
      "BATHS" => parseString($value,"<bathroom>","</bathroom>"),
      "DESC"  => parseString($value,'<description language="EN">','</description>'), 
      "PETS"  => parseString($value,"<pets>","</pets>"),
      "CHANGEOVER" => "Saturday",
    ); 
    // check for any unwanted data in the cottage reference and skip if any is found
    if(strpos($ref,'encoding="utf-8')===false)
        scraperwiki::save(array('COTTAGE_REF'), $record); 
}

 function parseString($passage, $startStr, $endStr){
    $start = strpos($passage, $startStr)+strlen($startStr);
    $end = strpos($passage, $endStr);
    $length = $end - $start;
    $txt = substr($passage,$start,$length);
    return  clean_text($txt);
 }


 function clean_text($txt){
    $txt = str_replace("\n"," ",$txt);
    $txt = str_replace("\r"," ",$txt);
    $txt = str_replace("&nbsp;"," ",$txt);
    $txt = str_replace("\t"," ",$txt);
    $txt = str_replace("&eacute","e",$txt);
    $txt = str_replace("&frac12;"," and a half",$txt);
    $txt = str_replace("&frac14;"," and a quarter",$txt);
    $txt = str_replace("&pound;","£",$txt);
    $txt = str_replace(",,",",",$txt);
    $txt = str_replace("&lsquo;",'"',$txt);
    $txt = str_replace("&rsquo;",'"',$txt);
    $txt = str_replace("</p>","",$txt);
    $txt = str_replace("<![CDATA[","",$txt);
    $txt = str_replace("]]>","",$txt);
    $txt = preg_replace('/\s+/', ' ',$txt);
    return trim($txt);
 }

?>
<?php
 $url = "http://mackays-self-catering.co.uk/xml/feed.php";
 $file = file_get_contents($url);
 $fArray = explode('<object request="update">',$file);
   
 foreach($fArray as $key => $value){
    $imagesList = "";
    // Get the cottage reference, this is used to check validity and to complete the clickthrough
    $ref = parseString($value,"<agentobjRef>","</agentobjRef>");
    
    // Get the High / Low Price
    $priceAll = parseString($value,'<seasons currency="GBP">','</seasons>');
    $priceArr = explode('price',$priceAll);
    $sortedArray = array();

    foreach($priceArr as $price_value){
      $price_value = substr($price_value,2,strpos($price_value,'till')); 
      $price_value = str_replace('" ti','',$price_value);
      array_push($sortedArray,$price_value);
    }
    rsort($sortedArray);

    // sort the prices to get high/low
    $high = $sortedArray[0];
    $low = $sortedArray[sizeof($sortedArray)-2];

    // Get the images
    $images = parseString($value,"<pictures>","</pictures>");
    $imagesList = str_replace('<picture type="1" label="" url="','',$images);
    $outside_img = substr($imagesList,0,strpos($imagesList,"/>" )); 
    $outside_img = str_replace('"',"",$outside_img);
    $imagesList = str_replace('<picture type="2" label="" url="','',$imagesList );    
    $imagesList = str_replace('" />',',',$imagesList );
    // remove the first entry as it will be a duplicate
    #  $imagesList = substr($imagesList,strpos($imagesList,',')+1); 
    $CimagesList = str_replace(trim($outside_img),"",$imagesList);
    $CimagesList = str_replace(', ','',$CimagesList);    


    $imagesList =  $outside_img.$CimagesList;
    echo  $imagesList ;

    $record = array(
      'PICTURES' =>$CimagesList,
      'PRICE_HIGH' => $high,
      'PRICE_LOW' => $low,
      'NAME' => parseString($value,"<title>","</title>"),
      'COTTAGE_REF' => $ref,
      "CLICKTHROUGH" => "http://www.mackays-self-catering.co.uk/s/process.php?r=".$ref,
      "LAT" => parseString($value,"<latitude>","</latitude>"),
      "LONG" => parseString($value,"<longitude>","</longitude>"),
      "SLEEPS" => parseString($value,"<beds>","</beds>"),
      "BEDS" => parseString($value,"<rooms>","</rooms>"),
      "BATHS" => parseString($value,"<bathroom>","</bathroom>"),
      "DESC"  => parseString($value,'<description language="EN">','</description>'), 
      "PETS"  => parseString($value,"<pets>","</pets>"),
      "CHANGEOVER" => "Saturday",
    ); 
    // check for any unwanted data in the cottage reference and skip if any is found
    if(strpos($ref,'encoding="utf-8')===false)
        scraperwiki::save(array('COTTAGE_REF'), $record); 
}

 function parseString($passage, $startStr, $endStr){
    $start = strpos($passage, $startStr)+strlen($startStr);
    $end = strpos($passage, $endStr);
    $length = $end - $start;
    $txt = substr($passage,$start,$length);
    return  clean_text($txt);
 }


 function clean_text($txt){
    $txt = str_replace("\n"," ",$txt);
    $txt = str_replace("\r"," ",$txt);
    $txt = str_replace("&nbsp;"," ",$txt);
    $txt = str_replace("\t"," ",$txt);
    $txt = str_replace("&eacute","e",$txt);
    $txt = str_replace("&frac12;"," and a half",$txt);
    $txt = str_replace("&frac14;"," and a quarter",$txt);
    $txt = str_replace("&pound;","£",$txt);
    $txt = str_replace(",,",",",$txt);
    $txt = str_replace("&lsquo;",'"',$txt);
    $txt = str_replace("&rsquo;",'"',$txt);
    $txt = str_replace("</p>","",$txt);
    $txt = str_replace("<![CDATA[","",$txt);
    $txt = str_replace("]]>","",$txt);
    $txt = preg_replace('/\s+/', ' ',$txt);
    return trim($txt);
 }

?>
