<?php
require 'scraperwiki/simple_html_dom.php';           

    function scrapePage($url){
        $html = scraperWiki::scrape($url);           

        $dom = new simple_html_dom();
        $dom->load($html);

        $cells = $dom->find('td.nom');
        foreach($cells as $cell){
            $name = $cell->find('a',0)->plaintext;
            $parent = $cell->parent();

            $count = $parent->find('td.compte',0)->plaintext;

            if($count) {        
                $payload = array(
                    'name'=> $name,
                    'count' => $count
                );
            
                scraperWiki::save_sqlite(array('name'), $payload);
            }
        
        }
    
    }
                
    scrapePage("http://surname.sofeminine.co.uk/w/surnames/most-common-surnames-in-great-britain.html");           
    //scrapePage("http://surname.sofeminine.co.uk/w/surnames/most-common-surnames-in-great-britain-2.html");
    //scrapePage("http://surname.sofeminine.co.uk/w/surnames/most-common-surnames-in-great-britain-3.html");
    //scrapePage("http://surname.sofeminine.co.uk/w/surnames/most-common-surnames-in-great-britain-4.html");
    //scrapePage("http://surname.sofeminine.co.uk/w/surnames/most-common-surnames-in-great-britain-5.html");
    
    

    

?>
