<?php


require 'scraperwiki/simple_html_dom.php';
                 $dom = new simple_html_dom();

foreach(range('A','Z') as $i) {
    $i = ucwords($i);

        $link = 'http://www.ratebeer.com/browsebrewers-'.$i.'.htm';
        $html = scraperwiki::scrape($link);
        
        $images = array('jpg', 'jpeg');
        $maxX = 250;
        $maxY = 250;
        
        $dom->load($html);
        
        foreach ($dom->find('a') as $img) {
        
           scraperwiki::save(
            array('table_cell','table'), 
            array(
                'table_cell' => $img->plaintext,
                'table' => $img->getAttribute('href')
                )
            );
        
         }
    $i++;
    }
?>
