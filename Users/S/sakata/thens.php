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

for ($i = 2; $i <=2 ; $i++) {


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
     print_r($add[$i]);
        $url = $add[$i];
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
    
    }




        //print_r($add);
//for($t = 0; $t<count($add); $t++)
  //   $datall[$t] =array("Tel"=>$fon[$t],"Address"=>$add[$t],"Name"=>$name[$t]);
//print_r($savedata);
       // scraperwiki::save(array('Shop','Info'), $savedata);             
//print_r('dah kluar');

?>
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

for ($i = 2; $i <=2 ; $i++) {


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
     print_r($add[$i]);
        $url = $add[$i];
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
    
    }




        //print_r($add);
//for($t = 0; $t<count($add); $t++)
  //   $datall[$t] =array("Tel"=>$fon[$t],"Address"=>$add[$t],"Name"=>$name[$t]);
//print_r($savedata);
       // scraperwiki::save(array('Shop','Info'), $savedata);             
//print_r('dah kluar');

?>
