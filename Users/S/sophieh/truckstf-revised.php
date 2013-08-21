<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.truckstopsf.com");
$html = str_get_html($html_content);
$i=0;

foreach($html->find("div[class=grid_2]") as $content){
    // $content = <div class="grid_2">.  first_child() should be the <p>


    // Get the <p>'s following the <div class="title">
    $next = $content->next_sibling();
    
    $output = $next->plaintext;
       
 //   $record = array( 'key' => $i, 'day' =>$next->innertext ); 
      print $output. "\n";
      $i++;
 //   scraperwiki::save(array('key'), $record); 

}




//print_r($data);


 /*
    while ($next->tag == 'div') {
        echo $next.'<hr />';
        $next = $next->next_sibling();
    }
    */

//http://oreilly.com/catalog/progphp/chapter/ch05.html

?>
