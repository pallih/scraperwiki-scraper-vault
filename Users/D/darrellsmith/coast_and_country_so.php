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


 function scrub_text($txt){
    $txt= str_replace("\n","",$txt);
    $txt= str_replace("\r","",$txt);
    $txt= str_replace("&nbsp;","",$txt);
    $txt= str_replace("\t","",$txt);
    $txt= str_replace("&eacute","",$txt);
    $txt= str_replace("&frac12;","",$txt);
    $txt= str_replace("&frac14;","",$txt);
    $txt= str_replace("&pound;","",$txt);
    $txt= str_replace(",,","",$txt);
    $txt= str_replace("&lsquo;","",$txt);
    $txt= str_replace("&rsquo;","",$txt);
    $txt= str_replace("</p>","",$txt);
    $txt= str_replace(".","",$txt);
    $txt= preg_replace('/\s+/', '',$txt);
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




/*
** getDiscountAmount($str)
** $str = the text to parse
** returns the discount in £
*/

function getDiscountAmount($str){
  $strArr = explode("off ",strtolower($str)); 
  $discount = substr($strArr[0],strrpos($strArr[0],"&pound;")+7); 
  if(strpos($discount, "call 01548 843773 to book today")){
    return;
  }    

  $discount = preg_replace('/[^0-9.]+/', '',substr($discount,0,5));
  return   $discount; 
}




/*
** getDiscountedPrice($str)
** $str = the text to parse
** returns the discounted price
*/

function getDiscountedPrice($str){
  $strArr = explode("off ",strtolower($str)); 
  
  $extraCase  = substr($strArr[0],strrpos($strArr[0],"&pound;")+7);
  $amountAfterDiscount = substr($strArr[1],strpos(strtolower($strArr[1]),"now")+3);
  $amountAfterDiscount = substr($strArr[1],strpos(strtolower($strArr[1]),"only")+4);
  $amountAfterDiscount = substr($strArr[1],strpos(strtolower($strArr[1]),"just")+4);  
  $strArr = explode("&pound;",strtolower($amountAfterDiscount)); 

  # include special cases that dont conform the normal pattern matching
  if(strpos($extraCase, "call 01548 843773 to book today")){
    $amountAfterDiscount =  $extraCase ;
    $amountAfterDiscount = preg_replace('/[^0-9.]+/', '',substr($amountAfterDiscount,0,5));
    if(substr($amountAfterDiscount, -1, 1) == "."){
       $amountAfterDiscount = str_replace(".","",$amountAfterDiscount);
    }
    return $amountAfterDiscount;
  }    
  $amountAfterDiscount = preg_replace('/[^0-9.]+/', '',substr($strArr[1],0,5));
  return $amountAfterDiscount;
}




/*
** calcPercentage($discountAmount,$originalPrice)
** $discountAmount = the discount in £
** $originalPrice = the original price in £
** returns the discount as a percentage
*/
function calcPercentage($discountAmount,$originalPrice){
      return round($discountAmount / $originalPrice * 100);
}



##
## Parse Dates
##
function getDates($str){
    $MONTH =array("January","Febuary","March","April","May","June","July","August","September","October","November","December");
    $start = strpos(strtolower($str),"commencing");
    foreach($MONTH as $item){
      $str = str_replace($item,$item."STOP",$str);  
      
    }
    foreach($MONTH as $mnth){
        if (strpos(strtolower($str),$mnth))
            $end = strpos(strtolower($str),"STOP");
    }
    $strArr = substr(strtolower($str),$start,$end);     
   

echo "$str";


    $month= "";

    switch($month){
        case "January":
        break;
        case "Febuary":
        break;
        case "March":
        break;
        case "April":
        break;
        case "May":
        break;
        case "June":
        break;
        case "July":
        break;
        case "August":
        break;
        case "September":
        break;  
        case "October":
        break;        
        case "November":
        break;
        case "December":
        break;
        default:
         return "Error"; 
    }


}





 $blacklist = array( );
 $i = 0;
 scraperwiki::attach("coastandcountrycouk_summary_so") ;
 # get an array of the cottage data to scrape
 $cottData = scraperwiki::select("COTTAGE_URL, PRICE_HIGH, PRICE_LOW from 'coastandcountrycouk_summary_so'.SWDATA order by COTTAGE_URL");

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
   
      $originalPrice ="";
     $discountedPrice="";
    $calcPercentage="";
      $discountAmount="";
  
    $url = "http://www.coastandcountry.co.uk/cottage-details/".$value['COTTAGE_URL'];
# $url = "http://www.coastandcountry.co.uk/cottage-details/1BEACH";
    //load the page into the scraper
    $html = scraperWiki::scrape($url);
    $dom->load($html);
    $feature = "";
    $image = "";
    $imgURL = "";
    $xtraFeatures = "";


   /*  Get the Data  */
   $specialOffer = "";
echo $url;
   foreach($dom->find('div[id=property-specialoffers-box]') as $name)
     foreach($name->find('div[id=property-specialoffers-box-content]') as $box)
        foreach($box->find('p') as $data){
            
           $specialOffer = $data->plaintext;

           // functions to parse the special offer string

           // deal with price
           $discountedPrice = "";
           $discountedPrice = getDiscountedPrice($specialOffer);           
          # print_r("discounted price = ".$discountedPrice);
          
           $discountAmount = "";
           $discountAmount = getDiscountAmount($specialOffer);
         #  print_r("discount amount= ".$discountAmount);

           $originalPrice = "";
           $calcPercentage = "";
            
           if( $discountedPrice!=""){
               $originalPrice = $discountedPrice + $discountAmount;
            #   print_r("original price = ($discountedPrice + $discountAmount)");
            #   echo $originalPrice;
               
               $calcPercentage = calcPercentage($discountAmount,$originalPrice);
             #  print_r("percentage ".$calcPercentage."%");
           }

           if($originalPrice == $discountedPrice)
             $originalPrice = "";


           // deal with dates
           
           
          $getDate = getDate($specialOffer);
             print_r($getDate);
        

    $r = "";
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

     if(@strpos($btds[2],"/tick.gif"))
        $features .= $btds[2]->plaintext."|";
     if(@strpos($btds[3],"/tick.gif"))
        $features .= $btds[3]->plaintext."|";
     if(@strpos($btds[4],"/tick.gif"))
        $features .= $btds[4]->plaintext."|";
     if(@strpos($btds[5],"/tick.gif"))
        $features .= $btds[5]->plaintext."|";
     if(@strpos($btds[6],"/tick.gif"))
        $features .= $btds[6]->plaintext."|";
     if(@strpos($btds[7],"/tick.gif"))
        $features .= $btds[7]->plaintext."|";
     if(@strpos($btds[8],"/tick.gif"))
        $features .= $btds[8]->plaintext."|";
     if(@strpos($btds[9],"/tick.gif"))
        $features .= $btds[9]->plaintext."|";
     if(@strpos($btds[10],"/tick.gif"))
        $features .= $btds[10]->plaintext."|";
     if(@strpos($btds[11],"/tick.gif"))
        $features .= $btds[11]->plaintext."|";
     if(@strpos($btds[12],"/tick.gif"))
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
      'ID'                => $i,
      'COTTAGE_LINK'      => trim($url),
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
      'Agent'             => "coastandcountry.co.uk",
      
      'DURATION'          => "Duration",
      'WAS_PRICE'         => $originalPrice,
      'NOW_PRICE'         => $discountedPrice,
      'DISCOUNT_PERCENT'  => $calcPercentage,
      'DISCOUNT_AMOUNT'   => $discountAmount,

    );

    scraperwiki::save(array('ID'), $record);
    $i++;
   }
}

?>
