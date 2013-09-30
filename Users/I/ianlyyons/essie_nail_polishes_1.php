<?php

require 'scraperwiki/simple_html_dom.php';  

// Set up the loop to get all the pages
for ($i = 1; $i <= 40; $i++) {
    $url = "http://www.mbeautylounge.com/nailpolish/4_opi?p=" . $i . "\n";
   
        // Now scrape the pages sequentially
        $html_content = scraperwiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html_content);
    
        $m = 0;
        $lis = $dom->find("div.center_block");
         foreach($lis as $li) {
            $desc = $li->find("p.product_desc a",0);
            $desc = $desc->innertext;
            $name = $li->find("h3 a",0);
            $name = $name->title;
            $imgsrc = $li->find("a.product_img_link img",0);
            $imgsrc = $imgsrc->src;
            $pageurl = $li->find("a.product_img_link",0);
            $pageurl = $pageurl->href;

            print($m . " Description: " . $desc . "\n");
            print ($m . " Name: " . $name . "\n");
            print ($m . " Img src: " . $imgsrc . "\n");
            print ($m . " Page URL: " . $pageurl . "\n");

          
               $record = array(
                    'desc' => $desc,
                    'name' => $name, 
                    'imgsrc' => $imgsrc,
                    'pageurl' => $pageurl
                ); 

                  scraperwiki::save(array('desc', 'name', 'imgsrc', 'pageurl'), $record); 
                }
        
    };


    
      


?><?php

require 'scraperwiki/simple_html_dom.php';  

// Set up the loop to get all the pages
for ($i = 1; $i <= 40; $i++) {
    $url = "http://www.mbeautylounge.com/nailpolish/4_opi?p=" . $i . "\n";
   
        // Now scrape the pages sequentially
        $html_content = scraperwiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html_content);
    
        $m = 0;
        $lis = $dom->find("div.center_block");
         foreach($lis as $li) {
            $desc = $li->find("p.product_desc a",0);
            $desc = $desc->innertext;
            $name = $li->find("h3 a",0);
            $name = $name->title;
            $imgsrc = $li->find("a.product_img_link img",0);
            $imgsrc = $imgsrc->src;
            $pageurl = $li->find("a.product_img_link",0);
            $pageurl = $pageurl->href;

            print($m . " Description: " . $desc . "\n");
            print ($m . " Name: " . $name . "\n");
            print ($m . " Img src: " . $imgsrc . "\n");
            print ($m . " Page URL: " . $pageurl . "\n");

          
               $record = array(
                    'desc' => $desc,
                    'name' => $name, 
                    'imgsrc' => $imgsrc,
                    'pageurl' => $pageurl
                ); 

                  scraperwiki::save(array('desc', 'name', 'imgsrc', 'pageurl'), $record); 
                }
        
    };


    
      


?>