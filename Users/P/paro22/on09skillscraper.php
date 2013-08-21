<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.webentwickler-jobs.de");
$dom = new simple_html_dom();
$dom->load($html);
$html_el = $dom->find( "div[@id='content'] table",0);           

//alle tr innerhalb der table rausfiltern
foreach ($html_el->find("tr") as $child1) {

    $url = "http://www.webentwickler-jobs.de". $child1->children(0)->children(0)->href;

    $subpage = scraperWiki::scrape($url);
    $subdom = new simple_html_dom();
    $subdom->load($subpage);
    
      foreach($subdom->find("div[@id='content']") as $newdata)
      {
        $dds = $newdata->find("dd");
        $h2 = $newdata->find("h2");

            // Daten aufbereiten:
            $job = strip_tags($h2[0]->plaintext);
            $text = strip_tags($dds[3]);

            //get informations:
            $record = array(
              'job' => $job,
              'text' => $text
            );

            $message = scraperwiki::save_sqlite(array("job", "text"), $record);      
        
      }
      $subdom->__destruct();

}   