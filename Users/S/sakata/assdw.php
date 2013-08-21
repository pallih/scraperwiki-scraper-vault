<?php

require  'scraperwiki/simple_html_dom.php';

     $namerest = array();
     $address = array();
     $phone= array();
     $namerest1 = array();
     $arr = array();
     $add = array();
     $fon = array();
     $data = array();

for ($i = 1; $i <=22 ; $i++) {


     $url = "http://blog.officekami.com/category/officekami-location/page/$i/";
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
 
   $address = $dom1->find('div.post h2 a');
    foreach($address as $tr)
   array_push( $add , $tr->href);
  

}

    $no_add = count($add);   

for($i=0;$i<$no_add;$i++){
   //  print_r($add[$i]);
        $url = $add[$i];
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
    

    $infobanyak= $dom1->find('div.entry p');
    $title = $dom1->find('div.post h2 a');
    $title1 = $title[0]->innertext;
    $indexer = count($infobanyak)-1;
    //print_r($title);
   

    for($re=0;$re<$indexer;$re++){
        $textdata = $infobanyak[$re]->innertext;
       array_push($data,$textdata );
         } 
    $mixdata = implode("<br />", $data);

    $savedata[$i] = array("Shop"=>$title1,"Info"=>$mixdata);
    //clear $data back not destroying it
    $data = array();
    //print_r($infobanyak[$index-2]->innertext);
    //print_r($title[0]->innertext);
    
    
        
    }




        //print_r($add);
//for($t = 0; $t<count($add); $t++)
  //   $datall[$t] =array("Tel"=>$fon[$t],"Address"=>$add[$t],"Name"=>$name[$t]);
//print_r($savedata);
        scraperwiki::save(array('Shop','Info'), $savedata);             
//print_r('dah kluar');

?>
