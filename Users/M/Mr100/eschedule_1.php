<?php
######################################
# Basic PHP scraper
######################################
$html = scraperWiki::scrape("http://www.valleycollege.edu/eSchedule/Online/Schedule/V/2012SP/index.html");
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$count=0;
foreach($dom->find('tr td') as $data)
{
    //foreach($tr->find('td') as $data)
    //{
       $tds = $data;
       //Do something
       $tds = $data->find('text');       
       $link = "http://valleycollege.edu/" . html_entity_decode($tds[0]->find('a[href="\(.*?)"]', 0)->href);
       $record = array( 'Subject' => $tds[0]->plaintext, 'link' => $link );
       //$title = array( 'link' => $link[0]->plaintext);
       //print_r($record);
       //$count++;
       //if ( $count > 10 ) break;
       scraperwiki::save(array('Subject'), $record);
    //}
   
}
