<?php

//Scraper to extract candidate information for PHP developers

require 'scraperwiki/simple_html_dom.php';

$country = array("uk");
$topic = array("PHP","symphony","technology","big-data","cloud","innovation");

for ($c = 0; $c < (count($country)); $c++) {

    for ($t = 0; $t < (count($topic)); $t++) {
        $page = "http://lanyrd.com/topics/".$topic[$t]."/in/".$country[$c];
        $html_content = scraperwiki::scrape($page);
        $html = str_get_html($html_content);
        $eventscount = count($html->find("li.conference"));
        
        for ($i = 0; $i < $eventscount; $i++) {
            $event = $html->find("li.conference h4", $i);
            $location = $html->find("p.location", $i);
            $date = $html->find("p.date", $i);
            $url = html_entity_decode($html->find("h4 a", $i)->href);

        //save the data
            scraperwiki::save_sqlite(array("event"),array("event"=>$event->plaintext, "location"=>$location->plaintext, "date"=>$date->plaintext,"url"=>"http://lanyrd.com".$url, "topic"=>$topic[$t], "country"=>$country[$c]));

        }

    }

}

?>
<?php

//Scraper to extract candidate information for PHP developers

require 'scraperwiki/simple_html_dom.php';

$country = array("uk");
$topic = array("PHP","symphony","technology","big-data","cloud","innovation");

for ($c = 0; $c < (count($country)); $c++) {

    for ($t = 0; $t < (count($topic)); $t++) {
        $page = "http://lanyrd.com/topics/".$topic[$t]."/in/".$country[$c];
        $html_content = scraperwiki::scrape($page);
        $html = str_get_html($html_content);
        $eventscount = count($html->find("li.conference"));
        
        for ($i = 0; $i < $eventscount; $i++) {
            $event = $html->find("li.conference h4", $i);
            $location = $html->find("p.location", $i);
            $date = $html->find("p.date", $i);
            $url = html_entity_decode($html->find("h4 a", $i)->href);

        //save the data
            scraperwiki::save_sqlite(array("event"),array("event"=>$event->plaintext, "location"=>$location->plaintext, "date"=>$date->plaintext,"url"=>"http://lanyrd.com".$url, "topic"=>$topic[$t], "country"=>$country[$c]));

        }

    }

}

?>
