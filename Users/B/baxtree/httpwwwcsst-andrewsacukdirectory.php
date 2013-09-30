<?php
require "scraperwiki/simple_html_dom.php";
$html = scraperWiki::scrape("http://www.cs.st-andrews.ac.uk/directory");
$dom = new simple_html_dom();
$dom->load($html);
$counter = 0;
foreach($dom->find("table.sorttable tr") as $data){
    if($counter == 0){
        $counter++;
        continue;
    }
    else{
        $tds = $data->find("td");
        $person_url = "http://www.cs.st-andrews.ac.uk" . array_shift($tds[1]->find("a"))->href . "/";
        $dom_temp = new simple_html_dom();
        $html_temp = scraperWiki::scrape($person_url);
        $dom_temp->load($html_temp);
        $person_info = array_shift($dom_temp->find("body"))->plaintext;
        $record = array(
            "name" => $tds[1]->plaintext,
            "position" => $tds[3]->plaintext,
            "url" => $person_url,
            "info" => $person_info == null ? "" : $person_info
        );
    }
    print_r($record);
    scraperwiki::save(array("url"), $record);
}
?><?php
require "scraperwiki/simple_html_dom.php";
$html = scraperWiki::scrape("http://www.cs.st-andrews.ac.uk/directory");
$dom = new simple_html_dom();
$dom->load($html);
$counter = 0;
foreach($dom->find("table.sorttable tr") as $data){
    if($counter == 0){
        $counter++;
        continue;
    }
    else{
        $tds = $data->find("td");
        $person_url = "http://www.cs.st-andrews.ac.uk" . array_shift($tds[1]->find("a"))->href . "/";
        $dom_temp = new simple_html_dom();
        $html_temp = scraperWiki::scrape($person_url);
        $dom_temp->load($html_temp);
        $person_info = array_shift($dom_temp->find("body"))->plaintext;
        $record = array(
            "name" => $tds[1]->plaintext,
            "position" => $tds[3]->plaintext,
            "url" => $person_url,
            "info" => $person_info == null ? "" : $person_info
        );
    }
    print_r($record);
    scraperwiki::save(array("url"), $record);
}
?>