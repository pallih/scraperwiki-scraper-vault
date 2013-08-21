<?php
scraperwiki::save_var('dummy', 0);

  function clean_text($txt){
     $txt= str_replace("&nbsp;"," ",$txt);
     $txt= str_replace("&eacute","e",$txt);
     $txt= str_replace("&frac12;"," and a half",$txt);
     $txt= str_replace("&frac14;"," and a quarter",$txt);
     $txt= str_replace("&pound;","£",$txt);
     $txt= str_replace(",,",",",$txt);
     $txt= str_replace("&lsquo;",'"',$txt);
     $txt= str_replace("&rsquo;",'"',$txt);
     $txt= str_replace("</p>","",$txt);
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

$blacklist = array('-dwc','-cxz','-bvp','-bnz' );


$url = "http://www.english-country-cottages.co.uk/cottages/";

scraperwiki::attach("english_country_cottages_summary") ;
# get an array of the cottage data to scrape
$cottData = scraperwiki::select("COTTAGE_URL, PRICE_HIGH,PRICE_LOW from 'english_country_cottages_summary'.SWDATA order by COTTAGE_URL");

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
    $html = scraperWiki::scrape("http://www.english-country-cottages.co.uk/cottages/".$value['COTTAGE_URL']);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";
/*  Get the Data  */

    // get Cottage name
    $element = $dom->find('title');
    $text = $element[0]->plaintext;
    $cottageName = substr($text,0, strpos($text,"("));
        
     
    // get Sleeps
    foreach($dom->find('li[class=rst_featureBoxSleepsCount]')as $data){
      $val = $data->find('span[class=fvalue]');
      $sleeps = $val[0]->plaintext;
    }
    
    // get Bedrooms
    foreach($dom->find('li[class=rst_featureBoxBedroomsCount]')as $data){
      $val = $data->find('span[class=fvalue]');
      $bedrooms = $val[0]->plaintext;
    }
    

    // get Pets
    foreach($dom->find('li[class=rst_featureBoxPetsCount]')as $data){
      $val = $data->find('span[class=fvalue]');
      $petCount= $val[0]->plaintext;
      if(intval($petCount) > 0)
        $pets = "Y";
      else
        $pets = "N";
    }
    


    // get Reference
    foreach($dom->find('span[class=pad8 padtb]')as $data){
      $val = $data->plaintext;
      $reference = str_replace("Property Reference: ","",$val);
       
    }
   
// get Features
   foreach($dom->find('div[class=propertyfeature]')as $data){
     $arr =  explode("</li>",$data);
     foreach($arr as $val){
       $feature .= substr($val,strripos($val,">")+1);
       $feature .= ",";
     }
   }


// get Description
    foreach($dom->find('div[class=propertydescriptionfull]')as $data){
      $description = str_replace("Property Description","",$data);
      # Put everything in the description into an array delimeted by <ul>
      $data = explode("<ul>",$description);
     
      # get the number of array elements
      $arraySize = count($data);
     
      # Get the main description
      $description = $data[0];
      $description = strip_tags($description);
      
      # get the extra features marked as bullet points
      for($i = 1; $i < $arraySize-1; $i++){
        $xtraFeatures .= $data[$i];       
      }
      # strip off the HTML tags
      $xtraFeatures = strip_tags($xtraFeatures);
    }

      
    // get Long / Lat
     $long_lat = substr($html,strpos($html,"latitude:"),54);

     $long_lat = str_replace("latitude:","",$long_lat);
     $long_lat = str_replace("longitude:","",$long_lat);
     $long_lat_arr = explode(",",$long_lat);
    
     if(!isset($long_lat_arr[1]))
        continue;

     if(stripos($long_lat_arr[1],'}')!== false){
        $pos = stripos($long_lat_arr[1],"}");
        $long_lat_arr[1] = substr($long_lat_arr[1],0,$pos);
     }
     $long =  $long_lat_arr[0];
     $lat =  $long_lat_arr[1];



    // get Grade
    foreach($dom->find('li[class=forange]')as $data){
     $val = $data->find('img');
     $rating = $val[0]->attr['alt'];
     $rating = str_replace("Star rating","", $rating);
    }

    // get Location
    foreach($dom->find('div[id=propertyTitle]') as $data){
       $val = $data->find('H3');
       $location = $val[0]->plaintext;
       $location = substr($location,stripos("Property",$location));
    }

    // get Images
     foreach($dom->find('ul[id=property_thumbs]') as $data){
       #    $data = $dom->find('ul[id=property_thumbs]');
       $ImgArr =  explode("<img>",$data);
       $section = $ImgArr[0];
       $dom->load($section );
       foreach($val = $dom->find('img') as $data){
         $img = $data->attr['src'];
         $imgURL .= str_replace("/95/","/400/",$img).',';
       }
     }

    /*  save the data  */
    $description  = clean_text($description );
    $feature  = clean_text($feature);
    $xtraFeatures = clean_text($xtraFeatures);

    $record = array(
      'COTTAGE_LINK'      => trim($url.$value['COTTAGE_URL']),
      'PRICE_HIGH'        => trim($value['PRICE_HIGH']),
      'PRICE_LOW'         => trim($value['PRICE_LOW']),
     # 'CHANGEOVERDAY'     => trim('Saturday'),
      'COTTAGE_NAME'      => trim($cottageName),
      'SLEEPS'            => trim($sleeps),
      'BEDROOMS'          => trim($bedrooms),
      'PETS'              => trim($pets),
      'COTTAGE_REFERENCE' => trim($reference),
      'FEATURES'          => trim($feature),
      'Extrafeatures'     => trim($xtraFeatures),
      'DESCRIPTION'       => trim($description),
      'Location'          => trim($location),
      'LONGITUDE'         => trim($long),
      'LATITUDE'          => trim($lat),
      'IMAGES'            => trim($imgURL),
      'Grade'             => trim($rating),
    );

    scraperwiki::save(array('COTTAGE_LINK'), $record);
   
}

?>