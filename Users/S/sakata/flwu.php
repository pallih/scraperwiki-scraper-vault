<?php

require  'scraperwiki/simple_html_dom.php';

     $namerest = array();
     $address = array();
     $phone= array();
     $namerest1 = array();
     $arr = array();
     $add = array();
    // $name = array();
     $fon = array();




     $url = "http://fynnjamal.blogspot.co.uk";
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
 
   $address = $dom1->find('ul.posts li a');
    $adwe = $dom1->find('#BlogArchive1');
    $wer = $adwe->find('ul.posts');
    foreach($address as $tr)
   array_push( $add , $tr->href);
  
print_r(count($wer));

/*

    for($i = 0;$i<count($urla);$i++){

    $html= scraperwiki::scrape($urla[$i]);
    $dom = new simple_html_dom();
    $dom->load($html);

    $name = $dom->find('h1.h-mount-red');
    $addr = $dom->find('address');
    $phone = $dom->find('span[id=bizPhone]');
    $mail= $dom->find('span[id=bizPhone] a');
    $premurl = $dom->find('div[id=bizUrl] a');
    
    $namenew = $name[0]->innertext;
    $addrnew = $addr[0]->innertext;
    $premUrl = $premurl[0]->innertext;

  // foreach($phone as $tr)
 //  array_push( $phone, $tr->innertext);
    
     
    
  
        $datall[$i] = array("Name"=>$namenew,"Address"=>$addrnew,"Tel"=>$phonetel,"Fax"=>$phonefax,"Mail"=>$phonemail,"URL"=>$premUrl);
    }

*/
    //$html= scraperwiki::scrape($urla[5]);
    
       // print_r($datall);
    //print_r($name[0]->innertext);
    //print_r($addr[0]->innertext);
   // print_r($phone[2]->innertext);


        //print_r($add);
//for($t = 0; $t<count($add); $t++)
  //   $datall[$t] =array("Tel"=>$fon[$t],"Address"=>$add[$t],"Name"=>$name[$t]);
//print_r($datall);
     //   scraperwiki::save(array('Name','Address'), $datall);             
//print_r('dah kluar');

?>
