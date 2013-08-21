<?php
error_reporting(E_ALL & ~(E_STRICT|E_NOTICE)); // seriously?  The wikiscraper libraries throw warnings?
require 'scraperwiki/simple_html_dom.php'; 
  
$urls = array("http://www.cool-smileys.com/text-emoticons","http://www.cool-smileys.com/text-emoticons-part2");
/* drop old data, since there were duplicate smiley entries in it
print_r(scraperwiki::show_tables());
scraperwiki::sqliteexecute("delete from swdata where 1");
scraperwiki::sqliteexecute("drop table swdata");
die();
*/
foreach ($urls  as $url){
        $html = scraperWiki::scrape($url);  
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("table tr") as $data){
    $tds = $data->find("td");
    $smiley = $data->find("input");
    $record = array(
        'name' => $tds[0]->plaintext, 
        'smiley' => $smiley[0]->value
    );
    if (!empty($record['name'])) {
        scraperwiki::save_sqlite(array("smiley"),$record); 
    }
}
}



?>
