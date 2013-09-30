<?php

require  'scraperwiki/simple_html_dom.php';

 $url = "http://blog.officekami.com/2012/02/tenshi-no-cafe-e-curve-kota-damansara/";
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
    
    $data = array();
    $infobanyak= $dom1->find('div.entry p');
    $title = $dom1->find('div.post h2 a');
    $index = count($infobanyak);

    for($i=0;$i<$index-1;$i++){
        $textdata = $infobanyak[$i]->innertext;
       array_push($data,$textdata );
         } 
    $mix = implode("<br />", $data);
    print_r($mix);
   // print_r(count($infobanyak));
   // print_r($infobanyak[$index-2]->innertext);
   // print_r($title[0]->innertext);
  /* for($i=0;$i<count($infobanyak);$i++){
        print_r($infobanyak[$i]->innertext);
        print_r('<br />');
            }*/
?>
<?php

require  'scraperwiki/simple_html_dom.php';

 $url = "http://blog.officekami.com/2012/02/tenshi-no-cafe-e-curve-kota-damansara/";
    $html= scraperwiki::scrape($url);
    $dom1 = new simple_html_dom();
    $dom1->load($html);
    
    $data = array();
    $infobanyak= $dom1->find('div.entry p');
    $title = $dom1->find('div.post h2 a');
    $index = count($infobanyak);

    for($i=0;$i<$index-1;$i++){
        $textdata = $infobanyak[$i]->innertext;
       array_push($data,$textdata );
         } 
    $mix = implode("<br />", $data);
    print_r($mix);
   // print_r(count($infobanyak));
   // print_r($infobanyak[$index-2]->innertext);
   // print_r($title[0]->innertext);
  /* for($i=0;$i<count($infobanyak);$i++){
        print_r($infobanyak[$i]->innertext);
        print_r('<br />');
            }*/
?>
