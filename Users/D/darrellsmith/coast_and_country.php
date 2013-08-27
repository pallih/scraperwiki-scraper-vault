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
    $txt= str_replace("&pound;","£",$txt);
    $txt= str_replace(",,",",",$txt);
    $txt= str_replace("&lsquo;",'"',$txt);
    $txt= str_replace("&rsquo;",'"',$txt);
    $txt= str_replace("</p>","",$txt);
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

 $blacklist = array( );
 
 $url = "http://www.coastandcountry.co.uk/cottage-details/";

 scraperwiki::attach("coastandcountrycouk") ;
 # get an array of the cottage data to scrape
 $cottData = scraperwiki::select("COTTAGE_URL, PRICE_HIGH, PRICE_LOW from 'coastandcountrycouk'.SWDATA order by COTTAGE_URL");

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
      if($value['COTTAGE_URL'] == $blItem)
        continue 2;
    }

    //load the page into the scraper
    $html = scraperWiki::scrape($url.$value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";


/*  Get the Data  */

    // get Cottage name
    $element = $dom->find('title');
    $text = $element[0]->plaintext;
    $cottageName = substr($text,0, strpos($text,"-"));
    $features = "";

    // get Pets and changeover
    foreach($dom->find('div[id=property-ataglance-box]')as $data){    
      $btds = $data->find("li");
      // changeover
      $changeover = str_replace("Changeover Day","",$btds[0]->plaintext);
      
      if(strpos($btds[1],"/tick.gif"))
       $pets = "Y";
      else
       $pets = "N";

     if(strpos($btds[2],"/tick.gif"))
        $features .= $btds[2]->plaintext."|";
     if(strpos($btds[3],"/tick.gif"))
        $features .= $btds[3]->plaintext."|";
     if(strpos($btds[4],"/tick.gif"))
        $features .= $btds[4]->plaintext."|";
     if(strpos($btds[5],"/tick.gif"))
        $features .= $btds[5]->plaintext."|";
     if(strpos($btds[6],"/tick.gif"))
        $features .= $btds[6]->plaintext."|";
     if(strpos($btds[7],"/tick.gif"))
        $features .= $btds[7]->plaintext."|";
     if(strpos($btds[8],"/tick.gif"))
        $features .= $btds[8]->plaintext."|";
     if(strpos($btds[9],"/tick.gif"))
        $features .= $btds[9]->plaintext."|";
     if(strpos($btds[10],"/tick.gif"))
        $features .= $btds[10]->plaintext."|";
     if(strpos($btds[11],"/tick.gif"))
        $features .= $btds[11]->plaintext."|";
     if(strpos($btds[12],"/tick.gif"))
        $features .= $btds[12]->plaintext."|";

    }


    // get Description
    foreach($dom->find('div[id=property-description]')as $data){
      $desc = $data->plaintext;
      $description = trim(clean_text($desc));
    }
    
    
    // get Summary
    foreach($dom->find('div[id=property-summary]')as $data){
      $sum = $data->plaintext;
      $summary = trim(clean_text($sum));
    }
    
    
    // get features
    foreach($dom->find('div[class=features]')as $data){
      $items = explode("&nbsp;",$data->plaintext);
      $sleeps = str_replace("Sleeps: ","",$items[0]);
      $bedrooms = str_replace("Bedrooms: ","",$items[1]);
      $bathrooms = str_replace("Bathrooms: ","",$items[2]);
    }
    
    
    // get Reference
    $reference = $value['COTTAGE_URL'];
    
    
    // get Long / Lat
    foreach($dom->find('input[id=lat]')as $data){
      $link = $data->value;
      $lat  =  trim($link);

    }
    foreach($dom->find('input[id=long]')as $data){
      $link = $data->value;
      $long  =  trim($link);
    }
   

    // get Location
    foreach($dom->find('div[id=property-heading]') as $data){
       $val = $data->find('span');
       $location = $val[0]->plaintext;
    }

    // get Images
    foreach($dom->find('div[class=property-thumbnail-images clearfix]') as $data){
      foreach($data->find('a')as $item){
        $link = $item->href;
        $imgURL   .=  "http://www.coastandcountry.co.uk".trim($link).",";
      }
       
    }


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($url.$value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($value['PRICE_HIGH']),
      'PRICE_LOW'         => trim($value['PRICE_LOW']),
      'CHANGEOVERDAY'     => trim($changeover),
      'COTTAGE_NAME'      => trim($cottageName),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($bathrooms),
      'PETS'              => trim($pets),
      'COTTAGE_REFERENCE' => trim($reference),
      'FEATURES'          => trim($features),  
      'Summary'           => trim($summary),
      'DESCRIPTION'       => trim($description),
      'Location'          => trim($location),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($imgURL),
      'Agent'             => "coastandcountry.co.uk",

    );

    scraperwiki::save(array('COTTAGE_LINK'), $record);
   
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
    $txt= str_replace("&pound;","£",$txt);
    $txt= str_replace(",,",",",$txt);
    $txt= str_replace("&lsquo;",'"',$txt);
    $txt= str_replace("&rsquo;",'"',$txt);
    $txt= str_replace("</p>","",$txt);
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

 $blacklist = array( );
 
 $url = "http://www.coastandcountry.co.uk/cottage-details/";

 scraperwiki::attach("coastandcountrycouk") ;
 # get an array of the cottage data to scrape
 $cottData = scraperwiki::select("COTTAGE_URL, PRICE_HIGH, PRICE_LOW from 'coastandcountrycouk'.SWDATA order by COTTAGE_URL");

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
      if($value['COTTAGE_URL'] == $blItem)
        continue 2;
    }

    //load the page into the scraper
    $html = scraperWiki::scrape($url.$value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";


/*  Get the Data  */

    // get Cottage name
    $element = $dom->find('title');
    $text = $element[0]->plaintext;
    $cottageName = substr($text,0, strpos($text,"-"));
    $features = "";

    // get Pets and changeover
    foreach($dom->find('div[id=property-ataglance-box]')as $data){    
      $btds = $data->find("li");
      // changeover
      $changeover = str_replace("Changeover Day","",$btds[0]->plaintext);
      
      if(strpos($btds[1],"/tick.gif"))
       $pets = "Y";
      else
       $pets = "N";

     if(strpos($btds[2],"/tick.gif"))
        $features .= $btds[2]->plaintext."|";
     if(strpos($btds[3],"/tick.gif"))
        $features .= $btds[3]->plaintext."|";
     if(strpos($btds[4],"/tick.gif"))
        $features .= $btds[4]->plaintext."|";
     if(strpos($btds[5],"/tick.gif"))
        $features .= $btds[5]->plaintext."|";
     if(strpos($btds[6],"/tick.gif"))
        $features .= $btds[6]->plaintext."|";
     if(strpos($btds[7],"/tick.gif"))
        $features .= $btds[7]->plaintext."|";
     if(strpos($btds[8],"/tick.gif"))
        $features .= $btds[8]->plaintext."|";
     if(strpos($btds[9],"/tick.gif"))
        $features .= $btds[9]->plaintext."|";
     if(strpos($btds[10],"/tick.gif"))
        $features .= $btds[10]->plaintext."|";
     if(strpos($btds[11],"/tick.gif"))
        $features .= $btds[11]->plaintext."|";
     if(strpos($btds[12],"/tick.gif"))
        $features .= $btds[12]->plaintext."|";

    }


    // get Description
    foreach($dom->find('div[id=property-description]')as $data){
      $desc = $data->plaintext;
      $description = trim(clean_text($desc));
    }
    
    
    // get Summary
    foreach($dom->find('div[id=property-summary]')as $data){
      $sum = $data->plaintext;
      $summary = trim(clean_text($sum));
    }
    
    
    // get features
    foreach($dom->find('div[class=features]')as $data){
      $items = explode("&nbsp;",$data->plaintext);
      $sleeps = str_replace("Sleeps: ","",$items[0]);
      $bedrooms = str_replace("Bedrooms: ","",$items[1]);
      $bathrooms = str_replace("Bathrooms: ","",$items[2]);
    }
    
    
    // get Reference
    $reference = $value['COTTAGE_URL'];
    
    
    // get Long / Lat
    foreach($dom->find('input[id=lat]')as $data){
      $link = $data->value;
      $lat  =  trim($link);

    }
    foreach($dom->find('input[id=long]')as $data){
      $link = $data->value;
      $long  =  trim($link);
    }
   

    // get Location
    foreach($dom->find('div[id=property-heading]') as $data){
       $val = $data->find('span');
       $location = $val[0]->plaintext;
    }

    // get Images
    foreach($dom->find('div[class=property-thumbnail-images clearfix]') as $data){
      foreach($data->find('a')as $item){
        $link = $item->href;
        $imgURL   .=  "http://www.coastandcountry.co.uk".trim($link).",";
      }
       
    }


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($url.$value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($value['PRICE_HIGH']),
      'PRICE_LOW'         => trim($value['PRICE_LOW']),
      'CHANGEOVERDAY'     => trim($changeover),
      'COTTAGE_NAME'      => trim($cottageName),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($bathrooms),
      'PETS'              => trim($pets),
      'COTTAGE_REFERENCE' => trim($reference),
      'FEATURES'          => trim($features),  
      'Summary'           => trim($summary),
      'DESCRIPTION'       => trim($description),
      'Location'          => trim($location),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($imgURL),
      'Agent'             => "coastandcountry.co.uk",

    );

    scraperwiki::save(array('COTTAGE_LINK'), $record);
   
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
    $txt= str_replace("&pound;","£",$txt);
    $txt= str_replace(",,",",",$txt);
    $txt= str_replace("&lsquo;",'"',$txt);
    $txt= str_replace("&rsquo;",'"',$txt);
    $txt= str_replace("</p>","",$txt);
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

 $blacklist = array( );
 
 $url = "http://www.coastandcountry.co.uk/cottage-details/";

 scraperwiki::attach("coastandcountrycouk") ;
 # get an array of the cottage data to scrape
 $cottData = scraperwiki::select("COTTAGE_URL, PRICE_HIGH, PRICE_LOW from 'coastandcountrycouk'.SWDATA order by COTTAGE_URL");

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
      if($value['COTTAGE_URL'] == $blItem)
        continue 2;
    }

    //load the page into the scraper
    $html = scraperWiki::scrape($url.$value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";


/*  Get the Data  */

    // get Cottage name
    $element = $dom->find('title');
    $text = $element[0]->plaintext;
    $cottageName = substr($text,0, strpos($text,"-"));
    $features = "";

    // get Pets and changeover
    foreach($dom->find('div[id=property-ataglance-box]')as $data){    
      $btds = $data->find("li");
      // changeover
      $changeover = str_replace("Changeover Day","",$btds[0]->plaintext);
      
      if(strpos($btds[1],"/tick.gif"))
       $pets = "Y";
      else
       $pets = "N";

     if(strpos($btds[2],"/tick.gif"))
        $features .= $btds[2]->plaintext."|";
     if(strpos($btds[3],"/tick.gif"))
        $features .= $btds[3]->plaintext."|";
     if(strpos($btds[4],"/tick.gif"))
        $features .= $btds[4]->plaintext."|";
     if(strpos($btds[5],"/tick.gif"))
        $features .= $btds[5]->plaintext."|";
     if(strpos($btds[6],"/tick.gif"))
        $features .= $btds[6]->plaintext."|";
     if(strpos($btds[7],"/tick.gif"))
        $features .= $btds[7]->plaintext."|";
     if(strpos($btds[8],"/tick.gif"))
        $features .= $btds[8]->plaintext."|";
     if(strpos($btds[9],"/tick.gif"))
        $features .= $btds[9]->plaintext."|";
     if(strpos($btds[10],"/tick.gif"))
        $features .= $btds[10]->plaintext."|";
     if(strpos($btds[11],"/tick.gif"))
        $features .= $btds[11]->plaintext."|";
     if(strpos($btds[12],"/tick.gif"))
        $features .= $btds[12]->plaintext."|";

    }


    // get Description
    foreach($dom->find('div[id=property-description]')as $data){
      $desc = $data->plaintext;
      $description = trim(clean_text($desc));
    }
    
    
    // get Summary
    foreach($dom->find('div[id=property-summary]')as $data){
      $sum = $data->plaintext;
      $summary = trim(clean_text($sum));
    }
    
    
    // get features
    foreach($dom->find('div[class=features]')as $data){
      $items = explode("&nbsp;",$data->plaintext);
      $sleeps = str_replace("Sleeps: ","",$items[0]);
      $bedrooms = str_replace("Bedrooms: ","",$items[1]);
      $bathrooms = str_replace("Bathrooms: ","",$items[2]);
    }
    
    
    // get Reference
    $reference = $value['COTTAGE_URL'];
    
    
    // get Long / Lat
    foreach($dom->find('input[id=lat]')as $data){
      $link = $data->value;
      $lat  =  trim($link);

    }
    foreach($dom->find('input[id=long]')as $data){
      $link = $data->value;
      $long  =  trim($link);
    }
   

    // get Location
    foreach($dom->find('div[id=property-heading]') as $data){
       $val = $data->find('span');
       $location = $val[0]->plaintext;
    }

    // get Images
    foreach($dom->find('div[class=property-thumbnail-images clearfix]') as $data){
      foreach($data->find('a')as $item){
        $link = $item->href;
        $imgURL   .=  "http://www.coastandcountry.co.uk".trim($link).",";
      }
       
    }


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($url.$value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($value['PRICE_HIGH']),
      'PRICE_LOW'         => trim($value['PRICE_LOW']),
      'CHANGEOVERDAY'     => trim($changeover),
      'COTTAGE_NAME'      => trim($cottageName),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($bathrooms),
      'PETS'              => trim($pets),
      'COTTAGE_REFERENCE' => trim($reference),
      'FEATURES'          => trim($features),  
      'Summary'           => trim($summary),
      'DESCRIPTION'       => trim($description),
      'Location'          => trim($location),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($imgURL),
      'Agent'             => "coastandcountry.co.uk",

    );

    scraperwiki::save(array('COTTAGE_LINK'), $record);
   
}

?>
