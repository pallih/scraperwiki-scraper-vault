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
    scrapeTeams("http://www.statto.com/football/teams/index/italy/serie-a");
    scrapeTeams("http://www.statto.com/football/teams/index/spain/primera-liga");
    scrapeTeams("http://www.statto.com/football/teams/index/germany/bundesliga");
    scrapeTeams("http://www.statto.com/football/teams/index/france/ligue-1");
    scrapeTeams("http://www.statto.com/football/teams/index/scotland");
    scrapeTeams("http://www.statto.com/football/teams/index/holland/eredivisie");
    scrapeTeams("http://www.statto.com/football/teams/index/wales/premier-league");
    scrapeTeams("http://www.statto.com/football/teams/index/portugal/liga");
    scrapeTeams("http://www.statto.com/football/teams/index/greece/super-league");
    scrapeTeams("http://www.statto.com/football/teams/index/austria/bundesliga");
    scrapeTeams("http://www.statto.com/football/teams/index/denmark/superligaen");
    scrapeTeams("http://www.statto.com/football/teams/index/finland/veikkausliga");



    

    

?>
