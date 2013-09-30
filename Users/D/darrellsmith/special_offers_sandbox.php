<?php
 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS turk_table (ID int, TEXT string, DATE string)");
 $id = 0;


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
    

    // parse text and extract useful data
    //$str - The Text
    //$start - the character to start scraping from
    //$end - the character to scrape to. Default = " " (space)
    function parseTextAround($str,$start,$end=" "){
       $returnArr = array();
       $strArr = explode($start,strtolower($str));
       $i = 0;
       if(count($strArr)>=2){
         foreach($strArr as $item){
           if(!$i % 2){           
             $parsedStr = substr($strArr[$i],-2,2);
             array_push($returnArr,$parsedStr);
             $i = $i+2;
           }
         }
         return $returnArr;
       }
    }
    


    /*
    ** getDiscountAmount($str)
    ** $str = the text to parse
    ** returns the discount in £
    */
    function getDiscountAmount($str){
      # split the text up by full stop for multiple deals
          $discount = "";
          // standardise the currency Symbol
          $str = str_replace("&pound;","£",$str);
          // dont parse any records with percentages in it
          // as we can work out the discount ourselves
          if(strpos(strtolower($str),"%"))
            return;
          if(strpos(strtolower($str),"saving") &&  $discount=="")
              $discount = substr($str,strpos(strtolower($str),"saving"));
          if(strpos(strtolower($str),"off") &&  $discount=="" )
              $discount = substr($str,strpos($str,"£"),strpos(strtolower($str),"off"));
          if(strpos(strtolower($str),"discount of") &&  $discount=="")
              $discount = substr($str,strpos($str,strpos($str,"£"),"discount of ")+12,8);
          $discount =  preg_replace('/[^0-9.]+/', '',$discount);
      return   $discount;
    }
    
    /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getDiscountedPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      
      $str = str_replace("&pound;","£",$str);
      $amount = "";

      if(strpos(strtolower($str),"just") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"just")+4,12);  
      if(strpos(strtolower($str),"from") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"from")+4,12);
      if(strpos(strtolower($str),"now") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"now")+3,12);
      if(strpos(strtolower($str),"only") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"only")+4,12);
      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);    
      return $amountAfterDiscount;
    }
    
     /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getOriginalPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      $str = str_replace("&pound;","£",$str);
      $amount = "";


      if(strpos(strtolower($str),"weeks ") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"weeks ")+6,3);  

      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
 
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);      
      return $amountAfterDiscount;
    }
    
    
    /*
    ** calcOriginalPrice($percentageAmount,$discountPrice)
    ** $percentageAmount = The percentage the price has been reduced by
    ** $discountPrice = The price after the deduction
    ** returns the Original Price
    ** eg 325 -  (100 - 25) = 4.33
    ** 4.33 * 100 = 433
    */
    function calcOriginalPrice($discountPrice,$percentageAmount){
          return  round(($discountPrice / (100 - $percentageAmount)) * 100);
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
    
    
  



  #################
  ## Parse Dates ##
  #################
  function getfromDate($str,$fromMonth){
    $date= "";
    if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
       $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
    return preg_replace('/[^0-9.]+/', '', $date);
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
      if(strrpos(strtolower($str),strtolower($monthToFind)) &&  $date=="")
          $date= substr($str,strrpos(strtolower($str),strtolower($monthToFind))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);
    }

 
 
   ////////////////////////////////////////////////////////
   //////// end of functions start of main code ///////////
   ////////////////////////////////////////////////////////

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
            
        // functions to parse the special offer string
        #### deal with price ####
       
        // initialise variables
        $discountAmount = "";
        $originalPrice = "";
        $calcPercentage = "";
                
        // Get discounted price
        $discountedPrice =  getDiscountedPrice($str);  


        // Get discount in £
        $discountAmount = getDiscountAmount($str);


        // get discount percentage
        $percentageArr = parseTextAround($specialOffer,"%");
        if(isset($percentageArr[0]))
           $percentage = $percentageArr[0];
        elseif($discountedPrice != ""){
           $originalPrice = $discountedPrice + $discountAmount;  
           $percentage= calcPercentage($discountAmount,$originalPrice);
        }

        // get original price from discount percentage and discounted price
        $originalPrice = $discountedPrice +  $discountAmount;

        if($originalPrice <=$discountedPrice){
            $originalPrice= getOriginalPrice($specialOffer);
            if($originalPrice == "" || $originalPrice < $discountedPrice || $originalPrice == $discountedPrice || $originalPrice == $discountAmount)
               $originalPrice = calcOriginalPrice($discountedPrice,$percentage);
        }
           
                   
        # now fill in any missing values
        $discountAmount =  $originalPrice - $discountedPrice;
 
        if($discountedPrice == "")
          $discountedPrice = $originalPrice - $discountAmount;
                
        if($percentage == ""){
           // get discount percentage
           $percentageArr = parseTextAround($specialOffer,"%");
           if(isset($percentageArr[0]))
               $percentage = $percentageArr[0];
           elseif( $discountedPrice!=""){
               $originalPrice = $discountedPrice + $discountAmount;  
               $percentage= calcPercentage($discountAmount,$originalPrice);
           }
        }

                
        if($originalPrice == "")
           $originalPrice = calcOriginalPrice($discountedPrice,$percentage );;  
              
           #### deal with dates ####
           $getToMonth = getToMonth($specialOffer);    
           $getToDate= getToDate($specialOffer,$getToMonth);  
                    
           $getFromMonth = getFromMonth($specialOffer);    
           $getFromDate= getFromDate($specialOffer,$getFromMonth);
        
           $dateFrom = date('dS  F Y',  strtotime($getFromDate." ".$getFromMonth));
           $dateTo = date('dS  F Y',  strtotime($getToDate." ".$getToMonth));            
         
           $datetime1 = date_create(date('Y-m-d',  strtotime($getFromDate." ".$getFromMonth)));
           $datetime2 = date_create(date('Y-m-d',  strtotime($getToDate." ".$getToMonth)));
           $interval = date_diff($datetime1, $datetime2);
           $interval = $interval->format('%a');
           if($interval == 0){
              $dealLength = 1;
           }else{
              $dealLength = ($interval / 7)+1;
           }
               
           if($dealLength > 10)
              $dealLength = 10; 


           #
           # work out dates and prepare them for the database
           # datelength - the number of weeks
           # startDate - the date to startr counting
           #
           $curreDate = "";
           $currDate = $dateFrom;
           $currDate = date('Y-m-d',strtotime('-1 week',strtotime($currDate)));
           
           for($j=0; $j<$dealLength; $j++){
               $currDate = date('Y-m-d',  strtotime($currDate));
               $curreDate = date('Y-m-d',strtotime('+1 week',strtotime($currDate)));
               $currEndDate = date('dS  F Y',strtotime('+1 week',strtotime($curreDate)));
               $id++;
               $originalPrice = round($originalPrice,0,PHP_ROUND_HALF_DOWN);
               $discountAmount= round($discountAmount,0,PHP_ROUND_HALF_DOWN);     
               $duration= abs(strtotime($currEndDate) - strtotime($curreDate ));
               $duration = $duration / (60*60*24);
               
               /*  save the data  */
               $record = array(
               'ID'                => $id,
               'COTTAGE_ID'        => "Cottage ID",
               'DATE_FROM'         => $dateFrom,
               'DATE_TO'           => $currEndDate ,
               'DURATION'          => $duration,
               'WAS_PRICE'         => $originalPrice,
               'NOW_PRICE'         => $discountedPrice,
               'DISCOUNT_PERCENT'  => $percentage,
               'DISCOUNT_AMOUNT'   => $discountAmount,
               'REF'               => "ref#",
               'Text'              => $specialOffer ,    
               'TIMESTAMP'         => $date->getTimestamp(),
        );
        #  print_r($record);
        if($originalPrice == 0 || $discountedPrice == 0 || $percentage == 0){
           scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));                 
        }else
           scraperwiki::save(array('ID'), $record);
        }
        $i++;
     }else{
        $record = array(
           'ID'                => $id,
           'COTTAGE_ID'        => "Cottage ID",
           'DATE_FROM'         => $dateFrom,
           'DATE_TO'           => $currEndDate ,
           'DURATION'          => $duration,
           'WAS_PRICE'         => $originalPrice,
           'NOW_PRICE'         => $discountedPrice,
           'DISCOUNT_PERCENT'  => $percentage,
           'DISCOUNT_AMOUNT'   => $discountAmount,
           'REF'               => "ref#",
           'Text'              => $specialOffer ,    
           'TIMESTAMP'         => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
        $i++;
     }
}
?><?php
 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS turk_table (ID int, TEXT string, DATE string)");
 $id = 0;


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
    

    // parse text and extract useful data
    //$str - The Text
    //$start - the character to start scraping from
    //$end - the character to scrape to. Default = " " (space)
    function parseTextAround($str,$start,$end=" "){
       $returnArr = array();
       $strArr = explode($start,strtolower($str));
       $i = 0;
       if(count($strArr)>=2){
         foreach($strArr as $item){
           if(!$i % 2){           
             $parsedStr = substr($strArr[$i],-2,2);
             array_push($returnArr,$parsedStr);
             $i = $i+2;
           }
         }
         return $returnArr;
       }
    }
    


    /*
    ** getDiscountAmount($str)
    ** $str = the text to parse
    ** returns the discount in £
    */
    function getDiscountAmount($str){
      # split the text up by full stop for multiple deals
          $discount = "";
          // standardise the currency Symbol
          $str = str_replace("&pound;","£",$str);
          // dont parse any records with percentages in it
          // as we can work out the discount ourselves
          if(strpos(strtolower($str),"%"))
            return;
          if(strpos(strtolower($str),"saving") &&  $discount=="")
              $discount = substr($str,strpos(strtolower($str),"saving"));
          if(strpos(strtolower($str),"off") &&  $discount=="" )
              $discount = substr($str,strpos($str,"£"),strpos(strtolower($str),"off"));
          if(strpos(strtolower($str),"discount of") &&  $discount=="")
              $discount = substr($str,strpos($str,strpos($str,"£"),"discount of ")+12,8);
          $discount =  preg_replace('/[^0-9.]+/', '',$discount);
      return   $discount;
    }
    
    /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getDiscountedPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      
      $str = str_replace("&pound;","£",$str);
      $amount = "";

      if(strpos(strtolower($str),"just") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"just")+4,12);  
      if(strpos(strtolower($str),"from") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"from")+4,12);
      if(strpos(strtolower($str),"now") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"now")+3,12);
      if(strpos(strtolower($str),"only") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"only")+4,12);
      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);    
      return $amountAfterDiscount;
    }
    
     /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getOriginalPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      $str = str_replace("&pound;","£",$str);
      $amount = "";


      if(strpos(strtolower($str),"weeks ") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"weeks ")+6,3);  

      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
 
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);      
      return $amountAfterDiscount;
    }
    
    
    /*
    ** calcOriginalPrice($percentageAmount,$discountPrice)
    ** $percentageAmount = The percentage the price has been reduced by
    ** $discountPrice = The price after the deduction
    ** returns the Original Price
    ** eg 325 -  (100 - 25) = 4.33
    ** 4.33 * 100 = 433
    */
    function calcOriginalPrice($discountPrice,$percentageAmount){
          return  round(($discountPrice / (100 - $percentageAmount)) * 100);
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
    
    
  



  #################
  ## Parse Dates ##
  #################
  function getfromDate($str,$fromMonth){
    $date= "";
    if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
       $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
    return preg_replace('/[^0-9.]+/', '', $date);
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
      if(strrpos(strtolower($str),strtolower($monthToFind)) &&  $date=="")
          $date= substr($str,strrpos(strtolower($str),strtolower($monthToFind))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);
    }

 
 
   ////////////////////////////////////////////////////////
   //////// end of functions start of main code ///////////
   ////////////////////////////////////////////////////////

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
            
        // functions to parse the special offer string
        #### deal with price ####
       
        // initialise variables
        $discountAmount = "";
        $originalPrice = "";
        $calcPercentage = "";
                
        // Get discounted price
        $discountedPrice =  getDiscountedPrice($str);  


        // Get discount in £
        $discountAmount = getDiscountAmount($str);


        // get discount percentage
        $percentageArr = parseTextAround($specialOffer,"%");
        if(isset($percentageArr[0]))
           $percentage = $percentageArr[0];
        elseif($discountedPrice != ""){
           $originalPrice = $discountedPrice + $discountAmount;  
           $percentage= calcPercentage($discountAmount,$originalPrice);
        }

        // get original price from discount percentage and discounted price
        $originalPrice = $discountedPrice +  $discountAmount;

        if($originalPrice <=$discountedPrice){
            $originalPrice= getOriginalPrice($specialOffer);
            if($originalPrice == "" || $originalPrice < $discountedPrice || $originalPrice == $discountedPrice || $originalPrice == $discountAmount)
               $originalPrice = calcOriginalPrice($discountedPrice,$percentage);
        }
           
                   
        # now fill in any missing values
        $discountAmount =  $originalPrice - $discountedPrice;
 
        if($discountedPrice == "")
          $discountedPrice = $originalPrice - $discountAmount;
                
        if($percentage == ""){
           // get discount percentage
           $percentageArr = parseTextAround($specialOffer,"%");
           if(isset($percentageArr[0]))
               $percentage = $percentageArr[0];
           elseif( $discountedPrice!=""){
               $originalPrice = $discountedPrice + $discountAmount;  
               $percentage= calcPercentage($discountAmount,$originalPrice);
           }
        }

                
        if($originalPrice == "")
           $originalPrice = calcOriginalPrice($discountedPrice,$percentage );;  
              
           #### deal with dates ####
           $getToMonth = getToMonth($specialOffer);    
           $getToDate= getToDate($specialOffer,$getToMonth);  
                    
           $getFromMonth = getFromMonth($specialOffer);    
           $getFromDate= getFromDate($specialOffer,$getFromMonth);
        
           $dateFrom = date('dS  F Y',  strtotime($getFromDate." ".$getFromMonth));
           $dateTo = date('dS  F Y',  strtotime($getToDate." ".$getToMonth));            
         
           $datetime1 = date_create(date('Y-m-d',  strtotime($getFromDate." ".$getFromMonth)));
           $datetime2 = date_create(date('Y-m-d',  strtotime($getToDate." ".$getToMonth)));
           $interval = date_diff($datetime1, $datetime2);
           $interval = $interval->format('%a');
           if($interval == 0){
              $dealLength = 1;
           }else{
              $dealLength = ($interval / 7)+1;
           }
               
           if($dealLength > 10)
              $dealLength = 10; 


           #
           # work out dates and prepare them for the database
           # datelength - the number of weeks
           # startDate - the date to startr counting
           #
           $curreDate = "";
           $currDate = $dateFrom;
           $currDate = date('Y-m-d',strtotime('-1 week',strtotime($currDate)));
           
           for($j=0; $j<$dealLength; $j++){
               $currDate = date('Y-m-d',  strtotime($currDate));
               $curreDate = date('Y-m-d',strtotime('+1 week',strtotime($currDate)));
               $currEndDate = date('dS  F Y',strtotime('+1 week',strtotime($curreDate)));
               $id++;
               $originalPrice = round($originalPrice,0,PHP_ROUND_HALF_DOWN);
               $discountAmount= round($discountAmount,0,PHP_ROUND_HALF_DOWN);     
               $duration= abs(strtotime($currEndDate) - strtotime($curreDate ));
               $duration = $duration / (60*60*24);
               
               /*  save the data  */
               $record = array(
               'ID'                => $id,
               'COTTAGE_ID'        => "Cottage ID",
               'DATE_FROM'         => $dateFrom,
               'DATE_TO'           => $currEndDate ,
               'DURATION'          => $duration,
               'WAS_PRICE'         => $originalPrice,
               'NOW_PRICE'         => $discountedPrice,
               'DISCOUNT_PERCENT'  => $percentage,
               'DISCOUNT_AMOUNT'   => $discountAmount,
               'REF'               => "ref#",
               'Text'              => $specialOffer ,    
               'TIMESTAMP'         => $date->getTimestamp(),
        );
        #  print_r($record);
        if($originalPrice == 0 || $discountedPrice == 0 || $percentage == 0){
           scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));                 
        }else
           scraperwiki::save(array('ID'), $record);
        }
        $i++;
     }else{
        $record = array(
           'ID'                => $id,
           'COTTAGE_ID'        => "Cottage ID",
           'DATE_FROM'         => $dateFrom,
           'DATE_TO'           => $currEndDate ,
           'DURATION'          => $duration,
           'WAS_PRICE'         => $originalPrice,
           'NOW_PRICE'         => $discountedPrice,
           'DISCOUNT_PERCENT'  => $percentage,
           'DISCOUNT_AMOUNT'   => $discountAmount,
           'REF'               => "ref#",
           'Text'              => $specialOffer ,    
           'TIMESTAMP'         => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
        $i++;
     }
}
?><?php
 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS turk_table (ID int, TEXT string, DATE string)");
 $id = 0;


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
    

    // parse text and extract useful data
    //$str - The Text
    //$start - the character to start scraping from
    //$end - the character to scrape to. Default = " " (space)
    function parseTextAround($str,$start,$end=" "){
       $returnArr = array();
       $strArr = explode($start,strtolower($str));
       $i = 0;
       if(count($strArr)>=2){
         foreach($strArr as $item){
           if(!$i % 2){           
             $parsedStr = substr($strArr[$i],-2,2);
             array_push($returnArr,$parsedStr);
             $i = $i+2;
           }
         }
         return $returnArr;
       }
    }
    


    /*
    ** getDiscountAmount($str)
    ** $str = the text to parse
    ** returns the discount in £
    */
    function getDiscountAmount($str){
      # split the text up by full stop for multiple deals
          $discount = "";
          // standardise the currency Symbol
          $str = str_replace("&pound;","£",$str);
          // dont parse any records with percentages in it
          // as we can work out the discount ourselves
          if(strpos(strtolower($str),"%"))
            return;
          if(strpos(strtolower($str),"saving") &&  $discount=="")
              $discount = substr($str,strpos(strtolower($str),"saving"));
          if(strpos(strtolower($str),"off") &&  $discount=="" )
              $discount = substr($str,strpos($str,"£"),strpos(strtolower($str),"off"));
          if(strpos(strtolower($str),"discount of") &&  $discount=="")
              $discount = substr($str,strpos($str,strpos($str,"£"),"discount of ")+12,8);
          $discount =  preg_replace('/[^0-9.]+/', '',$discount);
      return   $discount;
    }
    
    /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getDiscountedPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      
      $str = str_replace("&pound;","£",$str);
      $amount = "";

      if(strpos(strtolower($str),"just") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"just")+4,12);  
      if(strpos(strtolower($str),"from") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"from")+4,12);
      if(strpos(strtolower($str),"now") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"now")+3,12);
      if(strpos(strtolower($str),"only") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"only")+4,12);
      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);    
      return $amountAfterDiscount;
    }
    
     /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getOriginalPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      $str = str_replace("&pound;","£",$str);
      $amount = "";


      if(strpos(strtolower($str),"weeks ") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"weeks ")+6,3);  

      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
 
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);      
      return $amountAfterDiscount;
    }
    
    
    /*
    ** calcOriginalPrice($percentageAmount,$discountPrice)
    ** $percentageAmount = The percentage the price has been reduced by
    ** $discountPrice = The price after the deduction
    ** returns the Original Price
    ** eg 325 -  (100 - 25) = 4.33
    ** 4.33 * 100 = 433
    */
    function calcOriginalPrice($discountPrice,$percentageAmount){
          return  round(($discountPrice / (100 - $percentageAmount)) * 100);
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
    
    
  



  #################
  ## Parse Dates ##
  #################
  function getfromDate($str,$fromMonth){
    $date= "";
    if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
       $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
    return preg_replace('/[^0-9.]+/', '', $date);
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
      if(strrpos(strtolower($str),strtolower($monthToFind)) &&  $date=="")
          $date= substr($str,strrpos(strtolower($str),strtolower($monthToFind))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);
    }

 
 
   ////////////////////////////////////////////////////////
   //////// end of functions start of main code ///////////
   ////////////////////////////////////////////////////////

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
            
        // functions to parse the special offer string
        #### deal with price ####
       
        // initialise variables
        $discountAmount = "";
        $originalPrice = "";
        $calcPercentage = "";
                
        // Get discounted price
        $discountedPrice =  getDiscountedPrice($str);  


        // Get discount in £
        $discountAmount = getDiscountAmount($str);


        // get discount percentage
        $percentageArr = parseTextAround($specialOffer,"%");
        if(isset($percentageArr[0]))
           $percentage = $percentageArr[0];
        elseif($discountedPrice != ""){
           $originalPrice = $discountedPrice + $discountAmount;  
           $percentage= calcPercentage($discountAmount,$originalPrice);
        }

        // get original price from discount percentage and discounted price
        $originalPrice = $discountedPrice +  $discountAmount;

        if($originalPrice <=$discountedPrice){
            $originalPrice= getOriginalPrice($specialOffer);
            if($originalPrice == "" || $originalPrice < $discountedPrice || $originalPrice == $discountedPrice || $originalPrice == $discountAmount)
               $originalPrice = calcOriginalPrice($discountedPrice,$percentage);
        }
           
                   
        # now fill in any missing values
        $discountAmount =  $originalPrice - $discountedPrice;
 
        if($discountedPrice == "")
          $discountedPrice = $originalPrice - $discountAmount;
                
        if($percentage == ""){
           // get discount percentage
           $percentageArr = parseTextAround($specialOffer,"%");
           if(isset($percentageArr[0]))
               $percentage = $percentageArr[0];
           elseif( $discountedPrice!=""){
               $originalPrice = $discountedPrice + $discountAmount;  
               $percentage= calcPercentage($discountAmount,$originalPrice);
           }
        }

                
        if($originalPrice == "")
           $originalPrice = calcOriginalPrice($discountedPrice,$percentage );;  
              
           #### deal with dates ####
           $getToMonth = getToMonth($specialOffer);    
           $getToDate= getToDate($specialOffer,$getToMonth);  
                    
           $getFromMonth = getFromMonth($specialOffer);    
           $getFromDate= getFromDate($specialOffer,$getFromMonth);
        
           $dateFrom = date('dS  F Y',  strtotime($getFromDate." ".$getFromMonth));
           $dateTo = date('dS  F Y',  strtotime($getToDate." ".$getToMonth));            
         
           $datetime1 = date_create(date('Y-m-d',  strtotime($getFromDate." ".$getFromMonth)));
           $datetime2 = date_create(date('Y-m-d',  strtotime($getToDate." ".$getToMonth)));
           $interval = date_diff($datetime1, $datetime2);
           $interval = $interval->format('%a');
           if($interval == 0){
              $dealLength = 1;
           }else{
              $dealLength = ($interval / 7)+1;
           }
               
           if($dealLength > 10)
              $dealLength = 10; 


           #
           # work out dates and prepare them for the database
           # datelength - the number of weeks
           # startDate - the date to startr counting
           #
           $curreDate = "";
           $currDate = $dateFrom;
           $currDate = date('Y-m-d',strtotime('-1 week',strtotime($currDate)));
           
           for($j=0; $j<$dealLength; $j++){
               $currDate = date('Y-m-d',  strtotime($currDate));
               $curreDate = date('Y-m-d',strtotime('+1 week',strtotime($currDate)));
               $currEndDate = date('dS  F Y',strtotime('+1 week',strtotime($curreDate)));
               $id++;
               $originalPrice = round($originalPrice,0,PHP_ROUND_HALF_DOWN);
               $discountAmount= round($discountAmount,0,PHP_ROUND_HALF_DOWN);     
               $duration= abs(strtotime($currEndDate) - strtotime($curreDate ));
               $duration = $duration / (60*60*24);
               
               /*  save the data  */
               $record = array(
               'ID'                => $id,
               'COTTAGE_ID'        => "Cottage ID",
               'DATE_FROM'         => $dateFrom,
               'DATE_TO'           => $currEndDate ,
               'DURATION'          => $duration,
               'WAS_PRICE'         => $originalPrice,
               'NOW_PRICE'         => $discountedPrice,
               'DISCOUNT_PERCENT'  => $percentage,
               'DISCOUNT_AMOUNT'   => $discountAmount,
               'REF'               => "ref#",
               'Text'              => $specialOffer ,    
               'TIMESTAMP'         => $date->getTimestamp(),
        );
        #  print_r($record);
        if($originalPrice == 0 || $discountedPrice == 0 || $percentage == 0){
           scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));                 
        }else
           scraperwiki::save(array('ID'), $record);
        }
        $i++;
     }else{
        $record = array(
           'ID'                => $id,
           'COTTAGE_ID'        => "Cottage ID",
           'DATE_FROM'         => $dateFrom,
           'DATE_TO'           => $currEndDate ,
           'DURATION'          => $duration,
           'WAS_PRICE'         => $originalPrice,
           'NOW_PRICE'         => $discountedPrice,
           'DISCOUNT_PERCENT'  => $percentage,
           'DISCOUNT_AMOUNT'   => $discountAmount,
           'REF'               => "ref#",
           'Text'              => $specialOffer ,    
           'TIMESTAMP'         => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
        $i++;
     }
}
?><?php
 scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS turk_table (ID int, TEXT string, DATE string)");
 $id = 0;


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
    

    // parse text and extract useful data
    //$str - The Text
    //$start - the character to start scraping from
    //$end - the character to scrape to. Default = " " (space)
    function parseTextAround($str,$start,$end=" "){
       $returnArr = array();
       $strArr = explode($start,strtolower($str));
       $i = 0;
       if(count($strArr)>=2){
         foreach($strArr as $item){
           if(!$i % 2){           
             $parsedStr = substr($strArr[$i],-2,2);
             array_push($returnArr,$parsedStr);
             $i = $i+2;
           }
         }
         return $returnArr;
       }
    }
    


    /*
    ** getDiscountAmount($str)
    ** $str = the text to parse
    ** returns the discount in £
    */
    function getDiscountAmount($str){
      # split the text up by full stop for multiple deals
          $discount = "";
          // standardise the currency Symbol
          $str = str_replace("&pound;","£",$str);
          // dont parse any records with percentages in it
          // as we can work out the discount ourselves
          if(strpos(strtolower($str),"%"))
            return;
          if(strpos(strtolower($str),"saving") &&  $discount=="")
              $discount = substr($str,strpos(strtolower($str),"saving"));
          if(strpos(strtolower($str),"off") &&  $discount=="" )
              $discount = substr($str,strpos($str,"£"),strpos(strtolower($str),"off"));
          if(strpos(strtolower($str),"discount of") &&  $discount=="")
              $discount = substr($str,strpos($str,strpos($str,"£"),"discount of ")+12,8);
          $discount =  preg_replace('/[^0-9.]+/', '',$discount);
      return   $discount;
    }
    
    /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getDiscountedPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      
      $str = str_replace("&pound;","£",$str);
      $amount = "";

      if(strpos(strtolower($str),"just") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"just")+4,12);  
      if(strpos(strtolower($str),"from") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"from")+4,12);
      if(strpos(strtolower($str),"now") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"now")+3,12);
      if(strpos(strtolower($str),"only") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"only")+4,12);
      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);    
      return $amountAfterDiscount;
    }
    
     /*
    ** getDiscountedPrice($str)
    ** $str = the text to parse
    ** returns the discounted price
    */
    function getOriginalPrice($str){
      $i = 0;
      $amountAfterDiscount = "";
      $str = str_replace("&pound;","£",$str);
      $amount = "";


      if(strpos(strtolower($str),"weeks ") &&  $amountAfterDiscount=="")
          $amountAfterDiscount = substr($str,strpos(strtolower($str),"weeks ")+6,3);  

      # if there is a decimal point, remove it and everything after it
      if(strpos($amountAfterDiscount,"."))
          $amountAfterDiscount = substr($amountAfterDiscount,0,strpos($amountAfterDiscount,"."));
 
      $amountAfterDiscount = preg_replace('/[^0-9.]+/', '', $amountAfterDiscount);      
      return $amountAfterDiscount;
    }
    
    
    /*
    ** calcOriginalPrice($percentageAmount,$discountPrice)
    ** $percentageAmount = The percentage the price has been reduced by
    ** $discountPrice = The price after the deduction
    ** returns the Original Price
    ** eg 325 -  (100 - 25) = 4.33
    ** 4.33 * 100 = 433
    */
    function calcOriginalPrice($discountPrice,$percentageAmount){
          return  round(($discountPrice / (100 - $percentageAmount)) * 100);
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
    
    
  



  #################
  ## Parse Dates ##
  #################
  function getfromDate($str,$fromMonth){
    $date= "";
    if(strpos(strtolower($str),strtolower($fromMonth)) &&  $date=="")
       $date= substr($str,strpos(strtolower($str),strtolower($fromMonth))-5,5);
    return preg_replace('/[^0-9.]+/', '', $date);
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
      if(strrpos(strtolower($str),strtolower($monthToFind)) &&  $date=="")
          $date= substr($str,strrpos(strtolower($str),strtolower($monthToFind))-5,5);
        return preg_replace('/[^0-9.]+/', '', $date);
    }

 
 
   ////////////////////////////////////////////////////////
   //////// end of functions start of main code ///////////
   ////////////////////////////////////////////////////////

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
            
        // functions to parse the special offer string
        #### deal with price ####
       
        // initialise variables
        $discountAmount = "";
        $originalPrice = "";
        $calcPercentage = "";
                
        // Get discounted price
        $discountedPrice =  getDiscountedPrice($str);  


        // Get discount in £
        $discountAmount = getDiscountAmount($str);


        // get discount percentage
        $percentageArr = parseTextAround($specialOffer,"%");
        if(isset($percentageArr[0]))
           $percentage = $percentageArr[0];
        elseif($discountedPrice != ""){
           $originalPrice = $discountedPrice + $discountAmount;  
           $percentage= calcPercentage($discountAmount,$originalPrice);
        }

        // get original price from discount percentage and discounted price
        $originalPrice = $discountedPrice +  $discountAmount;

        if($originalPrice <=$discountedPrice){
            $originalPrice= getOriginalPrice($specialOffer);
            if($originalPrice == "" || $originalPrice < $discountedPrice || $originalPrice == $discountedPrice || $originalPrice == $discountAmount)
               $originalPrice = calcOriginalPrice($discountedPrice,$percentage);
        }
           
                   
        # now fill in any missing values
        $discountAmount =  $originalPrice - $discountedPrice;
 
        if($discountedPrice == "")
          $discountedPrice = $originalPrice - $discountAmount;
                
        if($percentage == ""){
           // get discount percentage
           $percentageArr = parseTextAround($specialOffer,"%");
           if(isset($percentageArr[0]))
               $percentage = $percentageArr[0];
           elseif( $discountedPrice!=""){
               $originalPrice = $discountedPrice + $discountAmount;  
               $percentage= calcPercentage($discountAmount,$originalPrice);
           }
        }

                
        if($originalPrice == "")
           $originalPrice = calcOriginalPrice($discountedPrice,$percentage );;  
              
           #### deal with dates ####
           $getToMonth = getToMonth($specialOffer);    
           $getToDate= getToDate($specialOffer,$getToMonth);  
                    
           $getFromMonth = getFromMonth($specialOffer);    
           $getFromDate= getFromDate($specialOffer,$getFromMonth);
        
           $dateFrom = date('dS  F Y',  strtotime($getFromDate." ".$getFromMonth));
           $dateTo = date('dS  F Y',  strtotime($getToDate." ".$getToMonth));            
         
           $datetime1 = date_create(date('Y-m-d',  strtotime($getFromDate." ".$getFromMonth)));
           $datetime2 = date_create(date('Y-m-d',  strtotime($getToDate." ".$getToMonth)));
           $interval = date_diff($datetime1, $datetime2);
           $interval = $interval->format('%a');
           if($interval == 0){
              $dealLength = 1;
           }else{
              $dealLength = ($interval / 7)+1;
           }
               
           if($dealLength > 10)
              $dealLength = 10; 


           #
           # work out dates and prepare them for the database
           # datelength - the number of weeks
           # startDate - the date to startr counting
           #
           $curreDate = "";
           $currDate = $dateFrom;
           $currDate = date('Y-m-d',strtotime('-1 week',strtotime($currDate)));
           
           for($j=0; $j<$dealLength; $j++){
               $currDate = date('Y-m-d',  strtotime($currDate));
               $curreDate = date('Y-m-d',strtotime('+1 week',strtotime($currDate)));
               $currEndDate = date('dS  F Y',strtotime('+1 week',strtotime($curreDate)));
               $id++;
               $originalPrice = round($originalPrice,0,PHP_ROUND_HALF_DOWN);
               $discountAmount= round($discountAmount,0,PHP_ROUND_HALF_DOWN);     
               $duration= abs(strtotime($currEndDate) - strtotime($curreDate ));
               $duration = $duration / (60*60*24);
               
               /*  save the data  */
               $record = array(
               'ID'                => $id,
               'COTTAGE_ID'        => "Cottage ID",
               'DATE_FROM'         => $dateFrom,
               'DATE_TO'           => $currEndDate ,
               'DURATION'          => $duration,
               'WAS_PRICE'         => $originalPrice,
               'NOW_PRICE'         => $discountedPrice,
               'DISCOUNT_PERCENT'  => $percentage,
               'DISCOUNT_AMOUNT'   => $discountAmount,
               'REF'               => "ref#",
               'Text'              => $specialOffer ,    
               'TIMESTAMP'         => $date->getTimestamp(),
        );
        #  print_r($record);
        if($originalPrice == 0 || $discountedPrice == 0 || $percentage == 0){
           scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));                 
        }else
           scraperwiki::save(array('ID'), $record);
        }
        $i++;
     }else{
        $record = array(
           'ID'                => $id,
           'COTTAGE_ID'        => "Cottage ID",
           'DATE_FROM'         => $dateFrom,
           'DATE_TO'           => $currEndDate ,
           'DURATION'          => $duration,
           'WAS_PRICE'         => $originalPrice,
           'NOW_PRICE'         => $discountedPrice,
           'DISCOUNT_PERCENT'  => $percentage,
           'DISCOUNT_AMOUNT'   => $discountAmount,
           'REF'               => "ref#",
           'Text'              => $specialOffer ,    
           'TIMESTAMP'         => $date->getTimestamp(),
        );
        scraperwiki::sqliteexecute("insert into turk_table values (?,?,?)",array($i,$specialOffer ,$date->getTimestamp()));
        $i++;
     }
}
?>