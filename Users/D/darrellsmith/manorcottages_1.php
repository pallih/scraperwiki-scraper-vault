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

 $blacklist = array("PEATS","MOOR","REEDS","START");


 $url = "http://www.manorcottages.co.uk/properties/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("manorcottages_index") ;
 $cottData = scraperwiki::select("COTTAGE_ID, BATHROOMS, PRICE_LOW,COTTAGE_URL, PETS, COTTAGE_NAME, CHANGEOVER from 'manorcottages_index'.SWDATA order by COTTAGE_ID");

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
    $html = scraperWiki::scrape($value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";
    $pictures = "";
    $location = "";
    $description = "";

    $price_low = $value['PRICE_LOW'];
/*  Get the Data  */
    $features = "|";
    // get Features
    foreach($dom->find('ul[class=features]')as $data){    
      foreach($data->find('li[class=property_attribute]')as $feature){    
        $features .= $feature->plaintext."|";
      }

    // Bedrooms

    // get property summary
    $items = "";
    foreach($dom->find('ul[class=property_summary]')as $data){    
      foreach($data->find('li')as $summary){
        $item = $summary->find('span');
        $items .= $item[0]->plaintext."|";
      }
    }
    $itemArr = explode("|",$items);

    $sleeps = substr($itemArr[1],0,strpos($itemArr[1],"(")-1);
    $bedrooms = $itemArr[2];

    foreach($dom->find('div[class=description tall]') as $data){
      foreach($data->find('p') as $para){
        $description .= $para->plaintext;
      }
    }

    foreach($dom->find("ul[class=thumbs]") as $data){
       foreach($data->find('li') as $img){
        foreach($img->find('a') as $lnk){
            $picLink = str_replace("500x400/","",$lnk->attr['href']);
            $pictures .=  "http://www.manorcottages.co.uk".$picLink.",";
        }
       }    
    }


    foreach($dom->find('div[class=description local]') as $data){
      $location = $data->plaintext;
    }


    // long / lat

    $element = $dom->find('span[class=coords]');
    $lat = $element[0]->attr['lat'];
    $long = $element[0]->attr['lng'];
    $price_high = $price_low * 1.55;


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($price_high),
      'PRICE_LOW'         => trim($price_low),
      'CHANGEOVERDAY'     => trim($value['CHANGEOVER']),
      'COTTAGE_NAME'      => trim($value['COTTAGE_NAME']),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($value['BATHROOMS']),
      'PETS'              => trim($value['PETS']),
      'COTTAGE_REFERENCE' => trim($value['COTTAGE_ID']),
      'FEATURES'          => trim($features),  
    # 'Summary'           => trim($summary),
      'DESCRIPTION'       => trim(clean_text($description)),
      'Location'          => trim(clean_text($location)),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($pictures),
      'Agent'             => "manorcottages.co.uk",
    );
    if(strlen(trim(clean_text($description)))!= 0)
        scraperwiki::save(array('COTTAGE_LINK'), $record);


}
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

 $blacklist = array("PEATS","MOOR","REEDS","START");


 $url = "http://www.manorcottages.co.uk/properties/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("manorcottages_index") ;
 $cottData = scraperwiki::select("COTTAGE_ID, BATHROOMS, PRICE_LOW,COTTAGE_URL, PETS, COTTAGE_NAME, CHANGEOVER from 'manorcottages_index'.SWDATA order by COTTAGE_ID");

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
    $html = scraperWiki::scrape($value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";
    $pictures = "";
    $location = "";
    $description = "";

    $price_low = $value['PRICE_LOW'];
/*  Get the Data  */
    $features = "|";
    // get Features
    foreach($dom->find('ul[class=features]')as $data){    
      foreach($data->find('li[class=property_attribute]')as $feature){    
        $features .= $feature->plaintext."|";
      }

    // Bedrooms

    // get property summary
    $items = "";
    foreach($dom->find('ul[class=property_summary]')as $data){    
      foreach($data->find('li')as $summary){
        $item = $summary->find('span');
        $items .= $item[0]->plaintext."|";
      }
    }
    $itemArr = explode("|",$items);

    $sleeps = substr($itemArr[1],0,strpos($itemArr[1],"(")-1);
    $bedrooms = $itemArr[2];

    foreach($dom->find('div[class=description tall]') as $data){
      foreach($data->find('p') as $para){
        $description .= $para->plaintext;
      }
    }

    foreach($dom->find("ul[class=thumbs]") as $data){
       foreach($data->find('li') as $img){
        foreach($img->find('a') as $lnk){
            $picLink = str_replace("500x400/","",$lnk->attr['href']);
            $pictures .=  "http://www.manorcottages.co.uk".$picLink.",";
        }
       }    
    }


    foreach($dom->find('div[class=description local]') as $data){
      $location = $data->plaintext;
    }


    // long / lat

    $element = $dom->find('span[class=coords]');
    $lat = $element[0]->attr['lat'];
    $long = $element[0]->attr['lng'];
    $price_high = $price_low * 1.55;


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($price_high),
      'PRICE_LOW'         => trim($price_low),
      'CHANGEOVERDAY'     => trim($value['CHANGEOVER']),
      'COTTAGE_NAME'      => trim($value['COTTAGE_NAME']),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($value['BATHROOMS']),
      'PETS'              => trim($value['PETS']),
      'COTTAGE_REFERENCE' => trim($value['COTTAGE_ID']),
      'FEATURES'          => trim($features),  
    # 'Summary'           => trim($summary),
      'DESCRIPTION'       => trim(clean_text($description)),
      'Location'          => trim(clean_text($location)),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($pictures),
      'Agent'             => "manorcottages.co.uk",
    );
    if(strlen(trim(clean_text($description)))!= 0)
        scraperwiki::save(array('COTTAGE_LINK'), $record);


}
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

 $blacklist = array("PEATS","MOOR","REEDS","START");


 $url = "http://www.manorcottages.co.uk/properties/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("manorcottages_index") ;
 $cottData = scraperwiki::select("COTTAGE_ID, BATHROOMS, PRICE_LOW,COTTAGE_URL, PETS, COTTAGE_NAME, CHANGEOVER from 'manorcottages_index'.SWDATA order by COTTAGE_ID");

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
    $html = scraperWiki::scrape($value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";
    $pictures = "";
    $location = "";
    $description = "";

    $price_low = $value['PRICE_LOW'];
/*  Get the Data  */
    $features = "|";
    // get Features
    foreach($dom->find('ul[class=features]')as $data){    
      foreach($data->find('li[class=property_attribute]')as $feature){    
        $features .= $feature->plaintext."|";
      }

    // Bedrooms

    // get property summary
    $items = "";
    foreach($dom->find('ul[class=property_summary]')as $data){    
      foreach($data->find('li')as $summary){
        $item = $summary->find('span');
        $items .= $item[0]->plaintext."|";
      }
    }
    $itemArr = explode("|",$items);

    $sleeps = substr($itemArr[1],0,strpos($itemArr[1],"(")-1);
    $bedrooms = $itemArr[2];

    foreach($dom->find('div[class=description tall]') as $data){
      foreach($data->find('p') as $para){
        $description .= $para->plaintext;
      }
    }

    foreach($dom->find("ul[class=thumbs]") as $data){
       foreach($data->find('li') as $img){
        foreach($img->find('a') as $lnk){
            $picLink = str_replace("500x400/","",$lnk->attr['href']);
            $pictures .=  "http://www.manorcottages.co.uk".$picLink.",";
        }
       }    
    }


    foreach($dom->find('div[class=description local]') as $data){
      $location = $data->plaintext;
    }


    // long / lat

    $element = $dom->find('span[class=coords]');
    $lat = $element[0]->attr['lat'];
    $long = $element[0]->attr['lng'];
    $price_high = $price_low * 1.55;


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($price_high),
      'PRICE_LOW'         => trim($price_low),
      'CHANGEOVERDAY'     => trim($value['CHANGEOVER']),
      'COTTAGE_NAME'      => trim($value['COTTAGE_NAME']),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($value['BATHROOMS']),
      'PETS'              => trim($value['PETS']),
      'COTTAGE_REFERENCE' => trim($value['COTTAGE_ID']),
      'FEATURES'          => trim($features),  
    # 'Summary'           => trim($summary),
      'DESCRIPTION'       => trim(clean_text($description)),
      'Location'          => trim(clean_text($location)),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($pictures),
      'Agent'             => "manorcottages.co.uk",
    );
    if(strlen(trim(clean_text($description)))!= 0)
        scraperwiki::save(array('COTTAGE_LINK'), $record);


}
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

 $blacklist = array("PEATS","MOOR","REEDS","START");


 $url = "http://www.manorcottages.co.uk/properties/";


 # get an array of the cottage data to scrape
 scraperwiki::attach("manorcottages_index") ;
 $cottData = scraperwiki::select("COTTAGE_ID, BATHROOMS, PRICE_LOW,COTTAGE_URL, PETS, COTTAGE_NAME, CHANGEOVER from 'manorcottages_index'.SWDATA order by COTTAGE_ID");

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
    $html = scraperWiki::scrape($value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";
    $pictures = "";
    $location = "";
    $description = "";

    $price_low = $value['PRICE_LOW'];
/*  Get the Data  */
    $features = "|";
    // get Features
    foreach($dom->find('ul[class=features]')as $data){    
      foreach($data->find('li[class=property_attribute]')as $feature){    
        $features .= $feature->plaintext."|";
      }

    // Bedrooms

    // get property summary
    $items = "";
    foreach($dom->find('ul[class=property_summary]')as $data){    
      foreach($data->find('li')as $summary){
        $item = $summary->find('span');
        $items .= $item[0]->plaintext."|";
      }
    }
    $itemArr = explode("|",$items);

    $sleeps = substr($itemArr[1],0,strpos($itemArr[1],"(")-1);
    $bedrooms = $itemArr[2];

    foreach($dom->find('div[class=description tall]') as $data){
      foreach($data->find('p') as $para){
        $description .= $para->plaintext;
      }
    }

    foreach($dom->find("ul[class=thumbs]") as $data){
       foreach($data->find('li') as $img){
        foreach($img->find('a') as $lnk){
            $picLink = str_replace("500x400/","",$lnk->attr['href']);
            $pictures .=  "http://www.manorcottages.co.uk".$picLink.",";
        }
       }    
    }


    foreach($dom->find('div[class=description local]') as $data){
      $location = $data->plaintext;
    }


    // long / lat

    $element = $dom->find('span[class=coords]');
    $lat = $element[0]->attr['lat'];
    $long = $element[0]->attr['lng'];
    $price_high = $price_low * 1.55;


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'      => trim($value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($price_high),
      'PRICE_LOW'         => trim($price_low),
      'CHANGEOVERDAY'     => trim($value['CHANGEOVER']),
      'COTTAGE_NAME'      => trim($value['COTTAGE_NAME']),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'BATHROOMS'         => trim($value['BATHROOMS']),
      'PETS'              => trim($value['PETS']),
      'COTTAGE_REFERENCE' => trim($value['COTTAGE_ID']),
      'FEATURES'          => trim($features),  
    # 'Summary'           => trim($summary),
      'DESCRIPTION'       => trim(clean_text($description)),
      'Location'          => trim(clean_text($location)),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($pictures),
      'Agent'             => "manorcottages.co.uk",
    );
    if(strlen(trim(clean_text($description)))!= 0)
        scraperwiki::save(array('COTTAGE_LINK'), $record);


}
}
?>
