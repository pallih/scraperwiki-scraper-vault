<?php
require 'scraperwiki/simple_html_dom.php';           

    function scrapeTeams($url){

        $html = scraperWiki::scrape($url);           
        
            $dom = new simple_html_dom();
            $dom->load($html);
        
            $cells = $dom->find('td.cw a');
            foreach($cells as $cell){
                $name = $cell->plaintext;
                $team = array( 'club'=> $name);
                scraperWiki::save_sqlite(array('club'), $team);
                
            }

    }

    scrapeTeams("http://www.statto.com/football/teams/index/england");


    

    

?>
