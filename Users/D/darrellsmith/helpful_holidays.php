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
    $txt= str_replace("&#039;","£",$txt);
    $txt= preg_replace('/\s+/', ' ',$txt);

    return $txt;
 }

function searchForId($id, $array) {
   foreach ($array as $key => $val) {
     if ($val['LINK'] === $id) {
       return $key;
     }
   }
   return null;
 }



 $url = "http://www.helpfulholidays.com";

 # get an array of the cottage data to scrape
 scraperwiki::attach("php_test_2") ;
 $cottData = scraperwiki::select(" LINK from 'php_test_2'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");
 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['LINK']);

echo $value['LINK'];
    
    // Get special offer 
    foreach($dom->find('div[class=default_box]') as $data){
      foreach($data->find('div[class=class=gen11]') as $specOffer){
          echo $specOffer;
      }
    }
/*

 
     $record = array(

        'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

        'COTTAGE_NAME'       => trim($cottageName),

        'LINK'               => $url,              
     );
    
        
print_r($record);

*/
 
  
 # save the data
  #  scraperwiki::save(array('COTTAGE_ID'), $record);
        
    # Move on to the next page
    $index++;
  }

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
    $txt= str_replace("&#039;","£",$txt);
    $txt= preg_replace('/\s+/', ' ',$txt);

    return $txt;
 }

function searchForId($id, $array) {
   foreach ($array as $key => $val) {
     if ($val['LINK'] === $id) {
       return $key;
     }
   }
   return null;
 }



 $url = "http://www.helpfulholidays.com";

 # get an array of the cottage data to scrape
 scraperwiki::attach("php_test_2") ;
 $cottData = scraperwiki::select(" LINK from 'php_test_2'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");
 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['LINK']);

echo $value['LINK'];
    
    // Get special offer 
    foreach($dom->find('div[class=default_box]') as $data){
      foreach($data->find('div[class=class=gen11]') as $specOffer){
          echo $specOffer;
      }
    }
/*

 
     $record = array(

        'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

        'COTTAGE_NAME'       => trim($cottageName),

        'LINK'               => $url,              
     );
    
        
print_r($record);

*/
 
  
 # save the data
  #  scraperwiki::save(array('COTTAGE_ID'), $record);
        
    # Move on to the next page
    $index++;
  }

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
    $txt= str_replace("&#039;","£",$txt);
    $txt= preg_replace('/\s+/', ' ',$txt);

    return $txt;
 }

function searchForId($id, $array) {
   foreach ($array as $key => $val) {
     if ($val['LINK'] === $id) {
       return $key;
     }
   }
   return null;
 }



 $url = "http://www.helpfulholidays.com";

 # get an array of the cottage data to scrape
 scraperwiki::attach("php_test_2") ;
 $cottData = scraperwiki::select(" LINK from 'php_test_2'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");
 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['LINK']);

echo $value['LINK'];
    
    // Get special offer 
    foreach($dom->find('div[class=default_box]') as $data){
      foreach($data->find('div[class=class=gen11]') as $specOffer){
          echo $specOffer;
      }
    }
/*

 
     $record = array(

        'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

        'COTTAGE_NAME'       => trim($cottageName),

        'LINK'               => $url,              
     );
    
        
print_r($record);

*/
 
  
 # save the data
  #  scraperwiki::save(array('COTTAGE_ID'), $record);
        
    # Move on to the next page
    $index++;
  }

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
    $txt= str_replace("&#039;","£",$txt);
    $txt= preg_replace('/\s+/', ' ',$txt);

    return $txt;
 }

function searchForId($id, $array) {
   foreach ($array as $key => $val) {
     if ($val['LINK'] === $id) {
       return $key;
     }
   }
   return null;
 }



 $url = "http://www.helpfulholidays.com";

 # get an array of the cottage data to scrape
 scraperwiki::attach("php_test_2") ;
 $cottData = scraperwiki::select(" LINK from 'php_test_2'.SWDATA order by COTTAGE_ID");

 $placeholder = scraperwiki::get_var("cottID");
 if($placeholder != ""){
   $index = searchForId($placeholder ,$cottData);
   $cottData = array_splice($cottData,$index);  
 }

 require 'scraperwiki/simple_html_dom.php';
 $dom = new simple_html_dom();
 

foreach($cottData as $value){
    scraperwiki::save_var("cottID",$value['LINK']);

echo $value['LINK'];
    
    // Get special offer 
    foreach($dom->find('div[class=default_box]') as $data){
      foreach($data->find('div[class=class=gen11]') as $specOffer){
          echo $specOffer;
      }
    }
/*

 
     $record = array(

        'COTTAGE_ID'         => trim(str_replace("Ref: ","",$tds[0]->plaintext)),

        'COTTAGE_NAME'       => trim($cottageName),

        'LINK'               => $url,              
     );
    
        
print_r($record);

*/
 
  
 # save the data
  #  scraperwiki::save(array('COTTAGE_ID'), $record);
        
    # Move on to the next page
    $index++;
  }

