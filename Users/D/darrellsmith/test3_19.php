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
    
#######################################################




 function getfromDate($str,$fromMonth){
        echo $str;
        $date= "";
        if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
          $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);;
    }

    

function getFromMonth($str){
    $mon  = "";

    $_MONTH = array("January", "Febuary","March","April","May","June","July","August","September","October","November","December");
    foreach($_MONTH as $month){
        if(strpos($str,$month) &&  $mon==""){
            $mon= substr($str,strpos($str,$month),5);
            return $month;
         }
    }
}

 
    

#######################################################



    


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
        $getFromMonth = getFromMonth($specialOffer);    
        $getFromDate= getFromDate($specialOffer,$getFromMonth);   

echo "\n---";
echo $getFromDate." ".$getFromMonth ;
echo "---\n";



      $i++;
     }else{
        $record = array(
             'ID'                => $i,
             'TEXT'              => $specialOffer ,    
             'DATE'              => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
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
    
#######################################################




 function getfromDate($str,$fromMonth){
        echo $str;
        $date= "";
        if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
          $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);;
    }

    

function getFromMonth($str){
    $mon  = "";

    $_MONTH = array("January", "Febuary","March","April","May","June","July","August","September","October","November","December");
    foreach($_MONTH as $month){
        if(strpos($str,$month) &&  $mon==""){
            $mon= substr($str,strpos($str,$month),5);
            return $month;
         }
    }
}

 
    

#######################################################



    


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
        $getFromMonth = getFromMonth($specialOffer);    
        $getFromDate= getFromDate($specialOffer,$getFromMonth);   

echo "\n---";
echo $getFromDate." ".$getFromMonth ;
echo "---\n";



      $i++;
     }else{
        $record = array(
             'ID'                => $i,
             'TEXT'              => $specialOffer ,    
             'DATE'              => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
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
    
#######################################################




 function getfromDate($str,$fromMonth){
        echo $str;
        $date= "";
        if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
          $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);;
    }

    

function getFromMonth($str){
    $mon  = "";

    $_MONTH = array("January", "Febuary","March","April","May","June","July","August","September","October","November","December");
    foreach($_MONTH as $month){
        if(strpos($str,$month) &&  $mon==""){
            $mon= substr($str,strpos($str,$month),5);
            return $month;
         }
    }
}

 
    

#######################################################



    


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
        $getFromMonth = getFromMonth($specialOffer);    
        $getFromDate= getFromDate($specialOffer,$getFromMonth);   

echo "\n---";
echo $getFromDate." ".$getFromMonth ;
echo "---\n";



      $i++;
     }else{
        $record = array(
             'ID'                => $i,
             'TEXT'              => $specialOffer ,    
             'DATE'              => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
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
    
#######################################################




 function getfromDate($str,$fromMonth){
        echo $str;
        $date= "";
        if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
          $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);;
    }

    

function getFromMonth($str){
    $mon  = "";

    $_MONTH = array("January", "Febuary","March","April","May","June","July","August","September","October","November","December");
    foreach($_MONTH as $month){
        if(strpos($str,$month) &&  $mon==""){
            $mon= substr($str,strpos($str,$month),5);
            return $month;
         }
    }
}

 
    

#######################################################



    


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
        $getFromMonth = getFromMonth($specialOffer);    
        $getFromDate= getFromDate($specialOffer,$getFromMonth);   

echo "\n---";
echo $getFromDate." ".$getFromMonth ;
echo "---\n";



      $i++;
     }else{
        $record = array(
             'ID'                => $i,
             'TEXT'              => $specialOffer ,    
             'DATE'              => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
        $i++;
     }
}
?>
