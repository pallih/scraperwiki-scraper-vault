<?php
$xpath = '//div[@class="article-body entry-content"]//img[@class="pict"]'; $url = 'http://iinoakazonae03.blog77.fc2.com/blog-entry-2422.html';

$html = scraperWiki::scrape($url);
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find($xpath) as $data){
    print_r($data);
/*    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
     print_r($record); 
*/
}
// scraperwiki::save(array('country'), $record); 