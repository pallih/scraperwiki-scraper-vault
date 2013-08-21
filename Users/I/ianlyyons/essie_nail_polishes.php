<?php

require 'scraperwiki/simple_html_dom.php';  

// Set up the loop to get all the pages
for ($i = 1; $i <= 300; $i++) {
    $url = "http://www.essie.com/shop/product_info.php?products_id=" . $i . "\n";
   
// Now scrape the pages sequentially
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);

// Now grab the h1s 

    foreach($html->find("div.shopright h1") as $h1) {
        $h1 = str_replace("<h1>","",$h1);
        $h1 = str_replace("</h1>","",$h1);
        $h1 = "\"" . $h1 . "\"";
        print $h1 . "\n";
    }

     foreach($html->find("p.dulling") as $ingred) {
        $ingred = str_replace("<p class=\"dulling\">","",$ingred);
        $ingred = str_replace("</p>","",$ingred);
        $ingred = "\"" . $ingred . "\"";
        print $ingred  . "\n";
    }
    
     foreach($html->find("div.shopright div.shopdesc") as $desc) {
        $desc = str_replace("<div class=\"shopdesc\">","",$desc);
        $desc = str_replace("</div>","",$desc);
        $desc = "\"" . $desc . "\"";
        print $desc . "\n";
    }

     foreach($html->find("div.shopimg a") as $imgsrc) {
        $imgsrc = "\"http://essie.com/shop/" . $imgsrc->href . "\"";
        print $imgsrc . "\n";
    }
    
     $record = array(
      'name' => $h1, 
      'description' => $desc,
      'image' => $imgsrc,
      'ingredients' => $ingred,
       'ingredients2' => $ingred
      );

      scraperwiki::save(array('name', 'description', 'image', 'ingredients2'), $record);
}   

?>
