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

 $blacklist = array();


 $url = "http://www.sykescottages.co.uk";


 # get an array of the cottage data to scrape
 scraperwiki::attach("sykes_summary") ;
 $cottData = scraperwiki::select("COTTAGE_ID, COTTAGE_URL,PRICE_LOW from 'sykes_summary'.SWDATA order by COTTAGE_ID");

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
  $feature = "";
  $image = "";
  $imgURL = "";
  $xtraFeatures = "";
  $pictures = "";
  $location = "";
  $description = "";
  
  // Get the fields alreaady scraped from the index run
  // COTTAGE_ID, COTTAGE_URL, SLEEPS, PETS 
  $cottage_id = $value['COTTAGE_ID'];
  $cottage_url = $value['COTTAGE_URL'];
  $priceLow = $value['PRICE_LOW'];
  $changeover = "Saturday";
  $priceHigh = round($priceLow * 1.8);
  
  foreach($dom->find('span[itemprop=name]')as $data){  
    $cottageName = $data->plaintext;
  }
  
  foreach($dom->find('span[itemprop=name]')as $data){  
    $cottageName = $data->plaintext;
  }

  foreach($dom->find('div[id=propertydetailtext]')as $data){ 
    
 
    $cottageDesc = $data;
    $cottageDescArr = explode("<h2>",$cottageDesc);

    $cottageDesc = substr($cottageDescArr[1],strpos($cottageDescArr[1],"<p>"));
    $cottageDesc = str_replace("<p>","",$cottageDesc);
    $cottageDesc = str_replace("</p>","",$cottageDesc);
    
    $cottageFeatures = $cottageDescArr[2];
    $cottageFeatures = substr($cottageDescArr[2],strpos($cottageDescArr[2],"<p>"));
    $cottageFeatures = str_replace("<p>","",$cottageFeatures );
    $cottageFeatures = str_replace("</p>","",$cottageFeatures );

    $cottageFeatures2 = $cottageDescArr[3];
    $cottageFeatures2 = substr($cottageDescArr[3],strpos($cottageDescArr[3],"<p>"));
    $cottageFeatures2 = str_replace("<p>","",$cottageFeatures2 );
    $cottageFeatures2 = str_replace("</p>","",$cottageFeatures2 );
    
    $cottageFeatures = $cottageFeatures . "," .$cottageFeatures2;
    $cottageFeatures = str_replace(".",",",$cottageFeatures);
    $cottageFeatures = str_replace("inc,","inc.",$cottageFeatures);
    $cottageFeatures = str_replace("Sorry,","sorry",$cottageFeatures);

  }
    
    
  foreach($dom->find('div[id=locationtext]')as $data){  
    $locationDesc = str_replace("</li>","",$data->plaintext);
    $locationDesc = substr($data->plaintext,"13");
  }



  foreach($dom->find('div[id=centercol]') as $data){
    foreach($data->find('table')as $table){ 
     $tableArr = explode("<td",$table);


     $pets =$tableArr[4];
     $pets = str_replace('class="tablecol2">',"",$pets); 
     $pets = str_replace('</td>',"",$pets);
     if($pets == "Yes")
       $pets = 1;
     else
       $pets = 0;       

     $sleeps=$tableArr[8];
     $sleeps = str_replace('class="tablecol2">',"",$sleeps); 
     $sleeps = str_replace('</td>',"",$sleeps); 

     $bedrooms =$tableArr[14];
     $bedrooms = str_replace('class="tablecol2">',"",$bedrooms ); 
     $bedrooms = str_replace('</td>',"",$bedrooms); 

     $bathrooms = $tableArr[20];
     $bathrooms = str_replace('</td>',"",$bathrooms);
     $bathrooms = str_replace('class="tablecol2">',"",$bathrooms);

    }
  }
    
  $snippet = substr($html,strpos($html,"var prop = new L.LatLng(")+24);

  $code =  substr($snippet,0,strpos($snippet,")"));

  $lnglatArray = explode(",",$code);
  $lat = $lnglatArray[0];
  $long = $lnglatArray[1];

 


 // pictures
 # 600x450

 foreach($dom->find('div[id=propertydetailgallery]')as $data){  
   foreach($data->find('a') as $lnk){
     $picLink = str_replace("533x400","600x500",$lnk->attr['href']);
     $pictures .=  "http://www.sykescottages.co.uk".$picLink.",";
   }
 }


    /*  save the data  */
    $record = array(
      'COTTAGE_LINK'        => trim("http://www.sykescottages.co.uk".$cottage_url),
      'PRICE_HIGH'          => trim($priceHigh),
      'PRICE_LOW'           => trim($priceLow),
      'CHANGEOVERDAY'       => trim($changeover),
      'COTTAGE_NAME'        => trim($cottageName),
      'SLEEPS'              => trim($sleeps),
      'BEDROOMS'            => trim($bedrooms),
      'BATHROOMS'           => trim($bathrooms),
      'PETS'                => trim($pets),
      'COTTAGE_REFERENCE'   => trim($cottage_id),
      'FEATURES'            => trim(clean_text($cottageFeatures) ),  
      'DESCRIPTION'         => trim(clean_text($cottageDesc)),
      'LOCATION_DESCRIPTON' => trim(clean_text($locationDesc )),
      'LONGITUDE'           => trim($long),
      'LATITUDE'            => trim($lat),
      'IMAGES'              => trim($pictures),
      'Agent'               => "www.sykescottages.co.uk/",
    );
    if(strlen(trim(clean_text($cottageDesc)))!= 0)
        scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
}
?>

