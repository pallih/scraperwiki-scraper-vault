<?php

# 
# Collect competitor data from teamgb.com
#http://www.teamgb.com/2012athletes
#Only 2012 selected athletes
#Iterate all athlete bio pages for key data


           
#extract data
#

#http://simplehtmldom.sourceforge.net/
require 'scraperwiki/simple_html_dom.php';

$htmlstr = "http://www.teamgb.com/2012athletes";
 $html = scraperWiki::scrape($htmlstr);
    $html = str_get_html($html);


   #loop on each athelete url
    foreach ($html->find('div.[class="gender male"] a') as $ael) {
   print $ael->href . "\n";

        $athhtml = scraperWiki::scrape("http://www.teamgb.com/".$ael->href);
        $athhtml = str_get_html($athhtml);
 
            foreach ($athhtml->find("div#header-athlete-profile") as $el) {
 
                #get athlete name from header tag       
                $athleteName = $el->find("h2");
                $athName = $athleteName[0]->plaintext;
                $record = array('Athlete' => $athName);
                $record["Gender"] = "Male";
                #scraperwiki::save(array('Athlete'), $record); 

                #Get main data
                foreach ($el->find("tr") as $tel) {
                $tds = $tel->find("td");
                $athLabel = $tds[0]->plaintext;
                $athValue = $tds[1]->plaintext;
                $record[$athLabel] = $athValue;
            }

                scraperwiki::save(array('Athlete', 'Gender', 'Sport', 'Date of Birth', 'Lives', 'Born', 'Height (cm)', 'Weight (kg)', 'Club', 'Coach'), $record); 

    }
}    


   #loop on each athelete url
    foreach ($html->find('div.[class="gender female"] a') as $ael) {
   print $ael->href . "\n";

        $athhtml = scraperWiki::scrape("http://www.teamgb.com/".$ael->href);
        $athhtml = str_get_html($athhtml);
 
            foreach ($athhtml->find("div#header-athlete-profile") as $el) {
 
                #get athlete name from header tag       
                $athleteName = $el->find("h2");
                $athName = $athleteName[0]->plaintext;
                $record = array('Athlete' => $athName);
                $record["Gender"] = "Female";
                #scraperwiki::save(array('Athlete'), $record); 

                #Get main data
                foreach ($el->find("tr") as $tel) {
                $tds = $tel->find("td");
                $athLabel = $tds[0]->plaintext;
                $athValue = $tds[1]->plaintext;
                $record[$athLabel] = $athValue;
            }

                scraperwiki::save(array('Athlete', 'Gender', 'Sport', 'Date of Birth', 'Lives', 'Born', 'Height (cm)', 'Weight (kg)', 'Club', 'Coach'), $record); 

    }
}    



?>
