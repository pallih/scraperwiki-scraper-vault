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
 scraperwiki::attach("marsdens_summary") ;
 $cottData = scraperwiki::select(" COTTAGE_ID, COTTAGE_URL, SLEEPS, BEDROOMS, PETS,COTTAGE_NAME, PRICE_LOW from 'marsdens_summary'.SWDATA order by COTTAGE_URL");

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
  $cottage_url   = $value['COTTAGE_URL'];
  $cottage_name  = $value['COTTAGE_NAME'];  
  $cottage_id    = $value['COTTAGE_ID'];
  $sleeps        = $value['SLEEPS'];
  $bedrooms      = $value['BEDROOMS']; 
  $pets          = $value['PETS'];
  $priceLow      = $value['PRICE_LOW'];
  $bathrooms     = "N/A"; 

   
// changeover
  foreach($dom->find('div[class=property-box]') as $box){
    foreach($box->find('div[class=page-section]') as $data){
      foreach($data->find('tr[class=cal-sub-title]') as $cal){
        $changeoverarray = explode("</td>",$cal);
        foreach($changeoverarray as $key=>$item){
          if(strpos($item,"cdAvaTd"))
            $changeoverKey = $key;;
        }
      }
    } 
 }
  
switch ($changeoverKey) {
    case "0":
        $changeover = "Sunday";
        break;
    case "1":
        $changeover = "Monday";
        break;
    case "2":
        $changeover = "Tuesday";
        break;
    case "3":
        $changeover = "Wednesday";
        break;
    case "4":
        $changeover = "Thursday";
        break;
    case "5":
        $changeover = "Friday";
        break;
    case "6":
        $changeover = "Saturday";
        break;
   default:
    $changeover = "N/A";
}

  // Price High
  $priceHigh = $priceLow * 2.1; ;

  // features 
  $cottage_facil = "";
  foreach($dom->find('div[id=property-left]')as $data)
  foreach($data->find('div[class=property-box-content]')as $description){
      $descArray = explode("<p>",$description);
             
      $cott_desc = strip_tags($descArray[1]);
      $area_desc = strip_tags($descArray[2]);
      $features = strip_tags($descArray[3]);

      $area_desc = str_replace("Accommodation:","",$area_desc); 

      $features = str_replace("Facilities and Services:","",$features); 
      $features = str_replace("Accommodation:","",$features); 

      $cott_desc = str_replace("Accommodation:","",$cott_desc );

      if($cott_desc =="") $cott_desc= "N/A";
      if($area_desc =="") $area_desc = "N/A";
      if($features =="") $features = "N/A";
  
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
  foreach($dom->find('div[class=carousel]')as $item){
    foreach($item->find('a')as $thumb){   
      $pic .= "http://www.marsdens.co.uk".$thumb->href.",";    
    }
  }

 // long lat
 $coords = substr($html,strpos($dom,"#property-map-frame",30000),100); 
 $latlong = substr($coords,strpos($coords,"latitude: "),strpos($coords,"}")); 
 $latlong = substr($latlong,0,strpos($latlong,"}"));
 $latlongArr = explode(",",$latlong);
 $lat = str_replace("latitude: ","",$latlongArr[0]);
 $lng = str_replace("longitude: ","",$latlongArr[1]);

   
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
      'Agent'               => "marsdens.co.uk",
   );
  
 if(strlen(trim(clean_text($cott_desc)))!= 0)
      scraperwiki::save(array('COTTAGE_REFERENCE'), $record);
}

?>


