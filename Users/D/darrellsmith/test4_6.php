<?php
 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS turk_table (ID int, TEXT string, DATE string)"); 


# $date= preg_replace('/[^0-9.]+/', '', $date);


  /*
  ** Check for offers that aren't wanted
  **
  */
  function isOffer($str){
    $invalidString = array("Please call","to book this offer","must be made by","over the phone","booked before","for remaining dates","REDUCTION ON SHORT BREAKS "
,"call 0","booked  before");
    $validString = array("%","£","&pound;","£","&pound;");
    $ok = false;
    # Test that its an offer
    $count = 0;
    foreach($validString as $vStr){
      if(strpos(strtolower($str), strtolower($vStr))!=false){
        $count++;
        $ok = true;
      }
    }  
    # Test that there are no invalid strings within the offer
    if($ok && $count >=2){
      foreach($invalidString as $invStr){
        if(strpos(strtolower($str), strtolower($invStr)))
          return false;
      }
      return true;
    }
    return false;
  }
    



















  function getToMonth($str){
        $_MONTH = array("January", "Febuary","March","April","May","June","July","August","September","October","November","December");
        $_MONTH = array_reverse($_MONTH);
        foreach($_MONTH as $month){
          if(strrpos($str,$month)){
             return $month;
           }
        }
  }



  function getToDate($str,$monthToFind){
        
      $date = "";
      echo $str;
  #    echo $monthToFind;
      if(strrpos(strtolower($str),strtolower($monthToFind)) &&  $date=="")
          $date= substr($str,strrpos(strtolower($str),strtolower($monthToFind))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);
    }

 
    









    


   $i = 1;
   require 'scraperwiki/simple_html_dom.php';
   $dom = new simple_html_dom();
    
   $originalPrice ="";
   $discountedPrice="";
   $calcPercentage="";
   $discountAmount="";
   $percentage = "";
      
   $url = "http://darrell.ecardsmedia.com/holidaycottage/index.html";
   //load the page into the scraper
   $html = scraperWiki::scrape($url);
   $dom->load($html);

   /*  Get the Data  */
   $specialOffer = "";
   date_default_timezone_set('GMT');
   $date = new DateTime();
       
   foreach($dom->find('p') as $data){
     $discountedPrice ="";
     $specialOffer = $data->plaintext;
     $valid = isOffer($specialOffer);

     if($valid){
        # break the text down into the deals available
       
       # $ok = false;
        $str = $specialOffer;
        $getToMonth = getToMonth($specialOffer);    
        $getToDate= getToDate($specialOffer,$getToMonth);   

echo "\n---";
echo $getToDate." ".$getToMonth ;
echo "---\n";



      $i++;
     }
}
?>
<?php
 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS turk_table (ID int, TEXT string, DATE string)"); 


# $date= preg_replace('/[^0-9.]+/', '', $date);


  /*
  ** Check for offers that aren't wanted
  **
  */
  function isOffer($str){
    $invalidString = array("Please call","to book this offer","must be made by","over the phone","booked before","for remaining dates","REDUCTION ON SHORT BREAKS "
,"call 0","booked  before");
    $validString = array("%","£","&pound;","£","&pound;");
    $ok = false;
    # Test that its an offer
    $count = 0;
    foreach($validString as $vStr){
      if(strpos(strtolower($str), strtolower($vStr))!=false){
        $count++;
        $ok = true;
      }
    }  
    # Test that there are no invalid strings within the offer
    if($ok && $count >=2){
      foreach($invalidString as $invStr){
        if(strpos(strtolower($str), strtolower($invStr)))
          return false;
      }
      return true;
    }
    return false;
  }
    



















  function getToMonth($str){
        $_MONTH = array("January", "Febuary","March","April","May","June","July","August","September","October","November","December");
        $_MONTH = array_reverse($_MONTH);
        foreach($_MONTH as $month){
          if(strrpos($str,$month)){
             return $month;
           }
        }
  }



  function getToDate($str,$monthToFind){
        
      $date = "";
      echo $str;
  #    echo $monthToFind;
      if(strrpos(strtolower($str),strtolower($monthToFind)) &&  $date=="")
          $date= substr($str,strrpos(strtolower($str),strtolower($monthToFind))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);
    }

 
    









    


   $i = 1;
   require 'scraperwiki/simple_html_dom.php';
   $dom = new simple_html_dom();
    
   $originalPrice ="";
   $discountedPrice="";
   $calcPercentage="";
   $discountAmount="";
   $percentage = "";
      
   $url = "http://darrell.ecardsmedia.com/holidaycottage/index.html";
   //load the page into the scraper
   $html = scraperWiki::scrape($url);
   $dom->load($html);

   /*  Get the Data  */
   $specialOffer = "";
   date_default_timezone_set('GMT');
   $date = new DateTime();
       
   foreach($dom->find('p') as $data){
     $discountedPrice ="";
     $specialOffer = $data->plaintext;
     $valid = isOffer($specialOffer);

     if($valid){
        # break the text down into the deals available
       
       # $ok = false;
        $str = $specialOffer;
        $getToMonth = getToMonth($specialOffer);    
        $getToDate= getToDate($specialOffer,$getToMonth);   

echo "\n---";
echo $getToDate." ".$getToMonth ;
echo "---\n";



      $i++;
     }
}
?>
