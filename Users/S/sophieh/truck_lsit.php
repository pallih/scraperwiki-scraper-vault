<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.truckstopsf.com/the-trucks/");
$html = str_get_html($html_content);


foreach ($html->find("section") as $content) {           
  

   
    foreach($content->find("li") as $node){
               
            //start parsing withing li

         

            // access h4
            $truckname = $node->children(0)->innertext;

            //div.description
            $blurb =  $node->children(1)->innertext;
            
            $index = str_replace("&#39;","",$truckname);
            $index = str_replace("&amp;","",$index);
            $index = str_replace(" ","",$index);
            $index = str_replace("-","",$index);

            //$links =     $node->find('div',1)->find('p',0)->innertext;
            
            $index = strtolower($index);
            
            $truck = array(
                'name' => $truckname,
                'blurb' =>$blurb
            );
              
           scraperwiki::save(array('name'), $truck);
     } 
}    





//http://oreilly.com/catalog/progphp/chapter/ch05.html

?>
