<?php

# From tutorial code
# Collect competitor data from teamgb.com
#get all athlete urls from 77 overview pages
#then
#iterate all athlete bio pages for key data


           
#extract data
#

#http://simplehtmldom.sourceforge.net/
require 'scraperwiki/simple_html_dom.php';

$htmlstr = "http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&field_lives_region_tid=All";
 $html = scraperWiki::scrape($htmlstr);
    $html = str_get_html($html);

    #loop on each athelete url
    foreach ($html->find("a.more") as $el) {
        $athhtml = scraperWiki::scrape("http://www.teamgb.com/".$el->href);
        $athhtml = str_get_html($athhtml);

            foreach ($athhtml->find("div#header-athlete-profile") as $el) {
 
                #get athlete name from header tag       
                $athleteName = $el->find("h2");
                $athName = $athleteName[0]->plaintext;
                $record = array('Athlete' => $athName);
                #scraperwiki::save(array('Athlete'), $record); 

                #Get main data
                foreach ($el->find("tr") as $tel) {
                $tds = $tel->find("td");

                $athLabel = $tds[0]->plaintext;
                $athValue = $tds[1]->plaintext;
                $record[$athLabel] = $athValue;
            }

    scraperwiki::save(array('Athlete', 'Sport', 'Date of Birth', 'Lives', 'Born', 'Height (cm)', 'Weight (kg)', 'Club', 'Coach'), $record); 
    #print_r($record);

    }
    }


#loop all 77 athlete overview pages from base string $htmlstr
for ($i = 1; $i <= 77; $i++) {

    #grab overview page and collect althlete urls
    $htmlstr = "http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=" . $i;

    $html = scraperWiki::scrape($htmlstr);
    $html = str_get_html($html);

    #loop on each athelete url
    foreach ($html->find("a.more") as $el) {
        $athhtml = scraperWiki::scrape("http://www.teamgb.com/".$el->href);
        $athhtml = str_get_html($athhtml);

            foreach ($athhtml->find("div#header-athlete-profile") as $el) {
 
                #get athlete name from header tag       
                $athleteName = $el->find("h2");
                $athName = $athleteName[0]->plaintext;
                $record = array('Athlete' => $athName);
                #scraperwiki::save(array('Athlete'), $record); 

                #Get main data
                foreach ($el->find("tr") as $tel) {
                $tds = $tel->find("td");

                $athLabel = $tds[0]->plaintext;
                $athValue = $tds[1]->plaintext;
                $record[$athLabel] = $athValue;
            }

    scraperwiki::save(array('Athlete', 'Sport', 'Date of Birth', 'Lives', 'Born', 'Height (cm)', 'Weight (kg)', 'Club', 'Coach'), $record); 
    #print_r($record);

    }
    }
}


?>
